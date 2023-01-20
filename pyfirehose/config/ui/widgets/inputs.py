"""
SPDX-License-Identifier: MIT

`Option` widget subclasses for input validation and display.
"""

import logging
from collections.abc import Sequence
from types import MethodType

from npyscreen import OptionBoolean, OptionFreeText, OptionListDisplay, OptionMultiFreeList, OptionSingleChoice
from npyscreen import notify_confirm
from npyscreen.apOptions import Option

import pyfirehose.config.ui.widgets.input_validators as validators
from pyfirehose.config.ui.widgets.custom import EnumTitleSelectOneOrNone

class InputsListDisplay(OptionListDisplay):
    """
    Custom option list display for increased option title width.

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/options.html#options-and-option-lists)
    for reference.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._contained_widgets.ANNOTATE_WIDTH = 50

class InputValidator(Option):
    """
    Generic class for validating an option input with the return value of the `set` method.

    Overload the `set(self, value)` method and return `True` to keep editing, `False` to quit.
    """
    def __init__(self, *args, multiline=False, **kwargs):
        super().__init__(*args, **kwargs)

        self.multiline = multiline

    def set_from_widget_value(self, vl):
        """
        Method override allowing to quit or continue the option editing depending on the return value.

        See `on_ok_input_validation_hook`.
        """
        return self.set(vl.split('\n') if self.multiline else vl)

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
        if value and validators.integer_validator(value):
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
        if value and validators.float_validator(value):
            logging.error('[%s] Trying to set a value that is not a FLOAT : %s', self.name, value)
            notify_confirm('Value entered is not a valid FLOAT', title=f'{self.name} validation error')

            # Returning `True` here allows to keep the editing form alive and prevent invalid input to be accepted
            return True

        self.value = value
        self.when_set()

        return False

class InputBool(OptionBoolean):
    """
    Custom option boolean input to convert string values to bool.
    """
    def when_set(self):
        if not isinstance(self.value, bool):
            self.value = str(self.value).lower() == 'true' #pylint: disable=attribute-defined-outside-init

class InputEnum(OptionSingleChoice):
    """
    Custom option single choice input to allow selecting enum values (or none).
    """
    WIDGET_TO_USE = EnumTitleSelectOneOrNone

class InputString(OptionFreeText):
    """
    Custom option input for string input.

    Note that this class is empty as everything is handled by the parent `OptionFreeText`.
    It exists to allow generic input creation (see `StubConfigInputsForm.create` method).
    """

class InputMessage(OptionFreeText):
    """
    Custom option input for complex `Message` object input.

    Note that this class is empty as everything is handled by the parent `OptionFreeText`.
    It exists to allow generic input creation (see `StubConfigInputsForm.create` method).
    """

class InputRepeated(InputValidator, OptionMultiFreeList):
    """
    Custom option input for repeated input fields with type validation.
    """
    def __init__(self, value_type: str, *args, choices: Sequence[str] | None = None, **kwargs):
        self.value_type = value_type
        # Associate the appropriate type validator function
        self.validate_input = lambda value: getattr(validators, f'{value_type.lower()}_validator')(
            value, enum_values=choices if choices else []
        )

        super().__init__(multiline=True, *args, **kwargs)

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
