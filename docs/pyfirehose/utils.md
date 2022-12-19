# Utils

[Eos-blockchain-data Index](../README.md#eos-blockchain-data-index) /
[Pyfirehose](./index.md#pyfirehose) /
Utils

> Auto-generated documentation for [pyfirehose.utils](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/utils.py) module.

- [Utils](#utils)
  - [date_to_block_num](#date_to_block_num)
  - [get_auth_token](#get_auth_token)
  - [get_current_task_name](#get_current_task_name)

## date_to_block_num

[Show source in utils.py:18](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/utils.py#L18)

Queries the `graphql_endpoint` specified in the main config file for the block number associated with a given date time.

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



## get_auth_token

[Show source in utils.py:73](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/utils.py#L73)

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

[Show source in utils.py:109](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/utils.py#L109)

Helper function for generating a unique task id from an asyncio task.

#### Signature

```python
def get_current_task_name() -> str:
    ...
```


