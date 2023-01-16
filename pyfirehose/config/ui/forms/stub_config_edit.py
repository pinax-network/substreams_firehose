"""
SPDX-License-Identifier: MIT
"""

import logging
import os.path
from typing import Optional

import grpc
import hjson
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.descriptor_pool import DescriptorPool
from grpc_reflection.v1alpha.proto_reflection_descriptor_database import ProtoReflectionDescriptorDatabase
from npyscreen import ActionFormV2
from npyscreen import TitleFilenameCombo, TitleSelectOne
from npyscreen import OptionList
from npyscreen import notify_yes_no
from pygments.lexers.data import JsonLexer

# This import is used to prevent circular dependency for the `utils` and `config.parser` modules.
from pyfirehose.args import check_period #pylint: disable=unused-import

import pyfirehose.config.ui.widgets.inputs as input_options
from pyfirehose.utils import get_auth_token
from pyfirehose.config.parser import Config, StubConfig
from pyfirehose.config.parser import load_config, load_stub_config
from pyfirehose.config.ui.forms.generic import ActionFormDiscard
from pyfirehose.config.ui.widgets.custom import CodeHighlightedTitlePager, EndpointsTitleSelectOne
from pyfirehose.config.ui.widgets.inputs import InputsListDisplay, InputRepeated

class StubConfigEndpointsForm(ActionFormV2):
    """
    Choose an endpoint to edit or create a new stub config for.

    Attributes:
        ml_endpoints: an `EndpointsTitleSelectOne` widget to select an endpoint.
    """
    def beforeEditing(self): #pylint: disable=invalid-name
        """
        Called by `npyscreen` before the form gets drawn on the screen.
        """
        if not hasattr(self, 'previous_value'):
            # Automatically select the first value to prevent empty selection
            self.previous_value = [0] #pylint: disable=attribute-defined-outside-init

        self.ml_endpoints.value = self.previous_value

    def create(self):
        self.ml_endpoints = self.add(
            EndpointsTitleSelectOne,
            name='Select an endpoint',
            values=sorted(self.parentApp.main_config['grpc'], key=lambda e: e['chain']),
            scroll_exit=True
        )

    def on_ok(self):
        self.previous_value = list(self.ml_endpoints.value) #pylint: disable=attribute-defined-outside-init
        self.parentApp.selected_endpoint = self.ml_endpoints.values[self.ml_endpoints.value.pop()]
        logging.info('[%s] Selected endpoint : %s', self.name, self.parentApp.selected_endpoint)

        self.parentApp.addForm(
            self.parentApp.STUB_CONFIG_SAVE_FILE_FORM,
            StubConfigSaveFileForm, name='Stub config editing - Save file'
        )
        self.parentApp.setNextForm(self.parentApp.STUB_CONFIG_SAVE_FILE_FORM)

    def on_cancel(self):
        del self.previous_value
        self.parentApp.setNextFormPrevious()

