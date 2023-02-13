"""
SPDX-License-Identifier: MIT

Forms specifying the workflow for editing stub config files.
"""

import logging
from collections.abc import MutableMapping, Sequence

from npyscreen import ActionFormV2
from npyscreen import OptionList
from npyscreen import notify

from pyfirehose.utils import get_auth_token
from pyfirehose.config.parser import Config
from pyfirehose.config.ui.forms.generic import CategorizedItemDisplayForm
from pyfirehose.config.ui.widgets.custom import notify_yes_no
from pyfirehose.config.ui.widgets.inputs import InputEnum, InputFile, InputListDisplay, InputSingleEnum, InputString

'''
    TODO: Generalize the endpoints editing form to also use it for auth providers
        - Don't work with `dict`, work with the underlying values
        - Provide a list of categories, a 'category' key (e.g. 'auth') and identify values by their display value (e.g. 'id')
        - Also provide main config key to override ? Or overload `on_ok` method ? Or call a validation function that does that ?
        - Need to provide the fields list description (see `EndpointField` object) for the items.
'''

class MainConfigApiKeysForm(ActionFormV2):
    """
    Edit API keys for the authentication endpoints present in the main configuration file.

    Checks that keys are valid by trying to fetch a JWT token from the endpoint. Any errors can be ignored if wanted.
    """
    def create(self):
        options = OptionList().options
        try:
            for auth_provider, value in self.parentApp.main_config['auth'].items():
                options.append(InputString(
                    name=auth_provider,
                    value=value['api_key'],
                    documentation=[f'Edit API key for endpoint "{value["endpoint"]}"']
                ))
        except KeyError as error:
            logging.error('[%s] Invalid main configuration file : could not find "%s"', self.name, error)
            raise

        self.w_inputs = self.add(
            InputListDisplay,
            w_id='inputs',
            name='Edit API keys',
            values=options,
            scroll_exit=True
        )

    def on_ok(self):
        for auth_option in self.w_inputs.values:
            if self.parentApp.main_config['auth'][auth_option.name]['api_key'] != auth_option.value:
                Config.AUTH_ENDPOINT = self.parentApp.main_config['auth'][auth_option.name]['endpoint']
                Config.API_KEY = auth_option.value

                notify(f'Testing JWT authentication token fetch from "{Config.AUTH_ENDPOINT}"...', title='Please wait')
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

class MainConfigEndpointsForm(CategorizedItemDisplayForm):
    """
    Display the list of endpoints from the main configuration files, grouped by their authentication endpoint id.

    Selecting an endpoint will bring up an `ActionButtonPopup` menu to edit or delete the endpoint.
    New endpoints can be added using the third `ActionForm` button at the bottom.
    """
    def __init__(self, *args, **kwargs):
        # Have to set `parentApp` manually for accessing main config values as parent constructor would also call `create()` form method.
        try:
            self.parentApp = kwargs['parentApp']
        except KeyError as error:
            logging.error('[MainConfigEndpointsForm] No parent app set, cannot access main config values : %s', error)
            raise RuntimeError from error

        ItemField = CategorizedItemDisplayForm.ItemField
        super().__init__(*args,
            items=self.parentApp.main_config['grpc'],
            item_fields=[
                ItemField('id', InputString, required=True, documentation=['Unique identifier for the endpoint.']),
                # Must select one of the available authentication providers
                ItemField('auth', InputSingleEnum, {'choices': list(self.parentApp.main_config['auth'].keys())}, True,
                    ['Authentication provider to use for making secure gRPC connections.']
                ),
                ItemField('chain', InputString, documentation=['Blockchain that the endpoint\'s data relates to.']),
                # Allow one or none of the options to be chosen with `InputEnum`
                ItemField('compression', InputEnum, {'choices': ['gzip', 'deflate']},
                    documentation=[
                    'WARNING: Not all endpoint might support this feature',
                    'Compression method to use for exchanging data with the endpoint.'
                ]),
                ItemField('stub', InputFile, documentation=['Default stub config file to load when using the endpoint.']),
                ItemField('url', InputString, required=True, documentation=['Endpoint url in the format {url}:{port}']),
            ],
            identifier_key='id',
            category_key='auth',
            **kwargs
        )

    def on_ok(self):
        self.parentApp.main_config['grpc'] = super().on_ok()

    def on_cancel(self):
        super().on_cancel()
        self.parentApp.restore_main_config_backup()
