"""
SPDX-License-Identifier: MIT

Custom widgets built on the `npyscreen` library and used by forms to display and edit configuration files.
"""

import re
from collections.abc import MutableMapping

import curses
from npyscreen import BoxTitle, Form, MultiLineAction, Pager, SelectOne, Textfield, TitlePager, TitleSelectOne
from npyscreen import MLTreeMultiSelectAnnotated, TreeData, TreeLineSelectableAnnotated
from npyscreen.fmPopup import ActionPopupWide
from npyscreen.utilNotify import YesNoPopup, _prepare_message, _wrap_message_lines
from pygments import highlight
from pygments.formatters import Terminal256Formatter #pylint: disable=no-name-in-module
from pygments.lexer import RegexLexer
from pygments.lexers.markup import MarkdownLexer
from pygments.style import Style

from substreams_firehose.config.ui.forms.custom import ActionButtonPopup

def colorize_256(text: str, default_color: int = 0) -> list[tuple[int, int]]:
    """
    Parses a string containing ANSI code escape sequences for `curses` display.

    The ANSI code supported are the ones defined for the 256 color palette (see [here](
        https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#256-colors
    ) for reference). Attributes such as bold, italic, etc. are also supported except for the strikethrough attribute.

    Background colors currently don't work.

    This is used internally by the `CodeHighlightedPager` for coloring text.

    Args:
        text: The text to colorize.
        default_color: A default color for the *reset* escape sequences.

    Returns:
        A list of tuples containing the `curses` attribute value and the number of character for which it applies.
    """
    # Create the color map only once
    if not hasattr(colorize_256, 'color_map'):
        curses.use_default_colors()

        colorize_256.color_map = {
            '39': default_color,
            '49': default_color,
            '39;49': default_color
        }

        # TODO: Figure out how to make backgrounds work
        for i in range(curses.COLORS):
            for j in range(curses.COLORS):
                curses.init_pair(i + j * curses.COLORS + 1, i, j - 1)
                colorize_256.color_map[f'38;5;{i};48;5;{j}'] = curses.color_pair(i + j * curses.COLORS + 1)
            colorize_256.color_map[f'38;5;{i}'] = curses.color_pair(i + 1)
            colorize_256.color_map[f'48;5;{i}'] = curses.color_pair(i * curses.COLORS + 1)

    # No escape code detected at all so print all text with the default color
    if not '\x1b[' in text:
        return [(default_color, len(text))]

    colors = []
    # See https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#colors--graphics-mode for reference
    attr = {
        "00": curses.A_NORMAL,
        "01": curses.A_BOLD,
        "02": curses.A_DIM,
        "03": curses.A_ITALIC,
        "04": curses.A_UNDERLINE,
        "05": curses.A_BLINK,
        "07": curses.A_REVERSE,
        "08": curses.A_INVIS,
        # `ESC[9m` strikethrough is not available in Python curses (see https://docs.python.org/3/library/curses.html#curses.ncurses_version)
        "09": curses.A_NORMAL
    }

    for substring in [sub for sub in text.split('\x1b[') if sub]:
        try:
            ansi_code, substring_text = substring.split('m', 1)
        except ValueError:
            # No ANSI code detected
            colors.append((default_color, len(substring)))
            continue

        text_attribute = 0

        # Validate ANSI code format or else its just plain text that happens to have an 'm' in it.
        if not all(code.isdigit() for code in ansi_code.split(';')):
            colors.append((default_color, len(substring_text)))
            continue

        codes = ansi_code.split(';')
        ansi_code = ''

        # Parses special attributes (bold, etc.) from the highlighted text and create a new ANSI code, keeping only the color attributes
        for code in codes:
            try:
                text_attribute |= attr[code]
            except KeyError:
                ansi_code += (f'{code};')
        ansi_code = ansi_code.rstrip(';')

        if ansi_code:
            colors.append((colorize_256.color_map[ansi_code] | text_attribute, len(substring_text)))
        else:
            colors.append((text_attribute, len(substring_text)))

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

    def __init__(self, *args, lexer: RegexLexer, style: str | Style = 'github-dark', **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: Move highlighting logic to separate function for dynamic update + add style chooser along side main menu
        # TODO: Sanitize text for escaping ANSI code in it ?
        text = self._wrap_message_lines(list(self.values), self.width - 1)
        # Removes the markdown markups from the output text
        if isinstance(lexer, MarkdownLexer):
            self.values = [self.unmark_markdown(t) for t in text]

        # TODO: Check color support for TrueColor, 256, or 16 (hint: `curses.has_extended_color_support` for TrueColor)
        highlighted_text_split = highlight('\n'.join(text), lexer, Terminal256Formatter(style=style)).splitlines()

        self.parent.stored_highlights = {}
        for i in range(len(highlighted_text_split)):
            self.parent.stored_highlights[self.values[i]] = [
                c for color, length in colorize_256( # TODO: Extend the function to work with all modes described above
                    self.unmark_markdown(highlighted_text_split[i]) if isinstance(lexer, MarkdownLexer) else highlighted_text_split[i],
                    self.parent.theme_manager.findPair(self, 'DEFAULT')
                ) for c in [color] * length
            ]

    def unmark_markdown(self, text: str) -> str:
        """
        Removes the **bold**, _italics_ and `code` markups from the input text.

        Args:
            text: The text to parse.

        Returns:
            The text stripped of the markup symbols.
        """
        return re.sub(r'((\*\*|__)|(\*|_)|(\`))(.*?)\1', r'\5', text)

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
                'Delete': lambda: _remove_item(act_on_this), # TODO: Move hook to parent ?
                'Cancel': lambda: None
            },
            name=action_popup_name,
            show_at_x=self.relx,
            show_at_y=self.rely + self.cursor_line,
            columns=len(action_popup_name) + 6
        )

        action_popup.edit()

    def display_value(self, vl: MutableMapping):
        try:
            return f'{vl[self.parent.identifier_key]}'
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

def view_help(message: str, title: str = "Message", form_color: str = "STANDOUT", scroll_exit: bool = True, autowrap: bool = False) -> None:
    """
    Reimplement the `view_help` method from `npyscreen` library to add markdown support using the `CodeHighlightedPager`.

    Args:
        message: The content of the help message.
        title: The title of the help message box.
        form_color: The default color for text in the form. See [`npyscreen` documentation](https://npyscreen.readthedocs.io/color.html)
        for the available values.
        scroll_exit: A boolean indicating if scrolling past the end of the help message exits the widget.
        autowrap: A boolean indicating if the message text should autowrap.
    """
    help_form = Form(name=title, color=form_color)
    markdown_pager = help_form.add(
        CodeHighlightedPager,
        values=message.splitlines(),
        lexer=MarkdownLexer(),
        scroll_exit=scroll_exit,
        autowrap=autowrap
    )
    help_form.edit()

    del markdown_pager
    del help_form
