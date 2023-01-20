# Main

[Pyfirehose Index](../../../../README.md#pyfirehose-index) /
[Pyfirehose](../../../index.md#pyfirehose) /
[Config](../../index.md#config) /
[Ui](../index.md#ui) /
[Forms](./index.md#forms) /
Main

> Auto-generated documentation for [pyfirehose.config.ui.forms.main](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/main.py) module.

- [Main](#main)
  - [MainForm](#mainform)
    - [MainForm().afterEditing](#mainform()afterediting)
    - [MainForm().beforeEditing](#mainform()beforeediting)
    - [MainForm().create](#mainform()create)
    - [MainForm().switch_form](#mainform()switch_form)

## MainForm

[Show source in main.py:14](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/main.py#L14)

Main form presenting the main config file with a menu for accessing the edit functions.

#### Attributes

- `main_menu` - holds the menu entries.
- `next_form` - describe the next form to be loaded after exiting the main form (`None` exits the application).
- `stored_highlights` - dictionary containing the highlighted text content for the `CodeHighlightedTitlePager` widget.

#### Signature

```python
class MainForm(FormWithMenus):
    ...
```

### MainForm().afterEditing

[Show source in main.py:25](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/main.py#L25)

Called by `npyscreen` when the form is cycled out of the screen.

#### Signature

```python
def afterEditing(self):
    ...
```

### MainForm().beforeEditing

[Show source in main.py:31](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/main.py#L31)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### MainForm().create

[Show source in main.py:41](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/main.py#L41)

#### Signature

```python
def create(self):
    ...
```

### MainForm().switch_form

[Show source in main.py:61](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/main.py#L61)

Helper function to set the next appropriate form when using the menu.

#### Arguments

- `form` - the form name.

#### Signature

```python
def switch_form(self, form: str) -> None:
    ...
```


