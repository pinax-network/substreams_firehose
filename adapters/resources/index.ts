import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Block } from "../../src/firehose.js"
import { streamBlocks, get_blocks } from "../../src/dfuse.js";
import { isMain, data_filepath } from "../../src/utils.js";
import { CHAIN } from "../../src/config.js";
import * as rex from "./rex.js";
import * as ram from "./ram.js";
import * as cpu from "./cpu.js";

// filters
const filter_actions = [
    ...rex.filter_actions,
    ...ram.filter_actions,
    ...cpu.filter_actions,
];
const include_filter_expr = filter_actions.map((filter) => {
    const [account, action] = filter.split("::");
    return `(account == "${account}" && action == "${action}" && receiver == "${account}")`;
}).join(" || ");
const exclude_filter_expr = 'action == "*"'

// adapter folder
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const adapter = path.basename(__dirname);

const init = {
    rex: rex.init,
    ram: ram.init,
    cpu: cpu.init,
}

function handle_state( tableName: string, newData: string, data: typeof init ) {
    rex.handle_state( tableName, newData, data );
    ram.handle_state( tableName, newData, data );
    cpu.handle_state( tableName, newData, data );
}

function handle_action( account: string, action: string, jsonData: any, data: typeof init ) {
    rex.handle_action( account, action, jsonData, data );
    ram.handle_action( account, action, jsonData, data );
    cpu.handle_action( account, action, jsonData, data );
}

export default async function main( start_date: string, stop_date: string ) {
    const data = Object.assign({}, init);

    function callback(block: Block) {
        const block_num = block.number;
        const timestamp = Number(block.header.timestamp.seconds);

        // log
        const date = new Date(timestamp * 1000).toISOString().slice(0, 19) + "Z";
        if ( block_num % 120 == 0 ) console.log(date, adapter, JSON.stringify({block_num}))

        //filtering actual trades and duplicated mine actions in a single block
        for ( const { actionTraces, dbOps } of block.filteredTransactionTraces ) {
            for ( const { receiver, action, filteringMatched, transactionId } of actionTraces ) {
                // validate input
                if ( filteringMatched !== true ) continue; // exclude not matched & additional inline notifications
                if ( action.jsonData.length == 0 ) continue; // sometimes return empty traces
                const jsonData = JSON.parse(action.jsonData);
                handle_action( action.account, action.name, jsonData, data );
            }

            // TO-DO handle table deltas for prices
            for ( const { operation, code, scope, tableName, primaryKey, oldData, newData } of dbOps ) {
                handle_state( tableName, newData, data );
            }
        }
    }

    console.log(`[${adapter}] starting...`);
    const { start_block, stop_block } = await get_blocks( start_date, stop_date );
    const message = await streamBlocks(start_block.num, stop_block.num, callback, {include_filter_expr, exclude_filter_expr});

    // save data
    if ( message == "stream.on::end") {
        console.log(`[${adapter}] saving...`);
        const date = start_date.slice(0, 10);
        fs.writeFileSync(data_filepath(CHAIN, adapter, date), JSON.stringify({
            start_block,
            stop_block,
            data,
        }, null, 4));
        console.log(`[${adapter}] done!`);
    } else {
        console.log(`[${adapter}] exit without saving`);
    }
}

// for testing purposes
if ( isMain(import.meta.url) ) {
    // main("2022-10-02T00:00:00Z", "2022-10-02T00:10:00Z");
    // main("2021-12-24T15:53:44Z", "2021-12-24T15:53:45Z");
}