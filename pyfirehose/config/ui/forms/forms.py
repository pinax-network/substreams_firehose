"""
SPDX-License-Identifier: MIT

Forms used by the main config GUI app to display and edit configuration files.

--- Cansi library (https://github.com/tslight/cansi) ---
Copyright (c) 2018, Toby Slight
All rights reserved.

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.
--- Cansi library (https://github.com/tslight/cansi) ---
"""

import logging
import os.path

import grpc
import hjson
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.descriptor_pool import DescriptorPool
from grpc_reflection.v1alpha.proto_reflection_descriptor_database import ProtoReflectionDescriptorDatabase
from npyscreen import FormWithMenus, ActionFormV2
from npyscreen import MiniButtonPress, TitleFilenameCombo, TitleSelectOne
from npyscreen import OptionList
from npyscreen import notify_confirm, notify_yes_no
from pygments.lexers.data import JsonLexer

# This import is used to prevent circular dependency for the `utils` and `config.utils` modules.
from pyfirehose.args import check_period #pylint: disable=unused-import

import pyfirehose.config.ui.widgets.inputs as input_options
from pyfirehose.utils import get_auth_token
from pyfirehose.config.parser import Config, StubConfig
from pyfirehose.config.parser import load_config, load_stub_config
from pyfirehose.config.ui.widgets.custom import CodeHighlightedTitlePager, EndpointsTitleSelectOne
from pyfirehose.config.ui.widgets.inputs import InputsListDisplay, InputRepeated

class MainForm(FormWithMenus):
    """
    Main form presenting the main config file with a menu for accessing the edit functions.

    Attributes:
        main_menu: holds the menu entries.
        next_form: describe the next form to be loaded after exiting the main form (`None` exits the application).
        stored_highlights: dictionary containing the highlighted text content for the `CodeHighlightedTitlePager` widget.
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

    def create(self):
        self.main_menu = self.new_menu(name='Main menu')
        self.main_menu.addItem(
            text='Edit main config',
            onSelect=self.switch_form,
            arguments=[self.parentApp.MAIN_CONFIG_EDIT_FORM]
        )
        self.main_menu.addItem(
            text='Edit stub config',
            onSelect=self.switch_form,
            arguments=[self.parentApp.STUB_CONFIG_ENPOINTS_FORM]
        )

        self.add(
            CodeHighlightedTitlePager,
            name=f'Main config (view only) - {self.parentApp.main_config_file}',
            values=hjson.dumpsJSON(self.parentApp.main_config, indent=4).split('\n'),
            lexer=JsonLexer()
        )

    def switch_form(self, form: str) -> None:
        """
        Helper function to set the next appropriate form when using the menu.

        Args:
            form: the form name.
        """
        self.next_form = form #pylint: disable=attribute-defined-outside-init
        self.parentApp.switchForm(form)

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
    def clear_input(self, show_popup=True):
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

class ActionFormDiscard(ActionFormV2):
    """
    Generic class for an action form with an additional *Discard* button.

    Overload the `on_discard` method to customize its behavior.
    """
    class Discard_Button(MiniButtonPress): #pylint: disable=invalid-name
        """
        Additional *Discard* button (name style chosen to match the `npyscreen` library).
        """
        def whenPressed(self):
            self.parent._on_discard() #pylint: disable=protected-access

    DISCARDBUTTON_TYPE = Discard_Button
    DISCARD_BUTTON_BR_OFFSET = (
        ActionFormV2.CANCEL_BUTTON_BR_OFFSET[0],
        ActionFormV2.OK_BUTTON_BR_OFFSET[1]
        + len(ActionFormV2.OK_BUTTON_TEXT)
        + ActionFormV2.CANCEL_BUTTON_BR_OFFSET[1]
        + len(ActionFormV2.CANCEL_BUTTON_TEXT)
    )
    DISCARD_BUTTON_TEXT = 'Discard'

    def _on_discard(self):
        self.editing = self.on_discard()

    def create_control_buttons(self):
        self._add_button('ok_button',
            self.__class__.OKBUTTON_TYPE,
            self.__class__.OK_BUTTON_TEXT,
            0 - self.__class__.OK_BUTTON_BR_OFFSET[0],
            0 - self.__class__.OK_BUTTON_BR_OFFSET[1] - len(self.__class__.OK_BUTTON_TEXT),
            None
        )

        self._add_button('cancel_button',
            self.__class__.CANCELBUTTON_TYPE,
            self.__class__.CANCEL_BUTTON_TEXT,
            0 - self.__class__.CANCEL_BUTTON_BR_OFFSET[0],
            0 - self.__class__.CANCEL_BUTTON_BR_OFFSET[1] - len(self.__class__.CANCEL_BUTTON_TEXT),
            None
        )

        self._add_button('discard_button',
            self.__class__.DISCARDBUTTON_TYPE,
            self.__class__.DISCARD_BUTTON_TEXT,
            0 - self.__class__.DISCARD_BUTTON_BR_OFFSET[0],
            0 - self.__class__.DISCARD_BUTTON_BR_OFFSET[1] - len(self.__class__.DISCARD_BUTTON_TEXT),
            None
        )

    def on_discard(self):
        """
        *Discard* button hook to overload for customizing the behavior of the button.
        """
        return False

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
