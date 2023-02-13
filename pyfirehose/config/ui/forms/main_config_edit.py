"""
SPDX-License-Identifier: MIT

Forms specifying the workflow for editing stub config files.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Type

from npyscreen import ActionFormV2
from npyscreen import OptionList
from npyscreen import notify, notify_confirm

from pyfirehose.utils import get_auth_token
from pyfirehose.config.parser import Config
from pyfirehose.config.ui.forms.generic import ActionFormDiscard
from pyfirehose.config.ui.widgets.custom import EndpointsViewerBoxTitle, notify_yes_no
from pyfirehose.config.ui.widgets.inputs import InputEnum, InputFile, InputGeneric, InputListDisplay, InputSingleEnum, InputString

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

class MainConfigEndpointsForm(ActionFormDiscard):
    """
    Display the list of endpoints from the main configuration files, grouped by their authentication endpoint id.

    Selecting an endpoint will bring up an `ActionButtonPopup` menu to edit or delete the endpoint.
    New endpoints can be added using the third `ActionForm` button at the bottom.
    """
    DISCARD_BUTTON_TEXT = 'New'
    # Needed so that `self.editw` (controlling the focused widget in the form) doesn't get reset when starting to edit the form
    PRESERVE_SELECTED_WIDGET_DEFAULT = True

    # def beforeEditing(self):
    # 	for boxtitle_widget in self.w_endpoints_boxtitle:
    # 		boxtitle_widget.values = [e for e in self.parentApp.main_config['grpc'] if e['auth'] == boxtitle_widget.name]

    def create(self):
        self.w_endpoints_boxtitle = []

        n_auth_providers = len(self.parentApp.main_config['auth'])
        for auth_provider in self.parentApp.main_config['auth']:
            self.w_endpoints_boxtitle.append(self.add(
                EndpointsViewerBoxTitle,
                name=auth_provider,
                values=[e for e in self.parentApp.main_config['grpc'] if e['auth'] == auth_provider],
                max_height=self.lines//n_auth_providers - 2,
                scroll_exit=True,
            ))

    def create_endpoint_edit_form(self, endpoint: dict) -> None:
        """
        Create and start a `MainConfigEndpointEditForm` for editing the specified endpoint.

        Args:
            endpoint: A dict representing the endpoint's current configuration.
        """
        self.parentApp.addForm(
            self.parentApp.MAIN_CONFIG_ENDPOINT_EDIT_FORM,
            MainConfigEndpointEditForm, name='Main config editing - Edit endpoint', endpoint=endpoint
        )
        self.parentApp.switchForm(self.parentApp.MAIN_CONFIG_ENDPOINT_EDIT_FORM)

    def on_ok(self):
        new_endpoints = []
        for boxtitle in self.w_endpoints_boxtitle:
            new_endpoints.extend(boxtitle.values)

        self.parentApp.main_config['grpc'] = new_endpoints
        self.parentApp.setNextFormPrevious()

    def on_cancel(self):
        self.parentApp.restore_main_config_backup()
        self.parentApp.setNextFormPrevious()

    def on_discard(self):
        """
        Override the default 'discard' behavior to create an new endpoint entry.
        """
        self.create_endpoint_edit_form({})

    def is_unique(self, item_id: Any) -> bool:
        """
        Check that the item identified by the `item_id` is not already present in the displayed values.

        Args:
            item_id: An identifier supposed to be unique for each item.

        Returns:
            A boolean indicating if the identifier is already present.

        Raises:
            ValueError: If the `item_id` is `None`.
        """
        if item_id is None:
            raise ValueError('Item id cannot be `None`')

        return item_id not in [v.get('id') for w in self.w_endpoints_boxtitle for v in w.values]

    def move_to_boxtitle(self, endpoint: dict, previous_boxtitle: str | None = None) -> None:
        """
        Move the specified endpoint from its previous `BoxTitle` to the new one defined in its `auth` attribute.

        If `previous_boxtitle` is `None`, the endpoint is simply added to the `BoxTitle`.

        Args:
            endpoint: A dict representing the endpoint to move.
            previous_boxtitle: An optional string specifying the previous `BoxTitle` the endpoint was present in.

        Raises:
            ValueError: If the endpoint could not be found in the `previous_boxtitle`.
        """
        for boxtitle_widget in self.w_endpoints_boxtitle:
            if endpoint['auth'] == boxtitle_widget.name:
                boxtitle_widget.values.append(endpoint)
            elif previous_boxtitle == boxtitle_widget.name:
                try:
                    boxtitle_widget.values = [v for v in boxtitle_widget.values if v['id'] != endpoint['id']]
                except ValueError:
                    logging.error('[%s] Endpoint not found in %s widget : %s', self.name, boxtitle_widget.name, endpoint)
                    raise

    def select_endpoint(self, endpoint: dict) -> None:
        """
        Move the cursor to the specified endpoint in the form. Used when finishing endpoint edition to select the edited endpoint.

        Args:
            endpoint: A dict representing the endpoint to select.
        """
        for boxtitle_widget in self.w_endpoints_boxtitle:
            if endpoint['auth'] == boxtitle_widget.name:
                try:
                    # Update cursor position within the `BoxTitle` widget
                    boxtitle_widget.entry_widget.cursor_line = boxtitle_widget.values.index(endpoint)

                    # Update the focused `BoxTitle` widget within the form
                    self.editw = self.w_endpoints_boxtitle.index(boxtitle_widget) #pylint: disable=attribute-defined-outside-init
                except ValueError:
                    logging.error('[%s] Endpoint not found in %s widget : %s', self.name, boxtitle_widget.name, endpoint)
                    raise

class MainConfigEndpointEditForm(ActionFormV2):
    """
    Edit an endpoint fields.

    Fields are marked as required (won't allow empty values) or optional, with different display (color and symbol) for each.
    """
    REQUIRED_FIELD_COLOR = 'WARNING'
    OPTIONAL_FIELD_COLOR = 'GOOD'

    def __init__(self, *args, endpoint: dict, **kwargs):
        self._endpoint = endpoint
        super().__init__(*args, **kwargs)

    def create(self):
        @dataclass
        class EndpointField:
            """
            Local class to store an endpoint field configuration values.

            Attributes:
                name: The field name.
                input_class: The input class from `inputs.py` to use for editing the field.
                input_args: A dictionary with additional arguments to the `input_class`.
                required: A boolean setting the field as required or optional.
                documentation: A list of strings describing the field purpose.
            """
            name: str
            input_class: Type[InputGeneric]
            input_args: dict = field(default_factory=dict)
            required: bool = False
            documentation: list[str] = field(default_factory=list)

        endpoint_fields = [
            EndpointField('id', InputString, required=True, documentation=['Unique identifier for the endpoint.']),
            # Must select one of the available authentication providers
            EndpointField('auth', InputSingleEnum, {'choices': list(self.parentApp.main_config['auth'].keys())}, True,
                ['Authentication provider to use for making secure gRPC connections.']
            ),
            EndpointField('chain', InputString, documentation=['Blockchain that the endpoint\'s data relates to.']),
            # Allow one or none of the options to be chosen with `InputEnum`
            EndpointField('compression', InputEnum, {'choices': ['gzip', 'deflate']},
                documentation=[
                'WARNING: Not all endpoint might support this feature',
                'Compression method to use for exchanging data with the endpoint.'
            ]),
            EndpointField('stub', InputFile, documentation=['Default stub config file to load when using the endpoint.']),
            EndpointField('url', InputString, required=True, documentation=['Endpoint url in the format {url}:{port}']),
        ]

        options = OptionList().options
        for endpoint_field in endpoint_fields:
            input_color = self.REQUIRED_FIELD_COLOR if endpoint_field.required else self.OPTIONAL_FIELD_COLOR

            options.append(endpoint_field.input_class(
                name=endpoint_field.name,
                value=self._endpoint.get(endpoint_field.name, ''),
                documentation=\
                    [f'{"="*16}', f'=== {"REQUIRED" if endpoint_field.required else "OPTIONAL"} ===', f'{"="*16}'] + endpoint_field.documentation,
                # Set the color inside the option editing window to match the displayed color from the fields list
                option_widget_keywords={'labelColor': input_color},
                **endpoint_field.input_args
            ))

            # Additional `Option` object parameters for display
            options[-1].annotation_color = input_color
            options[-1].required = endpoint_field.required

        self.w_inputs = self.add(
            InputListDisplay,
            w_id='inputs',
            name='Edit endpoint attributes',
            values=options,
            scroll_exit=True
        )

    def on_ok(self):
        previous_auth = self._endpoint.get('auth')
        previous_id = self._endpoint.get('id')
        endpoints_form = self.parentApp.getForm(self.parentApp.MAIN_CONFIG_ENDPOINTS_FORM)

        for endpoint_field in self.w_inputs.values:
            if endpoint_field.required and not endpoint_field.value:
                notify_confirm(f'A value is required for "{endpoint_field.name}"', title='Error: no value set for required field')
                return

            # Flag duplicate ids only when renaming
            if endpoint_field.name == 'id' and endpoint_field.value != previous_id and not endpoints_form.is_unique(endpoint_field.value):
                notify_confirm(
                    f'The "{endpoint_field.value}" id already exists. Please choose another identifier.',
                    title='Error: identifier not unique'
                )
                return

            # Get the value from single choice widgets (stored internally as a list in the widget)
            try:
                endpoint_field.value = endpoint_field.value.pop()
            except (AttributeError, IndexError):
                pass

            # Check if not empty or a boolean
            is_empty_input = not (endpoint_field.value or isinstance(endpoint_field.value, bool))

            # Delete any previously set parameter if it's empty or ignore it.
            if endpoint_field.name in self._endpoint and is_empty_input:
                del self._endpoint[endpoint_field.name]
            elif not is_empty_input:
                self._endpoint[endpoint_field.name] = endpoint_field.value

        # Update the endpoints list display to move the edited endpoint to its new corresponding `BoxTitle`
        if self._endpoint['auth'] != previous_auth:
            endpoints_form.move_to_boxtitle(self._endpoint, previous_auth)
        endpoints_form.select_endpoint(self._endpoint)

        self.parentApp.setNextFormPrevious()

    def on_cancel(self):
        self.parentApp.setNextFormPrevious()
