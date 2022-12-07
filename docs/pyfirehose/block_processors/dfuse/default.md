# Default

[Eos-blockchain-data Index](../../../README.md#eos-blockchain-data-index) /
[Pyfirehose](../../index.md#pyfirehose) /
[Block Processors](../index.md#block-processors) /
[Dfuse](./index.md#dfuse) /
Default

> Auto-generated documentation for [pyfirehose.block_processors.dfuse.default](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/block_processors/dfuse/default.py) module.

- [Default](#default)
  - [default_block_processor](#default_block_processor)

## default_block_processor

[Show source in default.py:15](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/block_processors/dfuse/default.py#L15)

Yield a processed transaction from a block returning relevant properties.

See `proto/codec.proto` file for a full list of available properties.

#### Arguments

raw_block:
 Raw block received from the gRPC stream.

#### Yields

A dictionary containing the extracted block data.

#### Examples

{
 - `"account"` - "eosio.bpay",
 - `"date"` - "2022-10-21 00:03:31",
 - `"timestamp"` - 1666310611,
 - `"amount"` - "344.5222",
 - `"token"` - "EOS",
 - `"from"` - "eosio.bpay",
 - `"to"` - "newdex.bp",
 - `"block_num"` - 274268407,
 - `"transaction_id"` - "353555074901da28cd6dd64b0b64e73f12fdc86a91c8ad5e25b68952979aeed0",
 - `"memo"` - "producer block pay",
 - `"contract"` - "eosio.token",
 - `"action"` - "transfer"
}

#### Signature

```python
def default_block_processor(raw_block: Message) -> dict:
    ...
```


