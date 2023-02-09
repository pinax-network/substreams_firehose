"""
SPDX-License-Identifier: MIT

Generic forms used as base class for other widget-holding forms.
"""

from collections.abc import Callable

from npyscreen import ActionFormV2, FormBaseNew, MiniButtonPress, SplitForm

class ActionButtonPopup(FormBaseNew):
    """
    Custom popup displaying a list of buttons to interact with.

    Passing a dictionary to the constructor will setup the buttons' name and callback functions.
    """
    def __init__(self,
        buttons: dict[str, Callable],
        *args,
        show_at_x: int = 10,
        show_at_y: int = 2,
        lines: int = 6,
        columns: int = 32,
        **kwargs
    ):
        self._buttons = buttons
        self.__class__.SHOW_ATX = show_at_x
        self.__class__.SHOW_ATY = show_at_y
        self.__class__.DEFAULT_LINES = lines
        self.__class__.DEFAULT_COLUMNS = columns

        super().__init__(*args, **kwargs)

    def _when_pressed_wrapper(self, callback: Callable) -> None:
        """
        Internal function to call the button callback function and exit the form afterwards.

        Args:
            callback: The button callback.
        """
        callback()
        self.editing = False

    def create(self):
        for button_name, button_callback in self._buttons.items():
            _b = self.add(MiniButtonPress, name=button_name)
            _b.whenPressed = lambda f=button_callback: self._when_pressed_wrapper(f)

class ActionFormDiscard(ActionFormV2):
    """
    Generic class for an action form with an additional *Discard* button.

    Overload the `on_discard` method to customize its behavior.
    """
    class Discard_Button(MiniButtonPress): #pylint: disable=invalid-name
        """
        Additional *Discard* button (name style chosen to match the `npyscreen` library).
        """
        def whenPressed(self):
            self.parent._on_discard() #pylint: disable=protected-access

    DISCARDBUTTON_TYPE = Discard_Button
    DISCARD_BUTTON_BR_OFFSET = (
        ActionFormV2.CANCEL_BUTTON_BR_OFFSET[0],
        ActionFormV2.OK_BUTTON_BR_OFFSET[1]
        + len(ActionFormV2.OK_BUTTON_TEXT)
        + ActionFormV2.CANCEL_BUTTON_BR_OFFSET[1]
        + len(ActionFormV2.CANCEL_BUTTON_TEXT)
    )
    DISCARD_BUTTON_TEXT = 'Discard'

    def _on_discard(self):
        self.editing = self.on_discard()

    def create_control_buttons(self):
        self._add_button('ok_button',
            self.__class__.OKBUTTON_TYPE,
            self.__class__.OK_BUTTON_TEXT,
            0 - self.__class__.OK_BUTTON_BR_OFFSET[0],
            0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(self.__class__.OK_BUTTON_TEXT),
            None
        )

        self._add_button('cancel_button',
            self.__class__.CANCELBUTTON_TYPE,
            self.__class__.CANCEL_BUTTON_TEXT,
            0 - self.__class__.CANCEL_BUTTON_BR_OFFSET[0],
            0 - self.__class__.CANCEL_BUTTON_BR_OFFSET[1] - len(self.__class__.CANCEL_BUTTON_TEXT),
            None
        )

        self._add_button('discard_button',
            self.__class__.DISCARDBUTTON_TYPE,
            self.__class__.DISCARD_BUTTON_TEXT,
            0 - self.__class__.DISCARD_BUTTON_BR_OFFSET[0],
            0 - self.__class__.DISCARD_BUTTON_BR_OFFSET[1] - len(self.__class__.DISCARD_BUTTON_TEXT),
            None
        )

    def on_discard(self):
        """
        *Discard* button hook to overload for customizing the behavior of the button.
        """
        return False

class SplitActionForm(ActionFormV2, SplitForm): #pylint: disable=too-many-ancestors
    """
    Combine `ActionFormV2` buttons with `SplitForm` horizontal line display.
    """
    def get_half_way(self, draw_line_at: int | None = None) -> int:
        if not hasattr(self, 'draw_line_at'):
            self.draw_line_at = draw_line_at if draw_line_at else self.curses_pad.getmaxyx()[0] // 2

        return self.draw_line_at
