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

[Show source in stub_config_edit.py:560](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L560)

Confirmation screen displaying the final stub config as it will appear in the saved file.

#### Signature

```python
class StubConfigConfirmEditForm(ActionFormDiscard):
    ...
```

#### See also

- [ActionFormDiscard](./generic.md#actionformdiscard)

### StubConfigConfirmEditForm().create

[Show source in stub_config_edit.py:564](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L564)

#### Signature

```python
def create(self):
    ...
```

### StubConfigConfirmEditForm().on_cancel

[Show source in stub_config_edit.py:590](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L590)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigConfirmEditForm().on_discard

[Show source in stub_config_edit.py:593](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L593)

#### Signature

```python
def on_discard(self):
    ...
```

### StubConfigConfirmEditForm().on_ok

[Show source in stub_config_edit.py:572](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L572)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigEndpointsForm

[Show source in stub_config_edit.py:33](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L33)

Choose an endpoint to edit or create a new stub config for.

#### Attributes

- `ml_endpoints` - an `EndpointsTitleSelectOne` widget to select an endpoint.

#### Signature

```python
class StubConfigEndpointsForm(ActionFormV2):
    ...
```

### StubConfigEndpointsForm().beforeEditing

[Show source in stub_config_edit.py:40](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L40)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigEndpointsForm().create

[Show source in stub_config_edit.py:50](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L50)

#### Signature

```python
def create(self):
    ...
```

### StubConfigEndpointsForm().on_cancel

[Show source in stub_config_edit.py:69](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L69)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigEndpointsForm().on_ok

[Show source in stub_config_edit.py:58](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L58)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigInputsForm

[Show source in stub_config_edit.py:230](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L230)

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

[Show source in stub_config_edit.py:239](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L239)

Callback function for clearing input shortcuts.

Pressing 'c' will ask for confirmation before clearing, 'C' will not.

#### Arguments

- `show_popup` - if True, asks the user for confirmation before clearing the input.

#### Signature

```python
def clear_input(self, show_popup: bool = True) -> None:
    ...
```

### StubConfigInputsForm().create

[Show source in stub_config_edit.py:262](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L262)

#### Signature

```python
def create(self):
    ...
```

### StubConfigInputsForm().on_cancel

[Show source in stub_config_edit.py:381](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L381)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigInputsForm().on_ok

[Show source in stub_config_edit.py:345](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L345)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigMethodsForm

[Show source in stub_config_edit.py:183](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L183)

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

[Show source in stub_config_edit.py:191](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L191)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigMethodsForm().create

[Show source in stub_config_edit.py:201](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L201)

#### Signature

```python
def create(self):
    ...
```

### StubConfigMethodsForm().on_cancel

[Show source in stub_config_edit.py:226](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L226)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigMethodsForm().on_ok

[Show source in stub_config_edit.py:212](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L212)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigOutputsForm

[Show source in stub_config_edit.py:384](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L384)

Select and filter fields that will be received from the gRPC stream.

The top selection widget presents a list of compatible output types while the bottom tree widget list the
available fields that can be selected to be kept from the response.

#### Attributes

- `is_substream` - Identifies if the service is using Substreams.
- `output_descriptors` - List of available `Descriptor` for the corresponding method.
- `saved_output_selection` - Stores the state of a selection tree to be restored when switching output types.

#### Signature

```python
class StubConfigOutputsForm(SplitActionForm):
    ...
```

#### See also

- [SplitActionForm](./generic.md#splitactionform)

### StubConfigOutputsForm().beforeEditing

[Show source in stub_config_edit.py:396](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L396)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigOutputsForm().create

[Show source in stub_config_edit.py:406](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L406)

#### Signature

```python
def create(self):
    ...
```

### StubConfigOutputsForm().create_output_selection

[Show source in stub_config_edit.py:469](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L469)

Create the output field selection tree from the selected output type. If `previous_selected` is supplied,
the state of the node in the tree (`selected` and `expanded`) will be set according to its description.

#### Arguments

- `previous_selected` - A dictionnary with a node's (depth, content) as key and its state (selected, expanded) as value.

#### Returns

The root node of the selection tree.

#### Signature

```python
def create_output_selection(
    self, previous_selected: dict[tuple[int, str], tuple[int, int]] | None = None
) -> OutputSelectionTreeData:
    ...
```

#### See also

- [OutputSelectionTreeData](../widgets/custom.md#outputselectiontreedata)

### StubConfigOutputsForm().on_cancel

[Show source in stub_config_edit.py:556](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L556)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigOutputsForm().on_ok

[Show source in stub_config_edit.py:519](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L519)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigSaveFileForm

[Show source in stub_config_edit.py:73](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L73)

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

[Show source in stub_config_edit.py:81](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L81)

#### Signature

```python
def create(self):
    ...
```

### StubConfigSaveFileForm().on_cancel

[Show source in stub_config_edit.py:128](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L128)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigSaveFileForm().on_ok

[Show source in stub_config_edit.py:101](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L101)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigServicesForm

[Show source in stub_config_edit.py:131](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L131)

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

[Show source in stub_config_edit.py:140](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L140)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigServicesForm().create

[Show source in stub_config_edit.py:150](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L150)

#### Signature

```python
def create(self):
    ...
```

### StubConfigServicesForm().on_cancel

[Show source in stub_config_edit.py:179](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L179)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigServicesForm().on_ok

[Show source in stub_config_edit.py:168](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L168)

#### Signature

```python
def on_ok(self):
    ...
```