class StubConfigSaveFileForm(ActionFormV2):
    """
    Choose the save file location for the stub config.

    Attributes:
        stub_loaded: indicates if the stub has been loaded from the specified file.
        tfc_stub_save_file: a `TitleFilenameCombo` widget to select the stub save file.
    """
    def create(self):
        try:
            endpoint_id = self.parentApp.selected_endpoint['id']
        except AttributeError:
            logging.error('[%s] No endpoint selected', self.name)
        except KeyError:
            logging.error('[%s] Could not get id from endpoint : %s', self.name, self.parentApp.selected_endpoint)

        default_stub_save_path = 'pyfirehose/config/new.hjson'
        self.stub_loaded = load_config(self.parentApp.main_config_file, endpoint_id)
        try:
            saved_stub = next(
                (e['stub'] for e in self.parentApp.main_config['grpc'] if e['id'] == endpoint_id),
                default_stub_save_path
            )
        except KeyError:
            saved_stub = default_stub_save_path

        self.tfc_stub_save_file = self.add(TitleFilenameCombo, name='Save to file', value=saved_stub)

    def on_ok(self):
        self.parentApp.stub_save_file = self.tfc_stub_save_file.value
        logging.info('[%s] Stub save file : %s', self.name, self.parentApp.stub_save_file)

        try:
            load_stub_config(self.parentApp.stub_save_file)
        except FileNotFoundError:
            if self.stub_loaded:
                # If user wants to edit new config than the one loaded, reset it
                # TODO : Ask user if wants to keep previous loaded values for new file (?)
                StubConfig.REQUEST_PARAMETERS = {}

        self.parentApp.stub_config = {}
        if os.path.isfile(self.parentApp.stub_save_file):
            with open(self.parentApp.stub_save_file, 'r', encoding='utf8') as config_file:
                try:
                    self.parentApp.stub_config = hjson.load(config_file)
                except hjson.HjsonDecodeError as error:
                    logging.exception('Error decoding stub config file (%s): %s', self.parentApp.stub_save_file, error)
                    raise

        self.parentApp.addForm(
            self.parentApp.STUB_CONFIG_SERVICES_FORM,
            StubConfigServicesForm, name='Stub config editing - Services'
        )
        self.parentApp.setNextForm(self.parentApp.STUB_CONFIG_SERVICES_FORM)

    def on_cancel(self):
        self.parentApp.setNextFormPrevious()

class StubConfigServicesForm(ActionFormV2):
    """
    Choose a service from the services available on the specified endpoint.

    The endpoint **has** to provide a reflection service in order to determine the available services.

    Attributes:
        ml_services: a `TitleSelectOne` widget to select which service the stub will use.
    """
    def beforeEditing(self): #pylint: disable=invalid-name
        """
        Called by `npyscreen` before the form gets drawn on the screen.
        """
        if not hasattr(self, 'previous_value'):
            # Automatically select the first value to prevent empty selection
            self.previous_value = [0] #pylint: disable=attribute-defined-outside-init

        self.ml_services.value = self.previous_value

    def create(self):
        jwt = get_auth_token()
        creds = grpc.composite_channel_credentials(
            grpc.ssl_channel_credentials(),
            grpc.access_token_call_credentials(jwt)
        )

        channel = grpc.secure_channel(Config.GRPC_ENDPOINT, creds)
        self.parentApp.reflection_db = ProtoReflectionDescriptorDatabase(channel)

        services = self.parentApp.reflection_db.get_services()
        self.ml_services = self.add(
            TitleSelectOne,
            name='Select a service',
            values=services,
            scroll_exit=True
        )

    def on_ok(self):
        self.previous_value = list(self.ml_services.value) #pylint: disable=attribute-defined-outside-init
        self.parentApp.selected_service = self.ml_services.values[self.ml_services.value.pop()]
        logging.info('[%s] Selected service : %s', self.name, self.parentApp.selected_service)

        self.parentApp.addForm(
            self.parentApp.STUB_CONFIG_METHODS_FORM,
            StubConfigMethodsForm, name='Stub config editing - Methods'
        )
        self.parentApp.setNextForm(self.parentApp.STUB_CONFIG_METHODS_FORM)

    def on_cancel(self):
        del self.previous_value
        self.parentApp.setNextFormPrevious()

class StubConfigMethodsForm(ActionFormV2):
    """
    Choose a gRPC method from the specified service.

    Attributes:
        methods: available methods provided by the reflection service.
        ml_methods: a `TitleSelectOne` widget to select which method the stub will use.
    """
    def beforeEditing(self): #pylint: disable=invalid-name
        """
        Called by `npyscreen` before the form gets drawn on the screen.
        """
        if not hasattr(self, 'previous_value'):
            # Automatically select the first value to prevent empty selection
            self.previous_value = [0] #pylint: disable=attribute-defined-outside-init

        self.ml_methods.value = self.previous_value

    def create(self):
        desc_pool = DescriptorPool(self.parentApp.reflection_db)
        self.methods = desc_pool.FindServiceByName(self.parentApp.selected_service).methods

        self.ml_methods = self.add(
            TitleSelectOne,
            name='Select a method',
            values=[m.name for m in self.methods],
            scroll_exit=True
        )

    def on_ok(self):
        self.previous_value = list(self.ml_methods.value) #pylint: disable=attribute-defined-outside-init
        self.parentApp.selected_method = next(
            (m for m in self.methods if m.name == self.ml_methods.values[self.ml_methods.value[0]]),
            None
        )
        logging.info('[%s] Selected method : %s', self.name, self.parentApp.selected_method.name)

        self.parentApp.addForm(
            self.parentApp.STUB_CONFIG_INPUTS_FORM,
            StubConfigInputsForm, name='Stub config editing - Inputs'
        )
        self.parentApp.setNextForm(self.parentApp.STUB_CONFIG_INPUTS_FORM)

    def on_cancel(self):
        del self.previous_value
        self.parentApp.setNextFormPrevious()

