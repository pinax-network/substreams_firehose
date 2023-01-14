"""
SPDX-License-Identifier: MIT

Widgets used by forms to display and edit configuration files.
"""

import logging
from typing import Optional

import curses
from pygments import highlight
from pygments.formatters import TerminalFormatter #pylint: disable=no-name-in-module
from npyscreen import Pager, SelectOne, Textfield, TitlePager, TitleSelectOne

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

    It can syntax highlight any language currently supported by the `pygments` library by passing the appropriate
    [lexer](https://pygments.org/docs/lexers/#) to the constructor.
    """
    _contained_widgets = CodeHighlightedTextfield

    def __init__(self, *args, lexer=None, **kwargs):
        super().__init__(*args, **kwargs)

        text = '\n'.join(self.values)
        highlighted_text_split = highlight(text, lexer, TerminalFormatter()).split('\n')

        self.parent.stored_highlights = {}
        for i in range(len(highlighted_text_split) - 1):
            self.parent.stored_highlights[self.values[i]] = [
                c for (color, length) in colorize(
                    self.parent.theme_manager.findPair(self, 'DEFAULT'),
                    highlighted_text_split[i]
                ) for c in [color] * length
            ]

class CodeHighlightedTitlePager(TitlePager):
    """
    Titled version of the `CodeHighlightedPager` widget.

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
    Title version of the `EndpointsSelectOne` widget.

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
    for reference.
    """
    _entry_type = EndpointsSelectOne

class EnumSelectOneOrNone(SelectOne):
    """
    Custom single selection widget to allow selecting one or none of the available values.

    Used by the `InputEnum` option widget.
    """
    def h_select(self, ch):
        if self.cursor_line in self.value:
            self.value = None
        else:
            self.value = [self.cursor_line,]

class EnumTitleSelectOneOrNone(TitleSelectOne):
    """
    Title version of the `EnumSelectOneOrNone` widget.

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
    for reference.
    """
    _entry_type = EnumSelectOneOrNone

def colorize(default_color: int, string: str) -> list[tuple[int, int]]:
    """
    Convert a string containg ANSI escape codes to `curses` control characters for color display.

    Adapted from Cansi library (https://github.com/tslight/cansi). Some of the original comments kept in the code.

    Args:
        default_color: passed to the `mkcolors` function (see documentation for reference).
        string: a string containing ANSI escape codes for color.

    Returns:
        A list of pairs of `curses`' control character and their applicable length.

    Example:
        `[(2097152, 10)]` will color 10 characters bold (`curses.A_BOLD = 2097152`).
    """

    def _mkcolor(default_color: int, offset: Optional[int] = 49) -> dict[str, int]:
        """
        Initialize `curses` colors and mapping of ANSI escape codes.

        Adapted from Cansi library (https://github.com/tslight/cansi). Original comments kept in code.

        See [Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters)
        for ANSI escape codes reference.

        Args:
            default_color: color pair used for the default background and foreground ANSI escape codes (`39;49;00`).
            offset: offset for the `curses.init_pair` function to avoid overwriting predefined colors of `npyscreen`'s theme.

        Returns:
            A dictionary mapping of ANSI escape sequences to `curses`' control characters.
        """
        color = {}

        curses.use_default_colors()  # https://stackoverflow.com/a/44015131
        for i in range(1, 8):
            curses.init_pair(i + offset, i, -1)  # color fg on black bg
            curses.init_pair(i + offset + 7, curses.COLOR_WHITE, i)  # white fg on color bg
            curses.init_pair(i + offset + 14, curses.COLOR_BLACK, i)  # black fg on color bg
            color[str(i + 30)] = curses.color_pair(i + offset)
            color[str(i + 40)] = curses.color_pair(i + offset + 7)
            color["0;" + str(i + 30)] = curses.color_pair(i + offset)
            color["0;" + str(i + 40)] = curses.color_pair(i + offset + 7)
            color[str(i + 30) + ";0"] = curses.color_pair(i + offset)
            color[str(i + 40) + ";0"] = curses.color_pair(i + offset + 7)
            color[str(i + 90)] = curses.color_pair(i + offset) | curses.A_BOLD
            color["1;" + str(i + 30)] = curses.color_pair(i + offset) | curses.A_BOLD
            color["1;" + str(i + 40)] = curses.color_pair(i + offset + 7) | curses.A_BOLD
            color[str(i + 30) + ";1"] = curses.color_pair(i + offset) | curses.A_BOLD
            color[str(i + 40) + ";1"] = curses.color_pair(i + offset + 7) | curses.A_BOLD

            color["39;49;00"] = default_color

        return color

    ansi_split = string.split("\x1b[")
    color_pair = curses.color_pair(0)

    color = _mkcolor(default_color)
    attr = {
        "1": curses.A_BOLD,
        "4": curses.A_UNDERLINE,
        "5": curses.A_BLINK,
        "7": curses.A_REVERSE,
    }
    colors = []

    for substring in ansi_split[1:]:
        if substring.startswith("0K"):
            return colors # 0K = clrtoeol so we are done with this line

        ansi_code = substring.split("m")[0]
        substring = substring[len(ansi_code) + 1 :]
        if ansi_code in ["1", "4", "5", "7", "8"]:
            color_pair = color_pair | attr[ansi_code]
        elif ansi_code not in ["0", "0;"]:
            color_pair = color[ansi_code]

        if substring:
            colors.append((color_pair, len(substring)))

    return colors
