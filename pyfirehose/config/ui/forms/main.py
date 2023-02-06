"""
SPDX-License-Identifier: MIT

Forms used by the main config TUI app to display and edit configuration files.
"""

from typing import Any

import hjson
from npyscreen import FormWithMenus
from npyscreen import notify_confirm
from pygments.lexers.data import JsonLexer

from pyfirehose.config.ui.forms.main_config_edit import MainConfigApiKeysForm
from pyfirehose.config.ui.forms.stub_config_edit import StubConfigEndpointsForm
from pyfirehose.config.ui.widgets.custom import CodeHighlightedTitlePager

class MainForm(FormWithMenus):
    """
    Main form presenting the main config file with a menu for accessing the edit functions.

    Attributes:
        next_form: The next form to be loaded after exiting the main form (`None` exits the application).
        stored_highlights: A dictionary containing the highlighted text content for the `CodeHighlightedTitlePager` widget.
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

        if self.parentApp.main_config_updated:
            self.ml_main_config_view.values = hjson.dumpsJSON(self.parentApp.main_config, indent=4).split('\n')

    def create(self):
        main_menu = self.new_menu(name='Main menu')
        main_config_submenu = main_menu.addNewSubmenu(name='Edit main config')

        main_menu.addItem(
            text='Edit stub config',
            onSelect=self.switch_form,
            arguments=[self.parentApp.STUB_CONFIG_ENPOINTS_FORM, StubConfigEndpointsForm, 'Stub config editing - Endpoints']
        )

        main_config_submenu.addItem(
            text='Edit API keys',
            onSelect=self.switch_form,
            arguments=[self.parentApp.MAIN_CONFIG_API_KEYS_FORM, MainConfigApiKeysForm, 'Main config editing - API keys']
        )

        self.ml_main_config_view = self.add(
            CodeHighlightedTitlePager,
            name=f'Main config (view only) - {self.parentApp.main_config_file}',
            values=hjson.dumpsJSON(self.parentApp.main_config, indent=4).split('\n'),
            lexer=JsonLexer()
        )

    def switch_form(self, form: str, form_class: Any, form_display_name: str) -> None:
        """
        Helper function to set the next appropriate form when using the menu.

        Args:
            form: The form name identifier.
            form_class: The form class.
            form_display_name: The `name` attribute of the form that will be displayed at the top of the screen.
        """
        self.next_form = form #pylint: disable=attribute-defined-outside-init
        self.parentApp.addForm(form, form_class, name=form_display_name)
        self.parentApp.switchForm(form)
