# Forms

[Pyfirehose Index](../../../README.md#pyfirehose-index) /
[Pyfirehose](../../index.md#pyfirehose) /
[Config](../index.md#config) /
[Ui](./index.md#ui) /
Forms

> Auto-generated documentation for [pyfirehose.config.ui.forms](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py) module.

- [Forms](#forms)
  - [ActionFormDiscard](#actionformdiscard)
    - [ActionFormDiscard().create_control_buttons](#actionformdiscard()create_control_buttons)
    - [ActionFormDiscard().on_discard](#actionformdiscard()on_discard)
    - [ActionFormDiscard().whenPressed](#actionformdiscard()whenpressed)
  - [MainForm](#mainform)
    - [MainForm().afterEditing](#mainform()afterediting)
    - [MainForm().beforeEditing](#mainform()beforeediting)
    - [MainForm().create](#mainform()create)
    - [MainForm().switch_form](#mainform()switch_form)
  - [StubConfigConfirmEditForm](#stubconfigconfirmeditform)
    - [StubConfigConfirmEditForm().create](#stubconfigconfirmeditform()create)
    - [StubConfigConfirmEditForm().on_cancel](#stubconfigconfirmeditform()on_cancel)
    - [StubConfigConfirmEditForm().on_discard](#stubconfigconfirmeditform()on_discard)
    - [StubConfigConfirmEditForm().on_ok](#stubconfigconfirmeditform()on_ok)
  - [StubConfigEndpointsForm](#stubconfigendpointsform)
    - [StubConfigEndpointsForm().create](#stubconfigendpointsform()create)
    - [StubConfigEndpointsForm().on_cancel](#stubconfigendpointsform()on_cancel)
    - [StubConfigEndpointsForm().on_ok](#stubconfigendpointsform()on_ok)
  - [StubConfigInputsForm](#stubconfiginputsform)
    - [StubConfigInputsForm().create](#stubconfiginputsform()create)
    - [StubConfigInputsForm().on_cancel](#stubconfiginputsform()on_cancel)
    - [StubConfigInputsForm().on_ok](#stubconfiginputsform()on_ok)
  - [StubConfigMethodsForm](#stubconfigmethodsform)
    - [StubConfigMethodsForm().create](#stubconfigmethodsform()create)
    - [StubConfigMethodsForm().on_cancel](#stubconfigmethodsform()on_cancel)
    - [StubConfigMethodsForm().on_ok](#stubconfigmethodsform()on_ok)
  - [StubConfigSaveFileForm](#stubconfigsavefileform)
    - [StubConfigSaveFileForm().create](#stubconfigsavefileform()create)
    - [StubConfigSaveFileForm().on_cancel](#stubconfigsavefileform()on_cancel)
    - [StubConfigSaveFileForm().on_ok](#stubconfigsavefileform()on_ok)
  - [StubConfigServicesForm](#stubconfigservicesform)
    - [StubConfigServicesForm().create](#stubconfigservicesform()create)
    - [StubConfigServicesForm().on_cancel](#stubconfigservicesform()on_cancel)
    - [StubConfigServicesForm().on_ok](#stubconfigservicesform()on_ok)
  - [colorize](#colorize)
  - [mkcolor](#mkcolor)

## ActionFormDiscard

[Show source in forms.py:409](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L409)

Parent class for an `ActionFormV2` with an additional *Discard* button.

Overload the `on_discard` method to customize its behavior.

#### Signature

```python
class ActionFormDiscard(ActionFormV2, MiniButtonPress):
    ...
```

### ActionFormDiscard().create_control_buttons

[Show source in forms.py:435](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L435)

#### Signature

```python
def create_control_buttons(self):
    ...
```

### ActionFormDiscard().on_discard

[Show source in forms.py:460](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L460)

*Discard* button hook to overload for customizing the behavior of the button.

#### Signature

```python
def on_discard(self):
    ...
```

### ActionFormDiscard().whenPressed

[Show source in forms.py:419](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L419)

#### Signature

```python
def whenPressed(self):
    ...
```



## MainForm

[Show source in forms.py:50](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L50)

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

[Show source in forms.py:61](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L61)

Called by `npyscreen` when the form is cycled out of the screen.

#### Signature

```python
def afterEditing(self):
    ...
```

### MainForm().beforeEditing

[Show source in forms.py:67](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L67)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### MainForm().create

[Show source in forms.py:77](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L77)

#### Signature

```python
def create(self):
    ...
```

### MainForm().switch_form

[Show source in forms.py:109](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L109)

Helper function to set the next appropriate form when using the menu.

#### Arguments

- `form` - the form name.

#### Signature

```python
def switch_form(self, form: str) -> None:
    ...
```



## StubConfigConfirmEditForm

[Show source in forms.py:466](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L466)

Confirmation screen displaying the final stub config as it will appear in the saved file.

#### Attributes

- `stored_highlights` - dictionary containing the highlighted text content for the `CodeHighlightedTitlePager` widget.

#### Signature

```python
class StubConfigConfirmEditForm(ActionFormDiscard):
    ...
```

#### See also

- [ActionFormDiscard](#actionformdiscard)

### StubConfigConfirmEditForm().create

[Show source in forms.py:473](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L473)

#### Signature

```python
def create(self):
    ...
```

### StubConfigConfirmEditForm().on_cancel

[Show source in forms.py:511](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L511)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigConfirmEditForm().on_discard

[Show source in forms.py:514](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L514)

#### Signature

```python
def on_discard(self):
    ...
```

### StubConfigConfirmEditForm().on_ok

[Show source in forms.py:493](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L493)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigEndpointsForm

[Show source in forms.py:119](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L119)

Choose an endpoint to edit or create a new the stub config for.

#### Attributes

- `ml_endpoints` - an `EndpointsTitleSelectOne` widget to select an endpoint.

#### Signature

```python
class StubConfigEndpointsForm(ActionFormV2):
    ...
```

### StubConfigEndpointsForm().create

[Show source in forms.py:126](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L126)

#### Signature

```python
def create(self):
    ...
```

### StubConfigEndpointsForm().on_cancel

[Show source in forms.py:145](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L145)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigEndpointsForm().on_ok

[Show source in forms.py:135](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L135)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigInputsForm

[Show source in forms.py:279](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L279)

Edit the request parameters sent to the gRPC endpoint.

Input options will be created according to their expected types (bool -> `InputBoolean`, etc.).

#### Attributes

- `w_inputs` - an `InputsListDisplay` widget to present the list of input options.

#### Signature

```python
class StubConfigInputsForm(ActionFormV2):
    ...
```

### StubConfigInputsForm().create

[Show source in forms.py:288](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L288)

#### Signature

```python
def create(self):
    ...
```

### StubConfigInputsForm().on_cancel

[Show source in forms.py:404](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L404)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigInputsForm().on_ok

[Show source in forms.py:385](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L385)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigMethodsForm

[Show source in forms.py:243](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L243)

Choose a gRPC method from the specified service.

#### Attributes

- `methods` - available methods provided by the reflection service.
- `ml_services` - a `TitleSelectOne` widget to select which method the stub will use.

#### Signature

```python
class StubConfigMethodsForm(ActionFormV2):
    ...
```

### StubConfigMethodsForm().create

[Show source in forms.py:251](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L251)

#### Signature

```python
def create(self):
    ...
```

### StubConfigMethodsForm().on_cancel

[Show source in forms.py:276](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L276)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigMethodsForm().on_ok

[Show source in forms.py:263](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L263)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigSaveFileForm

[Show source in forms.py:148](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L148)

Choose the save file location for the stub config.

#### Attributes

- `stub_loaded` - indicates if the stub has been loaded from the specified file.
- `tfc_stub_save_file` - a `TitleFilenameCombo` widget to select the stub save file.

#### Signature

```python
class StubConfigSaveFileForm(ActionFormV2):
    ...
```

### StubConfigSaveFileForm().create

[Show source in forms.py:156](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L156)

#### Signature

```python
def create(self):
    ...
```

### StubConfigSaveFileForm().on_cancel

[Show source in forms.py:199](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L199)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigSaveFileForm().on_ok

[Show source in forms.py:172](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L172)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigServicesForm

[Show source in forms.py:202](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L202)

Choose a service from the services available on the specified endpoint.

The endpoint **has** to provide a reflection service in order to determine the available services.

#### Attributes

- `ml_services` - a `TitleSelectOne` widget to select which service the stub will use.

#### Signature

```python
class StubConfigServicesForm(ActionFormV2):
    ...
```

### StubConfigServicesForm().create

[Show source in forms.py:211](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L211)

#### Signature

```python
def create(self):
    ...
```

### StubConfigServicesForm().on_cancel

[Show source in forms.py:240](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L240)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigServicesForm().on_ok

[Show source in forms.py:230](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L230)

#### Signature

```python
def on_ok(self):
    ...
```



## colorize

[Show source in forms.py:566](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L566)

Convert a string containg ANSI escape codes to `curses` control characters for color display.

Adapted from Cansi library (https://github.com/tslight/cansi). Some of the original kept in the code.

#### Arguments

- `default_color` - passed to the `mkcolors` function (see documentation for reference).
- `string` - a string containing ANSI escape codes for color.

#### Returns

A list of pairs of `curses`'s control character and their applicable length.

#### Examples

`[(2097152, 10)]` will color 10 characters bold (`curses.A_BOLD = 2097152`).

#### Signature

```python
def colorize(default_color: int, string: str) -> list[tuple[int, int]]:
    ...
```



## mkcolor

[Show source in forms.py:526](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms.py#L526)

Initialize `curses` colors and mapping of ANSI escape codes.

Adapted from Cansi library (https://github.com/tslight/cansi). Original comments kept in code.

See [Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters)
for ANSI escape codes reference.

#### Arguments

- `default_color` - color pair used for the default background and foreground ANSI escape codes ("39;49;00").
- `offset` - offset for the `curses.init_pair` function to avoid overwriting predefined colors of `npyscreen`'s theme.

#### Returns

A dictionary mapping of ANSI escape sequences to `curses`'s control characters.

#### Signature

```python
def mkcolor(default_color: int, offset: Optional[int] = 49) -> dict[str, int]:
    ...
```


