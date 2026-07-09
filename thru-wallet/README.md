# Thru Wallet

Wallet adapter untuk interact sama Thru blockchain.

## Setup

```bash
cd ~/thru-wallet
npm install
```

## CLI Usage

```bash
# Generate new wallet
node cli.js generate

# Import from private key
node cli.js import <private_key_hex>

# Check balance
node cli.js balance [address]

# Get current height
node cli.js height

# Derive PDA
node cli.js pda <program_address> <seed>
```

## Library Usage

```javascript
const { ThruWallet } = require('./wallet');

const wallet = new ThruWallet();
await wallet.connect();

// Generate new keypair
const { address, publicKey, privateKey } = await wallet.generateKeypair();

// Import existing key
wallet.importFromHex(privateKeyHex);

// Get balance
const balance = await wallet.getBalance();

// Derive PDA
const pda = wallet.derivePda(programAddress, 'my-seed');
```

## Features

- ✅ Generate keypair
- ✅ Import from private key
- ✅ Check balance
- ✅ Derive PDA addresses
- ✅ Get block height
- ⏳ Sign transactions (CLI fallback)
- ⏳ Passkey support (via @thru/passkey)
