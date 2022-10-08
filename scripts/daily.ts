import glob from 'glob';
import { loadJsonFileSync } from 'load-json-file';

const date = "2022-09-04"
const files = glob.sync(`data/tether/tether-${date}*.json`);

export interface Block {
    id: string;
    num: number;
    time: Date;
}

export interface Tether {
    start_block: Block;
    stop_block: Block;
    transfers: number;
    transfer_volume: number;
    cex_transfers: number;
    cex_transfer_volume: number;
    dex_transfers: number;
    dex_transfer_volume: number;
    hourly_active_accounts: number;
}

const daily = {
    date,
    cex_transfers: 0,
    cex_transfer_volume: 0,
    dex_transfers: 0,
    dex_transfer_volume: 0,
    daily_active_accounts: 0,
};

for ( const file of files ) {
    const data = loadJsonFileSync<Tether>(file);
    daily.cex_transfers += data.cex_transfers;
    daily.cex_transfer_volume += data.cex_transfer_volume;
    daily.dex_transfers += data.dex_transfers;
    daily.dex_transfer_volume += data.dex_transfer_volume;
    daily.daily_active_accounts += data.hourly_active_accounts;

    // normalize numbers
    daily.cex_transfer_volume = Number(daily.cex_transfer_volume.toFixed(0));
    daily.dex_transfer_volume = Number(daily.dex_transfer_volume.toFixed(0));
}

console.log(daily);