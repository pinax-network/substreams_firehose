"""
SPDX-License-Identifier: MIT

Custom widgets built on the `npyscreen` library and used by forms to display and edit configuration files.

--- Cansi library (https://github.com/tslight/cansi) ---
Copyright (c) 2018, Toby Slight
All rights reserved.

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.
--- Cansi library (https://github.com/tslight/cansi) ---
"""

from collections.abc import MutableMapping

import curses
from npyscreen import BoxTitle, MultiLineAction, Pager, SelectOne, Textfield, TitlePager, TitleSelectOne
from npyscreen import MLTreeMultiSelectAnnotated, TreeData, TreeLineSelectableAnnotated
from npyscreen.fmPopup import ActionPopupWide
from npyscreen.utilNotify import YesNoPopup, _prepare_message, _wrap_message_lines
from pygments import highlight
from pygments.formatters import TerminalFormatter #pylint: disable=no-name-in-module
from pygments.lexer import RegexLexer

from pyfirehose.config.ui.forms.custom import ActionButtonPopup

def colorize(default_color: int, string: str) -> list[tuple[int, int]]:
    """
    Convert a string containg ANSI escape codes to `curses` control characters for color display.

    Used by the `CodeHighlightedPager` to syntax highlight its content.

    Code is adapted from Cansi library (https://github.com/tslight/cansi). Some of the original comments kept in the code.

    Args:
        default_color: See `_mkcolor()` documentation for reference.
        string: A string containing ANSI escape codes.

    Returns:
        A list of pairs of `curses`' control character and their applicable length.

    Example:
        `[(2097152, 10)]` will color 10 characters bold (`curses.A_BOLD = 2097152`).
    """

    def _mkcolor(default_color: int, offset: int = 49) -> dict[str, int]:
        """
        Initialize `curses` colors and mapping of ANSI escape codes.

        Adapted from Cansi library (https://github.com/tslight/cansi). Original comments kept in code.

        See [Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters)
        for ANSI escape codes reference.

        Args:
            default_color: A `curses` color pair index used for the default background and foreground ANSI escape codes (`39;49;00`).
            offset: An offset for the `curses.init_pair` function to avoid overwriting predefined colors of `npyscreen`'s theme.

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

class CodeHighlightedTextfield(Textfield):
    """
    Syntax highlight enabled [`Textfield`](https://npyscreen.readthedocs.io/widgets-text.html#widgets-displaying-text)
    for displaying JSON config files.

    Attributes:
        _highlightingdata: A list specifying special control characters for curses to display colors (created from the `colorize()` method).
        syntax_highlighting: A boolean enabling syntax highlight, telling npyscreen to call the `update_highlight` method on redraw.
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

    def __init__(self, *args, lexer: RegexLexer, **kwargs):
        super().__init__(*args, **kwargs)

        text = '\n'.join(self.values)
        highlighted_text_split = highlight(text, lexer, TerminalFormatter()).split('\n')

        self.parent.stored_highlights = {}
        for i in range(len(highlighted_text_split) - 1):
            self.parent.stored_highlights[self.values[i]] = [
                c for color, length in colorize(
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

class ItemEditMultiLineAction(MultiLineAction):
    """
    Custom multiline display popping up a menu on selection for editing or deleting an item.

    Used by the `CategorizedItemViewerBoxTitle` widget.
    """
    def actionHighlighted(self, act_on_this, key_press):
        def _remove_item(item: MutableMapping):
            if notify_yes_no(f'Confirm deletion of "{self.display_value(item)}" entry ?', title='Warning'):
                del self.values[self.cursor_line]
                self.display()

        action_popup_name = f'Choose an action for "{self.display_value(act_on_this)}"'
        action_popup = ActionButtonPopup(
            buttons={
                'Edit': lambda: self.parent.create_item_edit_form(act_on_this),
                'Delete': lambda: _remove_item(act_on_this) # TODO: Move hook to parent ?
            },
            name=action_popup_name,
            show_at_x=self.relx,
            show_at_y=self.rely + self.cursor_line,
            columns=len(action_popup_name) + 6
        )

        action_popup.edit()

    def display_value(self, vl: MutableMapping):
        try:
            return f'{vl["id"]}' # TODO: How to specifiy the id key ?
        except KeyError:
            return str(vl)

class CategorizedItemViewerBoxTitle(BoxTitle):
    """
    Custom `BoxTitle` for displaying categorized item values.
    """
    _contained_widget = ItemEditMultiLineAction

class EndpointsSelectOne(SelectOne):
    """
    Custom single selection widget to display the main config's endpoint data.

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-multiline.html#widgets-picking-options)
    for reference.
    """
    def display_value(self, vl: dict):
        try:
            return f'{vl.get("chain", "<UNKNOWN CHAIN>")} ({vl["url"]})'
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

class OutputSelectionTreeData(TreeData):
    """
    A `TreeData` node representing an output field from a `Message` output type.

    Attributes:
        annotate: The text annotation to display next to the node content.
        annotate_color: The color of the text annotation (see the [documentation](
            https://npyscreen.readthedocs.io/color.html
        ) for a list of valid values).
    """
    def __init__(self, *args, annotate: str = '?', annotate_color: str = 'CONTROL', **kwargs):
        super().__init__(*args, **kwargs)
        self.annotate = f' {annotate} '
        self.annotate_color = annotate_color

class OutputSelectionTreeLineSelectableAnnotated(TreeLineSelectableAnnotated):
    """
    Custom tree line selectable widget implementing the annotation behavior.
    """
    def getAnnotationAndColor(self):
        return (self._tree_real_value.annotate, self._tree_real_value.annotate_color)

class OutputSelectionMLTreeMultiSelectAnnotated(MLTreeMultiSelectAnnotated):
    """
    Custom multi-selection tree widget using `OutputSelectionTreeLineSelectableAnnotated` as line display.
    """
    _contained_widgets = OutputSelectionTreeLineSelectableAnnotated

class OutputTypesSelectOne(SelectOne, MultiLineAction):
    """
    Custom single selection widget to display gRPC output types and link them to the output field selection widget.

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-multiline.html#widgets-picking-options)
    for reference.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent.saved_output_selection = {}

    def actionHighlighted(self, act_on_this, key_press):
        # Save the current output fields selection state
        self.parent.saved_output_selection[self.values[self.value[0]]] = {
            (node.find_depth(), node.get_content()): (node.selected, node.expanded)
            for node in self.parent.ml_output_select.values[0].walk_tree()
        }

        # Update the output field selection based on the saved `TreeData` properties if they exists
        self.value = [self.cursor_line]
        try:
            saved_data = self.parent.saved_output_selection[self.values[self.value[0]]]
        except KeyError:
            saved_data = None

        self.parent.ml_output_select.values = self.parent.create_output_selection(previous_selected=saved_data)
        self.parent.display()

class OutputTypesTitleSelectOne(TitleSelectOne):
    """
    Title version of the `OutputTypesSelectOne` widget.

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/widgets-title.html#widgets-titled-widgets)
    for reference.
    """
    _entry_type = OutputTypesSelectOne

class YesNoPopupWide(ActionPopupWide):
    """
    Custom YES/NO popup class with wide display.

    Used to emulate the same behavior as other [`notify` functions](
        https://github.com/npcole/npyscreen/blob/8ce31204e1de1fbd2939ffe2d8c3b3120e93a4d0/npyscreen/utilNotify.py#L46
    ) from the `npyscreen` library, supporting wide display for YES/NO popups as well.
    """
    OK_BUTTON_TEXT = "Yes"
    CANCEL_BUTTON_TEXT = "No"
    DEFAULT_LINES = 16

    def on_ok(self):
        self.value = True #pylint: disable=attribute-defined-outside-init

    def on_cancel(self):
        self.value = False #pylint: disable=attribute-defined-outside-init

def notify_yes_no(
    message: str,
    title: str = 'Message',
    form_color: str = 'STANDOUT',
    wrap: bool = True,
    wide: bool = False
) -> bool:
    """
    Display a YES/NO popup prompting for a choice.

    Adapted from the [`npyscreen` library](
        https://github.com/npcole/npyscreen/blob/8ce31204e1de1fbd2939ffe2d8c3b3120e93a4d0/npyscreen/utilNotify.py#L83
    ) to support wide popup display (see `YesNoPopupWide`).

    Args:
        message: The text content of the popup.
        title: The title of the popup window.
        form_color: The color of the popup content text (see https://npyscreen.readthedocs.io/color.html).
        wrap: If true, wrap the text content to the window border.
        wide: If true, use the wide display version of the popup.

    Returns:
        A boolean indicating the choice of the user (`YES = True`).
    """
    message = _prepare_message(message)
    if wide:
        popup_form = YesNoPopupWide(name=title, color=form_color)
    else:
        popup_form = YesNoPopup(name=title, color=form_color)
    popup_form.preserve_selected_widget = True

    mlw = popup_form.add(Pager)
    if wrap:
        message = _wrap_message_lines(message, mlw.width - 1)
    mlw.values = message

    popup_form.editw = 0 #pylint: disable=attribute-defined-outside-init
    popup_form.edit()

    return popup_form.value
