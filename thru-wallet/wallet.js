/**
 * Thru Wallet Adapter
 * 
 * Simple wallet management for Thru Alphanet.
 */

const { createThruClient, TransactionBuilder, Pubkey, keys, deriveAddress } = require('@thru/sdk');

const RPC_URL = 'https://rpc.alphanet.thru.org';

class ThruWallet {
    constructor(options = {}) {
        this.rpcUrl = options.rpcUrl || RPC_URL;
        this.client = null;
        this.keypair = null;
        this.address = null;
    }

    async connect() {
        this.client = createThruClient({ rpcUrl: this.rpcUrl });
        return this;
    }

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

    async getBalance(address) {
        if (!this.client) await this.connect();
        const addr = address || this.address;
        // Use CLI as fallback
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
        // Use CLI for now (SDK transaction building is complex)
        const { execSync } = require('child_process');
        
        let cmd = `thru --json txn execute --fee ${options.fee || 0} --fee-payer ${this.address || 'frio'}`;
        
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
