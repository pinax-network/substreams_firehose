"""
SPDX-License-Identifier: MIT

Main app for the config TUI application.
"""

import logging
from copy import deepcopy
from typing import BinaryIO, TextIO

import hjson
from npyscreen import NPSAppManaged
from npyscreen import notify_confirm, selectFile, setTheme
from npyscreen.npysThemes import DefaultTheme

from substreams_firehose.utils import open_file_from_package
from substreams_firehose.config.ui.forms.main import MainForm

class ConfigApp(NPSAppManaged):
    """
    Main app containing the forms for the config TUI.

    It acts as a medium of communication for getting value between forms, storing data as instance attributes \
    (via the `self.parentApp` variable available in child forms).

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/application-objects.html#in-detail) for reference.

    Attributes:
        display_main_popup: A string that the main form displays as an information message when created, if not empty.
        main_config: A dictionary representing the loaded main configuration file.
        main_config: A dictionary representing the loaded main configuration file at the start of the session.
        main_config_file: The filepath to the main configuration file.
    """
    # TODO: Load names, titles, help messages for each form through external resource file (YAML ?) ?

    # Generic editing forms
    CATEGORIZED_ITEM_EDIT_FORM = 'CATEGORIZED_ITEM_EDIT_FORM'

    # Main configuration editing forms
    MAIN_CONFIG_AUTH_PROVIDERS_FORM = 'MAIN_CONFIG_AUTH_PROVIDERS_FORM'
    MAIN_CONFIG_ENDPOINTS_FORM = 'MAIN_CONFIG_ENDPOINTS_FORM'
    MAIN_CONFIG_ENDPOINT_EDIT_FORM = 'MAIN_CONFIG_ENDPOINT_EDIT_FORM'

    # Stub configuration editing forms, in order of the workflow
    STUB_CONFIG_ENPOINTS_FORM = 'STUB_CONFIG_ENDPOINTS_FORM'
    STUB_CONFIG_SAVE_FILE_FORM = 'STUB_CONFIG_SAVE_FILE_FORM'
    STUB_CONFIG_SERVICES_FORM = 'STUB_CONFIG_SERVICES_FORM'
    STUB_CONFIG_METHODS_FORM = 'STUB_CONFIG_METHODS_FORM'
    STUB_CONFIG_INPUTS_FORM = 'STUB_CONFIG_INPUTS_FORM'
    STUB_CONFIG_OUTPUTS_FORM = 'STUB_CONFIG_OUTPUTS_FORM'
    STUB_CONFIG_CONFIRM_EDIT_FORM = 'STUB_CONFIG_CONFIRM_EDIT_FORM'

    def __init__(self):
        super().__init__()

        self.display_main_popup = None
        self.main_config = None
        self.main_config_backup = None
        # TODO: Allow changing the default path of the main config file -> CLI argument
        self.main_config_file = 'substreams_firehose/config.hjson'

    def has_main_config_changed(self) -> bool:
        """
        Compare the version of the main configuration file at the start of the session to the one currently on display.

        Returns:
            A boolean indicating if changes where made (field order ignored).
        """
        return self.main_config != self.main_config_backup

    def create_main_config_backup(self, config_file: BinaryIO | TextIO) -> None:
        """
        Loads the main configuration from the `config_file` as a backup.

        Args:
            config_file: A file descriptor of the main configuration file.
        """
        self.main_config_backup = hjson.load(config_file, object_pairs_hook=dict)

    def restore_main_config_backup(self) -> None:
        """
        Replace the main configuration file used for display with the one saved as a backup.
        """
        self.main_config = deepcopy(self.main_config_backup)

    def onStart(self):
        setTheme(DefaultTheme)

        while not self.main_config:
            try:
                with open_file_from_package(self.main_config_file) as config_file:
                    try:
                        # Using `dict` instead of default `OrderedDict` as order of fields doesn't matter in the config
                        self.main_config = hjson.load(config_file, object_pairs_hook=dict)

                        # Go back to start of file to also load backup config
                        config_file.seek(0)
                        self.create_main_config_backup(config_file)
                    except hjson.HjsonDecodeError as error:
                        logging.exception('Error decoding main config file (%s): %s', self.main_config_file, error)
                        raise
            except (FileNotFoundError, IsADirectoryError):
                notify_confirm(
                    f'Main configuration file not found at default location "{self.main_config_file}".\n'
                    f'Please select a valid configuration file.',
                    title="Warning: file not found",
                    editw=1
                )
                self.main_config_file = selectFile(must_exist=True, confirm_if_exists=False)

        self.addForm('MAIN', MainForm, name='Configuration editor', help=
            'CONTROLS\n'
            '========\n'
            'Press **[TAB]** to focus the next widget, **[SHIFT+TAB]** to go to the previous one.\n\n'
            'Most widgets displaying lists also allows to focus the next or previous one by scrolling all the way to the bottom or top.\n'
            'They also allow for filtering the displayed values using **[l]** to popup a filter input.\n'
            'Press **[n]** (next) and **[N]** or **[p]** (previous) to cycle through the results. **[L]** will clear the highlighted results from '
            'the display.\n\n'
            'Standard VI-like bindings also applies for navigating the application :\n'
            '**[j]** (up) and **[k]** (down), **[h]** (left) and **[l]** (right) and **[g]** (start) and **[G]** (end).\n\n'
            '*Shortcuts* may be displayed at the bottom left or the top right of the screen, with the \'^\' character standing for the '
            '**[CTRL]** key.\n'
            'So, for example, you can press **[CTRL+X]** to bring up the main menu on the starting screen.\n\n'
        )
