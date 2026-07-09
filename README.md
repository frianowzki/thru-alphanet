<p align="center">
  <img src="https://img.shields.io/badge/status-alphanet-yellow?style=for-the-badge&labelColor=1a1a2e" alt="Status">
  <img src="https://img.shields.io/badge/thru-v0.2.38-blue?style=for-the-badge&labelColor=1a1a2e" alt="Version">
  <img src="https://img.shields.io/badge/RISC--V-64--bit-orange?style=for-the-badge&labelColor=1a1a2e" alt="VM">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge&labelColor=1a1a2e" alt="License">
</p>

<h1 align="center">
  <br>
  🕊️ Thru Alphanet
  <br>
</h1>

<p align="center">
  <b>Complete Developer Guide</b><br>
  <sub>Build ultra-high performance programs on Thru — the RISC-V blockchain</sub>
</p>

<p align="center">
  <a href="https://docs.thru.org">Docs</a> •
  <a href="https://github.com/Unto-Labs/thru">GitHub</a> •
  <a href="https://scan.thru.org">Explorer</a> •
  <a href="https://docs.thru.org/llms-full.txt">LLM Docs</a>
</p>

<br>

---

## 📋 Table of Contents

<details>
<summary><b>🚀 Getting Started</b></summary>

- [What is Thru](#-what-is-thru)
- [Quick Start](#-quick-start)
- [DevKit Setup](#-devkit-setup)
- [Configuration](#-configuration)

</details>

<details>
<summary><b>🛠️ Development</b></summary>

- [Program Development (C SDK)](#-program-development-c-sdk)
- [ABI System](#-abi-system)
- [Core Concepts](#-core-concepts)

</details>

<details>
<summary><b>⚙️ Architecture</b></summary>

- [Virtual Machine (ThruVM)](#-virtual-machine-thruvm)
- [Runtime & Execution](#-runtime--execution)
- [Accounts & State](#-accounts--state)

</details>

<details>
<summary><b>🔌 Integration</b></summary>

- [SDKs & Packages](#-sdks--packages)
- [APIs (gRPC, REST, MCP)](#-apis)
- [Wallet & Passkey](#-wallet--passkey)

</details>

<details>
<summary><b>📦 On-Chain Programs</b></summary>

- [Token Program](#-token-program)
- [Token Program Flow (FRIO Example)](#-token-program-flow-frio-example)
- [NFT Program](#-nft-program)

</details>

<details>
<summary><b>🤖 AI & Automation</b></summary>

- [Building with AI Agents](#-building-with-ai-agents)
- [Useful Commands](#-useful-commands-cheat-sheet)
- [Deployed Programs](#-deployed-programs)

</details>

<br>

---

## 🌟 What is Thru

<p align="center">
  <img src="https://img.shields.io/badge/ULTRA--HIGH_PERFORMANCE-sub--ms_latency-critical?style=flat-square&labelColor=0d1117&color=critical" alt="Performance">
  <img src="https://img.shields.io/badge/RISC--V_VM-native_execution-success?style=flat-square&labelColor=0d1117" alt="VM">
  <img src="https://img.shields.io/badge/C_SDK-native_programs-informational?style=flat-square&labelColor=0d1117" alt="SDK">
</p>

<br>

**Thru** is a next-generation blockchain network built for developers who need enterprise-grade speed and reliability.

<table>
<tr>
<td width="50%">

### ✨ Key Features

- **⚡ Sub-millisecond latency** — industry-leading transaction speed
- **🔧 RISC-V VM** — native 64-bit execution environment
- **📦 C Programs** — write smart contracts in C
- **🗜️ State Compression** — efficient storage with Merkle proofs
- **🤖 AI-Ready** — MCP tools for coding agents
- **🌐 gRPC + REST** — high-performance APIs

</td>
<td width="50%">

### 📊 Why Thru?

| | Thru | Others |
|---|:---:|:---:|
| **VM** | RISC-V | EVM/WASM |
| **Language** | C | Solidity |
| **Latency** | `<1ms` | `1s+` |
| **State Model** | Accounts + Compress | Accounts |
| **AI Support** | Native MCP | Limited |

</td>
</tr>
</table>

<br>

---

## ⚡ Quick Start

<br>

<table>
<tr>
<td width="60%">

### 🚀 Get Running in 60 Seconds

```bash
# 1. Install CLI
npm i -g thru

# 2. Verify installation
thru --help

# 3. Check network
thru getversion

# 4. Generate keypair
thru keys generate default

# 5. Create account
thru account create default

# 6. Get testnet tokens
thru faucet withdraw default 10000
```

</td>
<td width="40%">

### 📦 Installation Options

| Method | Command |
|--------|---------|
| **npm** | `npm i -g thru` |
| **deb** | `apt install ./thru_*.deb` |
| **rpm** | `dnf install ./thru-*.rpm` |

<br>

> 💡 **npm** is recommended — no Rust toolchain needed

</td>
</tr>
</table>

<br>

---

## 🛠️ DevKit Setup

<br>

### Prerequisites

| Requirement | Version | Notes |
|------------|---------|-------|
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org) |
| **OS** | Linux x64 | Recommended for full toolchain |
| **macOS** | ARM64/x64 | CLI works, limited toolchain |
| **Windows** | x64 | CLI works via WSL |

<br>

### Full Setup

```bash
# Install CLI globally
npm i -g thru

# Install RISC-V cross-compilation toolchain
thru dev toolchain install

# Install C SDK
thru dev sdk install c

# Verify everything
thru --help
```

<br>

### 📁 SDK Locations

```
~/.thru/
├── cli/
│   └── config.yaml          # CLI configuration + keys
├── sdk/
│   ├── c/
│   │   └── thru-sdk/        # C SDK files
│   │       ├── include/      # Headers
│   │       ├── lib/          # Libraries
│   │       └── thru_c_program.mk  # Build rules
│   └── toolchain/           # RISC-V compiler
```

<br>

---

## 🔧 Configuration

<br>

### CLI Config (`~/.thru/cli/config.yaml`)

```yaml
# RPC endpoint (alphanet default)
rpc_base_url: https://rpc.alphanet.thru.org

# Keypairs (generated by `thru keys generate`)
keys:
  default:
    public: tayzC11YgWrPpXBon_hBxI_...
    private: <hex_encoded_private_key>  # ⚠️ NEVER SHARE
```

<br>

> ⚠️ **Security Warning**: Private keys are stored as plaintext hex. Never commit this file to version control.

<br>

---

## 🚀 Program Development (C SDK)

<br>

<table>
<tr>
<td width="50%">

### 📁 Project Structure

```
my-project/
├── GNUmakefile
└── examples/
    ├── Local.mk
    ├── my_program.h
    └── my_program.c
```

</td>
<td width="50%">

### 🔨 Build Commands

```bash
# Build program
make

# Verify output
ls build/thruvm/bin/

# Deploy to network
thru program create my_seed \
  ./build/thruvm/bin/my_program_c.bin

# Upgrade existing
thru program upgrade my_seed \
  ./build/thruvm/bin/my_program_c.bin
```

</td>
</tr>
</table>

<br>

### 📄 GNUmakefile

```makefile
BASEDIR:=$(CURDIR)/build
THRU_C_SDK_DIR:=$(HOME)/.thru/sdk/c/thru-sdk
include $(THRU_C_SDK_DIR)/thru_c_program.mk
```

### 📄 examples/Local.mk

```makefile
$(call make-bin,my_program_c,my_program,,-ltn_sdk)
```

<br>

### 📝 Program Header (.h)

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

<br>

### 📝 Program Implementation (.c)

```c
#include <thru-sdk/c/tn_sdk.h>
#include <thru-sdk/c/tn_sdk_syscall.h>
#include "my_program.h"

TSDK_ENTRYPOINT_FN void start(void) {
    tsdk_txn_t const *txn = tsdk_get_txn();
    uchar const *data = tsdk_txn_get_instr_data(txn);
    ulong data_sz = tsdk_txn_get_instr_data_sz(txn);

    /* Validate input */
    if (data_sz < sizeof(uint)) {
        tsdk_revert(MY_ERR_INVALID_DATA);
    }

    uint const *instr_type = (uint const *)data;

    switch (*instr_type) {
        case MY_INSTRUCTION_INIT: {
            ushort account_idx = *(ushort *)(data + sizeof(uint));

            /* Create account with state proof */
            ulong result = tsys_account_create(account_idx, seed, proof, proof_sz);
            if (result != TSDK_SUCCESS) tsdk_revert(MY_ERR_CREATE_FAILED);

            /* Initialize */
            tsys_set_account_data_writable(account_idx);
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

            /* Emit event */
            tsys_emit_event((uchar const *)&acct->value, sizeof(ulong));
            tsdk_return(TSDK_SUCCESS);
            break;
        }
        default:
            tsdk_revert(MY_ERR_INVALID_DATA);
    }
}
```

<br>

### 🔑 Key SDK Functions

| Function | Description |
|----------|-------------|
| `tsdk_get_txn()` | Get current transaction |
| `tsdk_txn_get_instr_data()` | Get instruction data bytes |
| `tsdk_get_account_data_ptr()` | Get pointer to account data |
| `tsdk_return(TSDK_SUCCESS)` | Exit program successfully |
| `tsdk_revert(error_code)` | Exit with error (revert) |
| `tsys_account_create()` | Create new on-chain account |
| `tsys_account_resize()` | Resize account data buffer |
| `tsys_set_account_data_writable()` | Mark account as writable |
| `tsys_account_compress()` | Compress account (save storage) |
| `tsys_account_decompress()` | Decompress account |
| `tsys_emit_event()` | Emit event to chain |

<br>

---

## 📋 ABI System

<br>

<details>
<summary><b>📖 What is ABI?</b></summary>

ABI (Application Binary Interface) defines the binary data layout for:
- **Instructions** — what operations programs accept
- **Account State** — how data is stored on-chain

ABIs on Thru are **handwritten YAML files** that must be validated before publishing.

</details>

<br>

### 📝 ABI YAML Structure

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
                variants:
                  - name: Init
                    fields:
                      - name: seed
                        field-type:
                          primitive: u8
                  - name: Update
                    fields:
                      - name: value
                        field-type:
                          primitive: u64
```

<br>

### 🔄 ABI Workflow

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Write  │ ──▶ │ Validate │ ──▶ │  Codegen │ ──▶ │ Publish  │
│  YAML   │     │  Analyze │     │  TS/C/Rs │     │  On-Chain│
└─────────┘     └──────────┘     └──────────┘     └──────────┘
```

```bash
# 1. Validate ABI
thru abi analyze ./program.abi.yaml

# 2. Generate client code
thru abi codegen \
  --files ./program.abi.yaml \
  --language typescript \
  --output ./generated/

# 3. Publish to chain
thru abi account create my_seed ./program.abi.yaml

# 4. Verify published ABI
thru abi account get --include-data <ABI_ADDRESS>
```

<br>

---

## 🧠 Core Concepts

<br>

### 🏦 Account Model

<table>
<tr>
<td width="50%">

**Every piece of state is an Account**

| Property | Description |
|----------|-------------|
| **Address** | Unique ID (starts with `ta`) |
| **Data** | Binary payload |
| **Owner** | Controlling program |
| **Flags** | Compressed, writable, etc. |

</td>
<td width="50%">

**Account Lifecycle**

```
    ┌─────────┐
    │ Create  │
    └────┬────┘
         ▼
    ┌─────────┐
    │ Active  │ ◄──────────────┐
    └────┬────┘                │
         │                     │
         ▼                     │
    ┌──────────┐          ┌────┴─────┐
    │ Compress │          │Decompress│
    └──────────┘          └──────────┘
         │
         ▼
    ┌─────────┐
    │ Archive │
    └─────────┘
```

</td>
</tr>
</table>

<br>

### 🔑 Program-Derived Addresses (PDAs)

Accounts can be **deterministically derived** from a program + seed:

```bash
# Derive address
thru program derive-address <program_address> <seed>

# Convert seed to hex
thru program seed-to-hex <seed>
```

> 💡 Same seed always produces the same address — no on-chain lookup needed

<br>

### 📜 State Proofs

Cryptographic proofs verify account existence in the Merkle tree:

```bash
# Generate proof for account creation
thru txn make-state-proof creating <account_address>

# Proof types
# ├── creating   — prove account doesn't exist yet
# ├── existing   — prove account exists (for decompress)
# └── updating   — prove account state (for re-compress)
```

<br>

### 📨 Transaction Structure

```
┌─────────────────────────────────────────┐
│  0: Fee Payer       (pays for execution)│
│  1: Program         (code to execute)   │
│  2+: Writable Accts (can modify)        │
│  N+: Read-only Accts (can only read)    │
└─────────────────────────────────────────┘
```

```bash
thru txn execute \
  --fee 0 \
  --readwrite-accounts <writable_account> \
  <program_address> \
  <hex_instruction_data>
```

<br>

### 💰 Compute Units (CUs)

Each transaction consumes compute units:

| Resource | CU Cost |
|----------|---------|
| Base transaction | 500 |
| Per instruction | Varies |
| Memory allocation | Per page |
| Account creation | Per account |

<br>

---

## ⚙️ Virtual Machine (ThruVM)

<br>

<table>
<tr>
<td width="50%">

### 🔧 RISC-V Extensions

| Extension | Purpose |
|-----------|---------|
| **RV64I** | Base integer (64-bit) |
| **M** | Multiply/divide |
| **C** | Compressed instructions (16-bit) |
| **B** | Bit manipulation |
| **Zknh** | SHA-256/512 acceleration |

</td>
<td width="50%">

### 📐 Key Constraints

| Constraint | Value |
|------------|-------|
| IALIGN | 16-bit |
| Page Size | 4KB |
| Max Stack | 16MB |
| Max Heap | 16MB |
| Threads | Single |
| Alignment | Strict |

</td>
</tr>
</table>

<br>

### 🧮 Memory Layout (48-bit Segmented)

```
Bits: 47-40  |  39-24   |  23-0
     seg_type| seg_idx  | offset
    (8 bits) |(16 bits) |(24 bits)
```

| Type | Name | Purpose |
|------|------|---------|
| `0x00` | Read-Only | TXN data, program code, block context |
| `0x02` | Account Meta | Account metadata |
| `0x03` | Account Data | Page-based data (COW) |
| `0x04` | Events | Event emission buffer |
| `0x05` | Stack | Grows ↓ (16MB) |
| `0x07` | Heap | Grows ↑ (16MB) |

<br>

### 📦 Executable Format

```
┌──────────────┐
│   Header     │  8 bytes (magic + version + size)
├──────────────┤
│   Bytecode   │  RISC-V instructions
├──────────────┤
│   Footer     │  4 bytes (checksum)
└──────────────┘
```

<br>

---

## 🔄 Runtime & Execution

<br>

### 📊 Execution Flow

```
┌─────────────┐
│  Deserialize│
│  Transaction│
└──────┬──────┘
       ▼
┌─────────────┐
│   Validate  │
│   Accounts  │
└──────┬──────┘
       ▼
┌─────────────┐
│  Setup VM   │
│  Memory     │
└──────┬──────┘
       ▼
┌─────────────┐
│   Execute   │
│  Bytecode   │
└──────┬──────┘
       ▼
┌─────────────┐
│   Apply/    │
│   Revert    │
└──────┬──────┘
       ▼
┌─────────────┐
│   Commit    │
│   State     │
└─────────────┘
```

<br>

### 📞 System Calls

| Code | Syscall | Description |
|------|---------|-------------|
| `0x01` | `account_create` | Create new account |
| `0x02` | `account_resize` | Resize account data |
| `0x03` | `account_delete` | Delete account |
| `0x04` | `account_compress` | Compress account |
| `0x05` | `account_decompress` | Decompress account |
| `0x06` | `emit_event` | Emit event |
| `0x07` | `exit` | Exit program |
| `0x08` | `invoke` | Call another program (CPI) |
| `0x09` | `log` | Log message |
| `0x0A` | `set_writable` | Mark account writable |

<br>

---

## 🏦 Accounts & State

<br>

### 🗜️ Account Compression

```c
// Compress account (archive to Merkle tree)
tsys_account_compress(account_idx, proof, proof_sz);

// Decompress account (restore from proof)
tsys_account_decompress(account_idx, proof, proof_sz);
```

| State | Storage | Access |
|-------|---------|--------|
| **Uncompressed** | Validator memory | Direct |
| **Compressed** | Off-chain (Merkle) | Via proof |

<br>

---

## 📦 SDKs & Packages

<br>

### 🟢 NPM Packages

<table>
<tr>
<td>

```bash
npm i @thru/sdk
```

**`@thru/sdk`** — TypeScript/JS client
- Blocks, accounts, transactions
- Events, proofs
- Typed domain models

</td>
<td>

```bash
npm i @thru/programs
```

**`@thru/programs`** — On-chain programs
- Token program bindings
- Instruction builders
- Address derivation

</td>
<td>

```bash
npm i @thru/passkey
```

**`@thru/passkey`** — Passkey/WebAuthn
- Registration & signing
- Mobile helpers
- Auth flows

</td>
</tr>
<tr>
<td>

```bash
npm i @thru/indexer
```

**`@thru/indexer`** — Indexer framework
- Drizzle-backed
- Stream definitions
- Background indexing

</td>
<td>

```bash
npm i @thru/replay
```

**`@thru/replay`** — Chain replay
- Historical backfill
- Live streaming
- No gaps/duplicates

</td>
<td>

```bash
# Rust crates
cargo add thru-base
cargo add thru-grpc-client
```

**Rust SDKs**
- `thru-base` — Core primitives
- `thru-grpc-client` — gRPC bindings

</td>
</tr>
</table>

<br>

---

## 🔌 APIs

<br>

### ⚡ gRPC API (Recommended)

High-performance Protocol Buffers API:

```text
Endpoint: https://grpc.alphanet.thru.org
```

| Service | Purpose |
|---------|---------|
| **CommandService** | Send transactions, batch operations |
| **QueryService** | Get blocks, accounts, transactions |
| **StreamingService** | Real-time streams |
| **DebugService** | Transaction debugging |

<br>

### 🌐 REST API

Browser-friendly JSON API:

```text
Endpoint: https://rpc.alphanet.thru.org
```

<br>

### 🤖 Explorer MCP (AI Agents)

Live chain context for coding agents:

```bash
# Claude Code
claude mcp add --transport http thru-explorer https://scan.thru.org/api/mcp

# Codex
# Add to config:
# mcpServers:
#   thru-explorer:
#     url: https://scan.thru.org/api/mcp
```

**Available Tools:**

| Tool | Description |
|------|-------------|
| `get_block` | Fetch block details |
| `get_transaction` | Fetch transaction details |
| `get_account` | Fetch account state |
| `list_recent_blocks` | Recent blocks |
| `list_recent_transactions` | Recent transactions |
| `search` | Search chain state |
| `get_program_abi` | Fetch program ABI |

<br>

---

## 🔐 Wallet & Passkey

<br>

### 🛡️ Passkey Manager Program

On-chain program for WebAuthn/passkey authorization:

```
┌─────────────────────────────────────────────┐
│              Passkey Flow                    │
├─────────────────────────────────────────────┤
│  1. Register passkey (WebAuthn credential)  │
│  2. Build challenge (nonce + accounts +     │
│     instructions)                           │
│  3. Sign with passkey (user device)         │
│  4. Verify on-chain (program)               │
└─────────────────────────────────────────────┘
```

| Account | Purpose |
|---------|---------|
| `WalletAccount` | Wallet state + nonce |
| `CredentialLookup` | Passkey credential mapping |

<br>

### 🔑 Scoped Approvals (New)

Wallet signing sessions with scoped approvals:
- Authorize **specific actions** per session
- Don't need to sign **every transaction**
- Better UX for repeated operations

```bash
npm i @thru/passkey @thru/programs
```

<br>

---

## 🪙 Token Program

<br>

### 📊 Token Accounts

| Account | Size | Purpose |
|---------|------|---------|
| `TokenMintAccount` | 115 bytes | Mint metadata + supply |
| `TokenAccount` | 73 bytes | Individual balance |

### 📝 Instructions

| Tag | Instruction | Description |
|-----|-------------|-------------|
| `0` | `initialize_mint` | Create new token mint |
| `1` | `initialize_account` | Create token account |
| `2` | `transfer` | Transfer tokens |
| `3` | `mint_to` | Mint new tokens |
| `4` | `burn` | Burn tokens |
| `5` | `close_account` | Close token account |
| `6` | `freeze_account` | Freeze account |
| `7` | `thaw_account` | Unfreeze account |

<br>

### ⚠️ Known Limitations

| Feature | Status | Notes |
|---------|--------|-------|
| `set_authority` | ❌ Not implemented | On-chain program doesn't support |
| `revoke_authority` | ❌ Not implemented | On-chain program doesn't support |
| Multi-sig | ❌ Not implemented | — |

> These features exist in SPL Token (Solana) but are **not yet implemented** in Thru's token program.

<br>

---

## 🪙 Token Program Flow (FRIO Example)

<br>

Complete walkthrough of creating, transferring, burning, and freezing a token.

### 1️⃣ Create Mint

```bash
# Generate seed
SEED=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Create mint (9 decimals, with freeze authority)
thru token initialize-mint \
  <CREATOR_ADDRESS> \
  FRIO \
  $SEED \
  --decimals 9 \
  --freeze-authority <FREEZE_AUTHORITY_ADDRESS> \
  --json
```

**Response:**
```json
{
  "token_initialize_mint": {
    "status": "success",
    "mint_account": "ta5YmaFApl_3d8d92gVRPVNCZldHxUtgXMTKPYCeTbc-4o",
    "ticker": "FRIO",
    "decimals": 9,
    "creator": "ta4xUEvMgPYGUiCrbX0az58_D4-j0lmwZEj_-Yb2-S2MrX",
    "mint_authority": "ta4xUEvMgPYGUiCrbX0az58_D4-j0lmwZEj_-Yb2-S2MrX",
    "freeze_authority": "ta4xUEvMgPYGUiCrbX0az58_D4-j0lmwZEj_-Yb2-S2MrX"
  }
}
```

<br>

### 2️⃣ Create Token Account

```bash
SEED=$(python3 -c "import secrets; print(secrets.token_hex(32))")

thru token initialize-account \
  <MINT_ADDRESS> \
  <OWNER_ADDRESS> \
  $SEED \
  --json
```

**Response:**
```json
{
  "token_initialize_account": {
    "status": "success",
    "token_account": "taQPEDM_d7C-cGQj8Yv6IRVUqmP22tfzUyGTsd_cnCCsMm",
    "mint": "ta5YmaFApl_3d8d92gVRPVNCZldHxUtgXMTKPYCeTbc-4o",
    "owner": "ta4xUEvMgPYGUiCrbX0az58_D4-j0lmwZEj_-Yb2-S2MrX"
  }
}
```

<br>

### 3️⃣ Mint Tokens

```bash
# Mint 1B tokens (1,000,000,000 * 10^9 = 1000000000000000000)
thru token mint-to \
  <MINT_ADDRESS> \
  <TOKEN_ACCOUNT_ADDRESS> \
  <AUTHORITY_ADDRESS> \
  1000000000000000000 \
  --json
```

<br>

### 4️⃣ Transfer Tokens

```bash
# First, create token account for recipient
SEED=$(python3 -c "import secrets; print(secrets.token_hex(32))")
thru token initialize-account <MINT> <RECIPIENT> $SEED --json

# Then transfer
thru token transfer \
  <SOURCE_TOKEN_ACCOUNT> \
  <DEST_TOKEN_ACCOUNT> \
  50000000000 \
  --json
```

<br>

### 5️⃣ Burn Tokens

```bash
thru token burn \
  <TOKEN_ACCOUNT> \
  <MINT_ADDRESS> \
  <AUTHORITY_ADDRESS> \
  100000000000 \
  --json
```

<br>

### 6️⃣ Freeze Account

```bash
thru token freeze-account \
  <TOKEN_ACCOUNT> \
  <MINT_ADDRESS> \
  <FREEZE_AUTHORITY_ADDRESS> \
  --json
```

**Verify frozen:**
```bash
thru token balance <TOKEN_ACCOUNT> --json
# "is_frozen": true
```

<br>

### 7️⃣ Thaw Account

```bash
thru token thaw-account \
  <TOKEN_ACCOUNT> \
  <MINT_ADDRESS> \
  <FREEZE_AUTHORITY_ADDRESS> \
  --json
```

<br>

### 📊 FRIO Token Summary

| Property | Value |
|----------|-------|
| **Mint** | `ta5YmaFApl_3d8d92gVRPVNCZldHxUtgXMTKPYCeTbc-4o` |
| **Ticker** | FRIO |
| **Decimals** | 9 |
| **Initial Supply** | 1,000,000,000 FRIO |
| **Mint Authority** | `ta4xUEvMgPYGUiCrbX0az58_D4-j0lmwZEj_-Yb2-S2MrX` |
| **Freeze Authority** | `ta4xUEvMgPYGUiCrbX0az58_D4-j0lmwZEj_-Yb2-S2MrX` |
| **Status** | Live on alphanet |

**Operations Performed:**
- ✅ Transfer 50 FRIO to faucet address
- ✅ Burn 150 FRIO
- ✅ Freeze faucet's token account
- ❌ Revoke authority — not supported on-chain

<br>

---

## 🎨 NFT Program

<br>

### 📊 NFT Accounts

| Account | Purpose |
|---------|---------|
| `NftMintAccount` | Mint metadata + supply |
| `NftAccount` | Individual NFT data |

### 📝 Instructions

| Instruction | Description |
|-------------|-------------|
| `initialize_mint` | Create NFT mint |
| `mint_to` | Mint new NFT |
| `transfer` | Transfer NFT ownership |
| `burn` | Burn NFT |
| `update_metadata` | Update NFT metadata |

<br>

---

## 🤖 Building with AI Agents

<br>

### 📦 Install Thru Skills

```bash
npx skills add Unto-Labs/ai
```

This installs `thru-best-practices` — recommended for agent-driven development.

<br>

### 🔄 Agent Development Pattern

```
┌─────────────┐
│  1. UNDERSTAND │  Read docs, explore chain via MCP
└──────┬──────┘
       ▼
┌─────────────┐
│  2. PLAN     │  Design program + instructions
└──────┬──────┘
       ▼
┌─────────────┐
│  3. BUILD    │  Write C code, compile to RISC-V
└──────┬──────┘
       ▼
┌─────────────┐
│  4. VALIDATE │  Check ABI, test locally
└──────┬──────┘
       ▼
┌─────────────┐
│  5. DEPLOY   │  Upload to alphanet
└──────┬──────┘
       ▼
┌─────────────┐
│  6. DEBUG    │  Inspect via Explorer MCP
└──────┬──────┘
       ▼
┌─────────────┐
│  7. ITERATE  │  Upgrade, re-validate
└─────────────┘
```

<br>

---

## 📚 Useful Commands

<br>

### 🔍 Quick Reference

<details>
<summary><b>🚀 Setup & Status</b></summary>

```bash
thru --help                  # Show all commands
thru getversion              # Node version
thru gethealth               # Health status
thru getstatus               # Operational status
thru getheight               # Block heights
```

</details>

<details>
<summary><b>🔑 Keys & Accounts</b></summary>

```bash
thru keys generate <name>    # Generate keypair
thru keys list               # List keypairs
thru account create <name>   # Create account
thru getbalance <address>    # Check balance
thru getaccountinfo <addr>   # Account details
thru transfer <to> <amount>  # Transfer tokens
```

</details>

<details>
<summary><b>📦 Programs</b></summary>

```bash
thru program create <seed> <binary>        # Deploy
thru program upgrade <seed> <binary>       # Upgrade
thru program set-pause <seed> true         # Pause
thru program finalize <seed>               # Make immutable
thru program destroy <seed>                # Destroy
thru program derive-address <prog> <seed>  # Derive PDA
thru program seed-to-hex <seed>            # Seed to hex
```

</details>

<details>
<summary><b>📋 ABI</b></summary>

```bash
thru abi analyze <abi.yaml>               # Validate
thru abi codegen --files <abi.yaml> \     # Generate code
  --language typescript \
  --output ./gen/
thru abi account create <seed> <abi.yaml>  # Publish
thru abi account get --include-data <addr> # Read
```

</details>

<details>
<summary><b>📨 Transactions</b></summary>

```bash
thru txn execute \                         # Execute
  --fee 0 \
  --readwrite-accounts <acct> \
  <program> \
  <hex_data>

thru txn make-state-proof creating <addr>  # Generate proof
```

</details>

<details>
<summary><b>🪙 Tokens</b></summary>

```bash
# Initialize mint
thru token initialize-mint <creator> <ticker> <seed> --decimals 9

# Initialize token account
thru token initialize-account <mint> <owner> <seed>

# Mint tokens
thru token mint-to <mint> <to> <authority> <amount>

# Transfer tokens
thru token transfer <from> <to> <amount>

# Burn tokens
thru token burn <account> <mint> <authority> <amount>

# Freeze account
thru token freeze-account <account> <mint> <authority>

# Thaw account
thru token thaw-account <account> <mint> <authority>

# Check balance
thru token balance <account>

# Close account
thru token close-account <account> <destination> <authority>
```

</details>

<details>
<summary><b>🛠️ Dev Tools</b></summary>

```bash
thru dev toolchain install  # Install RISC-V toolchain
thru dev sdk install c      # Install C SDK
thru network list           # List networks
thru network use <name>     # Switch network
thru faucet request <name>  # Get testnet tokens
```

</details>

<br>

---

## 🔗 Resources

<br>

<table>
<tr>
<td width="50%">

### 📖 Official

| Resource | Link |
|----------|------|
| Documentation | [docs.thru.org](https://docs.thru.org) |
| GitHub | [Unto-Labs/thru](https://github.com/Unto-Labs/thru) |
| Explorer | [scan.thru.org](https://scan.thru.org) |
| AI Skills | [Unto-Labs/ai](https://github.com/Unto-Labs/ai) |
| LLM Docs | [llms-full.txt](https://docs.thru.org/llms-full.txt) |

</td>
<td width="50%">

### 🔌 Endpoints

| Service | URL |
|---------|-----|
| RPC | `https://rpc.alphanet.thru.org` |
| gRPC | `https://grpc.alphanet.thru.org` |
| Explorer MCP | `https://scan.thru.org/api/mcp` |

</td>
</tr>
</table>

<br>

---

## 🚀 Deployed Programs

<table>
<tr>
<td width="50%">

### 🔄 Counter Program v2

| Property | Value |
|----------|-------|
| **Address** | `taLBRGzlvDoOBRPZlwQeMMizFrjWdYNw3Dnauw37N62dbm` |
| **Meta** | `ta2hkBlLSQMnOmx03aLuT4Qu-u0MnO95bnHrmHU50fMKkP` |
| **Deployer** | `ta4xUEvMgPYGUiCrbX0az58_D4-j0lmwZEj_-Yb2-S2MrX` |
| **Size** | 1162 bytes |

</td>
<td width="50%">

### 📋 Operations

| Instruction | Type | Description |
|-------------|------|-------------|
| Create | `0` | Init counter to 0 |
| Increment | `1` | Counter += 1 |
| Decrement | `2` | Counter -= 1 (underflow protected) |
| Reset | `3` | Counter = 0 |

**Quick Test:**
```bash
# Increment
thru txn execute --fee 0 \
  --readwrite-accounts <counter> \
  taLBRGzlvDoOBRPZlwQeMMizFrjWdYNw3Dnauw37N62dbm \
  010000000200

# Decrement
thru txn execute --fee 0 \
  --readwrite-accounts <counter> \
  taLBRGzlvDoOBRPZlwQeMMizFrjWdYNw3Dnauw37N62dbm \
  020000000200

# Reset
thru txn execute --fee 0 \
  --readwrite-accounts <counter> \
  taLBRGzlvDoOBRPZlwQeMMizFrjWdYNw3Dnauw37N62dbm \
  030000000200
```

</td>
</tr>
</table>

> 📁 Source code: [`examples/counter/`](examples/counter/)

<br>

### 🪙 FRIO Token

| Property | Value |
|----------|-------|
| **Mint** | `ta5YmaFApl_3d8d92gVRPVNCZldHxUtgXMTKPYCeTbc-4o` |
| **Ticker** | FRIO |
| **Decimals** | 9 |
| **Supply** | 1,000,000,000 FRIO |
| **Creator** | `ta4xUEvMgPYGUiCrbX0az58_D4-j0lmwZEj_-Yb2-S2MrX` |

<br>

---

<p align="center">
  <b>Built with ⚡ for the Thru Alphanet</b><br>
  <sub>Last updated: July 2026</sub>
</p>
