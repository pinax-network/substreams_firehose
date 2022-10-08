import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Block } from "../src/firehose.js"
import { streamBlocks, get_blocks } from "../src/dfuse.js";

// filters
const include_filter_expr = '';
const exclude_filter_expr = 'action == "*"'

// data folder
const folder = 'transactions'
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const base_path = path.join(__dirname, '..', 'data', folder )
fs.mkdirSync(base_path, {recursive: true});

export default async function main( start_date: string, stop_date: string ) {
    // data containers
    let actions = 0;
    let transactions = 0;
    let cpuUsageMicroSeconds = 0;
    let netUsage = 0;
    const accounts = new Set<string>();

    function callback(block: Block) {
        const block_num = block.number;
        const timestamp = Number(block.header.timestamp.seconds);

        // log
        actions += block.filteredExecutedTotalActionCount;
        transactions += block.filteredTransactionCount;
        const date = new Date(timestamp * 1000).toISOString().slice(0, 19) + "Z";
        if ( block_num % 120 == 0 ) console.log(date, folder, JSON.stringify({block_num, actions, transactions }))

        // filtering actual trades and duplicated mine actions in a single block
        for ( const trace of block.filteredTransactionTraces ) {

            // resource usage
            netUsage += Number(trace.netUsage);
            cpuUsageMicroSeconds += trace.receipt.cpuUsageMicroSeconds;

            // daily active users
            for ( const { action } of trace.actionTraces ) {
                for ( const authorization of action.authorization ) {
                    accounts.add(authorization.actor);
                }
            }
        }
    }

    console.log('[transactions] starting...');
    const { start_block, stop_block } = await get_blocks( start_date, stop_date );
    const message = await streamBlocks(start_block.num, stop_block.num, callback, {include_filter_expr, exclude_filter_expr});

    // save data
    if ( message == "stream.on::end") {
        console.log("[transactions] saving...");
        fs.writeFileSync(`${base_path}/${folder}-${start_date}.json`, JSON.stringify({
            start_block,
            stop_block,
            transactions,
            actions,
            cpu_usage: cpuUsageMicroSeconds,
            net_usage: netUsage,
            hourly_active_accounts: accounts.size,
            // accounts: Array.from(accounts).sort(),
        }, null, 4));

        console.log("[transactions] done!");
    } else {
        console.log("[transactions] exit without saving");
    }
}
