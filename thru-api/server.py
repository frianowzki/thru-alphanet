#!/usr/bin/env python3
"""
Thru On-Chain API Server
Zero dependencies — uses only Python stdlib.
Proxies frontend requests to thru CLI for real blockchain interaction.

Usage:
    python3 server.py                        # default port 3000
    PORT=8080 python3 server.py              # custom port
    THRU_KEY_NAME=mykey python3 server.py    # custom key name
"""

import os
import sys
import json
import struct
import base64
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ── Config ──────────────────────────────────────────────────────────────

KEY_NAME = os.environ.get("THRU_KEY_NAME", "default")
PROGRAM_ADDRESS = os.environ.get(
    "THRU_COUNTER_PROGRAM",
    "ta2sYKmgW-b0FQEP2-pMYROxnAIMTrZTgpJqgVvxAHe423"
)
FRONTEND_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "thru-frontend")
)
INDEX_HTML = os.path.join(FRONTEND_DIR, "index.html")

# Counter instruction opcodes (matching tn_counter_v7.c)
INSTR = {"create": 0, "increment": 1, "decrement": 2, "reset": 3, "read": 4}

# Pre-built instruction hex for operations (type=u32 LE + account_idx=u16 LE)
INSTR_HEX = {
    "increment": struct.pack("<IH", 1, 2).hex().upper(),
    "decrement": struct.pack("<IH", 2, 2).hex().upper(),
    "reset":     struct.pack("<IH", 3, 2).hex().upper(),
    "read":      struct.pack("<IH", 4, 2).hex().upper(),
}


# ── Helpers ─────────────────────────────────────────────────────────────

def thru_cmd(args, timeout=30):
    """Execute thru CLI and return parsed JSON."""
    cmd = ["thru", "--json"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.stdout.strip():
            return json.loads(result.stdout)
        return {"error": result.stderr.strip() or "No output"}
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out"}
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON: {result.stdout[:200]}"}
    except Exception as e:
        return {"error": str(e)}


def decode_counter_value(data_b64):
    """Decode counter value from base64 account data (8-byte LE uint64)."""
    try:
        raw = base64.b64decode(data_b64)
        if len(raw) >= 8:
            return struct.unpack("<Q", raw[:8])[0]
        return 0
    except Exception:
        return 0


def get_counter_value(pda):
    """Read counter value directly from account data."""
    data = thru_cmd(["account", "info", pda])
    acct = data.get("account_info", {})
    if acct.get("data"):
        return decode_counter_value(acct["data"])
    return None


def derive_pda(seed):
    """Derive PDA address from program + seed."""
    data = thru_cmd(["program", "derive-address", PROGRAM_ADDRESS, seed])
    return data.get("derive_address", {}).get("derived_address")


def make_state_proof(address):
    """Generate state proof for account creation."""
    data = thru_cmd(["txn", "make-state-proof", "creating", address])
    return data.get("makeStateProof", {}).get("proof_data_hex")


def build_create_instr(seed, proof_hex):
    """Build CREATE instruction data with state proof."""
    proof_bytes = bytes.fromhex(proof_hex)
    seed_bytes = seed.encode() + b"\x00" * (32 - len(seed))
    return (
        struct.pack("<I", 0)              # instruction type = create
        + struct.pack("<H", 2)            # account index
        + seed_bytes                       # 32-byte seed
        + struct.pack("<I", len(proof_bytes))  # proof size
        + proof_bytes                      # proof data
    ).hex().upper()


# ── HTTP Handler ────────────────────────────────────────────────────────

class ThruHandler(BaseHTTPRequestHandler):
    """Handles API + serves frontend. No external dependencies."""

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/status":
            return self.send_json(thru_cmd(["gethealth"]))

        if path == "/api/wallet/balance":
            data = thru_cmd(["account", "info", KEY_NAME])
            acct = data.get("account_info", {})
            return self.send_json({
                "address": acct.get("pubkey", ""),
                "balance": acct.get("balance", 0),
                "nonce": acct.get("nonce", 0),
            })

        if path == "/api/counter/value":
            qs = parse_qs(urlparse(self.path).query)
            pda = qs.get("pda", [None])[0]
            if not pda:
                return self.send_json({"error": "Missing ?pda="}, 400)
            value = get_counter_value(pda)
            if value is None:
                return self.send_json({"error": "Counter not found", "pda": pda}, 404)
            return self.send_json({"pda": pda, "value": value})

        # Everything else → serve frontend
        return self.serve_file(INDEX_HTML, "text/html")

    def do_POST(self):
        path = urlparse(self.path).path
        body = self.read_body()

        if path == "/api/counter/execute":
            pda = body.get("pda")
            action = body.get("action")
            if not pda or action not in INSTR_HEX:
                return self.send_json(
                    {"error": f"action must be: {list(INSTR_HEX.keys())}"}, 400
                )

            result = thru_cmd([
                "txn", "execute", "--fee", "0",
                "--readwrite-accounts", pda,
                PROGRAM_ADDRESS,
                INSTR_HEX[action],
            ])
            tx = result.get("transaction_execute", {})
            ok = tx.get("vm_error", -1) == 0 and tx.get("user_error_code", -1) == 0

            # Re-read value after mutation
            value = get_counter_value(pda)

            return self.send_json({
                "success": ok,
                "action": action,
                "value": value,
                "signature": tx.get("signature"),
                "compute_units": tx.get("compute_units_consumed"),
                "events": len(tx.get("events", [])),
                "error": tx.get("vm_error_name") if not ok else None,
            })

        if path == "/api/counter/create":
            seed = body.get("seed", "my-counter")

            pda = derive_pda(seed)
            if not pda:
                return self.send_json({"error": "Failed to derive PDA"}, 500)

            existing = get_counter_value(pda)
            if existing is not None:
                return self.send_json(
                    {"error": "Counter already exists", "pda": pda, "value": existing}, 409
                )

            proof_hex = make_state_proof(pda)
            if not proof_hex:
                return self.send_json({"error": "Failed to generate state proof"}, 500)

            instr_hex = build_create_instr(seed, proof_hex)

            result = thru_cmd([
                "txn", "execute", "--fee", "0",
                "--readwrite-accounts", pda,
                PROGRAM_ADDRESS,
                instr_hex,
            ])
            tx = result.get("transaction_execute", {})
            ok = tx.get("vm_error", -1) == 0 and tx.get("user_error_code", -1) == 0

            return self.send_json({
                "success": ok,
                "pda": pda,
                "seed": seed,
                "signature": tx.get("signature"),
                "value": 0 if ok else None,
                "error": tx.get("vm_error_name") if not ok else None,
            })

        return self.send_json({"error": "Not found"}, 404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
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
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_file(self, filepath, content_type):
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_json({"error": "File not found"}, 404)

    def log_message(self, fmt, *args):
        try:
            msg = str(args[0]) if args else ""
            if "/api/" in msg:
                sys.stdout.write(f"  → {msg}\n")
                sys.stdout.flush()
        except Exception:
            pass


# ── Main ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    server = HTTPServer(("0.0.0.0", port), ThruHandler)
    print(f"🕊️  Thru API Server")
    print(f"   http://localhost:{port}")
    print(f"   Key: {KEY_NAME}")
    print(f"   Program: {PROGRAM_ADDRESS}")
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
