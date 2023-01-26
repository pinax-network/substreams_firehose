# Stub Config Edit

[Pyfirehose Index](../../../../README.md#pyfirehose-index) /
[Pyfirehose](../../../index.md#pyfirehose) /
[Config](../../index.md#config) /
[Ui](../index.md#ui) /
[Forms](./index.md#forms) /
Stub Config Edit

> Auto-generated documentation for [pyfirehose.config.ui.forms.stub_config_edit](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py) module.

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

[Show source in stub_config_edit.py:563](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L563)

Confirmation screen displaying the final stub config as it will appear in the saved file.

#### Signature

```python
class StubConfigConfirmEditForm(ActionFormDiscard):
    ...
```

#### See also

- [ActionFormDiscard](./generic.md#actionformdiscard)

### StubConfigConfirmEditForm().create

[Show source in stub_config_edit.py:567](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L567)

#### Signature

```python
def create(self):
    ...
```

### StubConfigConfirmEditForm().on_cancel

[Show source in stub_config_edit.py:593](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L593)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigConfirmEditForm().on_discard

[Show source in stub_config_edit.py:596](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L596)

#### Signature

```python
def on_discard(self):
    ...
```

### StubConfigConfirmEditForm().on_ok

[Show source in stub_config_edit.py:575](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L575)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigEndpointsForm

[Show source in stub_config_edit.py:35](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L35)

Choose an endpoint to edit or create a new stub config for.

#### Attributes

- `ml_endpoints` - an `EndpointsTitleSelectOne` widget to select an endpoint.

#### Signature

```python
class StubConfigEndpointsForm(ActionFormV2):
    ...
```

### StubConfigEndpointsForm().beforeEditing

[Show source in stub_config_edit.py:42](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L42)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigEndpointsForm().create

[Show source in stub_config_edit.py:52](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L52)

#### Signature

```python
def create(self):
    ...
```

### StubConfigEndpointsForm().on_cancel

[Show source in stub_config_edit.py:71](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L71)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigEndpointsForm().on_ok

[Show source in stub_config_edit.py:60](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L60)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigInputsForm

[Show source in stub_config_edit.py:232](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L232)

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

[Show source in stub_config_edit.py:241](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L241)

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

[Show source in stub_config_edit.py:264](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L264)

#### Signature

```python
def create(self):
    ...
```

### StubConfigInputsForm().on_cancel

[Show source in stub_config_edit.py:383](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L383)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigInputsForm().on_ok

[Show source in stub_config_edit.py:347](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L347)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigMethodsForm

[Show source in stub_config_edit.py:185](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L185)

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

[Show source in stub_config_edit.py:193](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L193)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigMethodsForm().create

[Show source in stub_config_edit.py:203](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L203)

#### Signature

```python
def create(self):
    ...
```

### StubConfigMethodsForm().on_cancel

[Show source in stub_config_edit.py:228](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L228)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigMethodsForm().on_ok

[Show source in stub_config_edit.py:214](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L214)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigOutputsForm

[Show source in stub_config_edit.py:386](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L386)

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

[Show source in stub_config_edit.py:398](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L398)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigOutputsForm().create

[Show source in stub_config_edit.py:408](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L408)

#### Signature

```python
def create(self):
    ...
```

### StubConfigOutputsForm().create_output_selection

[Show source in stub_config_edit.py:472](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L472)

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

[Show source in stub_config_edit.py:559](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L559)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigOutputsForm().on_ok

[Show source in stub_config_edit.py:522](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L522)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigSaveFileForm

[Show source in stub_config_edit.py:75](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L75)

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

[Show source in stub_config_edit.py:83](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L83)

#### Signature

```python
def create(self):
    ...
```

### StubConfigSaveFileForm().on_cancel

[Show source in stub_config_edit.py:130](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L130)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigSaveFileForm().on_ok

[Show source in stub_config_edit.py:103](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L103)

#### Signature

```python
def on_ok(self):
    ...
```



## StubConfigServicesForm

[Show source in stub_config_edit.py:133](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L133)

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

[Show source in stub_config_edit.py:142](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L142)

Called by `npyscreen` before the form gets drawn on the screen.

#### Signature

```python
def beforeEditing(self):
    ...
```

### StubConfigServicesForm().create

[Show source in stub_config_edit.py:152](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L152)

#### Signature

```python
def create(self):
    ...
```

### StubConfigServicesForm().on_cancel

[Show source in stub_config_edit.py:181](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L181)

#### Signature

```python
def on_cancel(self):
    ...
```

### StubConfigServicesForm().on_ok

[Show source in stub_config_edit.py:170](https://github.com/pinax-network/pyfirehose/blob/main/pyfirehose/config/ui/forms/stub_config_edit.py#L170)

#### Signature

```python
def on_ok(self):
    ...
```


