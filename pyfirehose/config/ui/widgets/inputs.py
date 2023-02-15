"""
SPDX-License-Identifier: MIT

`Option` widget subclasses for input validation and display.
"""

import logging
from collections.abc import Sequence
from types import MethodType
from weakref import ref

from npyscreen import ActionFormV2
from npyscreen import OptionBoolean, OptionFilename, OptionFreeText, OptionMultiFreeList, OptionSingleChoice
from npyscreen import OptionListDisplay, OptionListDisplayLine
from npyscreen import notify_confirm
from npyscreen.apOptions import Option

import pyfirehose.config.ui.widgets.input_validators as validators
from pyfirehose.config.ui.widgets.custom import EnumTitleSelectOneOrNone

class InputListDisplayLine(OptionListDisplayLine):
    """
    Custom option line display for setting custom option name color.
    """
    def getAnnotationAndColor(self):
        try:
            return (self.value.get_name_user(), self.value.annotation_color)
        except AttributeError:
            return (self.value.get_name_user(), 'LABEL')

class InputListDisplay(OptionListDisplay):
    """
    Custom option list display for increased option title width.

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/options.html#options-and-option-lists)
    for reference.
    """
    ANNOTATE_WIDTH_PADDING = 10

    def __init__(self, *args, **kwargs):
        self._contained_widgets = InputListDisplayLine
        super().__init__(*args, **kwargs)

        # Set the annotation width according to the longuest displayed value + some offset
        self._contained_widgets.ANNOTATE_WIDTH = max(map(len, [o.get_name_user() for o in self.values])) + self.ANNOTATE_WIDTH_PADDING

    def _set_line_values(self, line, value_indexer):
        """
        Overwrite method for taking the `hidden` attribute value of the displayed widget into account.
        """
        try:
            _vl = self.values[value_indexer]
        except (IndexError, TypeError):
            self._set_line_blank(line)
        else:
            line.value = self.display_value(_vl)
            try:
                line.hidden = _vl.hidden
            except AttributeError:
                pass

class InputGeneric(Option): # TODO: Add markdown support for `documentation` field ?
    """
    Generic class allowing an input to be specified as required or optional.

    The returned annotated display value will be changed according to the parameter value, if it exists.

    Attributes:
        required: An optional boolean specifying if the input is required (`True`) or optional (`False`). If not used, the value is `None`.
        annotation_color: An optional string specifying the color of the displayed input name.
    """
    REQUIRED_DISPLAY_STRING = '[!]'
    OPTIONAL_DISPLAY_STRING = '[o]'

    def __init__(self, *args, required: bool | None = None, annotation_color: str = 'GOOD', **kwargs):
        super().__init__(*args, **kwargs)
        self.required = required
        self.annotation_color = annotation_color

    def get_name_user(self) -> str:
        if self.required is not None:
            return f'{self.REQUIRED_DISPLAY_STRING if self.required else self.OPTIONAL_DISPLAY_STRING} {self.name}'

        return self.name

class InputValidator(InputGeneric):
    """
    Generic class for validating an option input with the return value of the `set` method.

    Overload the `set(self, value)` method and return `True` to keep editing, `False` to quit.

    Attributes:
        multiline: A boolean indicating if the underlying widget is a multiline widget (its value being a `list`) or not.
    """
    def __init__(self, *args, multiline: bool = False, **kwargs):
        super().__init__(*args, **kwargs)

        self.multiline = multiline

    def set_from_widget_value(self, vl):
        """
        Method override allowing to quit or continue the option editing depending on the return value.

        See `on_ok_input_validation_hook`.
        """
        return self.set(vl.splitlines() if self.multiline else vl)

    def _set_up_widget_values(self, option_form, main_option_widget):
        """
        Method override to replace the option form `on_ok` event handler with our own hook.

        See `on_ok_input_validation_hook`.
        """
        main_option_widget.value = '\n'.join(self.value) if self.multiline else self.value
        option_form.on_ok = MethodType(on_ok_input_validation_hook, option_form)

def on_ok_input_validation_hook(self,):
    """
    Hook to replace the `on_ok` event handler for validating an option input.

    It returns the value of the `Option.set` function to continue or stop the editing.
    Used to prevent entering invalid input for options.
    """
    return self.OPTION_TO_CHANGE.set_from_widget_value(self.OPTION_WIDGET.value)

