# Pinax - PyFirehose

> Extract bulk and targeted historical blockchain data (powered by [**Firehose**](https://firehose.streamingfast.io/) and [**Substreams**](https://substreams.streamingfast.io))

[![Pylint](https://github.com/pinax-network/pyfirehose/actions/workflows/pylint.yml/badge.svg)](https://github.com/pinax-network/pyfirehose/actions/workflows/pylint.yml) [![Deploy Website](https://github.com/pinax-network/pyfirehose/actions/workflows/static.yml/badge.svg)](https://github.com/pinax-network/pyfirehose/actions/workflows/static.yml)

## Overview

*PyFirehose* is a data extraction tool leveraging the power of [**Firehose**](https://firehose.streamingfast.io/) and [**Substreams**](https://substreams.streamingfast.io) innovative technologies for accessing any blockchain-related data. It acts as an easy-to-use interface to communicate with gRPC endpoints, simplifying the process of extracting data that matters to *you*. 

Using a flexible approach, you can review and select which information to extract in the final output (JSONL is the default but it's entierly up to you how the data looks like at the end). You can then use this data to power other applications (see [`index.ipynb`](index.ipynb) for an example of building a chart of account transfers) or for your own purpose.  

## Quickstart

**Requires Python >= 3.10**

```console
$ git clone git@github.com:pinax-network/pyfirehose.git
$ cd pyfirehose
$ vim pyfirehose/sample.config.hjson # Edit sample config file with editor of your choice to add your API keys
$ mv pyfirehose/sample.config.hjson pyfirehose/config.hjson # Rename to config.hjson
$ python3 -m venv .venv # Create virtual environnement
$ source .venv/bin/activate # Activate virtual environnement
(.venv) $ pip install -r requirements.txt # Install dependencies
(.venv) $ python -m pyfirehose -h
usage: __main__.py [-h] [-c CONFIG] [-s STUB] [-o OUT_FILE] [-l [LOG]] [-q] [-g GRPC_ENTRY] [-e {optimized,single,multi}] [-p CUSTOM_PROCESSOR]
                   [--no-json-output] [--overwrite-log] [--request-parameters ...]
                   start end

Extract any data from the blockchain. Powered by Firehose (https://eos.firehose.eosnation.io/) and Substreams (https://substreams.streamingfast.io).

positional arguments:
  start                 period start as a date (iso-like format) or a block number
  end                   period end as a date (iso-like format) or a block number

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config file path in HJSON or JSON format (default: pyfirehose/config.hjson)
  -s STUB, --stub STUB  stub config file path in HJSON or JSON format (default: None)
  -o OUT_FILE, --out-file OUT_FILE
                        output file path (default: jsonl/{chain}_{start}_to_{end}.jsonl)
  -l [LOG], --log [LOG]
                        log debug information to log file (can specify the full path) (default: logs/{datetime}.log)
  -q, --quiet           disable console logging (default: False)
  -g GRPC_ENTRY, --grpc-entry GRPC_ENTRY
                        id of a grpc entry in the "grpc" array found in the main config file (default: None)
  -e {optimized,single,multi}, --extractor {optimized,single,multi}
                        type of extractor used for streaming blocks from the gRPC endpoint (default: optimized)
  -p CUSTOM_PROCESSOR, --custom-processor CUSTOM_PROCESSOR
                        name of a custom block processing function located in the "block_processors.processors" module (default: default_block_processor)
  --no-json-output      don't try to convert block processor output to JSON (default: False)
  --overwrite-log       overwrite log file, erasing its content (default is to append) (default: False)
  --request-parameters ...
                        optional keyword arguments (key=val) sent with the gRPC request (must match .proto definition, will override any parameters set in
                        the config) (default: None)
```

The period's *start* and *end* accepts either a block number or a [ISO-like formatted date time](https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat). By default, the extracted data will be stored in a `.jsonl` file inside the [`jsonl/`](jsonl/) directory.

A [`.pylintrc`](.pylintrc) file is provided if you want to run [Pylint](https://pypi.org/project/pylint/):
```console
(.venv) user@dev-eosnation:~/Documents/pyfirehose$ pylint pyfirehose --rcfile=.pylintrc
```

Auto-generated documentation can be browsed [here](https://krow10.github.io/pyfirehose/docs).

## Editing configuration files

The settings values are stored in a `config.hjson` file located in the [`pyfirehose/`](pyfirehose/) folder. A sample file is provided as [`sample.config.hjson`](pyfirehose/sample.config.hjson) that you can rename after adding your API keys.

For using [Pinax](https://pinax.network) based endpoints, go to https://pinax.network/ and create a free account for registering an API key.
For using [StreamingFast](https://streamingfast.io) based endpoints, go to https://app.streamingfast.io/ and create a free account for registering an API key.

Replace the placeholder values with the optained API keys in the config file:
```json
"auth": {
  "pinax": {
    "api_key": "<YOUR_API_KEY>",
    "endpoint": "https://auth.pinax.network/v1/auth/issue"
  },
  "streamingfast": {
    "api_key": "<YOUR_API_KEY>",
    "endpoint": "https://auth.streamingfast.io/v1/auth/issue"
  }
}
```

The format chosen, [`hjson`](https://hjson.github.io/hjson-py/), allow for adding comments to the config file but is fully compatible with plain JSON. You can extend the list of endpoints by adding entries to the `grpc` array following the format:
```json
{
  "id": "<string for identifying the gRPC entry (used as default or CLI argument)>",
  "auth": "<reference an 'auth' entry to authenticate with the gRPC endpoint>",
  "chain": "<the target blockchain (for information purpose only)>",
  "compression": "<compression method for gRPC messages, must be one of 'gzip' or 'deflate' if specified (no compression by default)>",
  "stub": "<path to a stub config file (optional, must be supplied as CLI argument if not specified here)>",
  "url": "<the gRPC endpoint url as 'ip:port'>"
}
```

Stubs (python-generated objects for communicating with the gRPC endpoint) configuration files must be specified in order for the tool to know how to communicate with the remote endpoint. Examples are provided in the [`pyfirehose/config/`](pyfirehose/config/) folder for reference. Since `.proto` files dictates every aspect of the block streaming process, refer to them for filling the stub config file. 

The template for stub config files looks like the following:
```json
{
  "python_import_dir": "<location of .proto file template used by gRPC endpoint (example: dfuse.bstream.v1)>",
  "name": "<name of the gRPC service used for the communication (example: BlockStreamV2)>",
  "request": "<type of the request as specified in the .proto file (example: BlocksRequestV2)>",
  "parameters": "<key-value pairs sent as the request parameters (refer to .proto file)>",
}
```

If the gRPC endpoint uses different protobuf definitions than the ones already provided, you will need to add the appropriate files to the [`proto/`](pyfirehose/proto/) folder and generate the python stubs (see following section).

### Protobuf

To communicate with the gRPC endpoint, Python objects are generated using `.proto` template files that describes the kind of data the client and server are going to manipulate. Those Python objects are already provided in the [`proto/generated/`](pyfirehose/proto/generated/) folder, however if you want to generate them yourself for adding new `.proto` definitions, use the provided script [`build_proto.sh`](pyfirehose/proto/build_proto.sh):

```console
$ cd proto/ # Must cd in directory
foo@bar:~/pyfirehose/proto$ ./build_proto.sh
```

*Note: you **must** add your own `.proto` files definitions inside the [`pyfirehose/proto`](pyfirehose/proto) directory with the folder hierarchy matching the `import` statements of the `.proto` files in order to successfully generate the Python stubs.*

### gRPC endpoints support

#### Currently implemented

Below is a list of the gRPC endpoints which have a default ready-to-use [stub config](pyfirehose/config/) and [processor](pyfirehose/block_processors) available for extracting blocks. All data available in the gRPC block response (as defined in their respective [`.proto` files](pyfirehose/proto/)) will be available upon completion.

### Using the config UI tool to edit config files

An early version of a GUI tool for editing configuration files is available to make it easier to manage, add, edit and delete gRPC endpoints and their stub configurations.

Simply run in the console :

```console
(.venv) $ python -m pyfirehose.config
```

In the first screen you will be able to see you main config file with all the listed endpoints. Use `Ctrl-X` to bring up a menu allowing edition of stub configuration files (*main config edit still WIP*). Go through the screens customizing which endpoint, service and method you want to use and specify at the end the request input parameters.

**Note: for substreams enabled endpoints, specify the path to a `.spkg` file for the `modules` parameter.**

See the [demo](#config-ui-tool-demo-for-substreams) at the bottom of this page for an example configuration using the [`eosio.token` Antelope substream](https://github.com/EOS-Nation/substreams-antelope/tree/develop/substreams/eosio.token) on `eos.firehose.eosnation.io:9001`. 

## Writing custom block processors

For even more control over the data extracted, the extraction process uses a modular approach for manipulating `Block` response objects coming from the gRPC stream. A block processing function is used for extracting the data that is later stored in the output file at the end of the block extraction process. Customizing which data is extracted is the main goal of writing a custom block processor.

In order to write custom block processing functions, some conditions must be respected:
- The function should be placed inside the [`processors.py`](pyfirehose/block_processors/processors.py) file in the [`block_processors`](pyfirehose/block_processors/) module (try to avoid name conflicts).
- The function should act as a **generator** (using the `yield` keyword) to return the data.
- The **first parameter** of the function should take the raw block extracted from the gRPC stream.

Since the function is getting the raw block, you should unpack it according to the `.proto` file definition the gRPC stream is using. For example, if you use Firehose v2 gRPC on Antelope chain, the block response is defined in the [`type.proto`](pyfirehose/proto/sf/antelope/type/v1/type.proto) file and you would unpack the raw data like the following:

```python
from proto.generated.sf.antelope.type.v1 import type_pb2

block = type_pb2.Block()
raw_block.Unpack(block)
``` 

If using Firehose v1 filters, a typical template for parsing the block data would look like the following:
```python
  block = codec_pb2.Block()
  raw_block.Unpack(block)

  for transaction_trace in block.filtered_transaction_traces: # Gets every filtered TransactionTrace from a Block
    for action_trace in transaction_trace.action_traces: # Gets every ActionTrace within a TransactionTrace
      if not action_trace.filtering_matched: # Only keep 'transfer' actions that matched the filters
        continue

      data = {}
      
      # Process the data...

      yield data # Make the function act as a generator
```

See the block processors in the [`block_processors/processors.py`](pyfirehose/block_processors/processors.py) file for more details. The default one extract all the block information (as defined in the proto files) as JSON.

You can then use custom block processors through the command-line using the `--custom-processor` (or `-p`) argument and providing the name of the function. 

For example, let's say you've implemented a custom function `my_block_processor` in `processors.py`. You would then pass the argument as `--custom-processor my_block_processor`. The script will locate it inside the `processors.py` module and use the `my_block_processor` function to parse block data and extract it to the output file.

## Additional information

### Using Firehose v1 filters

The `eos_firehose_v1` gRPC endpoint uses *include* and *exclude* filters for selecting blocks of interest directly within the gRPC block stream.
An example for extracting *transfer* information related to certain accounts is available in the [`producerpay.hjson`](pyfirehose/config/dfuse/producerpay.hjson) stub config file.

For full documentation about the syntax and variables available in the filter expressions, see the [Firehose documentation](https://github.com/streamingfast/playground-firehose-eosio-go#query-language).

*Note: the Firehose v1 is getting deprecated and will soon be replaced by the [Firehose v2](https://github.com/streamingfast/proto/blob/develop/sf/firehose/v2/firehose.proto) version.*

### Input

#### Main config

```json
{
  "default": "eos_firehose_v1",

  "max_block_size": 8388608,

  "auth": {
    "eosnation": {
      "api_key": "<REDACTED>",
      "endpoint": "https://auth.eosnation.io/v1/auth/issue"
    }
  },

  "graphql_endpoint": "https://eos.dfuse.eosnation.io/graphql",

  "grpc": [
    {
      "id": "eos_firehose_v1",
      "auth": "eosnation",
      "chain": "EOS",
      "stub": "pyfirehose/config/dfuse/producerpay.hjson",
      "url": "eos.firehose.eosnation.io:9000",
    },
  ]
}
```

#### `producerpay.hjson` stub config

```json
{
  "python_import_dir": "dfuse.bstream.v1",
  "name": "BlockStreamV2",
  "request": "BlocksRequestV2",
  "parameters": {
    "fork_steps": [
      "STEP_IRREVERSIBLE"
    ],
    "include_filter_expr": "receiver in ['eosio.bpay', 'eosio.vpay'] && action == 'transfer'",
    "exclude_filter_expr": "data['to'] in ['eosio.bpay', 'eosio.vpay']"
  }
}
```

#### Command-line

```console
(.venv) $ python pyfirehose 272368521 272369521 --quiet --log logs/eosio_pay.log --out jsonl/out.jsonl
```

### Output (jsonl/out.jsonl)

```jsonl
{"account": "eosio.bpay", "date": "2022-10-10 00:02:56", "timestamp": 1665360176, "amount": "344.5057", "token": "EOS", "from": "eosio.bpay", "to": "newdex.bp", "block_num": 272368850, "transaction_id": "22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6", "memo": "producer block pay", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.vpay", "date": "2022-10-10 00:02:56", "timestamp": 1665360176, "amount": "698.0213", "token": "EOS", "from": "eosio.vpay", "to": "newdex.bp", "block_num": 272368850, "transaction_id": "22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6", "memo": "producer vote pay", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.bpay", "date": "2022-10-10 00:00:12", "timestamp": 1665360012, "amount": "343.8791", "token": "EOS", "from": "eosio.bpay", "to": "aus1genereos", "block_num": 272368521, "transaction_id": "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75", "memo": "producer block pay", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.vpay", "date": "2022-10-10 00:00:12", "timestamp": 1665360012, "amount": "675.7402", "token": "EOS", "from": "eosio.vpay", "to": "aus1genereos", "block_num": 272368521, "transaction_id": "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75", "memo": "producer vote pay", "contract": "eosio.token", "action": "transfer"}
```

### Log file sample (logs/eosio_pay.log)

```
2022-11-29 14:55:59:T+189 [DEBUG] Script arguments: Namespace(start=272368521, end=272369521, config='pyfirehose/config.hjson', stub=None, out_file='jsonl/out.jsonl', log='logs/eosio_pay.log', quiet=True, grpc_entry=None, extractor='optimized', custom_processor=None, request_parameters={})
2022-11-29 14:55:59:T+190 [DEBUG] Main config: mappingproxy({'API_KEY': '<REDACTED>',
              'AUTH_ENDPOINT': 'https://auth.eosnation.io/v1/auth/issue',
              'CHAIN': 'EOS',
              'GRAPHQL_ENDPOINT': 'https://eos.dfuse.eosnation.io/graphql',
              'GRPC_ENDPOINT': 'eos.firehose.eosnation.io:9000',
              'MAX_BLOCK_SIZE': 8388608,
              [...]
2022-11-29 14:55:59:T+191 [DEBUG] Stub config: mappingproxy({'REQUEST_OBJECT': <class 'dfuse.bstream.v1.bstream_pb2.BlocksRequestV2'>,
              'REQUEST_PARAMETERS': {'exclude_filter_expr': "data['to'] in "
                                                            "['eosio.bpay', "
                                                            "'eosio.vpay']",
                                     'fork_steps': ['STEP_IRREVERSIBLE'],
                                     'include_filter_expr': 'receiver in '
                                                            "['eosio.bpay', "
                                                            "'eosio.vpay'] && "
                                                            'action == '
                                                            "'transfer'"},
              'STUB_OBJECT': <class 'proto.generated.dfuse.bstream.v1.bstream_pb2_grpc.BlockStreamV2Stub'>,
              [...]
2022-11-29 14:26:53:T+194 [DEBUG] Initializing backend: None jwt_token
2022-11-29 14:26:53:T+194 [DEBUG] Initializing SQLitePickleDict with serializer: <requests_cache.serializers.pipeline.SerializerPipeline object at 0x76a949847250>
2022-11-29 14:26:53:T+195 [DEBUG] Opening connection to /home/user/Documents/eos-blockchain-data/jwt_token.sqlite:responses
2022-11-29 14:26:53:T+195 [DEBUG] Initializing SQLiteDict with serializer: <requests_cache.serializers.pipeline.SerializerPipeline object at 0x76a949847250>
2022-11-29 14:26:53:T+195 [DEBUG] Opening connection to /home/user/Documents/eos-blockchain-data/jwt_token.sqlite:redirects
2022-11-29 14:26:53:T+196 [*] Getting JWT token...
2022-11-29 14:26:53:T+199 [DEBUG] Cache directives from request headers: {}
2022-11-29 14:26:53:T+202 [DEBUG] JWT response: {'token': '<REDACTED>', 'expires_at': 1669823698}
2022-11-29 14:26:53:T+202 [*] Got JWT token (cached) [SUCCESS]
2022-11-29 14:26:53:T+202 [DEBUG] Using selector: EpollSelector
2022-11-29 14:26:53:T+203 [*] Streaming 1000 blocks on EOS chain (running 25 workers)...
2022-11-29 14:26:53:T+203 [DEBUG] Initializing backend: None jwt_token
2022-11-29 14:26:53:T+203 [DEBUG] Initializing SQLitePickleDict with serializer: <requests_cache.serializers.pipeline.SerializerPipeline object at 0x76a949847250>
2022-11-29 14:26:53:T+203 [DEBUG] Opening connection to /home/user/Documents/eos-blockchain-data/jwt_token.sqlite:responses
2022-11-29 14:26:53:T+203 [DEBUG] Initializing SQLiteDict with serializer: <requests_cache.serializers.pipeline.SerializerPipeline object at 0x76a949847250>
2022-11-29 14:26:53:T+203 [DEBUG] Opening connection to /home/user/Documents/eos-blockchain-data/jwt_token.sqlite:redirects
2022-11-29 14:26:53:T+204 [*] Getting JWT token...
2022-11-29 14:26:53:T+204 [DEBUG] Cache directives from request headers: {}
2022-11-29 14:26:53:T+205 [DEBUG] JWT response: {'token': '<REDACTED>', 'expires_at': 1669823698}
2022-11-29 14:26:53:T+205 [*] Got JWT token (cached) [SUCCESS]
2022-11-29 14:26:53:T+206 [DEBUG] Using AsyncIOEngine.POLLER as I/O engine
2022-11-29 14:26:53:T+209 [DEBUG] [Task-02] Starting streaming blocks from #272368521 to #272368560...
2022-11-29 14:26:53:T+209 [DEBUG] [Task-03] Starting streaming blocks from #272368561 to #272368600...
2022-11-29 14:26:53:T+209 [DEBUG] [Task-04] Starting streaming blocks from #272368601 to #272368640...
2022-11-29 14:26:53:T+209 [DEBUG] [Task-05] Starting streaming blocks from #272368641 to #272368680...
2022-11-29 14:26:53:T+209 [DEBUG] [Task-06] Starting streaming blocks from #272368681 to #272368720...
2022-11-29 14:26:53:T+209 [DEBUG] [Task-07] Starting streaming blocks from #272368721 to #272368760...
2022-11-29 14:26:53:T+209 [DEBUG] [Task-08] Starting streaming blocks from #272368761 to #272368800...
2022-11-29 14:26:53:T+209 [DEBUG] [Task-09] Starting streaming blocks from #272368801 to #272368840...
2022-11-29 14:26:53:T+209 [DEBUG] [Task-10] Starting streaming blocks from #272368841 to #272368880...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-11] Starting streaming blocks from #272368881 to #272368920...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-12] Starting streaming blocks from #272368921 to #272368960...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-13] Starting streaming blocks from #272368961 to #272369000...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-14] Starting streaming blocks from #272369001 to #272369040...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-15] Starting streaming blocks from #272369041 to #272369080...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-16] Starting streaming blocks from #272369081 to #272369120...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-17] Starting streaming blocks from #272369121 to #272369160...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-18] Starting streaming blocks from #272369161 to #272369200...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-19] Starting streaming blocks from #272369201 to #272369240...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-20] Starting streaming blocks from #272369241 to #272369280...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-21] Starting streaming blocks from #272369281 to #272369320...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-22] Starting streaming blocks from #272369321 to #272369360...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-23] Starting streaming blocks from #272369361 to #272369400...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-24] Starting streaming blocks from #272369401 to #272369440...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-25] Starting streaming blocks from #272369441 to #272369480...
2022-11-29 14:26:53:T+210 [DEBUG] [Task-26] Starting streaming blocks from #272369481 to #272369521...
2022-11-29 14:26:55:T+1711 [DEBUG] [Task-04] Getting block number #272368601 (39 blocks remaining)...
2022-11-29 14:26:55:T+1712 [DEBUG] [Task-07] Getting block number #272368721 (39 blocks remaining)...
[...]
2022-11-29 14:27:02:T+8806 [*] Block streaming done !
2022-11-29 14:27:02:T+8812 [DEBUG] Data: {'account': 'eosio.bpay', 'date': '2022-10-10 00:02:56', 'timestamp': 1665360176, 'amount': '344.5057', 'token': 'EOS', 'from': 'eosio.bpay', 'to': 'newdex.bp', 'block_num': 272368850, 'transaction_id': '22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6', 'memo': 'producer block pay', 'contract': 'eosio.token', 'action': 'transfer'}
2022-11-29 14:27:02:T+8812 [DEBUG] Data: {'account': 'eosio.vpay', 'date': '2022-10-10 00:02:56', 'timestamp': 1665360176, 'amount': '698.0213', 'token': 'EOS', 'from': 'eosio.vpay', 'to': 'newdex.bp', 'block_num': 272368850, 'transaction_id': '22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6', 'memo': 'producer vote pay', 'contract': 'eosio.token', 'action': 'transfer'}
2022-11-29 14:27:02:T+8817 [DEBUG] Data: {'account': 'eosio.bpay', 'date': '2022-10-10 00:00:12', 'timestamp': 1665360012, 'amount': '343.8791', 'token': 'EOS', 'from': 'eosio.bpay', 'to': 'aus1genereos', 'block_num': 272368521, 'transaction_id': 'e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75', 'memo': 'producer block pay', 'contract': 'eosio.token', 'action': 'transfer'}
2022-11-29 14:27:02:T+8817 [DEBUG] Data: {'account': 'eosio.vpay', 'date': '2022-10-10 00:00:12', 'timestamp': 1665360012, 'amount': '675.7402', 'token': 'EOS', 'from': 'eosio.vpay', 'to': 'aus1genereos', 'block_num': 272368521, 'transaction_id': 'e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75', 'memo': 'producer vote pay', 'contract': 'eosio.token', 'action': 'transfer'}
2022-11-29 14:27:02:T+8819 [*] Finished block processing, parsed 4 rows of data [SUCCESS]
2022-11-29 14:27:02:T+8820 [*] Wrote 4 rows of data to jsonl/out.jsonl [SUCCESS]
```