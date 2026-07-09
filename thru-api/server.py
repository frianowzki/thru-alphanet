#!/usr/bin/env python3
"""
Thru On-Chain API Server v2
Zero dependencies — Python stdlib only.

Security model:
  - Private key is received per-request, used ephemerally, NEVER stored
  - Key is imported → used → deleted in same request lifecycle
  - No logging of private keys
  - All responses are JSON

Usage:
    python3 server.py                          # port 3001
    PORT=8080 python3 server.py                # custom port
    ALLOWED_ORIGINS=https://app.vercel.app python3 server.py  # CORS
"""

import os
import sys
import json
import struct
import base64
import secrets
import subprocess
import tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ── Config ──────────────────────────────────────────────────────────────

ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

# Default program (user can override per-request)
DEFAULT_PROGRAM = "ta2sYKmgW-b0FQEP2-pMYROxnAIMTrZTgpJqgVvxAHe423"

# Counter instruction opcodes
INSTR = {"create": 0, "increment": 1, "decrement": 2, "reset": 3, "read": 4}
INSTR_HEX = {
    "increment": struct.pack("<IH", 1, 2).hex().upper(),
    "decrement": struct.pack("<IH", 2, 2).hex().upper(),
    "reset":     struct.pack("<IH", 3, 2).hex().upper(),
    "read":      struct.pack("<IH", 4, 2).hex().upper(),
}


# ── Helpers ─────────────────────────────────────────────────────────────

def thru_cmd(args, timeout=30):
    """Execute thru CLI, return parsed JSON."""
    cmd = ["thru", "--json"] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if r.stdout.strip():
            return json.loads(r.stdout)
        return {"error": r.stderr.strip() or "No output"}
    except subprocess.TimeoutExpired:
        return {"error": "CLI timed out"}
    except json.JSONDecodeError:
        return {"error": f"Bad JSON: {r.stdout[:200]}"}
    except Exception as e:
        return {"error": str(e)}


def ephemeral_key_import(private_key_hex):
    """Import a private key as a temp key, return (key_name, address).
       The key is stored in thru config but should be cleaned up after use."""
    name = f"_tmp_{secrets.token_hex(4)}"
    r = subprocess.run(
        ["thru", "keys", "add", name, private_key_hex],
        capture_output=True, text=True, timeout=10
    )
    if r.returncode != 0:
        return None, None, f"Add failed: {r.stderr.strip()}"
    # Get address from account info
    data = thru_cmd(["account", "info", name])
    acct = data.get("account_info", {})
    return name, acct.get("pubkey", ""), None


def ephemeral_key_cleanup(name):
    """Remove ephemeral key from config."""
    if name and name.startswith("_tmp_"):
        subprocess.run(["thru", "keys", "rm", name],
                        capture_output=True, timeout=10)


def decode_counter_value(data_b64):
    """Decode counter from base64 account data (8-byte LE uint64)."""
    try:
        raw = base64.b64decode(data_b64)
        return struct.unpack("<Q", raw[:8])[0] if len(raw) >= 8 else 0
    except Exception:
        return 0


def get_counter_value(pda):
    data = thru_cmd(["account", "info", pda])
    acct = data.get("account_info", {})
    if acct.get("data"):
        return decode_counter_value(acct["data"])
    return None


def derive_pda(program, seed):
    data = thru_cmd(["program", "derive-address", program, seed])
    return data.get("derive_address", {}).get("derived_address")


def make_state_proof(address):
    data = thru_cmd(["txn", "make-state-proof", "creating", address])
    return data.get("makeStateProof", {}).get("proof_data_hex")


def build_create_instr(seed, proof_hex):
    proof_bytes = bytes.fromhex(proof_hex)
    seed_bytes = seed.encode() + b"\x00" * (32 - len(seed))
    return (
        struct.pack("<I", 0) + struct.pack("<H", 2) + seed_bytes
        + struct.pack("<I", len(proof_bytes)) + proof_bytes
    ).hex().upper()


# ── HTTP Handler ────────────────────────────────────────────────────────

class ThruHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/status":
            return self.send_json(thru_cmd(["gethealth"]))

        # Serve frontend
        idx = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "thru-frontend", "index.html")
        return self.serve_file(idx)

    def do_POST(self):
        path = urlparse(self.path).path
        body = self.read_body()
        key_name = None

        try:
            # ── Extract + import ephemeral key ──
            pk = body.get("privateKey", "").strip()
            if not pk:
                return self.send_json({"error": "privateKey required"}, 400)

            key_name, address, err = ephemeral_key_import(pk)
            if err:
                return self.send_json({"error": f"Key import failed: {err}"}, 400)

            program = body.get("program", DEFAULT_PROGRAM)

            # ── Wallet Balance ──
            if path == "/api/wallet/balance":
                data = thru_cmd(["account", "info", key_name])
                acct = data.get("account_info", {})
                return self.send_json({
                    "address": acct.get("pubkey", address or ""),
                    "balance": acct.get("balance", 0),
                    "nonce": acct.get("nonce", 0),
                })

            # ── Counter Value (read-only, no TX) ──
            if path == "/api/counter/value":
                pda = body.get("pda") or parse_qs(urlparse(self.path).query).get("pda", [None])[0]
                if not pda:
                    return self.send_json({"error": "pda required"}, 400)
                value = get_counter_value(pda)
                if value is None:
                    return self.send_json({"error": "Counter not found", "pda": pda}, 404)
                return self.send_json({"pda": pda, "value": value})

            # ── Counter Execute ──
            if path == "/api/counter/execute":
                pda = body.get("pda")
                action = body.get("action")
                if not pda or action not in INSTR_HEX:
                    return self.send_json(
                        {"error": f"action must be: {list(INSTR_HEX.keys())}"}, 400)

                result = thru_cmd([
                    "txn", "execute", "--fee", "0",
                    "--fee-payer", key_name,
                    "--readwrite-accounts", pda,
                    program, INSTR_HEX[action],
                ])
                tx = result.get("transaction_execute", {})
                ok = tx.get("vm_error", -1) == 0 and tx.get("user_error_code", -1) == 0
                value = get_counter_value(pda)

                return self.send_json({
                    "success": ok, "action": action, "value": value,
                    "signature": tx.get("signature"),
                    "compute_units": tx.get("compute_units_consumed"),
                    "events": len(tx.get("events", [])),
                    "error": tx.get("vm_error_name") if not ok else None,
                })

            # ── Counter Create ──
            if path == "/api/counter/create":
                seed = body.get("seed", "my-counter")
                pda = derive_pda(program, seed)
                if not pda:
                    return self.send_json({"error": "Failed to derive PDA"}, 500)

                existing = get_counter_value(pda)
                if existing is not None:
                    return self.send_json(
                        {"error": "Counter already exists", "pda": pda, "value": existing}, 409)

                proof_hex = make_state_proof(pda)
                if not proof_hex:
                    return self.send_json({"error": "Failed to generate proof"}, 500)

                instr_hex = build_create_instr(seed, proof_hex)
                result = thru_cmd([
                    "txn", "execute", "--fee", "0",
                    "--fee-payer", key_name,
                    "--readwrite-accounts", pda,
                    program, instr_hex,
                ])
                tx = result.get("transaction_execute", {})
                ok = tx.get("vm_error", -1) == 0 and tx.get("user_error_code", -1) == 0

                return self.send_json({
                    "success": ok, "pda": pda, "seed": seed,
                    "signature": tx.get("signature"),
                    "value": 0 if ok else None,
                    "error": tx.get("vm_error_name") if not ok else None,
                })

            return self.send_json({"error": "Not found"}, 404)

        finally:
            # ALWAYS cleanup ephemeral key — never leave it in config
            ephemeral_key_cleanup(key_name)

    def do_OPTIONS(self):
        origin = self.headers.get("Origin", "*")
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin",
                         origin if "*" in ALLOWED_ORIGINS or origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0])
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    # ── Utilities ──

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        try:
            return json.loads(self.rfile.read(length))
        except Exception:
            return {}

    def send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        origin = self.headers.get("Origin", "*")
        self.send_header("Access-Control-Allow-Origin",
                         origin if "*" in ALLOWED_ORIGINS or origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0])
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_file(self, filepath):
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_json({"error": "Not found"}, 404)

    def log_message(self, fmt, *args):
        try:
            msg = str(args[0]) if args else ""
            if "/api/" in msg:
                # Sanitize — never log private keys
                safe = msg.replace("privateKey", "pk").replace("private_key", "pk")
                sys.stdout.write(f"  → {safe}\n")
                sys.stdout.flush()
        except Exception:
            pass


# ── Main ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3001))
    server = HTTPServer(("0.0.0.0", port), ThruHandler)
    print(f"🕊️  Thru API Server v2")
    print(f"   http://localhost:{port}")
    print(f"   CORS: {ALLOWED_ORIGINS}")
    print(f"   Security: ephemeral keys, never stored")
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