class InputInteger(InputValidator, OptionFreeText):
    """
    Custom option input to only allow integer input.
    """
    def set(self, value):
        if value and not validators.integer_validator(value):
            logging.error('[%s] Trying to set a value that is not an INTEGER : %s', self.name, value)
            notify_confirm('Value entered is not a valid INTEGER', title=f'{self.name} validation error')

            return True

        self.value = value
        self.when_set()

        return False

class InputFloat(InputValidator, OptionFreeText):
    """
    Custom option input to only allow floating point input.
    """
    def set(self, value):
        if value and not validators.float_validator(value):
            logging.error('[%s] Trying to set a value that is not a FLOAT : %s', self.name, value)
            notify_confirm('Value entered is not a valid FLOAT', title=f'{self.name} validation error')

            # Returning `True` here allows to keep the editing form alive and prevent invalid input to be accepted
            return True

        self.value = value
        self.when_set()

        return False

class InputBool(InputGeneric, OptionBoolean):
    """
    Custom option boolean input to convert string values to bool.
    """
    def when_set(self):
        if not isinstance(self.value, bool):
            self.value = str(self.value).lower() == 'true' #pylint: disable=attribute-defined-outside-init

class InputSingleEnum(InputGeneric, OptionSingleChoice):
    """
    Wrapper for `OptionSingleChoice` to use `InputGeneric`.
    """

class InputEnum(InputGeneric, OptionSingleChoice):
    """
    Custom option single choice input to allow selecting enum values (or none).
    """
    WIDGET_TO_USE = EnumTitleSelectOneOrNone

class InputFile(InputGeneric, OptionFilename):
    """
    Wrapper for `OptionFilename` to use `InputGeneric`.
    """

class InputString(InputGeneric, OptionFreeText):
    """
    Custom option input for string input.

    Note that this class is empty as everything is handled by the parent `OptionFreeText`.
    It exists to allow generic input creation (see `StubConfigInputsForm.create` method).
    """

class InputMessage(InputGeneric, OptionFreeText):
    """
    Custom option input for generic `Message` object.

    Note that this class is empty as everything is handled by the parent `OptionFreeText`.
    It exists to allow generic input creation (see `StubConfigInputsForm.create` method).
    """

class InputPackage(InputValidator, OptionFilename):
    """
    Custom option input for a substream package file (.spkg).
    """
    def __init__(self, *args, parent: ActionFormV2, **kwargs):
        self.parent = ref(parent)
        super().__init__(*args, **kwargs)

    def set(self, value):
        if value and not validators.package_validator(value):
            logging.error('[%s] Trying to set a value that is not a valid package file : %s', self.name, value)
            notify_confirm('Value entered is not a valid package file', title=f'{self.name} validation error')

            return True

        self.value = value
        self.when_set()

        return False

    def when_set(self):
        try:
            output_module_option = next((w for w in self.parent().w_inputs.values if w.name == 'output_module'))

            # Update `output_module` input enum choices and value
            output_module_option.choices = \
                self.parent().get_output_module_choices(self.value)
            output_module_option.value = [next(iter(output_module_option.choices), '')]

            # Hide or unhide input option based on package url value
            self.parent().hide_input_option('output_module', self.value == '')
        except AttributeError:
            # Raised at the creation of the input form before the `InputListDisplay` is fully initialized.
            pass

class InputRepeated(InputValidator, OptionMultiFreeList):
    """
    Custom option input for repeated input fields with type validation.

    Attributes:
        value_type: The type of the repeated field.
        validate_input: A validator function used to validate input for this field (based on `value_type`).
    """
    def __init__(self, *args, value_type: str, choices: Sequence[str] | None = None, **kwargs):
        self.value_type = value_type
        # Get the appropriate type validator function based on the field type
        self.validate_input = lambda value: getattr(validators, f'{value_type.lower()}_validator')(
            value, enum_values=choices if choices else [], message_field_name=kwargs.get('name')
        )

        super().__init__(*args, multiline=True, **kwargs)

    def set(self, values): #pylint: disable=arguments-renamed
        validated_values = [self.validate_input(v) for v in values]
        if any(values) and not all(validated_values):
            logging.error('[%s] Wrong value type : expected %s got %s (values=%s)',
                self.name,
                self.value_type,
                type(values),
                values
            )

            invalid_values_message = [f'"{values[i]}" is invalid' for i in range(len(values)) if not validated_values[i]]
            notify_confirm(
                f'Values entered are not valid : expected {self.value_type} type\n'
                + '\n'.join(invalid_values_message),
                title=f'{self.name} validation error'
            )

            return True

        self.value = values
        self.when_set()

        return False
