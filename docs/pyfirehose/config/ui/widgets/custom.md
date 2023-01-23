# Custom

[Pyfirehose Index](../../../../README.md#pyfirehose-index) /
[Pyfirehose](../../../index.md#pyfirehose) /
[Config](../../index.md#config) /
[Ui](../index.md#ui) /
[Widgets](./index.md#widgets) /
Custom

> Auto-generated documentation for [pyfirehose.config.ui.widgets.custom](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py) module.

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

[Show source in custom.py:57](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L57)

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

[Show source in custom.py:30](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L30)

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

[Show source in custom.py:43](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L43)

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

[Show source in custom.py:82](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L82)

Titled version of the [CodeHighlightedPager](#codehighlightedpager) widget.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
for reference.

#### Signature

```python
class CodeHighlightedTitlePager(TitlePager):
    ...
```



## EndpointsSelectOne

[Show source in custom.py:91](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L91)

Custom single selection widget to display the main config's endpoint data.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-multiline.html#widgets-picking-options)
for reference.

#### Signature

```python
class EndpointsSelectOne(SelectOne):
    ...
```

### EndpointsSelectOne().display_value

[Show source in custom.py:98](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L98)

#### Signature

```python
def display_value(self, vl: dict):
    ...
```



## EndpointsTitleSelectOne

[Show source in custom.py:104](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L104)

Title version of the [EndpointsSelectOne](#endpointsselectone) widget.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
for reference.

#### Signature

```python
class EndpointsTitleSelectOne(TitleSelectOne):
    ...
```



## EnumSelectOneOrNone

[Show source in custom.py:113](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L113)

Custom single selection widget to allow selecting one or none of the available values.

Used by the `InputEnum` option widget.

#### Signature

```python
class EnumSelectOneOrNone(SelectOne):
    ...
```

### EnumSelectOneOrNone().h_select

[Show source in custom.py:119](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L119)

#### Signature

```python
def h_select(self, ch):
    ...
```



## EnumTitleSelectOneOrNone

[Show source in custom.py:125](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L125)

Title version of the [EnumSelectOneOrNone](#enumselectoneornone) widget.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
for reference.

#### Signature

```python
class EnumTitleSelectOneOrNone(TitleSelectOne):
    ...
```



## OutputSelectionMLTreeMultiSelectAnnotated

[Show source in custom.py:154](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L154)

Custom multi-selection tree widget using [OutputSelectionTreeLineSelectableAnnotated](#outputselectiontreelineselectableannotated) as line display.

#### Signature

```python
class OutputSelectionMLTreeMultiSelectAnnotated(MLTreeMultiSelectAnnotated):
    ...
```



## OutputSelectionTreeData

[Show source in custom.py:134](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L134)

A `TreeData` node representing an output field from a `Message` output type.

#### Attributes

- `annotate` - Text annotation to display next to the node content.
- `annotate_color` - Color of the text annotation (see [reference](https://npyscreen.readthedocs.io/color.html) for a list of valid values).

#### Signature

```python
class OutputSelectionTreeData(TreeData):
    def __init__(
        self, annotate: str = "?", annotate_color: str = "CONTROL", *args, **kwargs
    ):
        ...
```



## OutputSelectionTreeLineSelectableAnnotated

[Show source in custom.py:147](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L147)

Custom tree line selectable widget implementing the annotation behavior.

#### Signature

```python
class OutputSelectionTreeLineSelectableAnnotated(TreeLineSelectableAnnotated):
    ...
```

### OutputSelectionTreeLineSelectableAnnotated().getAnnotationAndColor

[Show source in custom.py:151](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L151)

#### Signature

```python
def getAnnotationAndColor(self):
    ...
```



## OutputTypesSelectOne

[Show source in custom.py:160](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L160)

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

[Show source in custom.py:171](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L171)

#### Signature

```python
def actionHighlighted(self, act_on_this, key_press):
    ...
```



## OutputTypesTitleSelectOne

[Show source in custom.py:188](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L188)

Title version of the [OutputTypesSelectOne](#outputtypesselectone) widget.

See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
for reference.

#### Signature

```python
class OutputTypesTitleSelectOne(TitleSelectOne):
    ...
```



## colorize

[Show source in custom.py:197](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/widgets/custom.py#L197)

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


