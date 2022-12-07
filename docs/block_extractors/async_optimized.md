# Async Optimized

[Eos-blockchain-data Index](../README.md#eos-blockchain-data-index) /
[Block Extractors](./index.md#block-extractors) /
Async Optimized

> Auto-generated documentation for [block_extractors.async_optimized](https://github.com/Krow10/eos-blockchain-data/blob/main/block_extractors/async_optimized.py) module.

- [Async Optimized](#async-optimized)
  - [asyncio_main](#asyncio_main)

## asyncio_main

[Show source in async_optimized.py:25](https://github.com/Krow10/eos-blockchain-data/blob/main/block_extractors/async_optimized.py#L25)

Extract blocks from a gRPC channel as raw blocks for later processing.

Using asynchronous directives, a *fixed* amount of workers will be initially spawned to
extract data from the gRPC channel until all blocks have been retrieved.
The returned list can then be parsed for extracting relevant data from the blocks.

#### Arguments

period_start:
    The first block number of the targeted period.
period_end:
    The last block number of the targeted period.
initial_tasks:
    The initial number of concurrent tasks to start for streaming blocks.
kwargs:
    Additional keyword arguments to pass to the gRPC request (must match .proto file definition).

#### Returns

A list of raw blocks (google.protobuf.any_pb2.Any objects) that can later be processed.

#### Signature

```python
async def asyncio_main(
    period_start: int, period_end: int, initial_tasks: int = 25, **kwargs
) -> list[Message]:
    ...
```


