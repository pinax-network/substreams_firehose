"""
SPDX-License-Identifier: MIT

Forms used by the main config TUI app to display and edit configuration files.
"""

import hjson
from npyscreen import FormWithMenus
from npyscreen import notify_confirm
from pygments.lexers.data import JsonLexer

from pyfirehose.config.ui.widgets.custom import CodeHighlightedTitlePager

class MainForm(FormWithMenus):
    """
    Main form presenting the main config file with a menu for accessing the edit functions.

    Attributes:
        next_form: describe the next form to be loaded after exiting the main form (`None` exits the application).
        stored_highlights: dictionary containing the highlighted text content for the `CodeHighlightedTitlePager` widget.
    """
    OK_BUTTON_TEXT = 'Quit'

    def afterEditing(self): #pylint: disable=invalid-name
        """
        Called by `npyscreen` when the form is cycled out of the screen.
        """
        self.parentApp.setNextForm(self.next_form)

    def beforeEditing(self): #pylint: disable=invalid-name
        """
        Called by `npyscreen` before the form gets drawn on the screen.
        """
        self.next_form = None #pylint: disable=attribute-defined-outside-init

        if self.parentApp.display_main_popup:
            notify_confirm(self.parentApp.display_main_popup, title='Information')
            self.parentApp.display_main_popup = None

    def create(self):
        main_menu = self.new_menu(name='Main menu')
        main_config_submenu = main_menu.addNewSubmenu(name='Edit main config')

        main_menu.addItem(
            text='Edit stub config',
            onSelect=self.switch_form,
            arguments=[self.parentApp.STUB_CONFIG_ENPOINTS_FORM]
        )

        main_config_submenu.addItem(
            text='Edit API keys',
            onSelect=self.switch_form,
            arguments=[self.parentApp.MAIN_CONFIG_API_KEYS_FORM]
        )

        self.add(
            CodeHighlightedTitlePager,
            name=f'Main config (view only) - {self.parentApp.main_config_file}',
            values=hjson.dumpsJSON(self.parentApp.main_config, indent=4).split('\n'),
            lexer=JsonLexer()
        )

    def switch_form(self, form: str) -> None:
        """
        Helper function to set the next appropriate form when using the menu.

        Args:
            form: the form name.
        """
        self.next_form = form #pylint: disable=attribute-defined-outside-init
        self.parentApp.switchForm(form)
