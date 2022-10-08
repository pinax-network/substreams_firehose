import { decode, amount_to_float } from "../../src/utils.js";

export const filter_actions = [
    "eosio::delegatebw",
    "eosio::undelegatebw"
];

export const root = "cpu";
interface Init {[root]: typeof init }
export const init = {
    actions: {
        delegatebw: {
            stake_net_quantity: 0,
            stake_cpu_quantity: 0,
            actions: 0,
        },
        undelegatebw: {
            unstake_net_quantity: 0,
            unstake_cpu_quantity: 0,
            actions: 0,
        },
    }
}

export function handle_state( tableName: string, newData: string, data: any ) {
}

export function handle_action( account: string, action: string, jsonData: any, data: any ) {
    if ( action === "delegatebw" ) return handle_delegatebw( action, jsonData, data );
    if ( action === "undelegatebw" ) return handle_undelegatebw( action, jsonData, data );
}

function handle_delegatebw( key: "delegatebw", jsonData: any, data: Init ) {
    data[root].actions[key].stake_net_quantity += amount_to_float(jsonData.stake_net_quantity);
    data[root].actions[key].stake_cpu_quantity += amount_to_float(jsonData.stake_cpu_quantity);
    data[root].actions[key].actions += 1;
}

function handle_undelegatebw( key: "undelegatebw", jsonData: any, data: Init ) {
    data[root].actions[key].unstake_net_quantity += amount_to_float(jsonData.unstake_net_quantity);
    data[root].actions[key].unstake_cpu_quantity += amount_to_float(jsonData.unstake_cpu_quantity);
    data[root].actions[key].actions += 1;
}