# Inputs

[Pyfirehose Index](../../../../README.md#pyfirehose-index) /
[Pyfirehose](../../../index.md#pyfirehose) /
[Config](../../index.md#config) /
[Ui](../index.md#ui) /
[Widgets](./index.md#widgets) /
Inputs

> Auto-generated documentation for [pyfirehose.config.ui.widgets.inputs](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py) module.

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

[Show source in inputs.py:97](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L97)

Custom option boolean input to convert string values to bool.

#### Signature

```python
class InputBool(OptionBoolean):
    ...
```

### InputBool().when_set

[Show source in inputs.py:101](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L101)

#### Signature

```python
def when_set(self):
    ...
```



## InputEnum

[Show source in inputs.py:105](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L105)

Custom option single choice input to allow selecting enum values (or none).

#### Signature

```python
class InputEnum(OptionSingleChoice):
    ...
```



## InputFloat

[Show source in inputs.py:80](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L80)

Custom option input to only allow floating point input.

#### Signature

```python
class InputFloat(InputValidator, OptionFreeText):
    ...
```

#### See also

- [InputValidator](#inputvalidator)

### InputFloat().set

[Show source in inputs.py:84](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L84)

#### Signature

```python
def set(self, value):
    ...
```



## InputInteger

[Show source in inputs.py:64](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L64)

Custom option input to only allow integer input.

#### Signature

```python
class InputInteger(InputValidator, OptionFreeText):
    ...
```

#### See also

- [InputValidator](#inputvalidator)

### InputInteger().set

[Show source in inputs.py:68](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L68)

#### Signature

```python
def set(self, value):
    ...
```



## InputMessage

[Show source in inputs.py:119](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L119)

Custom option input for complex `Message` object input.

Note that this class is empty as everything is handled by the parent `OptionFreeText`.
It exists to allow generic input creation (see `StubConfigInputsForm.create` method).

#### Signature

```python
class InputMessage(OptionFreeText):
    ...
```



## InputRepeated

[Show source in inputs.py:127](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L127)

Custom option input for repeated input fields with type validation.

#### Signature

```python
class InputRepeated(InputValidator, OptionMultiFreeList):
    def __init__(
        self, value_type: str, choices: Optional[Sequence[str]] = None, *args, **kwargs
    ):
        ...
```

#### See also

- [InputValidator](#inputvalidator)

### InputRepeated().set

[Show source in inputs.py:137](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L137)

#### Signature

```python
def set(self, values):
    ...
```



## InputString

[Show source in inputs.py:111](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L111)

Custom option input for string input.

Note that this class is empty as everything is handled by the parent `OptionFreeText`.
It exists to allow generic input creation (see `StubConfigInputsForm.create` method).

#### Signature

```python
class InputString(OptionFreeText):
    ...
```



## InputValidator

[Show source in inputs.py:27](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L27)

Generic class for validating an option input with the return value of the `set` method.

Overload the `set(self, value)` method and return `True` to keep editing, `False` to quit.

#### Signature

```python
class InputValidator(Option):
    def __init__(self, multiline=False, *args, **kwargs):
        ...
```

### InputValidator().set_from_widget_value

[Show source in inputs.py:38](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L38)

Method override allowing to quit or continue the option editing depending on the return value.

See [on_ok_input_validation_hook](#on_ok_input_validation_hook).

#### Signature

```python
def set_from_widget_value(self, vl):
    ...
```



## InputsListDisplay

[Show source in inputs.py:16](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L16)

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

[Show source in inputs.py:55](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/inputs.py#L55)

Hook to replace the `on_ok` event handler for validating an option input.

It returns the value of the `Option.set` function to continue or stop the editing.
Used to prevent entering invalid input for options.

#### Signature

```python
def on_ok_input_validation_hook(self):
    ...
```


