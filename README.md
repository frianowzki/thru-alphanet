# Thru Alphanet

Build ultra-high performance programs on Thru — a clean, fast blockchain for real apps.

## Quick Start

```bash
# Install CLI
npm i -g thru

# Generate keypair
thru keys generate default

# Create account + fund it
thru account create default
thru faucet withdraw default 10000
```

## Projects

| Project | Path | What it does |
|---------|------|--------------|
| Counter v7 | `examples/counter/` | Create, increment, decrement, reset, read |
| Voting v4 | `examples/counter/` | Create proposal, cast vote, close, results |
| Escrow v1 | `examples/counter/` | Create, release, dispute, refund, read |
| Telegram Bot | `thru-bot/` | Balance, send, deploy, status via Telegram |
| MCP Server | `thru-mcp/` | AI agent tools (9 on-chain functions) |
| Frontend | `thru-frontend/` | Web UI — real on-chain operations |
| API Server | `thru-api/` | Backend proxy with ephemeral key security |
| Wallet CLI | `thru-wallet/` | Multi-address wallet adapter |

## Frontend

**Live:** [thru-counter.vercel.app](https://thru-counter.vercel.app)

A dark-themed web UI for interacting with deployed Thru programs. Real on-chain — not a mock.

### Features

- 🔗 **Real on-chain operations** — increment, decrement, reset, read counter value
- 🔐 **Ephemeral key security** — your private key is imported, used, and deleted per-request
- 🎨 **Dynamic gradient background** — animated blobs with Thru accent colors
- 📱 **Mobile + desktop** — responsive design, touch-optimized, smooth animations
- 💧 **Faucet** — request testnet tokens directly from the UI
- 📡 **Auto-discovery** — API endpoint fetched from GitHub Gist (no hardcoded URLs)

### Self-Host

```bash
# Start API server + Cloudflare tunnel
./thru-api/start.sh
```

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `3001` | API server port |
| `THRU_KEY_NAME` | `frio` | Server key name (pays tx fees) |
| `THRU_GIST_ID` | (built-in) | Gist ID for API URL discovery |

### Architecture

```
Frontend (Vercel) → GitHub Gist (discover URL) → Cloudflare Tunnel → API (VPS) → thru CLI → Chain
```

Security model:
- Private key is **ephemeral** — imported → used → deleted per-request
- Never stored, logged, or cached on server
- Server owner **cannot access** your key
- All communication encrypted via HTTPS/TLS
- Server pays transaction fees (your key is optional)

## Deployed Programs

| Program | Address | Source |
|---------|---------|--------|
| Counter v7 | `ta2sYKmgW-b0FQEP2-pMYROxnAIMTrZTgpJqgVvxAHe423` | `tn_counter_v7.c` |
| Voting v4 | `taH5gAKRdirmY8kImoKAeW4lzk6fZCJbbNm6eLDtYcJxoo` | `tn_voting.c` |
| Escrow v1 | `taYRu8D8yaZksfNK42mTXIpbqVcmgS6Zr0agCeqOpBSOaL` | `tn_escrow.c` |

## CLI Guide

### Key Management

```bash
# List all keys
thru keys list

# Generate a new keypair
thru keys generate mykey

# Show public key
thru keys show frio
```

### Account Operations

```bash
# Create account from key
thru account create frio

# Check balance
thru account balance frio

# Request testnet tokens
thru faucet withdraw frio 10000
```

### Counter Program

```bash
# Read counter value
thru contract call --program <PROGRAM_ADDR> --data '{"Read":{}}' --accounts <PDA>

# Increment counter
thru contract call --program <PROGRAM_ADDR> --data '{"Increment":{}}' --accounts <PDA>

# Decrement counter
thru contract call --program <PROGRAM_ADDR> --data '{"Decrement":{}}' --accounts <PDA>

# Reset counter
thru contract call --program <PROGRAM_ADDR> --data '{"Reset":{}}' --accounts <PDA>
```

### Wallet CLI

```bash
# List all addresses
node thru-wallet/cli.js list

# Check balance for specific address
node thru-wallet/cli.js balance <address>

# Get address from key name
node thru-wallet/cli.js address frio
```

### MCP Server (AI Agent Tools)

The MCP server exposes 9 on-chain tools for AI agents:

| Tool | Description |
|------|-------------|
| `get_balance` | Get account balance |
| `create_account` | Create new account |
| `transfer` | Send tokens to address |
| `deploy_program` | Deploy a new program |
| `call_program` | Call a deployed program |
| `get_counter` | Read counter value |
| `increment_counter` | Increment by 1 |
| `decrement_counter` | Decrement by 1 |
| `reset_counter` | Reset to 0 |

```bash
# Start MCP server
python3 thru-mcp/server.py
```

## Common Pitfalls

1. **`account_not_found`** — Run `thru account create <key>` before making transactions
2. **`FaucetError: 2`** — Key already has an account. Use `thru faucet withdraw` instead
3. **PDA mismatch** — PDA must be derived with correct seed bytes for the program
4. **Insufficient balance** — Each tx costs ~1 token. Ensure account is funded
5. **Stale tunnel URL** — Quick tunnels change on restart. Check Gist for current URL

## Resources

| Resource | Link |
|----------|------|
| Docs | [docs.thru.org](https://docs.thru.org) |
| GitHub | [Unto-Labs/thru](https://github.com/Unto-Labs/thru) |
| Explorer | [scan.thru.org](https://scan.thru.org) |

| Endpoint | URL |
|----------|-----|
| RPC | `https://rpc.alphanet.thru.org` |
| gRPC | `https://grpc.alphanet.thru.org` |
