import fs from "node:fs";
import path from "node:path";
import { Block } from "../src/firehose.js"
import { fileURLToPath } from "node:url";
import { streamBlocks, get_blocks } from "../src/dfuse.js";

// filters
const filter_receiver = "eosio";
const filter_action = "voteproducer";
const include_filter_expr = `receiver == "${filter_receiver}" && action == "${filter_action}"`;
const exclude_filter_expr = ''

// data folder
const folder = "voteproducer";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const base_path = path.join(__dirname, '..', 'data', folder)
fs.mkdirSync(base_path, {recursive: true});

export default async function main( start_date: string, stop_date: string ) {
    // data containers
    let transfer_volume = 0;
    let transfers = 0;
    const accounts = new Set<string>();

    function callback(block: Block) {
        const block_num = block.number;
        const timestamp = Number(block.header.timestamp.seconds);

        fs.writeFileSync("block.json", JSON.stringify(block, null, 4))

        // log
        const date = new Date(timestamp * 1000).toISOString().slice(0, 19) + "Z";
        if ( block_num % 120 == 0 ) console.log(date, folder, JSON.stringify({block_num, transfers }))

        //filtering actual trades and duplicated mine actions in a single block
        for ( const { actionTraces } of block.filteredTransactionTraces ) {
            for ( const { action, filteringMatched } of actionTraces ) {
                // validate input
                if ( filteringMatched !== true ) continue; // exclude not matched & additional inline notifications
                if ( action.jsonData.length == 0 ) continue; // sometimes return empty traces
                const data = JSON.parse(action.jsonData);

                console.log(data);
                process.exit();
            }
        }
    }

    console.log('[transfers] starting...');
    const { start_block, stop_block } = await get_blocks( start_date, stop_date );
    const message = await streamBlocks(start_block.num, stop_block.num, callback, {include_filter_expr, exclude_filter_expr});

    // save data
    if ( message == "stream.on::end") {
        console.log("[transfers] saving...");
        fs.writeFileSync(`${base_path}/${folder}-${start_date}.json`, JSON.stringify({
            start_block,
            stop_block,
            transfers,
            transfer_volume: Number(transfer_volume.toFixed(4)),
            hourly_active_accounts: accounts.size,
        }, null, 4));
        console.log("[transfers] done!");
    } else {
        console.log("[transfers] exit without saving");
    }
}

main("2022-09-08T00:00:00", "2022-09-08T00:50:00")