"""
SPDX-License-Identifier: MIT

Forms specifying the workflow for editing stub config files.
"""

import logging

from npyscreen import ActionFormV2
from npyscreen import OptionList

from pyfirehose.utils import get_auth_token
from pyfirehose.config.parser import Config
from pyfirehose.config.ui.widgets.custom import notify_yes_no
from pyfirehose.config.ui.widgets.inputs import InputsListDisplay, InputString

class MainConfigApiKeysForm(ActionFormV2):
    """
    Bla
    """
    def create(self):
        options = OptionList().options
        try:
            for (auth_provider, value) in self.parentApp.main_config['auth'].items():
                options.append(InputString(
                    name=auth_provider,
                    value=value['api_key'],
                    documentation=[f'Edit API key for endpoint "{value["endpoint"]}"']
                ))
        except KeyError as error:
            logging.error('[%s] Invalid main configuration file : could not find "%s"', self.name, error)
            raise

        self.w_inputs = self.add(
            InputsListDisplay,
            w_id='inputs',
            name='Edit API keys',
            values=options,
            scroll_exit=True
        )

    def on_ok(self):
        for auth_option in self.w_inputs.values:
            logging.info('[%s] %s = %s', self.name, auth_option.name, auth_option.value)
            Config.AUTH_ENDPOINT = self.parentApp.main_config['auth'][auth_option.name]['endpoint']
            Config.API_KEY = auth_option.value

            try:
                get_auth_token()
            except RuntimeError as error:
                if not notify_yes_no(
                    f'There was an error fetching the authentication token from the endpoint :\n{error}\n'
                    f'{"-"*39}\nIgnore the error and save the API key ?',
                    title=f'Error: could not fetch JWT token from "{Config.AUTH_ENDPOINT}"',
                    wide=True
                ):
                    return
            self.parentApp.main_config['auth'][auth_option.name]['api_key'] = auth_option.value

        self.parentApp.setNextFormPrevious()

    def on_cancel(self):
        self.parentApp.setNextFormPrevious()
