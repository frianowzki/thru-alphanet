#!/usr/bin/env node
/**
 * Thru Wallet CLI
 * 
 * Usage:
 *   node cli.js generate              - Generate new wallet
 *   node cli.js import <private_key>  - Import from private key
 *   node cli.js balance [address]     - Check balance
 *   node cli.js send <to> <amount>    - Send tokens
 *   node cli.js pda <program> <seed>  - Derive PDA
 */

const { ThruWallet } = require('./wallet');

async function main() {
    const args = process.argv.slice(2);
    const command = args[0];

    const wallet = new ThruWallet();
    await wallet.connect();

    switch (command) {
        case 'generate': {
            const result = await wallet.generateKeypair();
            console.log(JSON.stringify({
                address: result.address,
                publicKey: result.publicKey,
                privateKey: result.privateKey,
            }, null, 2));
            console.log('\n⚠️ Save your private key securely!');
            break;
        }

        case 'import': {
            if (!args[1]) {
                console.error('Usage: node cli.js import <private_key_hex>');
                process.exit(1);
            }
            const result = wallet.importFromHex(args[1]);
            console.log(JSON.stringify(result, null, 2));
            break;
        }

        case 'balance': {
            const address = args[1]; // Optional, uses wallet address if not provided
            const result = await wallet.getBalance(address);
            console.log(`Address: ${result.address}`);
            console.log(`Balance: ${result.balance} tokens`);
            console.log(`Nonce: ${result.nonce}`);
            break;
        }

        case 'send': {
            if (!args[1] || !args[2]) {
                console.error('Usage: node cli.js send <to_address> <amount>');
                process.exit(1);
            }
            // For demo, we'd need to load the keypair
            console.log('Send functionality requires keypair loading.');
            console.log('Use: node cli.js import <private_key> first');
            break;
        }

        case 'pda': {
            if (!args[1] || !args[2]) {
                console.error('Usage: node cli.js pda <program_address> <seed>');
                process.exit(1);
            }
            const pda = wallet.derivePda(args[1], args[2]);
            console.log(`Program: ${args[1]}`);
            console.log(`Seed: ${args[2]}`);
            console.log(`PDA: ${pda}`);
            break;
        }

        case 'height': {
            const height = await wallet.getHeight();
            console.log(`Current height: ${height}`);
            break;
        }

        default:
            console.log('Thru Wallet CLI');
            console.log('');
            console.log('Commands:');
            console.log('  generate              Generate new wallet');
            console.log('  import <private_key>  Import from private key');
            console.log('  balance [address]     Check balance');
            console.log('  send <to> <amount>    Send tokens');
            console.log('  pda <program> <seed>  Derive PDA');
            console.log('  height                Get current height');
    }
}

main().catch(console.error);
