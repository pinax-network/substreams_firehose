"""
SPDX-License-Identifier: MIT
"""

import logging
from types import MethodType

from npyscreen import Pager, SelectOne, Textfield, TitlePager, TitleSelectOne
from npyscreen import OptionBoolean, OptionFreeText, OptionListDisplay
from npyscreen import notify_confirm

class CodeHighlightedTextfield(Textfield):
    def __init__(self, *args, **kwargs):
        super(CodeHighlightedTextfield, self).__init__(*args, **kwargs)
        self.syntax_highlighting = True

    def update_highlighting(self, start, end):
        substr = self._get_string_to_print()
        if not substr in self.parent.stored_highlights:
            return

        self._highlightingdata = self.parent.stored_highlights[substr]

class CodeHighlightedPager(Pager):
    _contained_widgets = CodeHighlightedTextfield

class CodeHighlightedTitlePager(TitlePager):
    _entry_type = CodeHighlightedPager

class EndpointsSelectOne(SelectOne):
    def display_value(self, vl: dict):
        try:
            return f'{vl["chain"]} ({vl["url"]})'
        except KeyError:
            return str(vl)

class EndpointsTitleSelectOne(TitleSelectOne):
    _entry_type = EndpointsSelectOne

class InputsListDisplay(OptionListDisplay):
    def __init__(self, *args, **kwargs):
        super(InputsListDisplay, self).__init__(*args, **kwargs)
        self._contained_widgets.ANNOTATE_WIDTH = 50

class InputBoolean(OptionBoolean):
    def when_set(self):
        if not isinstance(self.value, bool):
            self.value = str(self.value).lower() == 'true'

class InputFloat(OptionFreeText):
    def set(self, value):
        if value:
            try:
                float(value)
            except ValueError:
                logging.error('[%s] Trying to set a value that is not a FLOAT : %s', self.name, value)
                notify_confirm('Value entered is not a valid FLOAT', title=f'{self.name} validation error')

                return True

        self.value = value
        self.when_set()

        return False

    def set_from_widget_value(self, vl):
        """
        Method override allowing to quit or continue the option editing depending on the return value.

        See `on_ok_input_validation_hook`.
        """
        return self.set(vl)

    def _set_up_widget_values(self, option_form, main_option_widget):
        """
        Method override to replace the option form `on_ok` event handler with our own hook.

        See `on_ok_input_validation_hook`.
        """
        main_option_widget.value = self.value
        option_form.on_ok = MethodType(on_ok_input_validation_hook, option_form)

class InputInteger(OptionFreeText):
    def set(self, value):
        if value:
            try:
                int(value)
            except ValueError:
                logging.error('[%s] Trying to set a value that is not an INTEGER : %s', self.name, value)
                notify_confirm('Value entered is not a valid INTEGER', title=f'{self.name} validation error')

                # Returning `True` here allows to keep the editing form alive and prevent invalid input to be accepted
                return True

        self.value = value
        self.when_set()

        return False

    def set_from_widget_value(self, vl):
        """
        Method override allowing to quit or continue the option editing depending on the return value.

        See `on_ok_input_validation_hook`.
        """
        return self.set(vl)

    def _set_up_widget_values(self, option_form, main_option_widget):
        """
        Method override to replace the option form `on_ok` event handler with our own hook.

        See `on_ok_input_validation_hook`.
        """
        main_option_widget.value = self.value
        option_form.on_ok = MethodType(on_ok_input_validation_hook, option_form)

def on_ok_input_validation_hook(self,):
    """
    Hook to replace the `on_ok` event handler for validating an option input.

    It returns the value of the `Option.set` function to continue or stop the editing.
    Used to prevent entering invalid input for options.
    """
    return self.OPTION_TO_CHANGE.set_from_widget_value(self.OPTION_WIDGET.value)
