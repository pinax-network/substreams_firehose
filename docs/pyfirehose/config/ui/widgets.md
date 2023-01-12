# Widgets

[Pyfirehose Index](../../../README.md#pyfirehose-index) /
[Pyfirehose](../../index.md#pyfirehose) /
[Config](../index.md#config) /
[Ui](./index.md#ui) /
Widgets

> Auto-generated documentation for [pyfirehose.config.ui.widgets](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py) module.

- [Widgets](#widgets)
  - [CodeHighlightedPager](#codehighlightedpager)
  - [CodeHighlightedTextfield](#codehighlightedtextfield)
    - [CodeHighlightedTextfield().update_highlighting](#codehighlightedtextfield()update_highlighting)
  - [CodeHighlightedTitlePager](#codehighlightedtitlepager)
  - [EndpointsSelectOne](#endpointsselectone)
    - [EndpointsSelectOne().display_value](#endpointsselectone()display_value)
  - [EndpointsTitleSelectOne](#endpointstitleselectone)
  - [InputBoolean](#inputboolean)
    - [InputBoolean().when_set](#inputboolean()when_set)
  - [InputFloat](#inputfloat)
    - [InputFloat().set](#inputfloat()set)
    - [InputFloat().set_from_widget_value](#inputfloat()set_from_widget_value)
  - [InputInteger](#inputinteger)
    - [InputInteger().set](#inputinteger()set)
    - [InputInteger().set_from_widget_value](#inputinteger()set_from_widget_value)
  - [InputsListDisplay](#inputslistdisplay)
  - [on_ok_input_validation_hook](#on_ok_input_validation_hook)

## CodeHighlightedPager

[Show source in widgets.py:39](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L39)

Syntax highlight enabled [`Pager`](https://npyscreen.readthedocs.io/widgets-text.html#widgets-displaying-text)
using [CodeHighlightedTextfield](#codehighlightedtextfield) as line display.

#### Signature

```python
class CodeHighlightedPager(Pager):
    ...
```



## CodeHighlightedTextfield

[Show source in widgets.py:12](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L12)

Syntax highlight enabled [`Textfield`](https://npyscreen.readthedocs.io/widgets-text.html#widgets-displaying-text)
for displaying JSON config files.

#### Attributes

- `_highlightingdata` - internal array specifying special control characters for curses to display colors.
- `syntax_highlighting` - enable syntax highlight for npyscreen to call the `update_highlight` method on redraw.

#### Signature

```python
class CodeHighlightedTextfield(Textfield):
    def __init__(self, *args, **kwargs):
        ...
```

### CodeHighlightedTextfield().update_highlighting

[Show source in widgets.py:25](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L25)

Called on every call to the internal `_print` function.

See [`Textfield` implementation](
    https://github.com/npcole/npyscreen/blob/8ce31204e1de1fbd2939ffe2d8c3b3120e93a4d0/npyscreen/wgtextbox.py#L247
) for details

#### Signature

```python
def update_highlighting(self, start=None, end=None, clear=False):
    ...
```



## CodeHighlightedTitlePager

[Show source in widgets.py:46](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L46)

Titled version of the [CodeHighlightedPager](#codehighlightedpager).

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
for reference.

#### Signature

```python
class CodeHighlightedTitlePager(TitlePager):
    ...
```



## EndpointsSelectOne

[Show source in widgets.py:55](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L55)

Custom single selection widget to display main config's endpoint data.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-multiline.html#widgets-picking-options)
for reference.

#### Signature

```python
class EndpointsSelectOne(SelectOne):
    ...
```

### EndpointsSelectOne().display_value

[Show source in widgets.py:62](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L62)

#### Signature

```python
def display_value(self, vl: dict):
    ...
```



## EndpointsTitleSelectOne

[Show source in widgets.py:68](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L68)

Title version of the [EndpointsSelectOne](#endpointsselectone).

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
for reference.

#### Signature

```python
class EndpointsTitleSelectOne(TitleSelectOne):
    ...
```



## InputBoolean

[Show source in widgets.py:88](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L88)

Custom option boolean input to convert string values to bool.

#### Signature

```python
class InputBoolean(OptionBoolean):
    ...
```

### InputBoolean().when_set

[Show source in widgets.py:92](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L92)

#### Signature

```python
def when_set(self):
    ...
```



## InputFloat

[Show source in widgets.py:96](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L96)

Custom option input to only allow floating point input.

#### Signature

```python
class InputFloat(OptionFreeText):
    ...
```

### InputFloat().set

[Show source in widgets.py:100](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L100)

#### Signature

```python
def set(self, value):
    ...
```

### InputFloat().set_from_widget_value

[Show source in widgets.py:115](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L115)

Method override allowing to quit or continue the option editing depending on the return value.

See [on_ok_input_validation_hook](#on_ok_input_validation_hook).

#### Signature

```python
def set_from_widget_value(self, vl):
    ...
```



## InputInteger

[Show source in widgets.py:132](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L132)

Custom option input to only allow integer input.

#### Signature

```python
class InputInteger(OptionFreeText):
    ...
```

### InputInteger().set

[Show source in widgets.py:136](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L136)

#### Signature

```python
def set(self, value):
    ...
```

### InputInteger().set_from_widget_value

[Show source in widgets.py:152](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L152)

Method override allowing to quit or continue the option editing depending on the return value.

See [on_ok_input_validation_hook](#on_ok_input_validation_hook).

#### Signature

```python
def set_from_widget_value(self, vl):
    ...
```



## InputsListDisplay

[Show source in widgets.py:77](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L77)

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

[Show source in widgets.py:169](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets.py#L169)

Hook to replace the `on_ok` event handler for validating an option input.

It returns the value of the `Option.set` function to continue or stop the editing.
Used to prevent entering invalid input for options.

#### Signature

```python
def on_ok_input_validation_hook(self):
    ...
```


