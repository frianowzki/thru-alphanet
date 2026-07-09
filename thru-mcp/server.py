#!/usr/bin/env python3
"""Thru Alphanet MCP Server — Custom chain explorer for AI agents"""

import os
import subprocess
import json
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("thru-explorer")

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


@mcp.tool()
def get_balance(address: str) -> str:
    """Get account balance.
    
    Args:
        address: Account address (ta... format)
    """
    data = thru_cmd(["account", "info", address])
    if "account_info" in data:
        info = data["account_info"]
        return json.dumps({
            "address": info.get("address", address),
            "balance": info.get("balance", 0),
            "nonce": info.get("nonce", 0),
        }, indent=2)
    return json.dumps(data)


@mcp.tool()
def get_block_height() -> str:
    """Get current block height."""
    data = thru_cmd(["getheight"])
    return json.dumps(data, indent=2)


@mcp.tool()
def get_health() -> str:
    """Get network health status."""
    data = thru_cmd(["gethealth"])
    return json.dumps(data, indent=2)


@mcp.tool()
def get_transaction(signature: str) -> str:
    """Get transaction details by signature.
    
    Args:
        signature: Transaction signature (ts... format)
    """
    data = thru_cmd(["transaction", "get", signature])
    return json.dumps(data, indent=2)


@mcp.tool()
def get_program_info(address: str) -> str:
    """Get program information.
    
    Args:
        address: Program address (ta... format)
    """
    data = thru_cmd(["program", "get", address])
    return json.dumps(data, indent=2)


@mcp.tool()
def derive_address(program_id: str, seed: str) -> str:
    """Derive PDA address from program and seed.
    
    Args:
        program_id: Program address
        seed: Seed string for derivation
    """
    data = thru_cmd(["program", "derive-address", program_id, seed])
    if "derive_address" in data:
        info = data["derive_address"]
        return json.dumps({
            "program_id": info["program_id"],
            "seed": info["seed"],
            "derived_address": info["derived_address"],
        }, indent=2)
    return json.dumps(data)


@mcp.tool()
def make_state_proof(proof_type: str, address: str) -> str:
    """Generate state proof for an account.
    
    Args:
        proof_type: Proof type (creating, existing, updating)
        address: Account address
    """
    data = thru_cmd(["txn", "make-state-proof", proof_type, address])
    if "makeStateProof" in data:
        info = data["makeStateProof"]
        return json.dumps({
            "account": info["account"],
            "proof_type": info["proof_type"],
            "proof_size_bytes": info["proof_size_bytes"],
            "proof_data_hex": info["proof_data_hex"][:64] + "...",
        }, indent=2)
    return json.dumps(data)


@mcp.tool()
def list_programs(limit: int = 10) -> str:
    """List recent deployed programs.
    
    Args:
        limit: Number of programs to list
    """
    data = thru_cmd(["program", "list", "--limit", str(limit)])
    return json.dumps(data, indent=2)


@mcp.tool()
def get_network_info() -> str:
    """Get comprehensive network information."""
    height = thru_cmd(["getheight"])
    health = thru_cmd(["gethealth"])
    version = thru_cmd(["getversion"])
    
    return json.dumps({
        "height": height.get("height", "N/A"),
        "health": health.get("health", "N/A"),
        "version": version.get("version", "N/A"),
        "rpc_url": RPC_URL,
    }, indent=2)


@mcp.resource("thru://network/status")
def network_status() -> str:
    """Get current network status as a resource."""
    data = thru_cmd(["getheight"])
    return f"Current block height: {data.get('height', 'N/A')}"


@mcp.resource("thru://network/endpoints")
def network_endpoints() -> str:
    """Get available network endpoints."""
    return json.dumps({
        "rpc": RPC_URL,
        "grpc": "https://grpc.alphanet.thru.org",
        "explorer": "https://scan.thru.org",
        "mcp": "https://scan.thru.org/api/mcp",
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
