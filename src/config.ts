import 'dotenv/config'

// required
export const DFUSE_TOKEN = process.env.DFUSE_TOKEN;

// optional
export const CHAIN = process.env.CHAIN || "eos";
export const DFUSE_FIREHOSE_NETWORK = process.env.DFUSE_FIREHOSE_NETWORK || "eos.firehose.eosnation.io";
export const DFUSE_DFUSE_NETWORK = process.env.DFUSE_DFUSE_NETWORK || "eos.dfuse.eosnation.io";
export const TIMEOUT_MS = Number(process.env.TIMEOUT_MS ?? 3000);
export const CONCURRENCY = Number(process.env.CONCURRENCY ?? 3);
export const MAX_TASKS = Number(process.env.MAX_TASKS ?? 3);
export const ADAPTERS = new Set(process.env.ADAPTERS?.split(",") ?? ["resources"]);
if (!DFUSE_TOKEN) throw new Error("[DFUSE_TOKEN] is required");
if (!DFUSE_FIREHOSE_NETWORK) throw new Error("[DFUSE_FIREHOSE_NETWORK] is required");
if (!DFUSE_DFUSE_NETWORK) throw new Error("[DFUSE_DFUSE_NETWORK] is required");
export const SECURE = JSON.parse(process.env.SECURE ?? "true");
export const AUTHENTICATION = JSON.parse(process.env.AUTHENTICATION ?? "true");
export const REVERSE = JSON.parse(process.env.REVERSE ?? "true");