<p align="center">
  <img src="https://img.shields.io/badge/status-alphanet-yellow?style=for-the-badge&labelColor=1a1a2e" alt="Status">
  <img src="https://img.shields.io/badge/RISC--V-64--bit-orange?style=for-the-badge&labelColor=1a1a2e" alt="VM">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge&labelColor=1a1a2e" alt="License">
</p>

<h1 align="center">🕊️ Thru Alphanet</h1>

<p align="center">
  <b>Build ultra-high performance programs on Thru</b><br>
  <sub>C SDK · RISC-V VM · Sub-ms latency · On-chain programs</sub>
</p>

<p align="center">
  <a href="https://docs.thru.org">Docs</a> ·
  <a href="https://github.com/Unto-Labs/thru">GitHub</a> ·
  <a href="https://scan.thru.org">Explorer</a>
</p>

---

## Quick Start

```bash
npm i -g thru                              # install CLI
thru keys generate default                 # generate keypair
thru account create default                # create account
thru faucet withdraw default 10000         # get testnet tokens
```

## DevKit

```bash
thru dev toolchain install                 # RISC-V compiler
thru dev sdk install c                     # C SDK headers + libs
```

SDK paths:
- Headers: `~/.thru/sdk/c/thru-sdk/include/`
- Compiler: `~/.thru/sdk/toolchain/bin/riscv64-unknown-elf-gcc`

## Project Structure

```
thru-alphanet/
├── examples/counter/        # On-chain programs (C)
│   ├── tn_counter_v7.c     # Counter (create/increment/decrement/reset/read)
│   ├── tn_voting.c         # Voting (create/cast/close/results)
│   └── tn_escrow.c         # Escrow (create/release/dispute/refund/read)
├── thru-bot/                # Telegram bot + tools
│   ├── bot.py              # Telegram bot
│   ├── faucet.py           # Testnet faucet
│   └── airdrop.py          # Bulk airdrop
├── thru-mcp/                # MCP server for AI agents
│   └── server.py
├── thru-frontend/           # Web UI
│   └── index.html
└── thru-wallet/             # Multi-address wallet
    ├── wallet.js           # Wallet adapter
    └── cli.js              # CLI interface
```

## Building Programs

```bash
make -j                                          # build
thru program create <seed> build/thruvm/bin/*.bin # deploy
thru program derive-address <prog> <seed>         # derive PDA
```

### C Program Template

```c
#include <thru-sdk/c/tn_sdk.h>
#include <thru-sdk/c/tn_sdk_syscall.h>

TSDK_ENTRYPOINT_FN void start(void) {
    tsdk_txn_t const *txn = tsdk_get_txn();
    uchar const *data = tsdk_txn_get_instr_data(txn);
    ulong data_sz = tsdk_txn_get_instr_data_sz(txn);

    uint const *instr_type = (uint const *)data;

    switch (*instr_type) {
        case 0: /* create */ break;
        case 1: /* action */ break;
        default: tsdk_revert(0x1000);
    }
    tsdk_return(TSDK_SUCCESS);
}
```

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `vm_error=-767` | Wrong entry point | Use `start(void)`, not `start(void*,ulong)` |
| `vm_error=-765` | Meta account conflict | Use account_index from instr data (usually 2) |
| `error=0x1000` | Bad instruction data | Check struct size matches hex |
| `error=0x1002` | Missing state proof | `thru txn make-state-proof creating <addr>` |

## Deployed Programs

| Program | Address | Source |
|---------|---------|--------|
| Counter v7 | `ta2sYKmgW-b0FQEP2-pMYROxnAIMTrZTgpJqgVvxAHe423` | `tn_counter_v7.c` |
| Voting v4 | `taH5gAKRdirmY8kImoKAeW4lzk6fZCJbbNm6eLDtYcJxoo` | `tn_voting.c` |
| Escrow v1 | `taYRu8D8yaZksfNK42mTXIpbqVcmgS6Zr0agCeqOpBSOaL` | `tn_escrow.c` |

### Counter Usage

```bash
# derive PDA
thru program derive-address ta2sYKmgW-b0FQEP2-pMYROxnAIMTrZTgpJqgVvxAHe423 my-counter

# increment
thru txn execute --fee 0 --readwrite-accounts <PDA> ta2sYKmgW-b0FQEP2-pMYROxnAIMTrZTgpJqgVvxAHe423 010000000200

# decrement
thru txn execute --fee 0 --readwrite-accounts <PDA> ta2sYKmgW-b0FQEP2-pMYROxnAIMTrZTgpJqgVvxAHe423 020000000200

# reset
thru txn execute --fee 0 --readwrite-accounts <PDA> ta2sYKmgW-b0FQEP2-pMYROxnAIMTrZTgpJqgVvxAHe423 030000000200

# read
thru txn execute --fee 0 --readwrite-accounts <PDA> ta2sYKmgW-b0FQEP2-pMYROxnAIMTrZTgpJqgVvxAHe423 040000000200
```

