# Thru Alphanet — Complete Developer Guide

> Comprehensive reference for building on Thru, a high-performance blockchain network for ultra-low latency, ultra-high throughput applications.

**Status:** Alphanet (pre-mainnet)  
**Docs:** [docs.thru.org](https://docs.thru.org)  
**GitHub:** [Unto-Labs/thru](https://github.com/Unto-Labs/thru)  
**RPC:** `https://rpc.alphanet.thru.org`  
**Explorer:** [scan.thru.org](https://scan.thru.org)

---

## Table of Contents

- [What is Thru](#what-is-thru)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
- [DevKit Setup](#devkit-setup)
- [CLI Reference](#cli-reference)
- [Program Development (C SDK)](#program-development-c-sdk)
- [ABI System](#abi-system)
- [Core Concepts](#core-concepts)
- [Virtual Machine (ThruVM)](#virtual-machine-thruvm)
- [Runtime & Execution](#runtime--execution)
- [Accounts & State](#accounts--state)
- [SDKs & Packages](#sdks--packages)
- [APIs](#apis)
- [Wallet & Passkey](#wallet--passkey)
- [Token Program](#token-program)
- [NFT Program](#nft-program)
- [Core Specifications](#core-specifications)
- [Building with AI Agents](#building-with-ai-agents)
- [Useful Commands Cheat Sheet](#useful-commands-cheat-sheet)

---

## What is Thru

Thru is a high-performance blockchain network built by [Unto-Labs](https://github.com/Unto-Labs). Key characteristics:

- **Ultra-high throughput** with sub-millisecond latency
- **RISC-V based VM** (ThruVM) — programs written in C, compiled to RISC-V bytecode
- **Account-based state model** with compression and state proofs
- **Developer-first** — comprehensive SDKs, CLI, and AI-agent friendly docs
- **gRPC + REST APIs** for high-performance and browser-based access

### Why Thru?

| Feature | Thru | Traditional Blockchains |
|---------|------|------------------------|
| VM Architecture | RISC-V (64-bit) | EVM, WASM, custom |
| Program Language | C (native) | Solidity, Rust, etc. |
| Latency | Sub-millisecond | Seconds to minutes |
| State Model | Accounts + Compression | Accounts/UTXO |
| Developer Tooling | CLI + SDK + MCP | Varies |

---

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│                 Applications                 │
│         (Web, Mobile, Backend)               │
└─────────────────┬───────────────────────────┘
                  │ RPC / gRPC
┌─────────────────▼───────────────────────────┐
│              RPC Nodes                       │
│    (Query, Submit Transactions)              │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           Validator Network                  │
│  ┌─────────────────────────────────────┐    │
│  │         ThruVM (RISC-V)             │    │
│  │   Execute programs deterministically │    │
│  └─────────────────────────────────────┘    │
│  ┌─────────────────────────────────────┐    │
│  │      Consensus (agreement)          │    │
│  └─────────────────────────────────────┘    │
│  ┌─────────────────────────────────────┐    │
│  │      State Tree (Merkle)            │    │
│  │   Accounts + Compression            │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

### Key Components

| Component | Description |
|-----------|-------------|
| **ThruVM** | RISC-V virtual machine executing smart contracts |
| **Validators** | Physical nodes running consensus and execution |
| **RPC Nodes** | Interface for clients to query/submit transactions |
| **State Tree** | Merkle tree storing account state with compression support |
| **gRPC API** | High-performance Protocol Buffers API |
| **Explorer MCP** | Live chain context for AI coding agents |

---

## Quick Start

### 1. Install CLI

```bash
npm i -g thru
```

Or via .deb/.rpm:
```bash
# Debian/Ubuntu
curl -fsSLO https://github.com/Unto-Labs/thru/releases/download/v0.2.27/thru_0.2.27_amd64.deb
sudo apt install ./thru_0.2.27_amd64.deb

# RHEL/Fedora
sudo dnf install https://github.com/Unto-Labs/thru/releases/download/v0.2.27/thru-0.2.27-1.x86_64.rpm
```

### 2. Verify

```bash
thru --help
thru getversion
```

### 3. Generate Keypair

```bash
thru keys generate default
```

### 4. Create Account

```bash
thru account create default
```

### 5. Get Testnet Tokens

```bash
thru faucet request default
```

### 6. Deploy a Program

```bash
thru program create my_program ./path/to/program.bin
```

---

## DevKit Setup

### Prerequisites

- **Node.js 18+** — [nodejs.org](https://nodejs.org)
- **Linux x64** (recommended) with `curl` and `sudo`
- macOS/Windows supported for CLI, Linux needed for full toolchain

### Full Setup

```bash
# 1. Install CLI
npm i -g thru

# 2. Install RISC-V toolchain
thru dev toolchain install

# 3. Install C SDK
thru dev sdk install c

# 4. Verify
thru --help
```

### SDK Locations

| Component | Default Path |
|-----------|-------------|
| C SDK | `~/.thru/sdk/c/thru-sdk/` |
| Toolchain | `~/.thru/sdk/toolchain/` |
| Config | `~/.thru/cli/config.yaml` |

### Configuration

Edit `~/.thru/cli/config.yaml`:

```yaml
rpc_base_url: https://rpc.alphanet.thru.org
```

Keypairs are stored as plaintext hex in the same config file. **Never share your private key.**

---

## CLI Reference

### Core Commands

| Command | Description |
|---------|-------------|
| `thru getversion` | Get node version |
| `thru gethealth` | Health status |
| `thru getstatus` | Node operational status (consensus, repair, heights) |
| `thru getheight` | Cluster block heights |
| `thru getaccountinfo` | Account information |
| `thru getbalance` | Account balance |
| `thru transfer` | Transfer tokens |
| `thru keys generate` | Generate keypair |
| `thru account create` | Create on-chain account |

### Program Management

| Command | Description |
|---------|-------------|
| `thru program create` | Upload & create managed program |
| `thru program upgrade` | Upgrade existing program |
| `thru program set-pause` | Pause/unpause program |
| `thru program finalize` | Make program immutable |
| `thru program destroy` | Destroy program |
| `thru program derive-address` | Derive PDA address |
| `thru program seed-to-hex` | Convert seed to hex |

### ABI Management

| Command | Description |
|---------|-------------|
| `thru abi account create` | Publish ABI to chain |
| `thru abi account get` | Read ABI from chain |
| `thru abi analyze` | Validate ABI locally |
| `thru abi codegen` | Generate client code |
| `thru abi reflect` | Decode binary payloads |

### Transaction Commands

| Command | Description |
|---------|-------------|
| `thru txn execute` | Execute transaction |
| `thru txn make-state-proof` | Generate state proof |

### Network & Token

| Command | Description |
|---------|-------------|
| `thru network` | Network profile management |
| `thru token` | Token program commands |
| `thru faucet` | Faucet commands |
| `thru registrar` | Registrar commands |
| `thru nameservice` | Name service commands |
| `thru wthru` | Wrapped Thru (WTHRU) commands |
| `thru validator` | Validator program commands |

### Utility

| Command | Description |
|---------|-------------|
| `thru util` | Format conversion utilities |
| `thru debug` | Transaction analysis |
| `thru dev` | Developer tools (toolchain, SDK) |

---

## Program Development (C SDK)

### Project Structure

```
my-thru-project/
├── GNUmakefile
└── examples/
    ├── Local.mk
    ├── my_program.h
    └── my_program.c
```

### GNUmakefile

```makefile
BASEDIR:=$(CURDIR)/build
THRU_C_SDK_DIR:=$(HOME)/.thru/sdk/c/thru-sdk
include $(THRU_C_SDK_DIR)/thru_c_program.mk
```

### examples/Local.mk

```makefile
$(call make-bin,my_program_c,my_program,,-ltn_sdk)
```

### Program Header (.h)

```c
#ifndef MY_PROGRAM_H
#define MY_PROGRAM_H

#include <thru-sdk/c/tn_sdk.h>

/* Error codes */
#define MY_ERR_INVALID_DATA   (0x1000UL)
#define MY_ERR_CREATE_FAILED  (0x1001UL)

/* Instruction types */
#define MY_INSTRUCTION_INIT   (0U)
#define MY_INSTRUCTION_UPDATE (1U)

/* Account data structure */
typedef struct __attribute__((packed)) {
    ulong value;
} my_account_t;

#endif
```

### Program Implementation (.c)

```c
#include <thru-sdk/c/tn_sdk.h>
#include <thru-sdk/c/tn_sdk_syscall.h>
#include "my_program.h"

TSDK_ENTRYPOINT_FN void start(void) {
    tsdk_txn_t const *txn = tsdk_get_txn();
    uchar const *data = tsdk_txn_get_instr_data(txn);
    ulong data_sz = tsdk_txn_get_instr_data_sz(txn);

    /* Validate input size */
    if (data_sz < sizeof(uint)) {
        tsdk_revert(MY_ERR_INVALID_DATA);
    }

    uint const *instr_type = (uint const *)data;

    switch (*instr_type) {
        case MY_INSTRUCTION_INIT: {
            ushort account_idx = *(ushort *)(data + sizeof(uint));
            
            /* Create account */
            ulong result = tsys_account_create(account_idx, seed, proof, proof_sz);
            if (result != TSDK_SUCCESS) tsdk_revert(MY_ERR_CREATE_FAILED);
            
            /* Set writable */
            tsys_set_account_data_writable(account_idx);
            
            /* Resize and initialize */
            tsys_account_resize(account_idx, sizeof(my_account_t));
            my_account_t *acct = (my_account_t *)tsdk_get_account_data_ptr(account_idx);
            acct->value = 0;
            
            tsdk_return(TSDK_SUCCESS);
            break;
        }
        case MY_INSTRUCTION_UPDATE: {
            ushort account_idx = *(ushort *)(data + sizeof(uint));
            tsys_set_account_data_writable(account_idx);
            my_account_t *acct = (my_account_t *)tsdk_get_account_data_ptr(account_idx);
            acct->value++;
            tsys_emit_event((uchar const *)&acct->value, sizeof(ulong));
            tsdk_return(TSDK_SUCCESS);
            break;
        }
        default:
            tsdk_revert(MY_ERR_INVALID_DATA);
    }
}
```

### Build & Deploy

```bash
# Build
make

# Verify
ls build/thruvm/bin/

# Deploy
thru program create my_seed ./build/thruvm/bin/my_program_c.bin

# Upgrade (same seed)
thru program upgrade my_seed ./build/thruvm/bin/my_program_c.bin
```

### Key SDK Functions

| Function | Description |
|----------|-------------|
| `tsdk_get_txn()` | Get current transaction |
| `tsdk_txn_get_instr_data()` | Get instruction data |
| `tsdk_get_account_data_ptr()` | Get account data pointer |
| `tsdk_return(TSDK_SUCCESS)` | Exit successfully |
| `tsdk_revert(error_code)` | Exit with error |
| `tsys_account_create()` | Create new account |
| `tsys_account_resize()` | Resize account data |
| `tsys_set_account_data_writable()` | Mark account writable |
| `tssys_account_compress()` | Compress account (save storage) |
| `tsys_account_decompress()` | Decompress account |
| `tsys_emit_event()` | Emit event |

---

## ABI System

ABI (Application Binary Interface) on Thru defines the binary data layout for instructions and account state.

### ABI YAML Structure

```yaml
abi:
  package: my.program.name
  name: "My Program"
  abi-version: 1
  package-version: 1.0.0
  description: "Description here"
  imports: []
  options:
    program-metadata:
      instruction-root: "MyInstruction"
      account-root: "MyAccount"
      errors: "MyError"
      events: "MyEvent"

types:
  - name: MyInstruction
    kind:
      struct:
        packed: true
        fields:
          - name: tag
            field-type:
              primitive: u8
          - name: payload
            field-type:
              enum:
                packed: true
```

### ABI Workflow

1. **Author** — Write ABI YAML by hand (start from examples)
2. **Validate** — `thru abi analyze ./program.abi.yaml`
3. **Codegen** — `thru abi codegen --files ./program.abi.yaml --language typescript --output ./generated/`
4. **Publish** — `thru abi account create my_seed ./program.abi.yaml`
5. **Verify** — `thru abi account get --include-data <ABI_ADDRESS>`

### ABI Gotchas

- ABIs are **handwritten** — they don't auto-sync with program changes
- Always validate before publishing
- Use `__attribute__((packed))` in C structs
- Use `options.program-metadata.root-types` for explorer compatibility
- Match program seed between `thru program create` and `thru abi account create`

---

## Core Concepts

### Account Model

Every piece of state on Thru is an **account**. Accounts have:
- **Address** — unique identifier (starts with `ta`)
- **Data** — binary payload (program code or state)
- **Owner** — program that owns the account
- **Flags** — compressed, writable, etc.

### Program-Derived Addresses (PDAs)

Accounts can be deterministically derived from a program + seed:

```bash
thru program derive-address <program_address> <seed>
```

Same seed always produces the same address — no on-chain lookup needed.

### State Proofs

When creating or modifying accounts, cryptographic state proofs verify the account's existence in the Merkle tree:

```bash
thru txn make-state-proof creating <account_address>
```

Proof types: `creating`, `existing`, `updating`

### Transactions

A transaction contains:
1. **Fee payer** (index 0) — pays for execution
2. **Program** (index 1) — the code to execute
3. **Writable accounts** (index 2+) — accounts the program can modify
4. **Read-only accounts** — accounts the program can only read
5. **Instruction data** — hex-encoded payload

```bash
thru txn execute \
  --fee 0 \
  --readwrite-accounts <account_address> \
  <program_address> \
  <hex_instruction_data>
```

### Compute Units (CUs)

Each transaction consumes compute units based on:
- Instructions executed
- Memory used
- Account storage consumed

Max CUs per transaction limits program complexity.

---

## Virtual Machine (ThruVM)

### RISC-V Architecture

ThruVM implements a **64-bit RISC-V** virtual machine:

| Extension | Purpose |
|-----------|---------|
| **RV64I** | Base integer instructions (arithmetic, logic, control flow) |
| **M** | Integer multiplication/division |
| **C** | Compressed 16-bit instructions (smaller code) |
| **B** | Bit manipulation (count, rotate, permute) |
| **Zknh** | Cryptographic hash acceleration (SHA-256, SHA-512) |

### Memory Layout

48-bit segmented address space:

```
Bits: 47-40  |  39-24   |  23-0
     seg_type| seg_idx  | offset
    (8 bits) |(16 bits) |(24 bits)
```

| Segment Type | Name | Purpose |
|-------------|------|---------|
| 0x00 | Read-Only | Transaction data, shadow stack, program bytecode, block context |
| 0x02 | Account Metadata | Account metadata structures |
| 0x03 | Account Data | Page-based account data (COW) |
| 0x04 | Event Data | Event emission buffer |
| 0x05 | Stack | Grows downward (16MB max) |
| 0x07 | Heap | Grows upward (16MB max) |

### Executable Format

```
┌──────────┐
│ Header   │  8 bytes (magic + version + size)
├──────────┤
│ Bytecode │  RISC-V instructions
├──────────┤
│ Footer   │  4 bytes (checksum)
└──────────┘
```

### Key Constraints

- **IALIGN=16** — all instructions aligned to 16-bit boundaries
- **No unaligned access** — triggers exception
- **Single-threaded** — deterministic execution
- **4KB pages** — memory allocated in 4KB chunks
- **Copy-on-Write** — account data uses COW semantics

---

## Runtime & Execution

### Transaction Execution Flow

1. Deserialize transaction
2. Validate accounts and signatures
3. Set up VM memory segments
4. Execute program bytecode
5. Apply state changes (or revert on error)
6. Emit events
7. Commit to state tree

### Syscalls

Programs interact with the runtime via syscalls:

| Code | Syscall | Description |
|------|---------|-------------|
| 0x01 | `account_create` | Create new account |
| 0x02 | `account_resize` | Resize account data |
| 0x03 | `account_delete` | Delete account |
| 0x04 | `account_compress` | Compress account |
| 0x05 | `account_decompress` | Decompress account |
| 0x06 | `emit_event` | Emit event |
| 0x07 | `exit` | Exit program |
| 0x08 | `invoke` | Call another program (CPI) |
| 0x09 | `log` | Log message |
| 0x0A | `set_account_data_writable` | Mark account writable |

### Error Handling

Programs use:
- `tsdk_return(TSDK_SUCCESS)` — success
- `tsdk_revert(error_code)` — revert with custom error code

On revert, all state changes are rolled back.

---

## Accounts & State

### Account Lifecycle

```
Create → Active → Compress → (stored off-chain)
              ↓                ↓
          Decompress ←←←←←←←←←←
              ↓
          Active → Delete
```

### Account Compression

Accounts can be **compressed** to save validator storage:
- Data removed from active storage
- State committed to Merkle tree
- Decompress with state proof when needed

```c
// Compress
tsys_account_compress(account_idx, proof, proof_sz);

// Decompress
tsys_account_decompress(account_idx, proof, proof_sz);
```

### Account Addresses

Thru addresses start with `ta` and are base64url-encoded. Two account types:
- **Regular accounts** — created with `thru account create`
- **Program accounts** — created with `thru program create`

---

## SDKs & Packages

### NPM Packages

| Package | Description |
|---------|-------------|
| `@thru/sdk` | TypeScript/JS client — blocks, accounts, transactions, events, proofs |
| `@thru/programs` | Token program bindings — create/manage tokens |
| `@thru/passkey` | WebAuthn/passkey signing helpers |
| `@thru/indexer` | Drizzle-backed indexer framework |
| `@thru/replay` | Historical + live chain data replay |

### Rust Crates

| Crate | Description |
|-------|-------------|
| `thru-base` | Core Rust primitives, transaction builders, crypto helpers |
| `thru-grpc-client` | Generated gRPC bindings (tonic + prost) |
| `thru` | CLI implementation |

### Install

```bash
# NPM
npm i @thru/sdk @thru/programs @thru/passkey

# Rust
cargo add thru-base thru-grpc-client
```

---

## APIs

### gRPC API (Recommended for Performance)

- **Protocol Buffers** serialization (2-10x smaller than JSON)
- **Streaming** support (server-streaming, bidirectional)
- **Binary** encoding for efficiency

**Endpoint:** `https://grpc.alphanet.thru.org`

**Services:**

| Service | Purpose |
|---------|---------|
| `CommandService` | Send transactions, batch send, send-and-track |
| `QueryService` | Get blocks, transactions, accounts, events, state roots |
| `StreamingService` | Stream blocks, transactions, events, account updates |
| `DebugService` | Re-execute transactions for debugging |

### REST/JSON API

For browser and simple integrations. Same data, JSON format.

**Endpoint:** `https://rpc.alphanet.thru.org`

### Explorer MCP

Live chain context for AI coding agents:

```
https://scan.thru.org/api/mcp
```

Add to Claude Code:
```bash
claude mcp add --transport http thru-explorer https://scan.thru.org/api/mcp
```

**Tools:** `get_block`, `get_transaction`, `get_account`, `list_recent_blocks`, `list_recent_transactions`, `search`, `get_program_abi`

---

## Wallet & Passkey

### Passkey Manager Program

On-chain program for WebAuthn/passkey-backed authorization.

**How it works:**
1. User registers passkey (WebAuthn credential)
2. For each transaction, program builds a challenge from wallet nonce + accounts + instructions
3. User signs challenge with passkey
4. Program verifies WebAuthn signature

**Key accounts:**
- `WalletAccount` — wallet state and nonce
- `CredentialLookup` — passkey credential mapping

### SDK Packages

```bash
npm i @thru/passkey @thru/programs
```

| Package | Use Case |
|---------|----------|
| `@thru/passkey` | Browser WebAuthn registration, signing, mobile helpers |
| `@thru/programs/passkey-manager` | Build validate/transfer/invoke instructions |

### Scoped Approvals (New)

Wallet signing sessions with scoped approvals — authorize specific actions per session instead of signing every transaction individually.

---

## Token Program

Fungible token management on Thru.

**Core accounts:**
- `TokenMintAccount` — mint metadata and supply
- `TokenAccount` — individual token balance

**Instructions:**

| Instruction | Description |
|-------------|-------------|
| `initialize_mint` | Create new token mint |
| `initialize_account` | Create token account |
| `transfer` | Transfer tokens |
| `mint_to` | Mint new tokens |
| `burn` | Burn tokens |
| `close_account` | Close token account |
| `freeze_account` | Freeze account |
| `thaw_account` | Unfreeze account |

---

## NFT Program

Non-fungible token management.

**Core accounts:**
- `NftMintAccount` — mint metadata and supply
- `NftAccount` — individual NFT data

**Instructions:**

| Instruction | Description |
|-------------|-------------|
| `initialize_mint` | Create NFT mint |
| `mint_to` | Mint new NFT |
| `transfer` | Transfer NFT ownership |
| `burn` | Burn NFT |
| `update_metadata` | Update NFT metadata |

---

## Core Specifications

### Transaction Format

```
┌─────────────────────────┐
│ Signatures              │
├─────────────────────────┤
│ Message                 │
│  ├─ Header              │
│  ├─ Account Addresses   │
│  ├─ Recent Block Hash   │
│  └─ Instructions        │
└─────────────────────────┘
```

### Block Structure

- **Slot** — time-based execution window
- **Block** —集合 of transactions in a slot
- **Block Hash** — hash of block content
- **State Root** — Merkle root of all account state

### State Tree

Merkle tree of all account states. Used for:
- State proofs (prove account existence/value)
- Compression (archive old state)
- Light client verification

---

## Building with AI Agents

### Install Thru Skills

```bash
npx skills add Unto-Labs/ai
```

This installs `thru-best-practices` — the recommended skill for agent-driven Thru development.

### Explorer MCP Setup

```bash
# Claude Code
claude mcp add --transport http thru-explorer https://scan.thru.org/api/mcp

# Codex
# Add to config:
# mcpServers:
#   thru-explorer:
#     url: https://scan.thru.org/api/mcp
```

### Agent Development Pattern

1. **Understand** — Read docs, explore chain state via MCP
2. **Plan** — Design program structure and instruction set
3. **Build** — Write C code, compile to RISC-V
4. **Validate** — Check ABI, test locally
5. **Deploy** — Upload to alphanet
6. **Debug** — Use explorer MCP to inspect transactions
7. **Iterate** — Upgrade program, re-validate

---

## Useful Commands Cheat Sheet

### Quick Reference

```bash
# Setup
thru --help
thru getversion
thru gethealth

# Keys
thru keys generate <name>
thru keys list

# Accounts
thru account create <name>
thru getbalance <address>
thru getaccountinfo <address>

# Programs
thru program create <seed> <binary_path>
thru program upgrade <seed> <binary_path>
thru program derive-address <program_addr> <seed>
thru program seed-to-hex <seed>

# ABI
thru abi analyze <abi.yaml>
thru abi codegen --files <abi.yaml> --language typescript --output ./gen/
thru abi account create <seed> <abi.yaml>
thru abi account get --include-data <address>

# Transactions
thru txn execute --fee 0 --readwrite-accounts <acct> <program> <hex_data>
thru txn make-state-proof creating <address>

# Tokens
thru token transfer <from> <to> <amount>
thru token balance <address>

# Network
thru network list
thru network use <name>

# Faucet
thru faucet request <name>

# Dev Tools
thru dev toolchain install
thru dev sdk install c

# Debug
thru debug re-execute <txn_signature>
```

### Program Interaction Flow

```bash
# 1. Derive account address
thru program derive-address <program> my_counter

# 2. Generate state proof
thru txn make-state-proof creating <derived_address>

# 3. Construct instruction data (hex)
# instruction_type(4) + account_index(2) + seed(32) + proof_size(4) + proof

# 4. Execute
thru txn execute \
  --fee 0 \
  --readwrite-accounts <derived_address> \
  <program_address> \
  <hex_instruction_data>
```

---

## Resources

| Resource | URL |
|----------|-----|
| Documentation | [docs.thru.org](https://docs.thru.org) |
| GitHub | [github.com/Unto-Labs/thru](https://github.com/Unto-Labs/thru) |
| Explorer | [scan.thru.org](https://scan.thru.org) |
| RPC Endpoint | `https://rpc.alphanet.thru.org` |
| gRPC Endpoint | `https://grpc.alphanet.thru.org` |
| AI Skills | [github.com/Unto-Labs/ai](https://github.com/Unto-Labs/ai) |
| LLM-Friendly Docs | [docs.thru.org/llms-full.txt](https://docs.thru.org/llms-full.txt) |

---

## License

See [LICENSE](LICENSE) for details.
