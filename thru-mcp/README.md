# Thru Alphanet MCP Server

Model Context Protocol server untuk AI agents interact sama Thru blockchain.

## Setup

```bash
pip install mcp
python3 server.py
```

## Tools

| Tool | Description |
|------|-------------|
| `get_balance` | Check account balance |
| `get_block_height` | Get current block height |
| `get_health` | Network health status |
| `get_transaction` | Get transaction details |
| `get_program_info` | Get program information |
| `derive_address` | Derive PDA address |
| `make_state_proof` | Generate state proof |
| `list_programs` | List deployed programs |
| `get_network_info` | Comprehensive network info |

## Resources

| Resource | Description |
|----------|-------------|
| `thru://network/status` | Current network status |
| `thru://network/endpoints` | Available endpoints |

## Usage with Claude Code

```bash
claude mcp add --transport stdio thru-explorer python3 /home/frio/thru-mcp/server.py
```
