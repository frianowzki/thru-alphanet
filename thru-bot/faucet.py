#!/usr/bin/env python3
"""Thru Alphanet Faucet Bot — Auto-distribute testnet tokens"""

import os
import subprocess
import json
import time
import sys

# Config
AMOUNT_PER_REQUEST = 1000  # tokens per request
MAX_DAILY = 10000  # max tokens per address per day
COOLDOWN = 60  # seconds between requests from same address
FEE_PAYER = os.environ.get("THRU_KEY_NAME", "default")

# Track requests
requests_log = {}


def thru_cmd(args: list[str], timeout: int = 30) -> dict:
    """Execute thru CLI command."""
    cmd = ["thru", "--json"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.stdout.strip():
            return json.loads(result.stdout)
        return {"error": result.stderr or "No output"}
    except Exception as e:
        return {"error": str(e)}


def can_request(address: str) -> tuple[bool, str]:
    """Check if address can request tokens."""
    now = time.time()
    
    if address in requests_log:
        last_time, total_amount = requests_log[address]
        
        # Cooldown check
        if now - last_time < COOLDOWN:
            remaining = int(COOLDOWN - (now - last_time))
            return False, f"Cooldown: wait {remaining}s"
        
        # Daily limit check
        if total_amount >= MAX_DAILY:
            return False, f"Daily limit reached: {total_amount}/{MAX_DAILY}"
    
    return True, "OK"


def distribute(address: str) -> dict:
    """Distribute tokens to an address."""
    can, reason = can_request(address)
    if not can:
        return {"success": False, "reason": reason}
    
    # Transfer tokens
    data = thru_cmd(["transfer", FEE_PAYER, address, str(AMOUNT_PER_REQUEST)])
    
    if "transfer" in data and data["transfer"].get("status") == "success":
        # Update log
        now = time.time()
        if address in requests_log:
            _, total = requests_log[address]
            requests_log[address] = (now, total + AMOUNT_PER_REQUEST)
        else:
            requests_log[address] = (now, AMOUNT_PER_REQUEST)
        
        return {
            "success": True,
            "amount": AMOUNT_PER_REQUEST,
            "signature": data["transfer"].get("signature", "N/A"),
        }
    else:
        return {"success": False, "reason": data.get("error", "Transfer failed")}


def batch_distribute(addresses: list[str]) -> list[dict]:
    """Distribute tokens to multiple addresses."""
    results = []
    for addr in addresses:
        result = distribute(addr)
        results.append({"address": addr, **result})
        time.sleep(0.5)  # Rate limit
    return results


def show_stats():
    """Show faucet statistics."""
    print("\n📊 Faucet Statistics")
    print("-" * 40)
    total_distributed = sum(amount for _, amount in requests_log.values())
    unique_addresses = len(requests_log)
    print(f"Total distributed: {total_distributed:,} tokens")
    print(f"Unique addresses: {unique_addresses}")
    print("-" * 40)


def interactive_mode():
    """Interactive faucet mode."""
    print("🚰 Thru Alphanet Faucet")
    print(f"Amount per request: {AMOUNT_PER_REQUEST} tokens")
    print(f"Daily limit: {MAX_DAILY} tokens")
    print(f"Cooldown: {COOLDOWN}s")
    print("\nCommands:")
    print("  <address>     - Distribute tokens")
    print("  batch         - Batch distribute (enter addresses)")
    print("  stats         - Show statistics")
    print("  quit          - Exit")
    print()
    
    while True:
        try:
            user_input = input("🚰 > ").strip()
            
            if user_input.lower() in ("quit", "exit", "q"):
                show_stats()
                print("Bye!")
                break
            
            if user_input.lower() == "stats":
                show_stats()
                continue
            
            if user_input.lower() == "batch":
                print("Enter addresses (one per line, empty to finish):")
                addresses = []
                while True:
                    addr = input("  Address: ").strip()
                    if not addr:
                        break
                    addresses.append(addr)
                
                if addresses:
                    print(f"\nDistributing to {len(addresses)} addresses...")
                    results = batch_distribute(addresses)
                    for r in results:
                        status = "✅" if r["success"] else "❌"
                        print(f"  {status} {r['address'][:20]}... — {r.get('amount', 0)} tokens")
                continue
            
            # Single address
            if user_input.startswith("ta"):
                result = distribute(user_input)
                if result["success"]:
                    print(f"✅ Sent {result['amount']} tokens to {user_input[:20]}...")
                else:
                    print(f"❌ Failed: {result['reason']}")
            else:
                print("Invalid address. Must start with 'ta'")
        
        except KeyboardInterrupt:
            show_stats()
            print("\nBye!")
            break
        except EOFError:
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # CLI mode: python3 faucet.py <address> [address2] ...
        addresses = sys.argv[1:]
        results = batch_distribute(addresses)
        for r in results:
            print(json.dumps(r))
    else:
        interactive_mode()
