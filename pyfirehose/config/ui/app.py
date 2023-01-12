"""
SPDX-License-Identifier: MIT
"""

import logging

import hjson
from npyscreen import NPSAppManaged
from npyscreen import setTheme
from npyscreen.npysThemes import DefaultTheme

from pyfirehose.config.ui.forms import MainForm, StubConfigEndpointsForm

class ConfigApp(NPSAppManaged):
    STUB_CONFIG_CONFIRM_EDIT_FORM = 'STUB_CONFIG_CONFIRM_EDIT_FORM'
    STUB_CONFIG_ENPOINTS_FORM = 'STUB_CONFIG_ENDPOINTS_FORM'
    STUB_CONFIG_INPUTS_FORM = 'STUB_CONFIG_INPUTS_FORM'
    STUB_CONFIG_METHODS_FORM = 'STUB_CONFIG_METHODS_FORM'
    STUB_CONFIG_SAVE_FILE_FORM = 'STUB_CONFIG_SAVE_FILE_FORM'
    STUB_CONFIG_SERVICES_FORM = 'STUB_CONFIG_SERVICES_FORM'
    MAIN_CONFIG_EDIT_FORM = 'MAIN_CONFIG_EDIT_FORM'

    def __init__(self):
        super().__init__()

        self.display_main_popup = None
        self.main_config_file = 'pyfirehose/config.hjson'
        with open(self.main_config_file, 'r', encoding='utf8') as config_file:
            try:
                self.main_config = hjson.load(config_file)
            except hjson.HjsonDecodeError as error:
                logging.exception('Error decoding main config file (%s): %s', self.main_config_file, error)
                raise

    def onStart(self):
        setTheme(DefaultTheme)

        self.addForm('MAIN', MainForm, name='PyFirehose config')
        self.addForm(self.STUB_CONFIG_ENPOINTS_FORM, StubConfigEndpointsForm, name='Stub config editing - Endpoints')
        # self.addForm(self.MAIN_CONFIG_EDIT_FORM, mainEditForm, name='PyFirehose config')
