"""
SPDX-License-Identifier: MIT

Forms specifying the workflow for editing stub config files.
"""

import logging
import os.path

import grpc
import hjson
from google.protobuf.descriptor import Descriptor, FieldDescriptor
from google.protobuf.descriptor_pool import DescriptorPool
from grpc_reflection.v1alpha.proto_reflection_descriptor_database import ProtoReflectionDescriptorDatabase
from npyscreen import ActionFormV2
from npyscreen import TitleFilenameCombo, TitleSelectOne
from npyscreen import OptionList
from npyscreen import notify_confirm, notify_yes_no
from pygments.lexers.data import JsonLexer

# This import is used to prevent circular dependency for the `utils` and `config.parser` modules.
from pyfirehose.args import check_period #pylint: disable=unused-import

import pyfirehose.config.ui.widgets.inputs as input_options
from pyfirehose.utils import get_auth_token
from pyfirehose.config.parser import Config, StubConfig
from pyfirehose.config.parser import load_config, load_substream_package, load_stub_config
from pyfirehose.config.ui.forms.generic import ActionFormDiscard, SplitActionForm
from pyfirehose.config.ui.widgets.custom import CodeHighlightedTitlePager, EndpointsTitleSelectOne, \
                                                OutputSelectionMLTreeMultiSelectAnnotated, OutputTypesTitleSelectOne, \
                                                OutputSelectionTreeData
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
                # TODO : Handle stub config templates from here, loading previous stub config values
                # If user wants to edit new config than the one loaded, reset it
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

        try:
            services = self.parentApp.reflection_db.get_services()
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.UNAVAILABLE: #pylint: disable=no-member
                services = []
                # TODO: Allow providing a service descriptor (?)
                notify_confirm(
                    f'The endpoint "{Config.GRPC_ENDPOINT}" doesn\'t provide a gRPC reflection service.\n\n'
                    f'Please select another one or fill the stub config file manually.',
                    title='Error: no reflection service available'
                )
                self.on_ok = lambda *args, **kwargs: self.parentApp.setNextFormPrevious()

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

        # Currently detects if the endpoint is using substream by checking the name of the service
        # TODO: Is this robust and reliable enough (?)
        self.parentApp.is_substream = 'substream' in self.parentApp.selected_service

        self.parentApp.stub_config['base'], self.parentApp.stub_config['service'] = \
            self.parentApp.selected_service.rsplit('.', 1)

        # Load substream package object for the `load_substream_package` method
        if self.parentApp.is_substream:
            StubConfig.SUBSTREAMS_PACKAGE_OBJECT = Config.PROTO_MESSAGES_CLASSES[
                f'{self.parentApp.stub_config["base"]}.Package'
            ]

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

        self.parentApp.stub_config['method'] = self.parentApp.selected_method.name

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
    def clear_input(self, show_popup: bool = True) -> None:
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
        # Input clearing shortcuts, 'c' shows a warning, 'C' force clear the selected field
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
                stub_config_value = self.parentApp.stub_config['request']['params'][input_parameter.name]
            except KeyError:
                stub_config_value = None

            # Get the input type from the mapping (e.g. 'CPPTYPE_BOOL' -> 'Bool')
            input_type = cpptype_simplify_mapping[input_parameter.cpp_type]

            # Set the option type to the appropriate `InputXXX` class (e.g. 'InputBool')
            option_type = getattr(input_options, f'Input{input_type}')
            option_args = {
                'documentation': [
                    f'A parameter of type {input_type.upper()} '
                    f'is expected for "{input_parameter.name}".'
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
                if input_parameter.name.lower() == 'modules':
                    option_args.update(
                        documentation=option_args['documentation'] + [
                            'Input the path to a package file (.spkg) associated with the substream you want to use.'
                        ],
                        parent=self
                    )
            elif input_parameter.cpp_type == FieldDescriptor.CPPTYPE_STRING:
                if self.parentApp.is_substream:
                    # Skip deprecated `output_modules` input parameter, not allowing multiple output modules
                    # See: https://github.com/streamingfast/substreams/blob/develop/docs/release-notes/change-log.md#single-module-output
                    if input_parameter.name.lower() == 'output_modules':
                        continue

                    if input_parameter.name.lower() == 'output_module':
                        package_modules = self.get_output_module_choices(
                            self.parentApp.stub_config.get('request', {}).get('params', {}).get('modules')
                        )
                        option_type = input_options.InputEnum
                        option_args.update(
                            documentation=[
                                'A parameter of type ENUM is expected for "output_module".',
                                f'Valid values are {package_modules}.'
                            ],
                            choices=package_modules,
                            value=[stub_config_value]
                        )

            # Add the new input instance to the list of options
            options.append(option_type(**option_args))

        self.w_inputs = self.add(
            InputsListDisplay,
            w_id='inputs',
            name='Edit method inputs',
            values=options,
            scroll_exit=True
        )

        if self.parentApp.is_substream and not package_modules:
            self.hide_input_option('output_module')

    def hide_input_option(self, name: str, hide: bool = True) -> None:
        """
        Hide or display the designated input option.

        Args:
            name: Identifier of the input option in the `w_inputs` input list.
            hide: Boolean indicating to hide or show the specified option.

        Raises:
            StopIteration: If the input option could not be found.
        """
        try:
            next((w for w in self.w_inputs.values if w.name == name)).hidden = hide
        except StopIteration:
            logging.error('[%s] Could not find input widget "%s" in the list of inputs. Valid values are : %s',
                self.name,
                name,
                [w.name for w in self.w_inputs.values]
            )
            raise

    def get_output_module_choices(self, package_url: str) -> list:
        """
        Return the available output modules from the given package file.
        Only returns `map` modules according to [Streamingfast specifications](
            https://github.com/streamingfast/substreams/blob/develop/docs/release-notes/change-log.md#output-module-must-be-of-type-map
        ).

        Args:
            package_url: Filepath to a substream package file (`.spkg`).

        Returns:
            A list of available output modules for the given substream package (or an empty list).
        """
        try:
            return [m['name'] for m in load_substream_package(package_url)['modules']['modules'] if 'map' in m['name']] if package_url else []
        except KeyError as error:
            logging.error('[%s] Could not load output modules from package : missing %s', self.name, error)
            notify_confirm(
                'Package file doesn\'t seem to contain any output module, check that `map` outputs are available from this substream.',
                title=f'Warning : no output module found for "{package_url}"'
            )
            return []

    def on_ok(self):
        if 'request' not in self.parentApp.stub_config:
            self.parentApp.stub_config['request'] = {}
            self.parentApp.stub_config['request']['object'] = self.parentApp.selected_method.input_type.name
            self.parentApp.stub_config['request']['params'] = {}

        if 'response' not in self.parentApp.stub_config:
            self.parentApp.stub_config['response'] = {}
            self.parentApp.stub_config['response']['object'] = self.parentApp.selected_method.output_type.name
            self.parentApp.stub_config['response']['params'] = {}

        for input_option in self.w_inputs.values:
            is_empty_input = False
            try:
                # Check if input is a sequence
                iter(input_option.value)
            except TypeError:
                # Else check if not empty or a boolean
                is_empty_input = not (input_option.value or isinstance(input_option.value, bool))
            else:
                # Check the sequence is not empty
                is_empty_input = not any(input_option.value)

            # Delete any previously set parameter if it's empty or ignore it.
            if input_option.name in self.parentApp.stub_config['request']['params'] and is_empty_input:
                del self.parentApp.stub_config['request']['params'][input_option.name]
            elif not is_empty_input:
                self.parentApp.stub_config['request']['params'][input_option.name] = input_option.value

        logging.info('[%s] Stub config : %s', self.name, self.parentApp.stub_config)

        if self.parentApp.is_substream:
            if not ('output_modules' in self.parentApp.stub_config['request']['params'] or \
                                                'output_module' in self.parentApp.stub_config['request']['params']):
                notify_confirm(
                    'Please provide an output module before continuing.',
                    title='Error: no output module(s) specified for substream'
                )
                return

            # Flatten `output_module` list as it's only a single value parameter
            self.parentApp.stub_config['request']['params']['output_module'] = \
                next(iter(self.parentApp.stub_config['request']['params']['output_module']), None)

        self.parentApp.addForm(
            self.parentApp.STUB_CONFIG_OUTPUTS_FORM,
            StubConfigOutputsForm, name='Stub config editing - Outputs'
        )
        self.parentApp.setNextForm(self.parentApp.STUB_CONFIG_OUTPUTS_FORM)

    def on_cancel(self):
        self.parentApp.setNextFormPrevious()

class StubConfigOutputsForm(SplitActionForm): #pylint: disable=too-many-ancestors
    """
    Select and filter fields that will be received from the gRPC stream.

    The top selection widget presents a list of compatible output types while the bottom tree widget list the
    available fields that can be selected to be kept from the response.

    Attributes:
        output_descriptors: List of available `Descriptor` for the corresponding method.
        saved_output_selection: Stores the state of a selection tree to be restored when switching output types.
    """
    def beforeEditing(self): #pylint: disable=invalid-name
        """
        Called by `npyscreen` before the form gets drawn on the screen.
        """
        if not hasattr(self, 'previous_value'):
            # Automatically select the first value to prevent empty selection
            self.previous_value = [0] #pylint: disable=attribute-defined-outside-init

        self.ml_output_types.value = self.previous_value

    def create(self):
        if self.parentApp.is_substream:
            package_modules = load_substream_package(self.parentApp.stub_config['request']['params']['modules'])['modules']['modules']
            selected_output_modules = []
            try:
                selected_output_modules += self.parentApp.stub_config['request']['params']['output_modules']
            except KeyError:
                try:
                    selected_output_modules += [self.parentApp.stub_config['request']['params']['output_module']]
                except KeyError:
                    logging.error('No output module(s) specified for substream')
                    raise

            output_modules = [
                m for m in package_modules if m['name'] in selected_output_modules
            ]

            logging.info('[%s] Selected modules : %s', self.name, selected_output_modules)
            logging.info('[%s] Modules from package : %s', self.name,
                hjson.dumps(output_modules, indent=4)
            )

            self.output_descriptors = []
            output_types = []
            for module in output_modules:
                if 'output' in module:
                    self.output_descriptors.append(
                        Config.PROTO_MESSAGES_CLASSES[module['output']['type'].rsplit(':', 1)[1]].DESCRIPTOR
                    )
                    output_types.append(f'{module["name"]} ({self.output_descriptors[-1].full_name})')
        else:
            self.output_descriptors = [
                # TODO: Remove 'Block' naming convention assumption ?
                m_class.DESCRIPTOR for m_name, m_class in Config.PROTO_MESSAGES_CLASSES.items()
                if m_name.rsplit('.', 1)[1].lower() == 'block'
            ]
            output_types = [desc.full_name for desc in self.output_descriptors]

        self.ml_output_types = self.add(
            OutputTypesTitleSelectOne,
            name='Select an output type :',
            values=output_types,
            value=[0],
            scroll_exit=True,
            # First call to `get_half_way` will set the split line
            max_height=self.get_half_way(self.curses_pad.getmaxyx()[0] // 3) - 2
        )

        self.saved_output_selection = {}
        self.ml_output_select = self.add(
            OutputSelectionMLTreeMultiSelectAnnotated,
            name='Select which data to save from the output :',
            values=self.create_output_selection(),
            scroll_exit=True,
            rely=self.get_half_way() + 1
        )

    def create_output_selection(self, previous_selected: dict[tuple[int, str], tuple[int, int]] | None = None) -> OutputSelectionTreeData:
        """
        Create the output field selection tree from the selected output type. If `previous_selected` is supplied,
        the state of the node in the tree (`selected` and `expanded`) will be set according to its description.

        Args:
            previous_selected: A dictionnary with a node's (depth, content) as key and its state (selected, expanded) as value.

        Returns:
            The root node of the selection tree.
        """
        def _make_tree_node(
                node: OutputSelectionTreeData,
                descriptor: Descriptor,
                previous_desc: Descriptor | None = None,
                previous_selected: dict[tuple[int, str], tuple[int, int]] | None = None
            ) -> None:
            """
            Recursively append nodes from the `descriptor` fields to create the selection tree.

            Args:
                node: The current node in the tree.
                descriptor: The next descriptor if the field is a `Message` type.
                previous_desc: Parent descriptor to prevent infinite inclusion of `Message` types.
                previous_selected: See `create_output_selection()` documentation.
            """
            for field in descriptor.fields:
                child = node.new_child(content=field.name)
                child.expanded = False
                if previous_selected:
                    try:
                        child.selected, child.expanded = previous_selected[(child.find_depth(), child.get_content())]
                    except KeyError:
                        pass

                # Prevent recursive field inclusion
                if field.message_type and field.message_type != previous_desc:
                    _make_tree_node(child, field.message_type, descriptor, previous_selected)

        output_tree = OutputSelectionTreeData()
        root_element = output_tree.new_child(
            content='(select this to select all)',
            annotate='Select which data to save from the output',
            annotate_color='STANDOUT'
        )

        _make_tree_node(root_element, self.output_descriptors[self.ml_output_types.value[0]], previous_selected=previous_selected)

        return output_tree

    def on_ok(self):
        def _build_output_params(node: OutputSelectionTreeData) -> dict | str:
            if not node.has_children():
                # TODO: Extend custom TreeData functionality with 'Required' and 'Optional' output fields
                return "True"

            out = {}
            for child in node.get_children():
                if child.selected:
                    out[child.get_content()] = _build_output_params(child)

            return out if out else "True"

        self.previous_value = list(self.ml_output_types.value) #pylint: disable=attribute-defined-outside-init

        output_params = {}
        if self.parentApp.is_substream:
            # Simulate switching output types to generate the output parameters for each module
            output_modules = [v.split(' ', 1)[0] for v in self.ml_output_types.values]
            for output_module in output_modules:
                self.ml_output_types.entry_widget.cursor_line = output_modules.index(output_module)
                self.ml_output_types.entry_widget.actionHighlighted(None, None)
                output_params[output_module] = _build_output_params(self.ml_output_select.values[0])
        else:
            output_params = _build_output_params(self.ml_output_select.values[0])

        logging.info('[%s] Output params : %s', self.name, output_params)

        # TODO: Load previous output params from stub config file => NEED ADDING OUTPUT TYPE OBJECT TO STUB CONFIG !
        self.parentApp.stub_config['response']['params'] = output_params

        self.parentApp.addForm(
            self.parentApp.STUB_CONFIG_CONFIRM_EDIT_FORM,
            StubConfigConfirmEditForm, name='Stub config editing - Confirm'
        )
        self.parentApp.setNextForm(self.parentApp.STUB_CONFIG_CONFIRM_EDIT_FORM)

    def on_cancel(self):
        del self.previous_value
        self.parentApp.setNextFormPrevious()

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
