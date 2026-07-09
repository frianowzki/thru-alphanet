#!/usr/bin/env python3
"""Thru Alphanet Airdrop Tool — Bulk send tokens to multiple wallets"""

import os
import subprocess
import json
import csv
import time
import sys
from datetime import datetime

# Config
DEFAULT_AMOUNT = 100
FEE_PAYER = "frio"
RPC_URL = "https://rpc.alphanet.thru.org"


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


def get_balance(address: str) -> int:
    """Get account balance."""
    data = thru_cmd(["account", "info", address])
    if "account_info" in data:
        return data["account_info"].get("balance", 0)
    return 0


def send_tokens(to_address: str, amount: int) -> dict:
    """Send tokens to an address."""
    data = thru_cmd(["transfer", FEE_PAYER, to_address, str(amount)])
    
    if "transfer" in data and data["transfer"].get("status") == "success":
        return {
            "success": True,
            "signature": data["transfer"].get("signature", "N/A"),
            "amount": amount,
        }
    else:
        return {
            "success": False,
            "error": data.get("error", "Transfer failed"),
        }


def airdrop_from_csv(csv_path: str, amount: int = DEFAULT_AMOUNT, dry_run: bool = False) -> dict:
    """Airdrop tokens from a CSV file.
    
    CSV format: address,amount (amount is optional, uses default if not provided)
    """
    results = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "total_amount": 0,
        "transactions": [],
        "errors": [],
    }
    
    if not os.path.exists(csv_path):
        return {"error": f"File not found: {csv_path}"}
    
    # Read CSV
    addresses = []
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            addr = row[0].strip()
            amt = int(row[1].strip()) if len(row) > 1 and row[1].strip() else amount
            addresses.append((addr, amt))
    
    results["total"] = len(addresses)
    print(f"📋 Loaded {len(addresses)} addresses from {csv_path}")
    
    if dry_run:
        print("🔍 Dry run mode — no transactions will be sent")
        for addr, amt in addresses:
            print(f"  Would send {amt} tokens to {addr[:20]}...")
        return results
    
    # Execute airdrop
    for i, (addr, amt) in enumerate(addresses, 1):
        print(f"[{i}/{len(addresses)}] Sending {amt} tokens to {addr[:20]}...", end=" ")
        
        result = send_tokens(addr, amt)
        
        if result["success"]:
            results["success"] += 1
            results["total_amount"] += amt
            results["transactions"].append({
                "address": addr,
                "amount": amt,
                "signature": result["signature"],
            })
            print(f"✅ {result['signature'][:20]}...")
        else:
            results["failed"] += 1
            results["errors"].append({
                "address": addr,
                "error": result.get("error", "Unknown"),
            })
            print(f"❌ {result.get('error', 'Failed')[:50]}")
        
        time.sleep(0.5)  # Rate limit
    
    return results


def airdrop_from_list(addresses: list[str], amount: int = DEFAULT_AMOUNT) -> dict:
    """Airdrop tokens from a list of addresses."""
    results = {
        "total": len(addresses),
        "success": 0,
        "failed": 0,
        "total_amount": 0,
        "transactions": [],
        "errors": [],
    }
    
    for i, addr in enumerate(addresses, 1):
        print(f"[{i}/{len(addresses)}] Sending {amount} tokens to {addr[:20]}...", end=" ")
        
        result = send_tokens(addr, amount)
        
        if result["success"]:
            results["success"] += 1
            results["total_amount"] += amount
            results["transactions"].append({
                "address": addr,
                "amount": amount,
                "signature": result["signature"],
            })
            print(f"✅")
        else:
            results["failed"] += 1
            results["errors"].append({
                "address": addr,
                "error": result.get("error", "Unknown"),
            })
            print(f"❌")
        
        time.sleep(0.5)
    
    return results


def save_results(results: dict, output_path: str):
    """Save airdrop results to CSV."""
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["address", "amount", "status", "signature", "error"])
        
        for tx in results.get("transactions", []):
            writer.writerow([tx["address"], tx["amount"], "success", tx["signature"], ""])
        
        for err in results.get("errors", []):
            writer.writerow([err["address"], 0, "failed", "", err["error"]])
    
    print(f"\n📄 Results saved to {output_path}")


def print_summary(results: dict):
    """Print airdrop summary."""
    print("\n" + "=" * 50)
    print("📊 Airdrop Summary")
    print("=" * 50)
    print(f"Total addresses: {results['total']}")
    print(f"Successful: {results['success']}")
    print(f"Failed: {results['failed']}")
    print(f"Total distributed: {results['total_amount']:,} tokens")
    print("=" * 50)


def interactive_mode():
    """Interactive airdrop mode."""
    print("🚀 Thru Alphanet Airdrop Tool")
    print(f"Default amount: {DEFAULT_AMOUNT} tokens")
    print(f"Fee payer: {FEE_PAYER}")
    print("\nCommands:")
    print("  airdrop <csv> [amount]  - Airdrop from CSV file")
    print("  send <addr> <amount>    - Send to single address")
    print("  balance                 - Check fee payer balance")
    print("  quit                    - Exit")
    print()
    
    # Check balance
    balance = get_balance(FEE_PAYER)
    print(f"💰 Fee payer balance: {balance:,} tokens")
    print()
    
    while True:
        try:
            user_input = input("🚀 > ").strip()
            
            if user_input.lower() in ("quit", "exit", "q"):
                print("Bye!")
                break
            
            if user_input.lower() == "balance":
                balance = get_balance(FEE_PAYER)
                print(f"💰 Balance: {balance:,} tokens")
                continue
            
            parts = user_input.split()
            
            if parts[0].lower() == "send" and len(parts) >= 3:
                addr = parts[1]
                amt = int(parts[2])
                result = send_tokens(addr, amt)
                if result["success"]:
                    print(f"✅ Sent {amt} tokens to {addr[:20]}...")
                else:
                    print(f"❌ Failed: {result.get('error', 'Unknown')}")
                continue
            
            if parts[0].lower() == "airdrop":
                if len(parts) < 2:
                    print("Usage: airdrop <csv_file> [amount]")
                    continue
                
                csv_path = parts[1]
                amt = int(parts[2]) if len(parts) > 2 else DEFAULT_AMOUNT
                
                # Dry run first
                print("\n🔍 Dry run:")
                results = airdrop_from_csv(csv_path, amt, dry_run=True)
                
                confirm = input("\nProceed? (y/N): ").strip().lower()
                if confirm == "y":
                    results = airdrop_from_csv(csv_path, amt, dry_run=False)
                    print_summary(results)
                    
                    # Save results
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = f"airdrop_{timestamp}.csv"
                    save_results(results, output_path)
                else:
                    print("Cancelled.")
                continue
            
            print("Unknown command. Type 'help' for usage.")
        
        except KeyboardInterrupt:
            print("\nBye!")
            break
        except EOFError:
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "airdrop" and len(sys.argv) >= 3:
            csv_path = sys.argv[2]
            amount = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_AMOUNT
            results = airdrop_from_csv(csv_path, amount)
            print_summary(results)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_results(results, f"airdrop_{timestamp}.csv")
        elif sys.argv[1] == "send" and len(sys.argv) >= 4:
            result = send_tokens(sys.argv[2], int(sys.argv[3]))
            print(json.dumps(result))
        else:
            print("Usage:")
            print("  python3 airdrop.py airdrop <csv_file> [amount]")
            print("  python3 airdrop.py send <address> <amount>")
    else:
        interactive_mode()
