"""
SPDX-License-Identifier: MIT

Main app for the config TUI application.
"""

import logging
from importlib.resources import is_resource

import hjson
from npyscreen import NPSAppManaged
from npyscreen import notify_confirm, selectFile, setTheme
from npyscreen.npysThemes import DefaultTheme

from pyfirehose.utils import open_file_from_package
from pyfirehose.config.ui.forms.main import MainForm
from pyfirehose.config.ui.forms.stub_config_edit import StubConfigEndpointsForm

class ConfigApp(NPSAppManaged):
    """
    Main app containing the forms for the config TUI.

    It acts as a medium of communication for getting value between forms, storing data as instance attributes
    (via the `self.parentApp` variable available in child forms).

    See [npyscreen's documentation](https://npyscreen.readthedocs.io/application-objects.html#in-detail)
    for reference.

    Attributes:
        display_main_popup: Indicates if the main form should display a information message when loaded (holds the message itself in that case).
        main_config: Dictionary representing the loaded main configuration file.
        main_config_file: The filepath to the main configuration file.
    """
    MAIN_CONFIG_EDIT_FORM = 'MAIN_CONFIG_EDIT_FORM'

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
        self.main_config_file = 'pyfirehose/config.hjson'

    def onStart(self):
        setTheme(DefaultTheme)

        while not self.main_config:
            try:
                with open_file_from_package(self.main_config_file) as config_file:
                    try:
                        self.main_config = hjson.load(config_file)
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
        self.addForm(self.STUB_CONFIG_ENPOINTS_FORM, StubConfigEndpointsForm, name='Stub config editing - Endpoints')
        # self.addForm(self.MAIN_CONFIG_EDIT_FORM, mainEditForm, name='PyFirehose config')
