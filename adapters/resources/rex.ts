import { decode, amount_to_float } from "../../src/utils.js";

export const filter_actions = [
    "eosio::deposit",
    "eosio::unstaketorex",
    "eosio::withdraw",
    "eosio::buyrex",
    "eosio::sellrex",
    "eosio::rentcpu",
    "eosio::rentnet",
    "eosio::mvtosavings",
    "eosio::mvfrsavings",
    "eosio::powerup",
    "eosio.reserv::powupresult",
];

export const root = "rex";
interface Init {[root]: typeof init }
export const init = {
    state: {
        rexpool: {
            total_lent: 0,           // '3633530.8934 EOS',
            total_unlent: 0,         // '49661297.1217 EOS',
            total_rent: 0,           // '3522.8745 EOS',
            total_lendable: 0,       // '53294828.0151 EOS',
            total_rex: 0,            // '526109993069.8007 REX',
            namebid_proceeds: 0,     // '0.0000 EOS',
            loan_num: 0,             // 499797,
        },
        rexretpool: {
            last_dist_time: 0,             // '2022-10-02T00:00:00',
            pending_bucket_time: 0,        // '2022-10-02T12:00:00',
            oldest_bucket_time: 0,         // '2022-09-02T12:00:00',
            pending_bucket_proceeds: 0,    // 3174,
            current_rate_of_increase: 0,   // 23694,
            proceeds: 0,                   // 48953022
        },
    },
    actions: {
        deposit: {
            amount: 0,
            actions: 0,
        },
        withdraw: {
            amount: 0,
            actions: 0,
        },
        buyrex: {
            price: (null) as number | null,
            amount: 0,
            actions: 0,
        },
        sellrex: {
            price: (null) as number | null,
            rex: 0,
            actions: 0,
        },
        rentcpu: {
            price: (null) as number | null,
            loan_payment: 0,
            loan_fund: 0,
            actions: 0,
        },
        rentnet: {
            price: (null) as number | null,
            loan_payment: 0,
            loan_fund: 0,
            actions: 0,
        },
        unstaketorex: {
            from_net: 0,
            from_cpu: 0,
            actions: 0,
        },
        mvtosavings: {
            rex: 0,
            actions: 0,
        },
        mvfrsavings: {
            rex: 0,
            actions: 0,
        },
        powerup: {
            cpu_frac: 0,
            net_frac: 0,
            actions: 0,
        },
        powupresult: {
            fee: 0,
            powup_cpu: 0,
            powup_cpu_price: (null) as number | null,
            powup_net: 0,
            actions: 0,
        }
    }
}

export function handle_state( tableName: string, newData: string, data: any ) {
    if ( tableName == "rexpool" ) handle_rexpool( tableName, newData, data );
    if ( tableName == "rexretpool" ) handle_rexretpool( tableName, newData, data );
}

export function handle_action( account: string, action: string, jsonData: any, data: any ) {
    if ( action === "deposit" ) return handle_amount( action, jsonData, data );
    if ( action === "unstaketorex" ) return handle_unstaketorex( action, jsonData, data );
    if ( action === "withdraw" ) return handle_amount( action, jsonData, data );
    if ( action === "buyrex" ) return handle_amount( action, jsonData, data );
    if ( action === "sellrex" ) return handle_rex( action, jsonData, data );
    if ( action === "rentcpu" ) return handle_rent( action, jsonData, data );
    if ( action === "rentnet" ) return handle_rent( action, jsonData, data );
    if ( action === "mvtosavings" ) return handle_rex( action, jsonData, data );
    if ( action === "mvfrsavings" ) return handle_rex( action, jsonData, data );
    if ( action === "powerup" ) return handle_powerup( action, jsonData, data );
    if ( action === "powupresult" ) return handle_powupresult( action, jsonData, data );
}

