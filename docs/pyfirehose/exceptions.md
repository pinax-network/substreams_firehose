# Exceptions

[Eos-blockchain-data Index](../README.md#eos-blockchain-data-index) /
[Pyfirehose](./index.md#pyfirehose) /
Exceptions

> Auto-generated documentation for [pyfirehose.exceptions](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/exceptions.py) module.

- [Exceptions](#exceptions)
  - [BlockStreamException](#blockstreamexception)

## BlockStreamException

[Show source in exceptions.py:7](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/exceptions.py#L7)

Thrown by a task when failing to process a block.

The information will be used to start another task for the remaining blocks to be processed.

#### Attributes

start:
 The block stream's starting block.
end:
 The block stream's ending block.
failed:
 The block that failed processing.

#### Signature

```python
class BlockStreamException(Exception):
    def __init__(self, start: int, end: int, failed: int) -> None:
        ...
```


