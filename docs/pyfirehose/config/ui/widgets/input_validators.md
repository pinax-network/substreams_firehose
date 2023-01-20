# Input Validators

[Pyfirehose Index](../../../../README.md#pyfirehose-index) /
[Pyfirehose](../../../index.md#pyfirehose) /
[Config](../../index.md#config) /
[Ui](../index.md#ui) /
[Widgets](./index.md#widgets) /
Input Validators

> Auto-generated documentation for [pyfirehose.config.ui.widgets.input_validators](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py) module.

- [Input Validators](#input-validators)
  - [bool_validator](#bool_validator)
  - [enum_validator](#enum_validator)
  - [float_validator](#float_validator)
  - [integer_validator](#integer_validator)
  - [message_validator](#message_validator)
  - [string_validator](#string_validator)

## bool_validator

[Show source in input_validators.py:43](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L43)

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

[Show source in input_validators.py:56](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L56)

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

[Show source in input_validators.py:25](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L25)

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

[Show source in input_validators.py:7](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L7)

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

[Show source in input_validators.py:82](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L82)

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

[Show source in input_validators.py:69](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/input_validators.py#L69)

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