class StubConfigInputsForm(ActionFormV2):
    """
    Edit the request parameters sent to the gRPC endpoint.

    Input options will be created according to their expected types (bool -> `InputBoolean`, etc.).

    Attributes:
        w_inputs: an `InputsListDisplay` widget to present the list of input options.
    """
    def clear_input(self, show_popup: Optional[bool] = True) -> None:
        """
        Callback function for clearing input shortcuts.

        Pressing 'c' will ask for confirmation before clearing, 'C' will not.

        Args:
            show_popup: if True, asks the user for confirmation before clearing the input.
        """
        input_widget = self.get_widget('inputs')
        cleared_option = input_widget.values[input_widget.cursor_line]

        clear_confirm = True
        if show_popup:
            clear_confirm = notify_yes_no(
                'Are you sure you want to clear the value of this input ?',
                title=f'Clear "{cleared_option.get_name_user()}" ?'
            )

        if clear_confirm:
            input_widget.values[input_widget.cursor_line].set_from_widget_value('')
            input_widget.display()

    def create(self):
        self.add_handlers({
            'c': self.clear_input,
            'C': lambda _: self.clear_input(show_popup=False)
        })

        # Map the corresponding cpp types to their input type implementation
        cpptype_simplify_mapping = {
            FieldDescriptor.CPPTYPE_INT32: 'Integer',
            FieldDescriptor.CPPTYPE_INT64: 'Integer',
            FieldDescriptor.CPPTYPE_UINT32: 'Integer',
            FieldDescriptor.CPPTYPE_UINT64: 'Integer',
            FieldDescriptor.CPPTYPE_DOUBLE: 'Float',
            FieldDescriptor.CPPTYPE_FLOAT: 'Float',
            FieldDescriptor.CPPTYPE_BOOL: 'Bool',
            FieldDescriptor.CPPTYPE_ENUM: 'Enum',
            FieldDescriptor.CPPTYPE_STRING: 'String',
            FieldDescriptor.CPPTYPE_MESSAGE: 'Message'
        }
        # Reference :
        # https://googleapis.dev/python/protobuf/latest/google/protobuf/descriptor.html#google.protobuf.descriptor.FieldDescriptor.CPPTYPE_BOOL

        options = OptionList().options
        for input_parameter in [
            f for f in self.parentApp.selected_method.input_type.fields if not f.name in ('start_block_num', 'stop_block_num')
        ]:
            # Load config value from loaded stub if it exists
            try:
                stub_config_value = self.parentApp.stub_config['parameters'][input_parameter.name]
            except KeyError:
                stub_config_value = None

            # Get the input type from the mapping (e.g. 'CPPTYPE_BOOL' -> 'Bool')
            input_type = cpptype_simplify_mapping[input_parameter.cpp_type]

            # Set the option type to the appropriate `InputXXX` class (e.g. 'InputBool')
            option_type = getattr(input_options, f'Input{input_type}')
            option_args = {
                'documentation': [
                    f'A parameter of type {input_type.upper()}'
                    f'is expected for "{input_parameter.name}."'
                ],
                'name': input_parameter.name,
                'value': stub_config_value
            }

            # If its a repeated field, change to `InputRepeated` and pass the original type to the constructor
            if input_parameter.label == FieldDescriptor.LABEL_REPEATED:
                option_type = InputRepeated
                option_args.update(
                    # Allow the `InputRepeated` to pick the right validator (e.g. `bool_validator`)
                    value_type=input_type.lower(),
                )

            # Add or modify arguments based on the input type (`documentation`, etc.)
            if input_parameter.cpp_type == FieldDescriptor.CPPTYPE_BOOL:
                option_args.update(
                    documentation=option_args['documentation'] + [
                        'Press [X] or [SPACE] to toggle between checked/unchecked.'
                    ]
                )
            elif input_parameter.cpp_type == FieldDescriptor.CPPTYPE_ENUM:
                enum_choices = [e.name for e in input_parameter.enum_type.values]
                option_args.update(
                    documentation=option_args['documentation'] + [
                        f'Valid values are {enum_choices}.'
                    ],
                    choices=enum_choices
                )
            elif input_parameter.cpp_type == FieldDescriptor.CPPTYPE_MESSAGE:
                pass # TODO: Add description for 'modules' parameter of substreams

            # Add the new input instance to the list of options
            options.append(option_type(**option_args))

        self.w_inputs = self.add(
            InputsListDisplay,
            w_id='inputs',
            name='Edit method inputs',
            values=options,
            scroll_exit=True
        )

    def on_ok(self):
        if not self.parentApp.stub_config:
            self.parentApp.stub_config['parameters'] = {}
            self.parentApp.stub_config['python_import_dir'], self.parentApp.stub_config['name'] = \
                self.parentApp.selected_service.rsplit('.', 1)
            self.parentApp.stub_config['request'] = self.parentApp.selected_method.input_type.name

        for input_option in self.w_inputs.values:
            is_empty_input = False
            try:
                iter(input_option.value)
            except TypeError:
                is_empty_input = not input_option.value
            else:
                is_empty_input = not any(input_option.value)

            if input_option.name in self.parentApp.stub_config['parameters'] and is_empty_input:
                del self.parentApp.stub_config['parameters'][input_option.name]
            elif not is_empty_input:
                self.parentApp.stub_config['parameters'][input_option.name] = input_option.value

        logging.info('[%s] Stub config : %s', self.name, self.parentApp.stub_config)

        self.parentApp.addForm(
            self.parentApp.STUB_CONFIG_CONFIRM_EDIT_FORM,
            StubConfigConfirmEditForm, name='Stub config editing - Confirm'
        )
        self.parentApp.setNextForm(self.parentApp.STUB_CONFIG_CONFIRM_EDIT_FORM)

    def on_cancel(self):
        self.parentApp.setNextFormPrevious()

