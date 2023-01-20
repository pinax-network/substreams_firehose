# Custom

[Pyfirehose Index](../../../../README.md#pyfirehose-index) /
[Pyfirehose](../../../index.md#pyfirehose) /
[Config](../../index.md#config) /
[Ui](../index.md#ui) /
[Widgets](./index.md#widgets) /
Custom

> Auto-generated documentation for [pyfirehose.config.ui.widgets.custom](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py) module.

- [Custom](#custom)
  - [CodeHighlightedPager](#codehighlightedpager)
  - [CodeHighlightedTextfield](#codehighlightedtextfield)
    - [CodeHighlightedTextfield().update_highlighting](#codehighlightedtextfield()update_highlighting)
  - [CodeHighlightedTitlePager](#codehighlightedtitlepager)
  - [EndpointsSelectOne](#endpointsselectone)
    - [EndpointsSelectOne().display_value](#endpointsselectone()display_value)
  - [EndpointsTitleSelectOne](#endpointstitleselectone)
  - [EnumSelectOneOrNone](#enumselectoneornone)
    - [EnumSelectOneOrNone().h_select](#enumselectoneornone()h_select)
  - [EnumTitleSelectOneOrNone](#enumtitleselectoneornone)
  - [OutputSelectionMLTreeMultiSelectAnnotated](#outputselectionmltreemultiselectannotated)
  - [OutputSelectionTreeData](#outputselectiontreedata)
  - [OutputSelectionTreeLineSelectableAnnotated](#outputselectiontreelineselectableannotated)
    - [OutputSelectionTreeLineSelectableAnnotated().getAnnotationAndColor](#outputselectiontreelineselectableannotated()getannotationandcolor)
  - [OutputTypesSelectOne](#outputtypesselectone)
    - [OutputTypesSelectOne().actionHighlighted](#outputtypesselectone()actionhighlighted)
  - [OutputTypesTitleSelectOne](#outputtypestitleselectone)
  - [colorize](#colorize)

## CodeHighlightedPager

[Show source in custom.py:60](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L60)

Syntax highlight enabled [`Pager`](https://npyscreen.readthedocs.io/widgets-text.html#widgets-displaying-text)
using [CodeHighlightedTextfield](#codehighlightedtextfield) as line display.

It can syntax highlight any language currently supported by the `pygments` library by passing the appropriate
[lexer](https://pygments.org/docs/lexers/#) to the constructor.

#### Signature

```python
class CodeHighlightedPager(Pager):
    def __init__(self, lexer=None, *args, **kwargs):
        ...
```



## CodeHighlightedTextfield

[Show source in custom.py:33](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L33)

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

[Show source in custom.py:46](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L46)

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

[Show source in custom.py:85](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L85)

Titled version of the [CodeHighlightedPager](#codehighlightedpager) widget.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
for reference.

#### Signature

```python
class CodeHighlightedTitlePager(TitlePager):
    ...
```



## EndpointsSelectOne

[Show source in custom.py:94](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L94)

Custom single selection widget to display the main config's endpoint data.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-multiline.html#widgets-picking-options)
for reference.

#### Signature

```python
class EndpointsSelectOne(SelectOne):
    ...
```

### EndpointsSelectOne().display_value

[Show source in custom.py:101](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L101)

#### Signature

```python
def display_value(self, vl: dict):
    ...
```



## EndpointsTitleSelectOne

[Show source in custom.py:107](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L107)

Title version of the [EndpointsSelectOne](#endpointsselectone) widget.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
for reference.

#### Signature

```python
class EndpointsTitleSelectOne(TitleSelectOne):
    ...
```



## EnumSelectOneOrNone

[Show source in custom.py:116](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L116)

Custom single selection widget to allow selecting one or none of the available values.

Used by the `InputEnum` option widget.

#### Signature

```python
class EnumSelectOneOrNone(SelectOne):
    ...
```

### EnumSelectOneOrNone().h_select

[Show source in custom.py:122](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L122)

#### Signature

```python
def h_select(self, ch):
    ...
```



## EnumTitleSelectOneOrNone

[Show source in custom.py:128](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L128)

Title version of the [EnumSelectOneOrNone](#enumselectoneornone) widget.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
for reference.

#### Signature

```python
class EnumTitleSelectOneOrNone(TitleSelectOne):
    ...
```



## OutputSelectionMLTreeMultiSelectAnnotated

[Show source in custom.py:147](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L147)

#### Signature

```python
class OutputSelectionMLTreeMultiSelectAnnotated(MLTreeMultiSelectAnnotated):
    ...
```



## OutputSelectionTreeData

[Show source in custom.py:137](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L137)

#### Signature

```python
class OutputSelectionTreeData(TreeData):
    def __init__(
        self,
        annotate: Optional[str] = "?",
        annotate_color: Optional[str] = "CONTROL",
        *args,
        **kwargs
    ):
        ...
```



## OutputSelectionTreeLineSelectableAnnotated

[Show source in custom.py:143](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L143)

#### Signature

```python
class OutputSelectionTreeLineSelectableAnnotated(TreeLineSelectableAnnotated):
    ...
```

### OutputSelectionTreeLineSelectableAnnotated().getAnnotationAndColor

[Show source in custom.py:144](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L144)

#### Signature

```python
def getAnnotationAndColor(self):
    ...
```



## OutputTypesSelectOne

[Show source in custom.py:150](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L150)

Custom single selection widget to display gRPC output types and link them to the output field selection widget.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-multiline.html#widgets-picking-options)
for reference.

#### Signature

```python
class OutputTypesSelectOne(SelectOne, MultiLineAction):
    def __init__(self, *args, **kwargs):
        ...
```

### OutputTypesSelectOne().actionHighlighted

[Show source in custom.py:161](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L161)

#### Signature

```python
def actionHighlighted(self, act_on_this, key_press):
    ...
```



## OutputTypesTitleSelectOne

[Show source in custom.py:178](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L178)

Title version of the [OutputTypesSelectOne](#outputtypesselectone) widget.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
for reference.

#### Signature

```python
class OutputTypesTitleSelectOne(TitleSelectOne):
    ...
```



## colorize

[Show source in custom.py:187](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L187)

Convert a string containg ANSI escape codes to `curses` control characters for color display.

Adapted from Cansi library (https://github.com/tslight/cansi). Some of the original comments kept in the code.

#### Arguments

- `default_color` - passed to the `mkcolors` function (see documentation for reference).
- `string` - a string containing ANSI escape codes for color.

#### Returns

A list of pairs of `curses`' control character and their applicable length.

#### Examples

`[(2097152, 10)]` will color 10 characters bold (`curses.A_BOLD = 2097152`).

#### Signature

```python
def colorize(default_color: int, string: str) -> list[tuple[int, int]]:
    ...
```


