import path from "node:path";
import * as grpc from "@grpc/grpc-js"
import * as protoLoader from "@grpc/proto-loader"
import { fileURLToPath } from "node:url";
import { DFUSE_FIREHOSE_NETWORK, SECURE } from '../src/config.js';

function loadGrpcPackageDefinition(pkg: string) {
    const __dirname = path.dirname(fileURLToPath(import.meta.url));
    const protoPath = path.resolve(__dirname, "..", "src", "proto", pkg)
    const proto = protoLoader.loadSync(protoPath, {
        keepCase: true,
        longs: String,
        enums: String,
        defaults: true,
        oneofs: true,
    })
    return grpc.loadPackageDefinition(proto)
}

const bstreamService = loadGrpcPackageDefinition("dfuse/bstream/v1/bstream.proto").dfuse.bstream.v1

function grpcClient() {
    const endpoint = `${DFUSE_FIREHOSE_NETWORK}:9000`;
    const connection = SECURE ? grpc.credentials.createSsl() : grpc.credentials.createInsecure();
    const options = {
        "grpc.max_receive_message_length": 1024 * 1024 * 100,
        "grpc.max_send_message_length": 1024 * 1024 * 100
    }
    return new bstreamService.BlockStreamV2( endpoint, connection, options );
}

const client = grpcClient();

// console.log(client);