#!/usr/bin/env node
/**
 * Thru Wallet CLI v2
 * Multi-address wallet management for Thru Alphanet.
 *
 * Usage:
 *   node cli.js generate                              - Generate new wallet
 *   node cli.js import <name> <private_key>           - Import from private key
 *   node cli.js add <name> <address>                  - Add address to wallet
 *   node cli.js list                                  - List all addresses
 *   node cli.js switch <name>                         - Switch active address
 *   node cli.js remove <name>                         - Remove address
 *   node cli.js balance [name_or_address]             - Check balance
 *   node cli.js send <to_name_or_address> <amount>    - Send tokens
 *   node cli.js pda <program> <seed>                  - Derive PDA
 *   node cli.js height                                - Get current height
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
            // Auto-add to keystore
            const name = `wallet-${Date.now().toString(36)}`;
            wallet.addAddress(name, result.address);
            console.log(JSON.stringify({
                name,
                address: result.address,
                publicKey: result.publicKey,
                privateKey: result.privateKey,
            }, null, 2));
            console.log(`\n✅ Added as "${name}" to wallet`);
            console.log('⚠️  Save your private key securely!');
            break;
        }

        case 'import': {
            if (!args[1] || !args[2]) {
                console.error('Usage: node cli.js import <name> <private_key_hex>');
                process.exit(1);
            }
            const name = args[1];
            const result = wallet.importFromHex(args[2]);
            wallet.addAddress(name, result.address);
            console.log(JSON.stringify({ name, ...result }, null, 2));
            console.log(`\n✅ Imported as "${name}"`);
            break;
        }

        case 'add': {
            if (!args[1] || !args[2]) {
                console.error('Usage: node cli.js add <name> <address>');
                process.exit(1);
            }
            const result = wallet.addAddress(args[1], args[2]);
            console.log(`✅ Added "${result.name}" (${result.address})`);
            console.log(`   Total: ${result.total} addresses`);
            break;
        }

        case 'list': {
            const result = wallet.listAddresses();
            if (result.addresses.length === 0) {
                console.log('No addresses. Add one with: node cli.js add <name> <address>');
                break;
            }
            console.log('Addresses:');
            for (const addr of result.addresses) {
                const marker = addr.isActive ? ' ← active' : '';
                console.log(`  ${addr.name}: ${addr.address}${marker}`);
            }
            console.log(`\nActive: ${result.active || 'none'}`);
            break;
        }

        case 'switch': {
            if (!args[1]) {
                console.error('Usage: node cli.js switch <name>');
                process.exit(1);
            }
            const result = wallet.switchAddress(args[1]);
            console.log(`✅ Switched to "${result.active}"`);
            console.log(`   Address: ${result.address}`);
            break;
        }

        case 'remove': {
            if (!args[1]) {
                console.error('Usage: node cli.js remove <name>');
                process.exit(1);
            }
            const result = wallet.removeAddress(args[1]);
            console.log(`✅ Removed "${result.removed}"`);
            console.log(`   Remaining: ${result.total} addresses`);
            if (result.active) console.log(`   Active: ${result.active}`);
            break;
        }

        case 'balance': {
            const target = args[1];
            let addr;

            if (target) {
                // Check if it's a name
                const list = wallet.listAddresses();
                const found = list.addresses.find(a => a.name === target);
                addr = found ? found.address : target;
            } else {
                const active = wallet.getActiveAddress();
                addr = active?.address;
            }

            if (!addr) {
                console.error('No address specified and no active address set.');
                console.error('Use: node cli.js balance <address> or set one with node cli.js add');
                process.exit(1);
            }

            const result = await wallet.getBalance(addr);
            console.log(`Address: ${result.address}`);
            console.log(`Balance: ${result.balance} tokens`);
            console.log(`Nonce: ${result.nonce}`);
            break;
        }

        case 'send': {
            if (!args[1] || !args[2]) {
                console.error('Usage: node cli.js send <to_name_or_address> <amount>');
                process.exit(1);
            }

            const active = wallet.getActiveAddress();
            if (!active) {
                console.error('No active address. Set one with: node cli.js switch <name>');
                process.exit(1);
            }

            // Resolve recipient
            const list = wallet.listAddresses();
            const recipient = list.addresses.find(a => a.name === args[1])?.address || args[1];

            console.log(`From: ${active.address} (${active.name})`);
            console.log(`To: ${recipient}`);
            console.log(`Amount: ${args[2]} tokens`);
            console.log('\n⚠️  Send requires on-chain signing. Use CLI directly:');
            console.log(`thru transfer ${active.address} ${recipient} ${args[2]}`);
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
            console.log('Thru Wallet CLI v2');
            console.log('');
            console.log('Commands:');
            console.log('  generate                              Generate new wallet');
            console.log('  import <name> <private_key>           Import from private key');
            console.log('  add <name> <address>                  Add address to wallet');
            console.log('  list                                  List all addresses');
            console.log('  switch <name>                         Switch active address');
            console.log('  remove <name>                         Remove address');
            console.log('  balance [name_or_address]             Check balance');
            console.log('  send <to_name_or_address> <amount>    Send tokens');
            console.log('  pda <program> <seed>                  Derive PDA');
            console.log('  height                                Get current height');
    }
}

main().catch(console.error);
