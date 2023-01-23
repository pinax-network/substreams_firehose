# Inputs

[Pyfirehose Index](../../../../README.md#pyfirehose-index) /
[Pyfirehose](../../../index.md#pyfirehose) /
[Config](../../index.md#config) /
[Ui](../index.md#ui) /
[Widgets](./index.md#widgets) /
Inputs

> Auto-generated documentation for [pyfirehose.config.ui.widgets.inputs](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py) module.

- [Inputs](#inputs)
  - [InputBool](#inputbool)
    - [InputBool().when_set](#inputbool()when_set)
  - [InputEnum](#inputenum)
  - [InputFloat](#inputfloat)
    - [InputFloat().set](#inputfloat()set)
  - [InputInteger](#inputinteger)
    - [InputInteger().set](#inputinteger()set)
  - [InputMessage](#inputmessage)
  - [InputRepeated](#inputrepeated)
    - [InputRepeated().set](#inputrepeated()set)
  - [InputString](#inputstring)
  - [InputValidator](#inputvalidator)
    - [InputValidator().set_from_widget_value](#inputvalidator()set_from_widget_value)
  - [InputsListDisplay](#inputslistdisplay)
  - [on_ok_input_validation_hook](#on_ok_input_validation_hook)

## InputBool

[Show source in inputs.py:99](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L99)

Custom option boolean input to convert string values to bool.

#### Signature

```python
class InputBool(OptionBoolean):
    ...
```

### InputBool().when_set

[Show source in inputs.py:103](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L103)

#### Signature

```python
def when_set(self):
    ...
```



## InputEnum

[Show source in inputs.py:107](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L107)

Custom option single choice input to allow selecting enum values (or none).

#### Signature

```python
class InputEnum(OptionSingleChoice):
    ...
```



## InputFloat

[Show source in inputs.py:82](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L82)

Custom option input to only allow floating point input.

#### Signature

```python
class InputFloat(InputValidator, OptionFreeText):
    ...
```

#### See also

- [InputValidator](#inputvalidator)

### InputFloat().set

[Show source in inputs.py:86](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L86)

#### Signature

```python
def set(self, value):
    ...
```



## InputInteger

[Show source in inputs.py:66](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L66)

Custom option input to only allow integer input.

#### Signature

```python
class InputInteger(InputValidator, OptionFreeText):
    ...
```

#### See also

- [InputValidator](#inputvalidator)

### InputInteger().set

[Show source in inputs.py:70](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L70)

#### Signature

```python
def set(self, value):
    ...
```



## InputMessage

[Show source in inputs.py:121](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L121)

Custom option input for complex `Message` object input.

Note that this class is empty as everything is handled by the parent `OptionFreeText`.
It exists to allow generic input creation (see `StubConfigInputsForm.create` method).

#### Signature

```python
class InputMessage(OptionFreeText):
    ...
```



## InputRepeated

[Show source in inputs.py:129](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L129)

Custom option input for repeated input fields with type validation.

#### Signature

```python
class InputRepeated(InputValidator, OptionMultiFreeList):
    def __init__(
        self, value_type: str, choices: Sequence[str] | None = None, *args, **kwargs
    ):
        ...
```

#### See also

- [InputValidator](#inputvalidator)

### InputRepeated().set

[Show source in inputs.py:142](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L142)

#### Signature

```python
def set(self, values):
    ...
```



## InputString

[Show source in inputs.py:113](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L113)

Custom option input for string input.

Note that this class is empty as everything is handled by the parent `OptionFreeText`.
It exists to allow generic input creation (see `StubConfigInputsForm.create` method).

#### Signature

```python
class InputString(OptionFreeText):
    ...
```



## InputValidator

[Show source in inputs.py:29](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L29)

Generic class for validating an option input with the return value of the `set` method.

Overload the `set(self, value)` method and return `True` to keep editing, `False` to quit.

#### Signature

```python
class InputValidator(Option):
    def __init__(self, multiline=False, *args, **kwargs):
        ...
```

### InputValidator().set_from_widget_value

[Show source in inputs.py:40](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L40)

Method override allowing to quit or continue the option editing depending on the return value.

See [on_ok_input_validation_hook](#on_ok_input_validation_hook).

#### Signature

```python
def set_from_widget_value(self, vl):
    ...
```



## InputsListDisplay

[Show source in inputs.py:18](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L18)

Custom option list display for increased option title width.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/options.html#options-and-option-lists)
for reference.

#### Signature

```python
class InputsListDisplay(OptionListDisplay):
    def __init__(self, *args, **kwargs):
        ...
```



## on_ok_input_validation_hook

[Show source in inputs.py:57](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L57)

Hook to replace the `on_ok` event handler for validating an option input.

It returns the value of the `Option.set` function to continue or stop the editing.
Used to prevent entering invalid input for options.

#### Signature

```python
def on_ok_input_validation_hook(self):
    ...
```


