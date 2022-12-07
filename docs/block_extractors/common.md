# Common

[Eos-blockchain-data Index](../README.md#eos-blockchain-data-index) /
[Block Extractors](./index.md#block-extractors) /
Common

> Auto-generated documentation for [block_extractors.common](https://github.com/Krow10/eos-blockchain-data/blob/main/block_extractors/common.py) module.

- [Common](#common)
  - [get_secure_channel](#get_secure_channel)
  - [process_blocks](#process_blocks)
  - [stream_blocks](#stream_blocks)

## get_secure_channel

[Show source in common.py:20](https://github.com/Krow10/eos-blockchain-data/blob/main/block_extractors/common.py#L20)

Instantiate a secure gRPC channel as an asynchronous context manager for use by block extractors.

#### Yields

A grpc.aio.Channel as an asynchronous context manager.

#### Signature

```python
@asynccontextmanager
async def get_secure_channel() -> Generator[grpc.aio.Channel, None, None]:
    ...
```



## process_blocks

[Show source in common.py:45](https://github.com/Krow10/eos-blockchain-data/blob/main/block_extractors/common.py#L45)

Parse data using the given block processor, feeding it previously extracted raw blocks from a gRPC stream.

#### Arguments

raw_blocks:
    A sequence of packed blocks (google.protobuf.any_pb2.Any objects) extracted from a gRPC stream.
block_processor:
    A generator function extracting relevant data from a block.

#### Returns

A list of parsed data in the format returned by the block processor.

#### Signature

```python
def process_blocks(
    raw_blocks: Sequence[Message], block_processor: Callable[[Message], dict]
) -> list[dict]:
    ...
```



## stream_blocks

[Show source in common.py:67](https://github.com/Krow10/eos-blockchain-data/blob/main/block_extractors/common.py#L67)

Return raw blocks (or parsed data) for the subset period between `start` and `end` using the provided filters.

#### Arguments

start:
    The stream's starting block.
end:
    The stream's ending block.
secure_channel:
    The gRPC secure channel (SSL/TLS) to extract block from.
block_processor:
    Optional block processor function for directly parsing raw blocks.
    The function will then return the parsed blocks instead.

Discouraged as it might cause congestion issues for the gRPC channel if the block processing takes too long.
Parsing the blocks *after* extraction allows for maximum throughput from the gRPC stream.

#### Returns

A list of raw blocks (google.protobuf.any_pb2.Any objects) or parsed data if a block processor is supplied.

#### Raises

BlockStreamException:
    If an rpc error is encountered. Contains the start, end, and failed block number.

#### Signature

```python
async def stream_blocks(
    start: int,
    end: int,
    secure_channel: grpc.aio.Channel,
    block_processor: Optional[Callable[[Message], dict]] = None,
    **kwargs
) -> list[Message | dict]:
    ...
```


