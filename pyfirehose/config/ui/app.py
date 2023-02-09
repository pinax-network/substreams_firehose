"""
SPDX-License-Identifier: MIT

Main app for the config TUI application.
"""

import logging
import os
import os.path

import hjson
from npyscreen import NPSAppManaged
from npyscreen import notify_confirm, notify_yes_no, selectFile, setTheme
from npyscreen.npysThemes import DefaultTheme

from pyfirehose.utils import open_file_from_package
from pyfirehose.config.ui.forms.main import MainForm

class ConfigApp(NPSAppManaged):
    """
    Main app containing the forms for the config TUI.

    It acts as a medium of communication for getting value between forms, storing data as instance attributes
    (via the `self.parentApp` variable available in child forms).

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/application-objects.html#in-detail)
    for reference.

    Attributes:
        display_main_popup: A string that the main form displays as an information message when created, if not empty.
        main_config: A dictionary representing the loaded main configuration file.
        main_config: A dictionary representing the loaded main configuration file at the start of the session.
        main_config_file: The filepath to the main configuration file.
    """
    # Main configuration editing forms
    MAIN_CONFIG_API_KEYS_FORM = 'MAIN_CONFIG_API_KEYS_FORM'
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
        # TODO: Allow changing the default path of the main config file
        self.main_config_file = 'pyfirehose/config.hjson'

    def has_main_config_changed(self) -> bool:
        """
        Compare the version of the main configuration file at the start of the session to the one currently on display.

        Returns:
            A boolean indicating if changes where made (field order ignored).
        """
        return self.main_config != self.main_config_backup

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
                        self.main_config_backup = hjson.load(config_file, object_pairs_hook=dict)
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

        self.addForm('MAIN', MainForm, name='PyFirehose config')

    def onCleanExit(self):
        if self.has_main_config_changed():
            overwrite_confirm = notify_yes_no(
                'Overwrite main configuration file with the updated values ?',
                title=f'Changes detected for "{self.main_config_file}"'
            )

            if not overwrite_confirm:
                return

            try:
                os.makedirs(os.path.dirname(self.main_config_file), exist_ok=True)
                with open(self.main_config_file, 'w+', encoding='utf8') as config_file:
                    hjson.dumpJSON(self.main_config, config_file, indent=4)
            except OSError as error:
                logging.error('Could not write out file to "%s": %s', self.main_config_file, error)
                notify_confirm(
                    f'Could not write output file to "{self.main_config_file}" : {error}',
                    title='Error'
                )
                return
            else:
                notify_confirm(
                    f'Main configuration file successfully saved at :\n{self.main_config_file}',
                    title='Success'
                )
