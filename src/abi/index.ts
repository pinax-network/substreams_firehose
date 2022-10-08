import path from "node:path"
import { fileURLToPath } from "node:url";
import { loadJsonFileSync } from 'load-json-file';
import { ABI } from "@greymass/eosio";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const filepath = path.join(__dirname, "eosio.abi.json");
const value: any = loadJsonFileSync(filepath);
const abi = ABI.from(value);

export default abi;