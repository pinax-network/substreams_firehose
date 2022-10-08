import test from "node:test"
import assert from 'assert/strict';
import { decode, parseTimestamp } from "./utils.js";

test('parseTimestamp', (t) => {
    assert.strictEqual(parseTimestamp("2022-10-02T13:00:00.500"), "2022-10-02T13:00:00");
});

test('decode - eosio::global4', (t) => {
    const decoded = decode<any>("Y9a+o6lEnj8wdQAAAAAAAECcAAAAAAAA", "eosio_global_state4");
    assert.strictEqual(decoded.continuous_rate, '0.0295588022415444');
    assert.strictEqual(decoded.inflation_pay_factor, 30000);
    assert.strictEqual(decoded.votepay_factor, 40000);
});

test('decode - eosio::rexretpool', (t) => {
    const decoded = decode<any>("AAA5vmLA4b5iwFSXYp2UAAAAAAAAVWYAAAAAAADl8aUDAAAAAA==", "rex_return_pool");
    assert.strictEqual(decoded.version, 0);
    assert.strictEqual(decoded.last_dist_time, '2022-07-01T00:00:00');
    assert.strictEqual(decoded.pending_bucket_time, '2022-07-01T12:00:00');
    assert.strictEqual(decoded.oldest_bucket_time, '2022-06-01T12:00:00');
    assert.strictEqual(decoded.pending_bucket_proceeds, 38045);
    assert.strictEqual(decoded.current_rate_of_increase, 26197);
    assert.strictEqual(decoded.proceeds, 61207013);
});
