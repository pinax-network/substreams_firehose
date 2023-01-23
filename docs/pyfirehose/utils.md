# Utils

[Pyfirehose Index](../README.md#pyfirehose-index) /
[Pyfirehose](./index.md#pyfirehose) /
Utils

> Auto-generated documentation for [pyfirehose.utils](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py) module.

- [Utils](#utils)
  - [date_to_block_num](#date_to_block_num)
  - [filter_keys](#filter_keys)
  - [generate_proto_messages_classes](#generate_proto_messages_classes)
  - [get_auth_token](#get_auth_token)
  - [get_current_task_name](#get_current_task_name)
  - [import_all_from_module](#import_all_from_module)

## date_to_block_num

[Show source in utils.py:25](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py#L25)

Query the `graphql_endpoint` specified in the main config file for the block number associated with a given date time.

Cache the results for the duration specified in the main config file (`graphql_cache`, default is 30 days).

#### Arguments

- `date` - A date to retrieve the associated block number.
- `jwt` - A JWT token used for authenticating with the GraphQL API (will be fetched automatically if not specified).

#### Returns

The block number associated with the given date time.

#### Signature

```python
def date_to_block_num(date: datetime, jwt: str | None = None) -> int:
    ...
```



## filter_keys

[Show source in utils.py:81](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py#L81)

Recursively filters the `input_` dictionary based on the keys present in `keys_filter`.

#### Arguments

- `input_` - The input nested dictionary to filter.
- `keys_filter` - The nested dictionary filter matching subset of keys present in the `input_`.

#### Returns

The filtered `input_` as a new dict.

#### Examples

#### Input

```json
{
    'a': 'value',
    'b': {
        'b1': 'important stuff',
        'b2': {
            'x': 'stop nesting stuff',
            'y': 'keep me !'
        }
    },
    'c': {
        'c1': [1, 2, 3],
        'c2': 'Hello'
    },
    'd': [
        {'d1': 1},
        {'d1': 2, 'd2': 3}
    ]
}
```

#### Filter

```json
{
    'a': True,
    'b': {
        'b1': True,
        'b2': {
            'y': True
        }
    },
    'c': True,
    'd': {
        'd1': True,
    }
}
```

#### Output

```json
{
    'a': 'value',
    'b': {
        'b1': 'important stuff',
        'b2': {
            'y': 'keep me !'
        }
    },
    'c': {
        'c1': [1, 2, 3],
        'c2': 'Hello'
    },
    'd': [
        {'d1': 1},
        {'d1': 2}
    ]
}
```

#### Signature

```python
def filter_keys(input_: dict, keys_filter: dict) -> dict:
    ...
```



## generate_proto_messages_classes

[Show source in utils.py:168](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py#L168)

Generate a mapping of services and messages full name to their class object and populates the default descriptor pool
with the loaded `.proto` definitions.

Should only be called once for different descriptor sets.

#### Arguments

- `path` - Path to a descriptor set file (generated from `protoc --descriptor_set_out`).

#### Returns

A dictionary with pairs of message full name and the Python class object associated with it.

#### Examples

```python
{
    'dfuse.bstream.v1.BlockStream': <class 'pyfirehose.proto.generated.dfuse.bstream.v1.bstream_pb2_grpc.BlockStreamStub'>,
    'dfuse.bstream.v1.BlockStreamV2': <class 'pyfirehose.proto.generated.dfuse.bstream.v1.bstream_pb2_grpc.BlockStreamV2Stub'>,
    'dfuse.bstream.v1.BlockRequest': <class 'BlockRequest'>,
    'dfuse.bstream.v1.IrreversibleBlocksRequestV2': <class 'IrreversibleBlocksRequestV2'>,
    'dfuse.bstream.v1.BlocksRequestV2': <class 'BlocksRequestV2'>,
    'dfuse.bstream.v1.BlockResponseV2': <class 'BlockResponseV2'>,
    ...
}
```

#### Signature

```python
def generate_proto_messages_classes(
    path: str = "pyfirehose/proto/generated/protos.desc",
):
    ...
```



## get_auth_token

[Show source in utils.py:247](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py#L247)

Fetch a JWT authorization token from the authentication endpoints defined in the main config file.

Cache the token for 24-hour use.

#### Arguments

- `use_cache` - A boolean enabling/disabling fetching the cache for the JWT token request.

#### Returns

The JWT token or an empty string if the request failed.

#### Signature

```python
def get_auth_token(use_cache: bool = True) -> str:
    ...
```



## get_current_task_name

[Show source in utils.py:283](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py#L283)

Helper function for generating a unique task id from an asyncio task.

#### Signature

```python
def get_current_task_name() -> str:
    ...
```



## import_all_from_module

[Show source in utils.py:292](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py#L292)

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


