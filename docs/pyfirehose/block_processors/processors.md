# Processors

[Eos-blockchain-data Index](../../README.md#eos-blockchain-data-index) /
[Pyfirehose](../index.md#pyfirehose) /
[Block Processors](./index.md#block-processors) /
Processors

> Auto-generated documentation for [pyfirehose.block_processors.processors](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/block_processors/processors.py) module.

- [Processors](#processors)
  - [default_block_processor](#default_block_processor)
  - [filtered_block_processor](#filtered_block_processor)

## default_block_processor

[Show source in processors.py:61](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/block_processors/processors.py#L61)

Yield all the block data as a JSON-formatted dictionary.

First unpacks the block and converts all its properties to JSON.

#### Arguments

- `raw_block` - Raw block received from the gRPC stream.

#### Yields

A dictionary containing all the block's properties as defined in the proto files.

#### Signature

```python
def default_block_processor(raw_block: Message) -> dict:
    ...
```



## filtered_block_processor

[Show source in processors.py:79](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/block_processors/processors.py#L79)

Yield a all transactions from a gRPC filtered block, returning a subset of relevant properties.

See the `README.md` file for more information on building filtered stream.

#### Arguments

- `raw_block` - Raw block received from the gRPC stream.

#### Yields

A dictionary containing the filtered block data.

#### Examples

```json
{
    "account": "eosio.bpay",
    "date": "2022-10-21 00:03:31",
    "timestamp": 1666310611,
    "amount": "344.5222",
    "token": "EOS",
    "from": "eosio.bpay",
    "to": "newdex.bp",
    "block_num": 274268407,
    "transaction_id": "353555074901da28cd6dd64b0b64e73f12fdc86a91c8ad5e25b68952979aeed0",
    "memo": "producer block pay",
    "contract": "eosio.token",
    "action": "transfer"
}
```

#### Signature

```python
def filtered_block_processor(raw_block: Message) -> dict:
    ...
```


