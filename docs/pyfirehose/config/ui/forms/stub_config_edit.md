# Stub Config Edit

[Pyfirehose Index](../../../../README.md#pyfirehose-index) /
[Pyfirehose](../../../index.md#pyfirehose) /
[Config](../../index.md#config) /
[Ui](../index.md#ui) /
[Forms](./index.md#forms) /
Stub Config Edit

> Auto-generated documentation for [pyfirehose.config.ui.forms.stub_config_edit](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py) module.

- [Stub Config Edit](#stub-config-edit)
  - [StubConfigConfirmEditForm](#stubconfigconfirmeditform)
    - [StubConfigConfirmEditForm().create](#stubconfigconfirmeditform()create)
    - [StubConfigConfirmEditForm().on_cancel](#stubconfigconfirmeditform()on_cancel)
    - [StubConfigConfirmEditForm().on_discard](#stubconfigconfirmeditform()on_discard)
    - [StubConfigConfirmEditForm().on_ok](#stubconfigconfirmeditform()on_ok)
  - [StubConfigEndpointsForm](#stubconfigendpointsform)
    - [StubConfigEndpointsForm().beforeEditing](#stubconfigendpointsform()beforeediting)
    - [StubConfigEndpointsForm().create](#stubconfigendpointsform()create)
    - [StubConfigEndpointsForm().on_cancel](#stubconfigendpointsform()on_cancel)
    - [StubConfigEndpointsForm().on_ok](#stubconfigendpointsform()on_ok)
  - [StubConfigInputsForm](#stubconfiginputsform)
    - [StubConfigInputsForm().clear_input](#stubconfiginputsform()clear_input)
    - [StubConfigInputsForm().create](#stubconfiginputsform()create)
    - [StubConfigInputsForm().on_cancel](#stubconfiginputsform()on_cancel)
    - [StubConfigInputsForm().on_ok](#stubconfiginputsform()on_ok)
  - [StubConfigMethodsForm](#stubconfigmethodsform)
    - [StubConfigMethodsForm().beforeEditing](#stubconfigmethodsform()beforeediting)
    - [StubConfigMethodsForm().create](#stubconfigmethodsform()create)
    - [StubConfigMethodsForm().on_cancel](#stubconfigmethodsform()on_cancel)
    - [StubConfigMethodsForm().on_ok](#stubconfigmethodsform()on_ok)
  - [StubConfigOutputsForm](#stubconfigoutputsform)
    - [StubConfigOutputsForm().beforeEditing](#stubconfigoutputsform()beforeediting)
    - [StubConfigOutputsForm().create](#stubconfigoutputsform()create)
    - [StubConfigOutputsForm().create_output_selection](#stubconfigoutputsform()create_output_selection)
    - [StubConfigOutputsForm().on_cancel](#stubconfigoutputsform()on_cancel)
    - [StubConfigOutputsForm().on_ok](#stubconfigoutputsform()on_ok)
  - [StubConfigSaveFileForm](#stubconfigsavefileform)
    - [StubConfigSaveFileForm().create](#stubconfigsavefileform()create)
    - [StubConfigSaveFileForm().on_cancel](#stubconfigsavefileform()on_cancel)
    - [StubConfigSaveFileForm().on_ok](#stubconfigsavefileform()on_ok)
  - [StubConfigServicesForm](#stubconfigservicesform)
    - [StubConfigServicesForm().beforeEditing](#stubconfigservicesform()beforeediting)
    - [StubConfigServicesForm().create](#stubconfigservicesform()create)
    - [StubConfigServicesForm().on_cancel](#stubconfigservicesform()on_cancel)
    - [StubConfigServicesForm().on_ok](#stubconfigservicesform()on_ok)

## StubConfigConfirmEditForm

[Show source in stub_config_edit.py:535](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L535)

Confirmation screen displaying the final stub config as it will appear in the saved file.

#### Signature

```python
class StubConfigConfirmEditForm(ActionFormDiscard):
    ...
```

#### See also

- [ActionFormDiscard](./generic.md#actionformdiscard)

### StubConfigConfirmEditForm().create

[Show source in stub_config_edit.py:539](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L539)

#### Signature

```python
def create(self):
    ...
```

### StubConfigConfirmEditForm().on_cancel

[Show source in stub_config_edit.py:565](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L565)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigConfirmEditForm().on_discard

[Show source in stub_config_edit.py:568](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L568)

#### Signature

```python
def on_discard(self):
    ...
```

### StubConfigConfirmEditForm().on_ok

[Show source in stub_config_edit.py:547](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L547)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigEndpointsForm

[Show source in stub_config_edit.py:34](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L34)

Choose an endpoint to edit or create a new stub config for.

#### Attributes

- `ml_endpoints` - an `EndpointsTitleSelectOne` widget to select an endpoint.

#### Signature

```python
class StubConfigEndpointsForm(ActionFormV2):
    ...
```

### StubConfigEndpointsForm().beforeEditing

[Show source in stub_config_edit.py:41](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L41)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigEndpointsForm().create

[Show source in stub_config_edit.py:51](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L51)

#### Signature

```python
def create(self):
    ...
```

### StubConfigEndpointsForm().on_cancel

[Show source in stub_config_edit.py:70](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L70)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigEndpointsForm().on_ok

[Show source in stub_config_edit.py:59](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L59)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigInputsForm

[Show source in stub_config_edit.py:231](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L231)

Edit the request parameters sent to the gRPC endpoint.

Input options will be created according to their expected types (bool -> `InputBoolean`, etc.).

#### Attributes

- `w_inputs` - an `InputsListDisplay` widget to present the list of input options.

#### Signature

```python
class StubConfigInputsForm(ActionFormV2):
    ...
```

### StubConfigInputsForm().clear_input

[Show source in stub_config_edit.py:240](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L240)

Callback function for clearing input shortcuts.

Pressing 'c' will ask for confirmation before clearing, 'C' will not.

#### Arguments

- `show_popup` - if True, asks the user for confirmation before clearing the input.

#### Signature

```python
def clear_input(self, show_popup: Optional[bool] = True) -> None:
    ...
```

### StubConfigInputsForm().create

[Show source in stub_config_edit.py:263](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L263)

#### Signature

```python
def create(self):
    ...
```

### StubConfigInputsForm().on_cancel

[Show source in stub_config_edit.py:382](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L382)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigInputsForm().on_ok

[Show source in stub_config_edit.py:346](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L346)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigMethodsForm

[Show source in stub_config_edit.py:184](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L184)

Choose a gRPC method from the specified service.

#### Attributes

- `methods` - available methods provided by the reflection service.
- `ml_methods` - a `TitleSelectOne` widget to select which method the stub will use.

#### Signature

```python
class StubConfigMethodsForm(ActionFormV2):
    ...
```

### StubConfigMethodsForm().beforeEditing

[Show source in stub_config_edit.py:192](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L192)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigMethodsForm().create

[Show source in stub_config_edit.py:202](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L202)

#### Signature

```python
def create(self):
    ...
```

### StubConfigMethodsForm().on_cancel

[Show source in stub_config_edit.py:227](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L227)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigMethodsForm().on_ok

[Show source in stub_config_edit.py:213](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L213)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigOutputsForm

[Show source in stub_config_edit.py:385](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L385)

...

#### Signature

```python
class StubConfigOutputsForm(SplitActionForm):
    ...
```

#### See also

- [SplitActionForm](./generic.md#splitactionform)

### StubConfigOutputsForm().beforeEditing

[Show source in stub_config_edit.py:389](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L389)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigOutputsForm().create

[Show source in stub_config_edit.py:399](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L399)

#### Signature

```python
def create(self):
    ...
```

### StubConfigOutputsForm().create_output_selection

[Show source in stub_config_edit.py:462](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L462)

#### Signature

```python
def create_output_selection(
    self, previous_selected: Optional[dict[tuple[int, str], tuple[int, int]]] = None
) -> OutputSelectionTreeData:
    ...
```

#### See also

- [OutputSelectionTreeData](../widgets/custom.md#outputselectiontreedata)

### StubConfigOutputsForm().on_cancel

[Show source in stub_config_edit.py:531](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L531)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigOutputsForm().on_ok

[Show source in stub_config_edit.py:494](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L494)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigSaveFileForm

[Show source in stub_config_edit.py:74](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L74)

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

[Show source in stub_config_edit.py:82](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L82)

#### Signature

```python
def create(self):
    ...
```

### StubConfigSaveFileForm().on_cancel

[Show source in stub_config_edit.py:129](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L129)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigSaveFileForm().on_ok

[Show source in stub_config_edit.py:102](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L102)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigServicesForm

[Show source in stub_config_edit.py:132](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L132)

Choose a service from the services available on the specified endpoint.

The endpoint **has** to provide a reflection service in order to determine the available services.

#### Attributes

- `ml_services` - a `TitleSelectOne` widget to select which service the stub will use.

#### Signature

```python
class StubConfigServicesForm(ActionFormV2):
    ...
```

### StubConfigServicesForm().beforeEditing

[Show source in stub_config_edit.py:141](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L141)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigServicesForm().create

[Show source in stub_config_edit.py:151](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L151)

#### Signature

```python
def create(self):
    ...
```

### StubConfigServicesForm().on_cancel

[Show source in stub_config_edit.py:180](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L180)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigServicesForm().on_ok

[Show source in stub_config_edit.py:169](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L169)

#### Signature

```python
def on_ok(self):
    ...
```


