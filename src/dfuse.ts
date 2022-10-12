import fetch from "node-fetch";
import ws from "ws";
import * as grpc from "@grpc/grpc-js"
import ProtoBuf from "protobufjs"
import * as protoLoader from "@grpc/proto-loader"
import path from "node:path"
import { fileURLToPath } from "node:url";
import { createDfuseClient, InMemoryApiTokenStore } from "@dfuse/client"
import { timeout } from "./utils.js"
import { Block } from "./firehose.js"
import { DFUSE_TOKEN, DFUSE_DFUSE_NETWORK, DFUSE_FIREHOSE_NETWORK, TIMEOUT_MS, SECURE, AUTHENTICATION } from './config.js';

// Global required by dfuse client
global.fetch = fetch as any;
global.WebSocket = ws as any;
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// protobufs
export const bstreamProto = loadProto("dfuse/bstream/v1/bstream.proto")
export const eosioProto = loadProto("dfuse/eosio/codec/v1/codec.proto")
export const bstreamService = loadGrpcPackageDefinition("dfuse/bstream/v1/bstream.proto").dfuse.bstream.v1

export const blockMsg = bstreamProto.root.lookupType("dfuse.bstream.v1.Block")
export const eosioBlockMsg = eosioProto.root.lookupType("dfuse.eosio.codec.v1.Block")
export const forkStepEnum = bstreamProto.root.lookupEnum("dfuse.bstream.v1.ForkStep")

export const forkStepIrreversible = forkStepEnum.values["STEP_IRREVERSIBLE"]

function loadGrpcPackageDefinition(pkg: any): any {
    const protoPath = path.resolve(__dirname, "proto", pkg)
    const proto = protoLoader.loadSync(protoPath, {
        keepCase: true,
        longs: String,
        enums: String,
        defaults: true,
        oneofs: true,
    })
    return grpc.loadPackageDefinition(proto)
}

function loadProto(pkg: any) {
    const protoPath = path.resolve(__dirname, "proto", pkg)
    return ProtoBuf.loadSync(protoPath)
}

interface StreamError {
    details: string;
    code: number;
    metadata: any;
}

// dfuse clients
export const firehose = createDfuseClient({
    apiKey: DFUSE_TOKEN,
    network: DFUSE_FIREHOSE_NETWORK,
    apiTokenStore: new InMemoryApiTokenStore(),
    secure: SECURE,
    authentication: AUTHENTICATION,
})

export const dfuse = createDfuseClient({
    apiKey: DFUSE_TOKEN,
    network: DFUSE_DFUSE_NETWORK,
    apiTokenStore: new InMemoryApiTokenStore()
})

// kill everything if true
let SIGINT = false;

export async function streamBlocks( start_block_num: number, stop_block_num: number, callback: (block: Block) => void, options: { exclude_filter_expr?: string; include_filter_expr?: string } = {} ) {
    if ( SIGINT ) return;

    console.log("streamBlocks", {start_block_num, stop_block_num, options});
    const client = new bstreamService.BlockStreamV2(
        `${DFUSE_FIREHOSE_NETWORK}:9000`,
        SECURE ? grpc.credentials.createSsl() : grpc.credentials.createInsecure(), {
        "grpc.max_receive_message_length": 1024 * 1024 * 100,
        "grpc.max_send_message_length": 1024 * 1024 * 100
        }
    )

    const metadata = new grpc.Metadata()
    const token = (await firehose.getTokenInfo()).token;
    metadata.set("authorization", token);

    // active variables
    let last_block_num: number;
    let blocks_to_processed = stop_block_num - start_block_num + 1;

    const stream = client.Blocks({
        start_block_num,
        stop_block_num,
        exclude_filter_expr: options.exclude_filter_expr,
        include_filter_expr: options.include_filter_expr,
        fork_steps: [forkStepIrreversible],
    }, metadata );

    async function exitStream(message: string, resolve: (value: any) => void) {
        console.log("exitStream", {message});
        cancelStream(message);
        if ( message == 'SIGINT') return SIGINT = true;
        console.log(`exiting in ${TIMEOUT_MS}ms...`);
        await timeout(TIMEOUT_MS);
        resolve(message);
    }

    async function endStream(message: string, resolve: (value: any) => void) {
        if ( last_block_num != stop_block_num ) message = "stream.on::incomplete";
        if ( blocks_to_processed != 0 ) message = "stream.on::incomplete";
        console.log("endStream", {message});
        if ( SIGINT ) return resolve("SIGINT");
        cancelStream(message);
        resolve(message);
    }

    function cancelStream(message: string) {
        console.log("cancelStream", {message});
        try { client.close(); } catch (e) { console.error({error: e}); }
        try { firehose.release(); } catch (e) { console.error({error: e}); }
        try { dfuse.release(); } catch (e) { console.error({error: e}); }
        try { if ( stream ) stream.cancel(); } catch (e) { console.error({error: e}); }
    }

    async function errorStream(message: string, error: StreamError, resolve: (value: any ) => void ) {
        const details = error?.details;
        if ( details == "Cancelled") return; // ignore, being handled by exitStream
        console.log("errorStream", {message, details, last_block_num});
        if ( details.match("unable to create preproc function") ) return exitStream(message, resolve );
        if ( message == 'SIGINT') return SIGINT = true;
        if ( error.details == "Cancelled on client") return SIGINT = true;
        cancelStream(message);
        console.log(`restart in ${TIMEOUT_MS}ms...`);
        await timeout(TIMEOUT_MS);
        if ( last_block_num ) streamBlocks(last_block_num, stop_block_num, callback, options );
    }

    function onData( data: any, resolve: (value: any) => void ) {
        const { block: rawBlock } = data;
        if (rawBlock.type_url !== "type.googleapis.com/dfuse.eosio.codec.v1.Block") {
            exitStream("[type_url] invalid", resolve);
        }
        const block: Block = eosioBlockMsg.decode(rawBlock.value) as any;
        if ( block.number ) {
            last_block_num = block.number;
            blocks_to_processed--;
        }
        callback(block);
    }

    return new Promise((resolve) => {
        process.on('SIGINT', () => exitStream("SIGINT", resolve));
        stream.on("data", (data: any) => onData( data, resolve));
        stream.on("end", () => endStream("stream.on::end", resolve));
        stream.on("error", (error: any) => errorStream("stream.on::error", error, resolve ));
    })
}

interface GetBlock {
    id: string;
    num: number;
    time: string;
}

export async function get_blocks(start_date: string, stop_date: string ): Promise<{start_block: GetBlock, stop_block: GetBlock}> {
    try {
        const start_block = (await dfuse.fetchBlockIdByTime(start_date, "eq")).block;
        const stop_block = (await dfuse.fetchBlockIdByTime(stop_date, "lt")).block;
        if ( !start_block.num ) throw new Error("stat_block.num invalid");
        if ( !stop_block.num ) throw new Error("stop_block.num invalid");
        dfuse.release();
        return { start_block, stop_block };
    } catch (e) {
        console.log('retrying... get_blocks', {e, start_date, stop_date});
        await timeout(1000);
        return get_blocks(start_date, stop_date);
    }
}