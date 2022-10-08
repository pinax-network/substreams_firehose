import { Serializer } from "@greymass/eosio";
import { argv } from "process"
import { fileURLToPath } from "url"
import fs from "node:fs";
import path from "node:path";
import abi from "./abi/index.js";

export function timeout(ms: number) {
  return new Promise((resolve) => {
    setTimeout(() => {
      return resolve(true);
    }, ms);
  })
}

export function amount_to_float( amount: string ) {
  return parseFloat(amount.split(" ")[0]);
}

export function data_filepath(chain: string, adapter: string, date: string) {
  const __dirname = path.dirname(fileURLToPath(import.meta.url));
  const folder = path.join(__dirname, "..", "data", chain, adapter );
  if ( !fs.existsSync(folder)) fs.mkdirSync(folder, {recursive: true});
  return path.join(folder, `${adapter}-${date}.json` );
}

export function parseTimestamp( timestamp: string ) {
  return timestamp.split(".")[0];
}

export function decode<T = unknown>( data: string, type: string ): T | null {
  const result: any = {};
  const hex = Buffer.from(data, 'base64').toString("hex");

  let decoded: any;
  try {
    decoded = Serializer.decode({abi, type, data: hex });
  } catch (e) {
    console.error("Serializer.decode::", e);
    return null;
  }

  for ( const struct of abi.structs ) {
    if ( struct.name == type ) {
      for ( const field of struct.fields ) {
        try {
          result[field.name] = decoded[field.name].toJSON();
        } catch (e) {
          result[field.name] = decoded[field.name];
        }
      }
      return result;
    }
  }
  throw new Error(`Unknown type: ${type}`);
}

export function isMain(moduleUrl: string) {
  const modulePath = fileURLToPath(moduleUrl)
  const [_binPath, mainScriptPath] = argv
  return modulePath === mainScriptPath
}