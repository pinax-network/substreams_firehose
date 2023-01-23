# Input Validators

[Pyfirehose Index](../../../../README.md#pyfirehose-index) /
[Pyfirehose](../../../index.md#pyfirehose) /
[Config](../../index.md#config) /
[Ui](../index.md#ui) /
[Widgets](./index.md#widgets) /
Input Validators

> Auto-generated documentation for [pyfirehose.config.ui.widgets.input_validators](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py) module.

- [Input Validators](#input-validators)
  - [bool_validator](#bool_validator)
  - [enum_validator](#enum_validator)
  - [float_validator](#float_validator)
  - [integer_validator](#integer_validator)
  - [message_validator](#message_validator)
  - [string_validator](#string_validator)

## bool_validator

[Show source in input_validators.py:45](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L45)

Checks that a string is a valid boolean representation.

#### Arguments

- `value` - the string to test.
- `kwargs` - additional keyword arguments (unused, allow generic use of validators).

#### Returns

A boolean indicating if the given string is a valid boolean representation.

#### Signature

```python
def bool_validator(value: str, **kwargs) -> bool:
    ...
```



## enum_validator

[Show source in input_validators.py:58](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L58)

Checks that a string is a valid enum value from a given sequence of enum values.

#### Arguments

- `value` - the string to test.
- `enum_values` - the valid string values for the enum.

#### Returns

A boolean indicating if the given string is a valid enum representation.

#### Signature

```python
def enum_validator(value: str, enum_values: Sequence[str]):
    ...
```



## float_validator

[Show source in input_validators.py:27](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L27)

Checks that a string is a valid floating point representation.

#### Arguments

- `value` - the string to test.
- `kwargs` - additional keyword arguments (unused, allow generic use of validators).

#### Returns

A boolean indicating if the given string is a valid floating point representation.

#### Signature

```python
def float_validator(value: str, **kwargs) -> bool:
    ...
```



## integer_validator

[Show source in input_validators.py:9](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L9)

Checks that a string is a valid integer representation.

#### Arguments

- `value` - the string to test.
- `kwargs` - additional keyword arguments (unused, allow generic use of validators).

#### Returns

A boolean indicating if the given string is a valid integer representation.

#### Signature

```python
def integer_validator(value: str, **kwargs) -> bool:
    ...
```



## message_validator

[Show source in input_validators.py:84](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L84)

Placeholder validator for messages.

#### Arguments

- `value` - a string (unused).
- `kwargs` - additional keyword arguments (unused, allow generic use of validators).

#### Returns

True

#### Signature

```python
def message_validator(value: str, **kwargs):
    ...
```



## string_validator

[Show source in input_validators.py:71](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L71)

Placeholder validator for strings.

#### Arguments

- `value` - a string (unused).
- `kwargs` - additional keyword arguments (unused, allow generic use of validators).

#### Returns

True

#### Signature

```python
def string_validator(value: str, **kwargs):
    ...
```


