"""
SPDX-License-Identifier: MIT

Widgets used by forms to display and edit configuration files.
"""

import logging
from types import MethodType
from typing import Optional, Sequence

from google.protobuf.descriptor import FieldDescriptor

from npyscreen import Pager, SelectOne, Textfield, TitlePager, TitleSelectOne
from npyscreen import OptionBoolean, OptionFreeText, OptionListDisplay, OptionMultiFreeList, OptionSingleChoice
from npyscreen import notify_confirm
from npyscreen.apOptions import Option

class CodeHighlightedTextfield(Textfield):
    """
    Syntax highlight enabled [`Textfield`](https://npyscreen.readthedocs.io/widgets-text.html#widgets-displaying-text)
    for displaying JSON config files.

    Attributes:
        _highlightingdata: internal array specifying special control characters for curses to display colors.
        syntax_highlighting: enable syntax highlight for npyscreen to call the `update_highlight` method on redraw.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.syntax_highlighting = True

    def update_highlighting(self, start=None, end=None, clear=False):
        """
        Called on every call to the internal `_print` function.

        See [`Textfield` implementation](
            https://github.com/npcole/npyscreen/blob/8ce31204e1de1fbd2939ffe2d8c3b3120e93a4d0/npyscreen/wgtextbox.py#L247
        ) for details
        """
        substr = self._get_string_to_print()
        if not substr in self.parent.stored_highlights:
            return

        self._highlightingdata = self.parent.stored_highlights[substr]

class CodeHighlightedPager(Pager):
    """
    Syntax highlight enabled [`Pager`](https://npyscreen.readthedocs.io/widgets-text.html#widgets-displaying-text)
    using `CodeHighlightedTextfield` as line display.
    """
    _contained_widgets = CodeHighlightedTextfield

class CodeHighlightedTitlePager(TitlePager):
    """
    Titled version of the `CodeHighlightedPager`.

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
    for reference.
    """
    _entry_type = CodeHighlightedPager

class EndpointsSelectOne(SelectOne):
    """
    Custom single selection widget to display the main config's endpoint data.

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-multiline.html#widgets-picking-options)
    for reference.
    """
    def display_value(self, vl: dict):
        try:
            return f'{vl["chain"]} ({vl["url"]})'
        except KeyError:
            return str(vl)

class EndpointsTitleSelectOne(TitleSelectOne):
    """
    Title version of the `EndpointsSelectOne`.

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
    for reference.
    """
    _entry_type = EndpointsSelectOne

class EnumSelectOneOrNone(SelectOne):
    def h_select(self, ch):
        if self.cursor_line in self.value:
            self.value = None
        else:
            self.value = [self.cursor_line,]

class EnumTitleSelectOneOrNone(TitleSelectOne):
    _entry_type = EnumSelectOneOrNone

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

class InputBoolean(OptionBoolean):
    """
    Custom option boolean input to convert string values to bool.
    """
    def when_set(self):
        if not isinstance(self.value, bool):
            self.value = str(self.value).lower() == 'true' #pylint: disable=attribute-defined-outside-init

class InputEnum(OptionSingleChoice):
    WIDGET_TO_USE = EnumTitleSelectOneOrNone

class InputFloat(InputValidator, OptionFreeText):
    """
    Custom option input to only allow floating point input.
    """
    def set(self, value):
        if value and float_validator(value):
            logging.error('[%s] Trying to set a value that is not a FLOAT : %s', self.name, value)
            notify_confirm('Value entered is not a valid FLOAT', title=f'{self.name} validation error')

            # Returning `True` here allows to keep the editing form alive and prevent invalid input to be accepted
            return True

        self.value = value
        self.when_set()

        return False

class InputInteger(InputValidator, OptionFreeText):
    """
    Custom option input to only allow integer input.
    """
    def set(self, value):
        if value and integer_validator(value):
            logging.error('[%s] Trying to set a value that is not an INTEGER : %s', self.name, value)
            notify_confirm('Value entered is not a valid INTEGER', title=f'{self.name} validation error')

            return True

        self.value = value
        self.when_set()

        return False

class InputRepeated(InputValidator, OptionMultiFreeList):
    """
    Custom option input for repeated input fields with type validation.
    """
    def __init__(self, validator, value_type: int, *args, choices: Optional[Sequence[str]] = None, **kwargs):
        self.value_type = cpptype_to_string(value_type)
        self.validate_input = lambda x: validator(x, choices) if choices else validator

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

def cpptype_to_string(cpp_type: int) -> str:
    """
    Convert a `FieldDescriptor.CPPTYPE_XXX` integer enum to its string representation.

    See [Google GRPC documentation](
        https://googleapis.dev/python/protobuf/latest/google/protobuf/descriptor.html#google.protobuf.descriptor.FieldDescriptor.CPPTYPE_BOOL
    )
    for reference.

    Args:
        cpp_type: the `CPPTYPE_XXX` enum integer.

    Returns:
        A string representation of the enum type.

    Examples:
        `CPPTYPE_BOOL` -> "BOOL"
        `CPPTYPE_MESSAGE` -> "MESSAGE"
    """
    return {
        value: key.split('_')[1] for key, value in vars(FieldDescriptor).items() if 'CPPTYPE_' in key
    }[cpp_type]

def bool_validator(value: str) -> bool:
    return value.lower() in ['true', 'false']

def float_validator(value: str) -> bool:
    try:
        float(value)
    except ValueError:
        return True

    return False

def integer_validator(value: str) -> bool:
    try:
        int(value)
    except ValueError:
        return True

    return False

def enum_validator(value: str, enum_values: Sequence[str]):
    return value in enum_values

def message_validator(value: str):
    return True

def string_validator(value: str):
    return True
