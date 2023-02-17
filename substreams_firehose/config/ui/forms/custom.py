"""
SPDX-License-Identifier: MIT

Custom forms built on the [`npyscreen`](https://npyscreen.readthedocs.io) library.
"""

from collections.abc import Callable

from npyscreen import FormBaseNew, MiniButtonPress

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
        lines: int = 8,
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
