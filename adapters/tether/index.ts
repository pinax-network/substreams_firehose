import fs from "node:fs";
import path from "node:path";
import { Block } from "../../src/firehose.js"
import { fileURLToPath } from "node:url";
import { isMain, data_filepath } from "../../src/utils.js";
import { streamBlocks, get_blocks } from "../../src/dfuse.js";
import { CHAIN } from "../../src/config.js";

// filters
const filter_receiver = "tethertether";
const filter_action = "transfer";
const include_filter_expr = `receiver == "${filter_receiver}" && action == "${filter_action}"`;
const exclude_filter_expr = 'action == "*"'
const kucoin_accounts = new Set([
    "qlwzviixzm1h", // KuCoin
    "kucoinrise11", // KuCoin
])
const cex_accounts = new Set([
    ...kucoin_accounts,
    "gateiowallet", // Gate
    "bitfinexcw55", // Bitfinex
    "mxcexdeposit", // MXCEX
])
const dex_accounts = new Set([
    "swap.defi", // Defibox Swap
    "defisswapcnt", // DFS
    "swap.pcash", // PCash
    "bal.defi", // Defibox Balance
    "mxcexdeposit", // MXCEX
])

// adapter folder
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const adapter = path.basename(__dirname);

export default async function main( start_date: string, stop_date: string ) {
    // data containers
    let transfer_volume = 0;
    let transfers = 0;

    let kucoin_transfer_volume = 0;
    let kucoin_transfers = 0;
    let kucoin_withdraws = 0;

    let cex_transfer_volume = 0;
    let cex_transfers = 0;
    let cex_withdraws = 0;

    let dex_transfer_volume = 0;
    let dex_transfers = 0;
    const accounts = new Set<string>();

    function callback(block: Block) {
        const block_num = block.number;
        const timestamp = Number(block.header.timestamp.seconds);

        // log
        const date = new Date(timestamp * 1000).toISOString().slice(0, 19) + "Z";
        if ( block_num % 120 == 0 ) console.log(date, adapter, JSON.stringify({block_num}));

        //filtering actual trades and duplicated mine actions in a single block
        for ( const { actionTraces } of block.filteredTransactionTraces ) {
            for ( const { action, filteringMatched } of actionTraces ) {
                // validate input
                if ( filteringMatched !== true ) continue; // exclude not matched & additional inline notifications
                if ( action.jsonData.length == 0 ) continue; // sometimes return empty traces
                const data = JSON.parse(action.jsonData);

                if ( action.name == "transfer" ) {
                    const { from, to, quantity } = data;

                    if ( !quantity ) continue;
                    const amount = Number(quantity?.split(" ")[0] ?? 0);
                    accounts.add(from);
                    accounts.add(to);

                    // global volume
                    transfer_volume += amount;
                    transfers += 1;

                    // cex volume
                    if ( cex_accounts.has( from ) || cex_accounts.has( to ) ) {
                        cex_transfer_volume += amount;
                        cex_transfers += 1;

                        if ( cex_accounts.has( from ) ) cex_withdraws += 1;
                    }

                    // dex volume
                    if ( dex_accounts.has( from ) || dex_accounts.has( to ) ) {
                        dex_transfer_volume += amount;
                        dex_transfers += 1;
                    }

                    // kucoin volume
                    if ( kucoin_accounts.has( from ) || kucoin_accounts.has( to ) ) {
                        kucoin_transfer_volume += amount;
                        kucoin_transfers += 1;

                        if ( kucoin_accounts.has( from ) ) kucoin_withdraws += 1;
                    }
                }
            }
        }
    }

    console.log('[transfers] starting...');
    const { start_block, stop_block } = await get_blocks( start_date, stop_date );
    const message = await streamBlocks(start_block.num, stop_block.num, callback, {include_filter_expr, exclude_filter_expr});

    // save data
    if ( message == "stream.on::end") {
        console.log("[transfers] saving...");
        const date = start_date.slice(0, 10);
        fs.writeFileSync(data_filepath(CHAIN, adapter, date), JSON.stringify({
            start_block,
            stop_block,
            transfers,
            transfer_volume: Number(transfer_volume.toFixed(4)),
            cex_transfers,
            cex_transfer_volume: Number(cex_transfer_volume.toFixed(4)),
            dex_transfers,
            dex_transfer_volume: Number(dex_transfer_volume.toFixed(4)),
            kucoin_transfers,
            kucoin_transfer_volume: Number(kucoin_transfer_volume.toFixed(4)),
            daily_active_accounts: accounts.size,
        }, null, 4));
        console.log("[transfers] done!");
    } else {
        console.log("[transfers] exit without saving");
    }
}

// for testing purposes
if ( isMain(import.meta.url) ) {
    const date = process.argv[2] || "2022-10-01";
    main(`${date}T00:00:00Z`, `${date}T23:59:59.5Z`);
}