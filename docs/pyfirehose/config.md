# Config

[Eos-blockchain-data Index](../README.md#eos-blockchain-data-index) /
[Pyfirehose](./index.md#pyfirehose) /
Config

> Auto-generated documentation for [pyfirehose.config](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/config.py) module.

- [Config](#config)
  - [Config](#config-1)
  - [StubConfig](#stubconfig)
  - [import_all_from_module](#import_all_from_module)
  - [load_config](#load_config)
  - [load_stub_config](#load_stub_config)

## Config

[Show source in config.py:31](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/config.py#L31)

Holds the main config.

#### Signature

```python
class Config:
    ...
```



## StubConfig

[Show source in config.py:22](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/config.py#L22)

Holds the stub config.

#### Signature

```python
class StubConfig:
    ...
```



## import_all_from_module

[Show source in config.py:45](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/config.py#L45)

Dynamically import all python files located in the specified module's folder.

#### Arguments

- `module_name` - Name of the module to import files from.

#### Returns

The list of imported modules.

#### Signature

```python
def import_all_from_module(module_name: str) -> list[ModuleType]:
    ...
```



## load_config

[Show source in config.py:65](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/config.py#L65)

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

[Show source in config.py:130](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/config.py#L130)

Load the stub config from a file (str) or directly from a key-value dictionary.

#### Arguments

stub:
 The stub to load either as a filepath or a dictionary.

#### Raises

HjsonDecodeError:
 If the hjson module fails to parse the config file.
ImportError:
 If the specified stub or request object cannot be imported.
KeyError:
 If a required key is missing from the config file.

#### Signature

```python
def load_stub_config(stub: str | dict) -> None:
    ...
```


