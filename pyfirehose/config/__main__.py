"""
SPDX-License-Identifier: MIT
"""

import logging
import os.path
from typing import Optional

import grpc
import hjson
from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem, FunctionItem
from grpc_reflection.v1alpha.proto_reflection_descriptor_database import ProtoReflectionDescriptorDatabase
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.descriptor_pool import DescriptorPool

# Prevent circular import with 'check_period'
from pyfirehose.args import check_period
from pyfirehose.config.utils import Config, StubConfig
from pyfirehose.config.utils import load_config, load_stub_config
from pyfirehose.utils import get_auth_token

def get_parameter_input(item: MenuItem, msg: Optional[str] = 'Enter an input : ', 
                        default_value: Optional[str] = '') -> str:
    val = input(msg) if not default_value else default_value
    try:
        item.text = f'{item.text[:item.text.rindex("=")]}={val if val else "None"}'
    except ValueError:
        item.text = f'{item.text}={val if val else "None"}'

    return val

def make_selection(options: list[str], title: str = 'Pyfirehose config', subtitle: str = '') -> str:
    return options[CursesMenu.get_selection(
        options,
        title=title,
        subtitle=subtitle
    )]

def type_to_string(type_: int) -> str:
    return dict( #pylint: disable=consider-using-dict-comprehension
        [(value, key.split('_')[1]) for key, value in vars(FieldDescriptor).items() if 'TYPE_' in key and not 'CPP' in key]
    )[type_]

def main() -> int:
    """
    Main
    """
    logging.basicConfig(
        handlers=[logging.FileHandler('logs/config.log', mode='w')],
        level=logging.INFO,
        format='%(asctime)s:T+%(relativeCreated)d %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True
    )

    logging.addLevelName(logging.DEBUG, '[DEBUG]')
    logging.addLevelName(logging.INFO, '[*]')
    logging.addLevelName(logging.WARNING, '[!]')
    logging.addLevelName(logging.ERROR, '[ERROR]')
    logging.addLevelName(logging.CRITICAL, '[CRITICAL]')

    file = 'pyfirehose/config.hjson'
    with open(file, 'r', encoding='utf8') as config_file:
        try:
            main_config = hjson.load(config_file)
        except hjson.HjsonDecodeError as error:
            logging.exception('Error decoding main config file (%s): %s', file, error)
            raise

    endpoints = main_config['grpc']

    selected_endpoint = make_selection([f"{e['id']}" for e in endpoints], subtitle='Select an endpoint')
    logging.info('Selected endpoint : %s', selected_endpoint)

    stub_loaded = load_config(file, selected_endpoint)
    default_stub_filepath = 'pyfirehose/config/default.hjson'
    stub_save_file = input(
        'Edit "'
        f'{next((e["stub"] for e in endpoints if e["id"] == selected_endpoint)) if stub_loaded else default_stub_filepath}'
        '" config file (enter path to change or press [ENTER]) : '
    )

    if not stub_save_file and not stub_loaded:
        stub_save_file = default_stub_filepath

    if stub_save_file:
        try:
            load_stub_config(stub_save_file)
        except FileNotFoundError:
            if stub_loaded:
                # If user wants to edit new config than the one loaded, reset it
                # TODO : Ask user if wants to keep previous loaded values for new file (?)
                StubConfig.REQUEST_PARAMETERS = {}

    jwt = get_auth_token()
    creds = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(),
        grpc.access_token_call_credentials(jwt)
    )

    channel = grpc.secure_channel(Config.GRPC_ENDPOINT, creds)
    reflection_db = ProtoReflectionDescriptorDatabase(channel)

    services = reflection_db.get_services()
    logging.info('Services : %s', services)

    desc_pool = DescriptorPool(reflection_db)

    selected_service = make_selection(services, subtitle='Select a service')
    is_substreams = 'substreams' in selected_service
    logging.info('Selected service : %s', selected_service)
    logging.info('[%s] Is using substreams ? %s', selected_service, is_substreams)

    methods = desc_pool.FindServiceByName(selected_service).methods
    logging.info('[%s] Methods : %s', selected_service, [m.name for m in methods])

    selected_method = make_selection([m.name for m in methods], subtitle='Select a method')
    selected_method = next((m for m in methods if m.name == selected_method), None)
    logging.info('Selected method : %s', selected_method.name)
    logging.info('[%s:%s] Input : %s / Output : %s',
        selected_service,
        selected_method.name,
        [f'{f.type}:{f.name}' for f in selected_method.input_type.fields],
        [f'{f.type}:{f.name}' for f in selected_method.output_type.fields]
    )

    menu = CursesMenu('Pyfirehose config', 'Configure gRPC request')

    for input_parameter in [
        f for f in selected_method.input_type.fields if not f.name in ('start_block_num', 'stop_block_num')
    ]:
        function_item = FunctionItem(f'{input_parameter.name}:{type_to_string(input_parameter.type)}', get_parameter_input)
        function_item.args = [function_item]
        try:
            if is_substreams and input_parameter.name == 'modules':
                function_item.return_value = StubConfig.SUBSTREAMS_PACKAGE_FILE
            else:
                function_item.return_value = StubConfig.REQUEST_PARAMETERS[input_parameter.name]

            get_parameter_input(function_item, default_value=function_item.return_value)
        except KeyError:
            get_parameter_input(function_item, default_value='None')

        menu.items.append(function_item)

    menu.show()

    for item in menu.items:
        logging.info('[Item] %s : %s', item.text, item.get_return())
        key, value = (item.text.split(':')[0], item.get_return())
        StubConfig.REQUEST_PARAMETERS[key] = value
    logging.info('StubConfig : %s', vars(StubConfig))

    # TODO: Response config menu

    stub_config = {}
    if os.path.isfile(stub_save_file):
        with open(stub_save_file, 'r', encoding='utf8') as config_file:
            try:
                stub_config = hjson.load(config_file)
            except hjson.HjsonDecodeError as error:
                logging.exception('Error decoding stub config file (%s): %s', file, error)
                raise
    else:
        stub_config['python_import_dir'], stub_config['name'] = selected_service.rsplit('.', 1)
        stub_config['request'] = selected_method.input_type.name

    stub_config['parameters'] = {key: value for (key, value) in StubConfig.REQUEST_PARAMETERS.items() if value}
    logging.info('Saved stub config : %s', stub_config)

    with open(stub_save_file, 'w+', encoding='utf8') as config_file:
        hjson.dumpJSON(stub_config, config_file, indent=4)

    return 0

if __name__ == '__main__':
    main()
