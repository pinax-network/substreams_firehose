# Utils

[Pyfirehose Index](../README.md#pyfirehose-index) /
[Pyfirehose](./index.md#pyfirehose) /
Utils

> Auto-generated documentation for [pyfirehose.utils](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py) module.

- [Utils](#utils)
  - [date_to_block_num](#date_to_block_num)
  - [generate_proto_messages_classes](#generate_proto_messages_classes)
  - [get_auth_token](#get_auth_token)
  - [get_current_task_name](#get_current_task_name)
  - [import_all_from_module](#import_all_from_module)

## date_to_block_num

[Show source in utils.py:26](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py#L26)

Query the `graphql_endpoint` specified in the main config file for the block number associated with a given date time.

Cache the results for the duration specified in the main config file (`graphql_cache`, default is 30 days).

#### Arguments

- `date` - A date to retrieve the associated block number.
- `jwt` - A JWT token used for authenticating with the GraphQL API (will be fetched automatically if not specified).

#### Returns

The block number associated with the given date time.

#### Signature

```python
def date_to_block_num(date: datetime, jwt: Optional[str] = None) -> int:
    ...
```



## generate_proto_messages_classes

[Show source in utils.py:82](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py#L82)

Generate a mapping of services and messages full name to their class object and populates the default descriptor pool
with the loaded `.proto` definitions.

Should only be called once for different descriptor sets.

#### Arguments

- `path` - Path to a descriptor set file (generated from `protoc --descriptor_set_out`).

#### Returns

A dictionary with pairs of message full name and the Python class object associated with it.

#### Examples

```json
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

[Show source in utils.py:161](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py#L161)

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

[Show source in utils.py:197](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py#L197)

Helper function for generating a unique task id from an asyncio task.

#### Signature

```python
def get_current_task_name() -> str:
    ...
```



## import_all_from_module

[Show source in utils.py:206](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/utils.py#L206)

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


