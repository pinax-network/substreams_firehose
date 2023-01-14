"""
SPDX-License-Identifier: MIT

Widgets used by forms to display and edit configuration files.
"""

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
    """
    _contained_widgets = CodeHighlightedTextfield

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
