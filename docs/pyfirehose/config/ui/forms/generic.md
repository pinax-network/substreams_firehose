# Generic

[Pyfirehose Index](../../../../README.md#pyfirehose-index) /
[Pyfirehose](../../../index.md#pyfirehose) /
[Config](../../index.md#config) /
[Ui](../index.md#ui) /
[Forms](./index.md#forms) /
Generic

> Auto-generated documentation for [pyfirehose.config.ui.forms.generic](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/generic.py) module.

- [Generic](#generic)
  - [ActionFormDiscard](#actionformdiscard)
    - [ActionFormDiscard().create_control_buttons](#actionformdiscard()create_control_buttons)
    - [ActionFormDiscard().on_discard](#actionformdiscard()on_discard)
    - [ActionFormDiscard().whenPressed](#actionformdiscard()whenpressed)
  - [SplitActionForm](#splitactionform)
    - [SplitActionForm().get_half_way](#splitactionform()get_half_way)

## ActionFormDiscard

[Show source in generic.py:7](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/generic.py#L7)

Generic class for an action form with an additional *Discard* button.

Overload the `on_discard` method to customize its behavior.

#### Signature

```python
class ActionFormDiscard(ActionFormV2, MiniButtonPress):
    ...
```

### ActionFormDiscard().create_control_buttons

[Show source in generic.py:33](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/generic.py#L33)

#### Signature

```python
def create_control_buttons(self):
    ...
```

### ActionFormDiscard().on_discard

[Show source in generic.py:58](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/generic.py#L58)

*Discard* button hook to overload for customizing the behavior of the button.

#### Signature

```python
def on_discard(self):
    ...
```

### ActionFormDiscard().whenPressed

[Show source in generic.py:17](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/generic.py#L17)

#### Signature

```python
def whenPressed(self):
    ...
```



## SplitActionForm

[Show source in generic.py:64](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/generic.py#L64)

#### Signature

```python
class SplitActionForm(ActionFormV2, SplitForm):
    ...
```

### SplitActionForm().get_half_way

[Show source in generic.py:65](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/generic.py#L65)

#### Signature

```python
def get_half_way(self, draw_line_at=None):
    ...
```


