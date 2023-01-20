# App

[Pyfirehose Index](../../../README.md#pyfirehose-index) /
[Pyfirehose](../../index.md#pyfirehose) /
[Config](../index.md#config) /
[Ui](./index.md#ui) /
App

> Auto-generated documentation for [pyfirehose.config.ui.app](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/app.py) module.

- [App](#app)
  - [ConfigApp](#configapp)
    - [ConfigApp().onStart](#configapp()onstart)

## ConfigApp

[Show source in app.py:17](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/app.py#L17)

Main app containing the forms for the config GUI.

It acts as a medium of communication for getting value between forms, storing data as instance attributes
(via the `self.parentApp` variable available in child forms).

See [npyscreen's documentation](https://npyscreen.readthedocs.io/application-objects.html#in-detail)
for reference.

#### Signature

```python
class ConfigApp(NPSAppManaged):
    def __init__(self):
        ...
```

### ConfigApp().onStart

[Show source in app.py:48](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/config/ui/app.py#L48)

#### Signature

```python
def onStart(self):
    ...
```


