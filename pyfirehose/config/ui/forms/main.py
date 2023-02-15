"""
SPDX-License-Identifier: MIT

Forms used by the main config TUI app to display and edit configuration files.
"""

import logging
import os
import os.path
from typing import Any

import hjson
from npyscreen import FormWithMenus
from npyscreen import notify_confirm
from pygments.lexers.data import JsonLexer

from pyfirehose.config.ui.forms.main_config_edit import MainConfigAuthProvidersForm, MainConfigEndpointsForm
from pyfirehose.config.ui.forms.generic import MarkdownEnabledHelpForm
from pyfirehose.config.ui.forms.stub_config_edit import StubConfigEndpointsForm
from pyfirehose.config.ui.widgets.custom import CodeHighlightedTitlePager, notify_yes_no

class MainForm(FormWithMenus, MarkdownEnabledHelpForm):
    """
    Main form presenting the main config file with a menu for accessing the edit functions.

    Attributes:
        next_form: The next form to be loaded after exiting the main form (`None` exits the application).
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

        if self.parentApp.has_main_config_changed():
            overwrite_confirm = notify_yes_no(
                'Overwrite main configuration file with the updated values ?',
                title=f'Changes detected for "{self.parentApp.main_config_file}"'
            )

            if not overwrite_confirm:
                self.parentApp.restore_main_config_backup()
                return

            try:
                os.makedirs(os.path.dirname(self.parentApp.main_config_file), exist_ok=True)
                with open(self.parentApp.main_config_file, 'w+', encoding='utf8') as config_file:
                    hjson.dumpJSON(self.parentApp.main_config, config_file, indent=4)

                    # Go back to start of file to reload backup config
                    config_file.seek(0)
                    self.parentApp.create_main_config_backup(config_file)
            except OSError as error:
                logging.error('Could not write out file to "%s": %s', self.parentApp.main_config_file, error)
                notify_confirm(
                    f'Could not write output file to "{self.parentApp.main_config_file}" : {error}',
                    title='Error'
                )
                return
            else:
                notify_confirm(
                    f'Main configuration file successfully saved at :\n{self.parentApp.main_config_file}',
                    title='Success'
                )

            # TODO: Figure out color display bug when updating main config file -> Colors not updated dynamically
            # Update the main configuration view text
            self.ml_main_config_view.values = hjson.dumpsJSON(self.parentApp.main_config, indent=4).splitlines()

    def create(self):
        main_menu = self.new_menu(name='Main menu')
        main_config_submenu = main_menu.addNewSubmenu(name='Edit main configuration')

        main_menu.addItem(
            text='Edit stub configuration',
            onSelect=self.switch_form,
            arguments=[self.parentApp.STUB_CONFIG_ENPOINTS_FORM, StubConfigEndpointsForm, 'Stub configuration editing - Endpoints'],
            keywords={
                'help':
                'This screen shows a list of endpoints extracted from the main configuration file.\n'
                'Each one is shown with the blockchain it is associated with as well as its URL.\n\n'
                'Select one to start editing a new stub configuration that can then be used to extract relevant data from it.'
            }
        )

        main_config_submenu.addItem(
            text='Authentication providers',
            onSelect=self.switch_form,
            arguments=[
                self.parentApp.MAIN_CONFIG_AUTH_PROVIDERS_FORM,
                MainConfigAuthProvidersForm,
                'Main configuration editing - Authentication providers'
            ],
            keywords={
                'help':
                'This screen shows a list of authentication providers extracted from the main configuration file.\n\n'
                'An authentication provider is an endpoint that can deliver authentication (JWT) tokens to communicate with the data endpoints.\n'
                'These endpoints hold a reference to one of the authentication provider listed here by referencing their ID.\n\n'
                'Therefore, the following warning must be disclosed :\n'
                '**If you delete an authentication provider, any endpoint refering to it won\'t be able to properly function.**\n\n'
                'You can always add more authentication providers by selecting the **[New]** button.\n'
                'To edit or delete an existing one, move the cursor to it and press **[ENTER]** (or **[SPACE]**) to bring an action submenu.'
            }
        )

        main_config_submenu.addItem(
            text='Endpoints',
            onSelect=self.switch_form,
            arguments=[self.parentApp.MAIN_CONFIG_ENDPOINTS_FORM, MainConfigEndpointsForm, 'Main configuration editing - Endpoints'],
            keywords={
                'help':
                'This screen shows a list of endpoints extracted from the main configuration file.\n\n'
                'An endpoint in this context is a Firehose/Substreams-enabled server with a gRPC service allowing for data queries.\n'
                'Endpoints must refer to an authentication provider in order for the application to be able to exchange data securely.\n\n'
                'A unique identifier is also necessary to be able to select it later from the command-line data extraction tool.\n'
                'Try to choose a name descriptive of the endpoint and its data. Additional information (such as the blockchain it indexes) '
                'may also be supplied.\n\n'
                'You can always add more data endpoints by selecting the **[New]** button.\n'
                'To edit or delete an existing one, move the cursor to it and press **[ENTER]** (or **[SPACE]**) to bring an action submenu.'
            }
        )

        main_menu.addItem(
            text='Return to main screen',
            onSelect=lambda: None
        )

        self.ml_main_config_view = self.add(
            CodeHighlightedTitlePager,
            name=f'Main configuration (view only) - {self.parentApp.main_config_file}',
            values=hjson.dumpsJSON(self.parentApp.main_config, indent=4).splitlines(),
            lexer=JsonLexer()
        )

    def switch_form(self, form: str, form_class: Any, form_display_name: str, **kwargs) -> None:
        """
        Helper function to set the next appropriate form when using the menu.

        Args:
            form: The form name identifier.
            form_class: The form class.
            form_display_name: The `name` attribute of the form that will be displayed at the top of the screen.
            kwargs: Additional keywords arguments for the created form.
        """
        self.next_form = form #pylint: disable=attribute-defined-outside-init
        self.parentApp.addForm(form, form_class, name=form_display_name, **kwargs)
        self.parentApp.switchForm(form)