# TODO : Add output config screen

class StubConfigConfirmEditForm(ActionFormDiscard):
    """
    Confirmation screen displaying the final stub config as it will appear in the saved file.
    """
    def create(self):
        self.add(
            CodeHighlightedTitlePager,
            name=f'Stub config recap (view only) - {self.parentApp.stub_save_file}',
            values=hjson.dumpsJSON(self.parentApp.stub_config, indent=4).split('\n'),
            lexer=JsonLexer()
        )

    def on_ok(self):
        if os.path.isfile(self.parentApp.stub_save_file):
            overwrite_confirm = notify_yes_no(
                'Overwrite the previous stub config file ?',
                title=f'Overwrite "{self.parentApp.stub_save_file}" ?'
            )

            if not overwrite_confirm:
                return True

        with open(self.parentApp.stub_save_file, 'w+', encoding='utf8') as config_file:
            hjson.dumpJSON(self.parentApp.stub_config, config_file, indent=4)

        self.parentApp.display_main_popup = f'Stub file successfully saved at :\n{self.parentApp.stub_save_file}'
        self.parentApp.setNextForm('MAIN')

        return False

    def on_cancel(self):
        self.parentApp.setNextFormPrevious()

    def on_discard(self):
        discard_confirm = notify_yes_no(
            'Do you really want to discard this stub ? (No changes will be saved)',
            title=f'Discard "{self.parentApp.stub_save_file}" ?'
        )

        if discard_confirm:
            self.parentApp.switchForm('MAIN')
        else:
            pass