import { decode, amount_to_float } from "../../src/utils.js";

export const filter_actions = [
    "eosio::buyram",
    "eosio::buyrambytes"
];

export const root = "ram";
interface Init {[root]: typeof init }
export const init = {
    state: {
        rammarket: {
            supply: 0,      // 10000000000.0000 RAMCORE
            base: 0,        // { "balance": "276190691804 RAM", "weight": "0.50000000000000000" }
            quote: 0,       // { "balance": "5387216.6479 EOS", "weight": "0.50000000000000000" }
        },
        global: {
            max_ram_size: 0,                // 341362233344
            total_ram_bytes_reserved: 0,    // 65172694131
            total_ram_stake: 0,             // 43872157204
        }
    },
    actions: {
        buyram: {
            price_kb: (null) as number | null, // 49.977610030706245 (EOS per KB)
            quant: 0,
            actions: 0,
        },
        buyrambytes: {
            price_kb: (null) as number | null, // 0.02000896 (KB per EOS)
            bytes: 0,
            actions: 0,
        }
    }
}

export function handle_state( tableName: string, newData: string, data: any ) {
    if ( tableName == "global" ) handle_global( tableName, newData, data );
    if ( tableName == "rammarket" ) handle_rammarket( tableName, newData, data );
}

export function handle_action( account: string, action: string, jsonData: any, data: any ) {
    if ( action === "buyram" ) return handle_buyram( action, jsonData, data );
    if ( action === "buyrambytes" ) return handle_buyrambytes( action, jsonData, data );
}

function handle_global( key: "global", newData: string, data: Init ) {
    const decoded = decode<any>(newData, "eosio_global_state")
    if ( !decoded ) return;

    // fixed data
    data[root].state[key].max_ram_size = parseInt(decoded.max_ram_size);
    data[root].state[key].total_ram_bytes_reserved = parseInt(decoded.total_ram_bytes_reserved);
    data[root].state[key].total_ram_stake = parseInt(decoded.total_ram_stake);
}

function handle_rammarket( key: "rammarket", newData: string, data: Init ) {
    const decoded = decode<any>(newData, "exchange_state");
    if ( !decoded ) return;

    // prices
    const base = amount_to_float(decoded.base.balance.toJSON());
    const quote = amount_to_float(decoded.quote.balance.toJSON());
    const supply = amount_to_float(decoded.supply);
    const price_kb = Number((quote / base).toFixed(8)) * 1024;
    data[root].actions.buyram.price_kb = 1 / price_kb;
    data[root].actions.buyrambytes.price_kb = price_kb;

    // fixed data
    data[root].state[key].base = base;
    data[root].state[key].quote = quote;
    data[root].state[key].supply = supply;
}

function handle_buyram( key: "buyram", jsonData: any, data: Init ) {
    const { quant } = jsonData;
    data[root].actions[key].quant += amount_to_float(quant);
    data[root].actions[key].actions += 1;
}

function handle_buyrambytes( key: "buyrambytes", jsonData: any, data: Init ) {
    const { bytes } = jsonData;
    data[root].actions[key].bytes += bytes;
    data[root].actions[key].actions += 1;
}