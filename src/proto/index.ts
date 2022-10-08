import path from "node:path";
import * as grpc from "@grpc/grpc-js"
import * as protoLoader from "@grpc/proto-loader"
import { fileURLToPath } from "node:url";

export function loadGrpcPackageDefinition(pkg: string) {
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