function handle_rexretpool( key: "rexretpool", newData: string, data: Init ) {
    const decoded = decode<any>(newData, "rex_return_pool")
    if ( !decoded ) return;

    // fixed data
    data[root].state[key].last_dist_time = decoded.last_dist_time;
    data[root].state[key].pending_bucket_time = decoded.pending_bucket_time;
    data[root].state[key].oldest_bucket_time = decoded.oldest_bucket_time;
    data[root].state[key].pending_bucket_proceeds = decoded.pending_bucket_proceeds;
    data[root].state[key].current_rate_of_increase = decoded.current_rate_of_increase;
    data[root].state[key].proceeds = decoded.proceeds;
}

function handle_rexpool( key: "rexpool", newData: string, data: Init ) {
    const decoded = decode<any>(newData, "rex_pool");
    if ( !decoded ) return;

    const total_lendable = amount_to_float(decoded.total_lendable);
    const total_rex = amount_to_float(decoded.total_rex);
    const total_unlent = amount_to_float(decoded.total_unlent);
    const total_rent = amount_to_float(decoded.total_rent);

    // prices
    const rex_price = total_lendable / total_rex;
    const rent_rex = (1.0 * total_unlent) / (total_rent + 1.0);
    data[root].actions.buyrex.price = rex_price;
    data[root].actions.sellrex.price = rex_price;
    data[root].actions.rentcpu.price = rent_rex;
    data[root].actions.rentnet.price = rent_rex;

    // fixed data
    data[root].state[key].total_lent = amount_to_float(decoded.total_lent);
    data[root].state[key].total_unlent = amount_to_float(decoded.total_unlent);
    data[root].state[key].total_rent = amount_to_float(decoded.total_rent);
    data[root].state[key].total_lendable = amount_to_float(decoded.total_lendable);
    data[root].state[key].total_rex = amount_to_float(decoded.total_rex);
    data[root].state[key].namebid_proceeds = amount_to_float(decoded.namebid_proceeds);
    data[root].state[key].loan_num = decoded.loan_num;
}

function handle_amount( key: any, jsonData: any, data: Init ) {
    const { amount } = jsonData;
    (data[root] as any).actions[key].amount += parseFloat(amount.split(" ")[0]);
    (data[root] as any).actions[key].actions += 1;
}

function handle_rex( key: any, jsonData: any, data: Init ) {
    const { rex } = jsonData;
    (data[root] as any).actions[key].rex += amount_to_float(rex);
    (data[root] as any).actions[key].actions += 1;
}

function handle_rent( key: any, jsonData: any, data: Init ) {
    const { loan_payment, loan_fund } = jsonData;
    (data[root] as any).actions[key].loan_payment += amount_to_float(loan_payment);
    (data[root] as any).actions[key].loan_fund += amount_to_float(loan_fund);
    (data[root] as any).actions[key].actions += 1;
}

function handle_unstaketorex( key: "unstaketorex", jsonData: any, data: Init ) {
    const { from_net, from_cpu } = jsonData;
    data[root].actions[key].from_cpu += amount_to_float(from_cpu);
    data[root].actions[key].from_net += amount_to_float(from_net);
    data[root].actions[key].actions += 1;
}

function handle_powerup( key: "powerup", jsonData: any, data: Init ) {
    const { net_frac, cpu_frac } = jsonData;
    data[root].actions[key].net_frac += parseFloat(net_frac);
    data[root].actions[key].cpu_frac += parseFloat(cpu_frac);
    data[root].actions[key].actions += 1;
}

function handle_powupresult( key: "powupresult", jsonData: any, data: Init ) {
    // const { fee, powup_cpu, powup_net } = jsonData;
    const fee = amount_to_float(jsonData.fee);
    const powup_cpu = parseInt(jsonData.powup_cpu);
    const powup_net = parseInt(jsonData.powup_net);

    // calculate price if NET is 0
    if ( fee > 0.0010 && powup_cpu && powup_net === 0 ) {
        data[root].actions[key].powup_cpu_price = powup_cpu / (fee * 10000);
    }

    data[root].actions[key].fee += fee;
    data[root].actions[key].powup_cpu += powup_cpu;
    data[root].actions[key].powup_net += powup_net;
    data[root].actions[key].actions += 1;
}
