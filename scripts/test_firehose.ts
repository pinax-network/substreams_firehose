import ws from "ws";
import { createDfuseClient, InMemoryApiTokenStore } from "@dfuse/client"
import { DFUSE_TOKEN, DFUSE_FIREHOSE_NETWORK, SECURE, AUTHENTICATION } from '../src/config.js';

global.fetch = fetch as any;
global.WebSocket = ws as any;

// dfuse clients
console.log('connecting...');
const firehose = createDfuseClient({
    apiKey: DFUSE_TOKEN,
    network: DFUSE_FIREHOSE_NETWORK,
    apiTokenStore: new InMemoryApiTokenStore(),
    secure: SECURE,
    authentication: AUTHENTICATION,
})

const token = (await firehose.getTokenInfo()).token;
console.log({token});
firehose.release();
console.log('connected!');