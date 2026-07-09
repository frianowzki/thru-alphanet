/**
 * Thru Wallet Adapter v2
 * Multi-address wallet management for Thru Alphanet.
 */

const { createThruClient, TransactionBuilder, Pubkey, keys, deriveAddress } = require('@thru/sdk');
const fs = require('fs');
const path = require('path');

const RPC_URL = 'https://rpc.alphanet.thru.org';
const KEYSTORE_PATH = path.join(process.env.HOME, '.thru', 'keystore', 'wallet.json');

class ThruWallet {
    constructor(options = {}) {
        this.rpcUrl = options.rpcUrl || RPC_URL;
        this.client = null;
        this.keypair = null;
        this.address = null;
        this.addresses = this._loadKeystore();
    }

    // === Keystore ===

    _loadKeystore() {
        try {
            if (fs.existsSync(KEYSTORE_PATH)) {
                return JSON.parse(fs.readFileSync(KEYSTORE_PATH, 'utf-8'));
            }
        } catch (e) {}
        return { addresses: [], active: null };
    }

    _saveKeystore() {
        const dir = path.dirname(KEYSTORE_PATH);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(KEYSTORE_PATH, JSON.stringify(this.addresses, null, 2));
    }

    // === Address Management ===

    addAddress(name, address) {
        const existing = this.addresses.addresses.find(a => a.name === name);
        if (existing) throw new Error(`Address "${name}" already exists`);

        this.addresses.addresses.push({
            name,
            address,
            addedAt: new Date().toISOString(),
        });

        if (!this.addresses.active) this.addresses.active = name;
        this._saveKeystore();
        return { name, address, total: this.addresses.addresses.length };
    }

    removeAddress(name) {
        const idx = this.addresses.addresses.findIndex(a => a.name === name);
        if (idx === -1) throw new Error(`Address "${name}" not found`);

        this.addresses.addresses.splice(idx, 1);
        if (this.addresses.active === name) {
            this.addresses.active = this.addresses.addresses[0]?.name || null;
        }
        this._saveKeystore();
        return { removed: name, total: this.addresses.addresses.length, active: this.addresses.active };
    }

    switchAddress(name) {
        const found = this.addresses.addresses.find(a => a.name === name);
        if (!found) throw new Error(`Address "${name}" not found`);

        this.addresses.active = name;
        this._saveKeystore();
        return { active: name, address: found.address };
    }

    listAddresses() {
        return {
            addresses: this.addresses.addresses.map(a => ({
                ...a,
                isActive: a.name === this.addresses.active,
            })),
            active: this.addresses.active,
        };
    }

    getActiveAddress() {
        if (!this.addresses.active) return null;
        return this.addresses.addresses.find(a => a.name === this.addresses.active);
    }

    // === Connection ===

    async connect() {
        this.client = createThruClient({ rpcUrl: this.rpcUrl });
        return this;
    }

    // === Keypair ===

    async generateKeypair() {
        this.keypair = await keys.generateKeyPair();
        this.address = this.keypair.address;
        return {
            address: this.address,
            publicKey: Buffer.from(this.keypair.publicKey).toString('hex'),
            privateKey: Buffer.from(this.keypair.privateKey).toString('hex'),
        };
    }

    importFromHex(privateKeyHex) {
        const privKeyBytes = Buffer.from(privateKeyHex, 'hex');
        this.keypair = keys.fromPrivateKey(privKeyBytes);
        this.address = this.keypair.address;
        return {
            address: this.address,
            publicKey: Buffer.from(this.keypair.publicKey).toString('hex'),
        };
    }

    // === RPC ===

    async getBalance(address) {
        if (!this.client) await this.connect();
        const addr = address || this.address || this.getActiveAddress()?.address;
        const { execSync } = require('child_process');
        try {
            const output = execSync(`thru --json account info ${addr}`, { encoding: 'utf-8' });
            const data = JSON.parse(output);
            if (data.account_info) {
                return {
                    address: addr,
                    balance: data.account_info.balance || 0,
                    nonce: data.account_info.nonce || 0,
                };
            }
        } catch (e) {}
        return { address: addr, balance: 0, nonce: 0 };
    }

    async execute(options) {
        const { execSync } = require('child_process');
        const payer = options.feePayer || this.address || this.getActiveAddress()?.address || 'frio';
        
        let cmd = `thru --json txn execute --fee ${options.fee || 0} --fee-payer ${payer}`;
        
        if (options.readwriteAccounts) {
            for (const acct of options.readwriteAccounts) {
                cmd += ` --readwrite-accounts ${acct}`;
            }
        }
        
        cmd += ` ${options.program} ${options.instructionData}`;
        
        try {
            const output = execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
            return JSON.parse(output);
        } catch (e) {
            return { error: e.message };
        }
    }

    derivePda(programAddress, seed) {
        const { execSync } = require('child_process');
        try {
            const output = execSync(`thru --json program derive-address ${programAddress} ${seed}`, { encoding: 'utf-8' });
            const data = JSON.parse(output);
            return data.derive_address?.derived_address;
        } catch (e) {
            return null;
        }
    }

    async getHeight() {
        const { execSync } = require('child_process');
        try {
            const output = execSync('thru --json getheight', { encoding: 'utf-8' });
            const data = JSON.parse(output);
            return data.getheight?.finalized || data.height;
        } catch (e) {
            return null;
        }
    }
}

function hexToBytes(hex) {
    const bytes = new Uint8Array(hex.length / 2);
    for (let i = 0; i < hex.length; i += 2) {
        bytes[i / 2] = parseInt(hex.substr(i, 2), 16);
    }
    return bytes;
}

function bytesToHex(bytes) {
    return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('');
}

module.exports = { ThruWallet, hexToBytes, bytesToHex };
