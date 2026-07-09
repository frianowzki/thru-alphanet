# Thru Alphanet

Build ultra-high performance programs on Thru.

## Quick Start

```bash
npm i -g thru
thru keys generate default
thru account create default
thru faucet withdraw default 10000
```

## Projects

| Project | Path | Description |
|---------|------|-------------|
| Counter v7 | `examples/counter/` | Create, increment, decrement, reset, read |
| Voting v4 | `examples/counter/` | Create proposal, cast vote, close, results |
| Escrow v1 | `examples/counter/` | Create, release, dispute, refund, read |
| Telegram Bot | `thru-bot/` | Balance, send, deploy, status |
| MCP Server | `thru-mcp/` | AI agent tools (9 functions) |
| Frontend | `thru-frontend/` | Web UI — real on-chain |
| API Server | `thru-api/` | Backend proxy with ephemeral keys |
| Wallet | `thru-wallet/` | Multi-address wallet adapter |

## Frontend (Real On-Chain)

**Live:** [thru-counter.vercel.app](https://thru-counter.vercel.app)

Users enter their own private key + custom program/PDA addresses. API endpoint is auto-discovered.

### Self-Host API

```bash
# Install dependencies
# (thru CLI, cloudflared, gh CLI)

# Start API + tunnel
./thru-api/start.sh
```

Environment variables:
| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `3001` | API server port |
| `THRU_KEY_NAME` | `frio` | Key name from thru config |
| `THRU_GIST_ID` | (built-in) | Gist ID for API discovery |

### How It Works

```
Frontend (Vercel) → Gist (discover URL) → Cloudflare Tunnel → API (VPS) → thru CLI → Chain
```

Security model:
- Private key is ephemeral — imported → used → deleted per-request
- Never stored, logged, or cached on server
- All communication via HTTPS/TLS

## Deployed Programs

| Program | Address | Source |
|---------|---------|--------|
| Counter v7 | `ta2sYKmgW-b0FQEP2-pMYROxnAIMTrZTgpJqgVvxAHe423` | `tn_counter_v7.c` |
| Voting v4 | `taH5gAKRdirmY8kImoKAeW4lzk6fZCJbbNm6eLDtYcJxoo` | `tn_voting.c` |
| Escrow v1 | `taYRu8D8yaZksfNK42mTXIpbqVcmgS6Zr0agCeqOpBSOaL` | `tn_escrow.c` |

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
