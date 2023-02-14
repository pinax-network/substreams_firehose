"""
SPDX-License-Identifier: MIT

Forms specifying the workflow for editing stub config files.
"""

import logging

from npyscreen import notify
from requests.exceptions import RequestException

from pyfirehose.utils import get_auth_token
from pyfirehose.config.parser import Config
from pyfirehose.config.ui.forms.generic import CategorizedItemDisplayForm
from pyfirehose.config.ui.widgets.custom import notify_yes_no
from pyfirehose.config.ui.widgets.inputs import InputEnum, InputFile, InputSingleEnum, InputString

class MainConfigAuthProvidersForm(CategorizedItemDisplayForm):
    """
    Display the list of authentication providers from the main configuration file.

    See `CategorizedItemDisplayForm` documentation for details.
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
            items=self.parentApp.main_config['auth'],
            item_fields=[
                ItemField('id', InputString, required=True, documentation=[
                    # TODO: Replace documentation warning with `notify_yes_no` to propose to change them ?
                    'WARNING: Changing the id will require to update all related gRPC endpoint entries in the main configuration file.',
                    'Unique identifier for the authentication provider.'
                ]),
                ItemField('api_key', InputString, required=True, documentation=['Valid API key from the provider.']),
                ItemField('endpoint', InputString, required=True, documentation=['Authentication endpoint url']),
            ],
            identifier_key='id',
            category_key=None,
            default_category='Authentication providers',
            **kwargs
        )

    def on_ok(self):
        new_auth_providers = super().on_ok()

        for auth_provider in new_auth_providers:
            Config.AUTH_ENDPOINT = auth_provider['endpoint']
            Config.API_KEY = auth_provider['api_key']

            notify(f'Testing JWT authentication token fetch from "{Config.AUTH_ENDPOINT}"...', title='Please wait')
            try:
                get_auth_token()
            except (RequestException, RuntimeError) as error:
                if not notify_yes_no(
                    f'There was an error fetching the authentication token from the endpoint :\n{error}\n'
                    f'{"-"*39}\nIgnore the error and save the API key ?',
                    title=f'Error: could not fetch JWT token from "{Config.AUTH_ENDPOINT}"',
                    wide=True
                ):
                    self.parentApp.setNextForm(self.parentApp.MAIN_CONFIG_AUTH_PROVIDERS_FORM)
                    return

        self.parentApp.main_config['auth'] = new_auth_providers

    def on_cancel(self):
        super().on_cancel()
        self.parentApp.restore_main_config_backup()

class MainConfigEndpointsForm(CategorizedItemDisplayForm):
    """
    Display the list of endpoints from the main configuration files, grouped by their authentication endpoint id.

    See `CategorizedItemDisplayForm` documentation for details.
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
                ItemField('auth', InputSingleEnum, {'choices': sorted(list({entry['id'] for entry in self.parentApp.main_config['auth']}))},
                    required=True,
                    documentation=['Authentication provider to use for making secure gRPC connections.']
                ),
                ItemField('chain', InputString, documentation=['Blockchain that the endpoint\'s data relates to.']),
                # Allow one or none of the options to be chosen with `InputEnum`
                ItemField('compression', InputEnum, {'choices': ['gzip', 'deflate']},
                    documentation=[
                    'WARNING: Not all endpoint might support this feature',
                    'Compression method to use for exchanging data with the endpoint.'
                ]),
                ItemField('stub', InputFile, documentation=['Default stub configuration file to load when using the endpoint.']),
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
