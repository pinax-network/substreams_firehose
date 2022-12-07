# Async Single Channel

[Eos-blockchain-data Index](../README.md#eos-blockchain-data-index) /
[Block Extractors](./index.md#block-extractors) /
Async Single Channel

> Auto-generated documentation for [block_extractors.async_single_channel](https://github.com/Krow10/eos-blockchain-data/blob/main/block_extractors/async_single_channel.py) module.

- [Async Single Channel](#async-single-channel)
  - [asyncio_main](#asyncio_main)

## asyncio_main

[Show source in async_single_channel.py:30](https://github.com/Krow10/eos-blockchain-data/blob/main/block_extractors/async_single_channel.py#L30)

Extract blocks from a gRPC channel as raw blocks for later processing.

Using asynchronous directives, a number of workers will be periodically spawned to
extract data from the gRPC channel until all blocks have been retrieved.
The returned list can then be parsed for extracting relevant data from the blocks.

#### Arguments

period_start:
    The first block number of the targeted period.
period_end:
    The last block number of the targeted period.
initial_tasks:
    The initial number of concurrent tasks to start for streaming blocks.
workload:
    The number of blocks to extract for each task.
auto_adjust_frequency:
    Enable the task spawner to auto adjust the task spawning frequency based on the tasks' average runtime.
spawn_frequency:
    The sleep time (in seconds) for the spawner to wait before trying to spawn a new task.
    Will be overridden if `auto_adjust_frequency` is enabled.
kwargs:
    Additional keyword arguments to pass to the gRPC request (must match .proto file definition).

#### Returns

A list of raw blocks (google.protobuf.any_pb2.Any objects) that can later be processed.

#### Signature

```python
async def asyncio_main(
    period_start: int,
    period_end: int,
    initial_tasks: int = 25,
    workload: int = 100,
    auto_adjust_frequency: bool = False,
    spawn_frequency: float = 0.1,
    **kwargs
) -> list[Message]:
    ...
```


