# Utils

[Pyfirehose Index](../../README.md#pyfirehose-index) /
[Pyfirehose](../index.md#pyfirehose) /
[Config](./index.md#config) /
Utils

> Auto-generated documentation for [pyfirehose.config.utils](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/utils.py) module.

- [Utils](#utils)
  - [Config](#config)
  - [StubConfig](#stubconfig)
  - [load_config](#load_config)
  - [load_stub_config](#load_stub_config)

## Config

[Show source in utils.py:30](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/utils.py#L30)

Holds the main config.

#### Signature

```python
class Config:
    ...
```



## StubConfig

[Show source in utils.py:21](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/utils.py#L21)

Holds the stub config.

#### Signature

```python
class StubConfig:
    ...
```



## load_config

[Show source in utils.py:44](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/utils.py#L44)

Load the main config from the specified file. If a gRPC entry id is specified, it overwrites the default specified
in the config.

#### Arguments

- `file` - Filepath to the main config file.
- `grpc_entry_id` - Id of a gRPC entry present in the "grpc" array of the main config file.

#### Returns

A boolean indicating if the stub config file has also been loaded.

#### Raises

- `ArgumentTypeError` - If the specified compression argument for a gRPC endpoint is not one of "gzip" or "deflate".
- `HjsonDecodeError` - If the hjson module fails to parse the config file.
- `ImportError` - If the stub config files fails to import the specified modules.
- `KeyError` - If a required key is missing from the config file.

#### Signature

```python
def load_config(file: str, grpc_entry_id: Optional[str] = None) -> bool:
    ...
```



## load_stub_config

[Show source in utils.py:109](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/utils.py#L109)

Load the stub config from a file (str) or directly from a key-value dictionary.

#### Arguments

- `stub` - The stub to load either as a filepath or a dictionary.

#### Raises

- `HjsonDecodeError` - If the hjson module fails to parse the config file.
- `ImportError` - If the specified stub or request object cannot be imported.
- `KeyError` - If a required key is missing from the config file.

#### Signature

```python
def load_stub_config(stub: str | dict) -> None:
    ...
```


