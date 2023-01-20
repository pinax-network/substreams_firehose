# Parser

[Pyfirehose Index](../../README.md#pyfirehose-index) /
[Pyfirehose](../index.md#pyfirehose) /
[Config](./index.md#config) /
Parser

> Auto-generated documentation for [pyfirehose.config.parser](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/parser.py) module.

- [Parser](#parser)
  - [Config](#config)
  - [StubConfig](#stubconfig)
  - [load_config](#load_config)
  - [load_stub_config](#load_stub_config)
  - [load_substreams_modules_from_package](#load_substreams_modules_from_package)

## Config

[Show source in parser.py:34](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/parser.py#L34)

Holds the main config.

#### Signature

```python
class Config:
    ...
```



## StubConfig

[Show source in parser.py:22](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/parser.py#L22)

Holds the stub config.

#### Signature

```python
class StubConfig:
    ...
```



## load_config

[Show source in parser.py:49](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/parser.py#L49)

Load the main config from the specified file. If a gRPC entry id is specified, it overwrites the default specified
in the config.

#### Arguments

- `file` - Filepath to the main config file.
- `grpc_entry_id` - Id of a gRPC entry present in the "grpc" array of the main config file.

#### Returns

A boolean indicating if the stub config file has also been loaded.

#### Raises

- `ArgumentTypeError` - If an entry is not recognized within the config file.
- `HjsonDecodeError` - If the hjson module fails to parse the config file.
- `ImportError` - If the stub config files fails to import the specified modules.
- `KeyError` - If a required key is missing from the config file.

#### Signature

```python
def load_config(file: str, grpc_entry_id: str | None = None) -> bool:
    ...
```



## load_stub_config

[Show source in parser.py:137](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/parser.py#L137)

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



## load_substreams_modules_from_package

[Show source in parser.py:121](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/parser.py#L121)

Parses substreams modules from an `.spkg` file.

#### Arguments

- `url` - Local path to `.spkg` file.

#### Returns

A dictionary of modules available in the package file.

#### Signature

```python
def load_substreams_modules_from_package(url: str) -> dict:
    ...
```