## Wallet

Multi-address wallet adapter for Thru Alphanet.

```bash
cd thru-wallet && npm install

node cli.js generate                        # generate new keypair
node cli.js add alice <YOUR_ADDRESS>        # add existing address
node cli.js list                            # list all addresses
node cli.js switch alice                    # set active address
node cli.js balance                         # check active balance
node cli.js balance bob                     # check specific address
node cli.js pda <program> <seed>            # derive PDA
```

### Keystore

Saved to `~/.thru/keystore/wallet.json`:

```json
{
  "addresses": [
    { "name": "alice", "address": "ta...", "addedAt": "2026-07-09T..." },
    { "name": "bob", "address": "ta2sY...", "addedAt": "2026-07-09T..." }
  ],
  "active": "alice"
}
```

## Telegram Bot

```bash
pip install python-telegram-bot
export THRU_BOT_TOKEN="token-from-BotFather"
python3 thru-bot/bot.py
```

Commands: `/balance`, `/send`, `/deploy`, `/programs`, `/status`

## MCP Server (AI Agents)

```bash
pip install mcp
python3 thru-mcp/server.py

# Add to Claude Code
claude mcp add --transport stdio thru-mcp python3 ~/thru-mcp/server.py
```

Tools: `get_balance`, `get_block_height`, `get_health`, `get_transaction`, `derive_address`, `make_state_proof`

## Frontend (Real On-Chain)

**Live:** [thru-counter.vercel.app](https://thru-counter.vercel.app)

Web UI with real on-chain execution. Users enter their own private key + custom program/PDA addresses.

**Security:** Private key is ephemeral — imported → used → deleted per-request. Never stored or logged.

```bash
# Start API server (proxies to thru CLI)
cd ~/thru-alphanet && THRU_KEY_NAME=frio PORT=3001 python3 thru-api/server.py

# Open http://localhost:3001
```

**How it works:**
```
Browser → API Server (localhost:3001) → thru CLI → Thru Blockchain
```

**API Endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Network health |
| `/api/wallet/balance` | GET | Active wallet balance |
| `/api/counter/value?pda=<addr>` | GET | Read counter value |
| `/api/counter/execute` | POST | Execute inc/dec/reset |
| `/api/counter/create` | POST | Create new counter PDA |

**Environment Variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `3001` | Server port |
| `THRU_KEY_NAME` | `default` | Key name from `~/.thru/cli/config.yaml` |
| `THRU_COUNTER_PROGRAM` | (counter v7 address) | Program address |

## Faucet & Airdrop

```bash
# Faucet
python3 thru-bot/faucet.py                          # interactive
python3 thru-bot/faucet.py <address1> <address2>    # CLI

# Airdrop
python3 thru-bot/airdrop.py airdrop addresses.csv 100
python3 thru-bot/airdrop.py send <address> 100
```

CSV format: `address,amount` per line.

## Useful Commands

```bash
# Status
thru getversion; thru gethealth; thru getheight

# Keys & Accounts
thru keys generate <name>; thru keys list
thru account create <name>; thru getbalance <addr>

# Programs
thru program create <seed> <binary>
thru program upgrade <seed> <binary>
thru program derive-address <prog> <seed>
thru program seed-to-hex <seed>

# Transactions
thru txn execute --fee 0 --readwrite-accounts <acct> <program> <hex>
thru txn make-state-proof creating <addr>

# Tokens
thru token initialize-mint <creator> <ticker> <seed> --decimals 9
thru token initialize-account <mint> <owner> <seed>
thru token mint-to <mint> <to> <authority> <amount>
thru token transfer <from> <to> <amount>
thru token balance <account>
```

## Resources

| Resource | Link |
|----------|------|
| Documentation | [docs.thru.org](https://docs.thru.org) |
| GitHub | [Unto-Labs/thru](https://github.com/Unto-Labs/thru) |
| Explorer | [scan.thru.org](https://scan.thru.org) |
| AI Skills | [Unto-Labs/ai](https://github.com/Unto-Labs/ai) |
| LLM Docs | [llms-full.txt](https://docs.thru.org/llms-full.txt) |

| Endpoint | URL |
|----------|-----|
| RPC | `https://rpc.alphanet.thru.org` |
| gRPC | `https://grpc.alphanet.thru.org` |
| Explorer MCP | `https://scan.thru.org/api/mcp` |

---

<p align="center">
  <sub>Built with ⚡ for the Thru Alphanet · July 2026</sub>
</p>
