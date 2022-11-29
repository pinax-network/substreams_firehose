# EOSNation - Blockchain Data for Analytics (Python version)

> Aggregates historical blockchain data & outputs result in JSONL format (powered by [**Firehose**](https://eos.firehose.eosnation.io/) and [**Substreams**](https://substreams.streamingfast.io))

[![Pylint](https://github.com/Krow10/eos-blockchain-data/actions/workflows/pylint.yml/badge.svg)](https://github.com/Krow10/eos-blockchain-data/actions/workflows/pylint.yml)

[![Extract Firehose](https://github.com/Krow10/eos-blockchain-data/actions/workflows/firehose_daily_extraction.yml/badge.svg)](https://github.com/Krow10/eos-blockchain-data/actions/workflows/firehose_daily_extraction.yml)
[![Update Index](https://github.com/Krow10/eos-blockchain-data/actions/workflows/update_index_notebook.yml/badge.svg)](https://github.com/Krow10/eos-blockchain-data/actions/workflows/update_index_notebook.yml)
[![Deploy Website](https://github.com/Krow10/eos-blockchain-data/actions/workflows/static.yml/badge.svg)](https://github.com/Krow10/eos-blockchain-data/actions/workflows/static.yml)

## Github Actions workflow

This repo uses Github actions to automatically fetch transactions related to EOS block producer's (BP) addresses payments, parse them and generate a [Sankey chart](https://en.wikipedia.org/wiki/Sankey_diagram) for visualizing the flow of funds. Below is a flow diagram showing what the actual pipeline looks like:

![Github actions workflow pipeline](github_actions_workflow.png)

You can see the rendered chart [here](https://krow10.github.io/eos-blockchain-data/) at the bottom of the page.

## Quickstart

```console
foo@bar:~$ git clone git@github.com:Krow10/eos-blockchain-data.git
foo@bar:~$ cd eos-blockchain-data
foo@bar:~/eos-blockchain-data$ vim pyfirehose/sample.config.hjson # Edit sample config file with editor of your choice to add your API keys
foo@bar:~/eos-blockchain-data$ mv pyfirehose/sample.config.hjson pyfirehose/config.hjson # Rename to config.hjson
foo@bar:~/eos-blockchain-data$ python3 -m venv .venv # Create virtual environnement
foo@bar:~/eos-blockchain-data$ source .venv/bin/activate # Activate virtual environnement
(.venv) foo@bar:~/eos-blockchain-data$ pip install -r requirements.txt # Install dependencies
(.venv) foo@bar:~/eos-blockchain-data$ python pyfirehose -h
usage: pyfirehose [-h] [-c CONFIG] [-s STUB] [-o OUT_FILE] [-l [LOG]] [-q] [-g GRPC_ENTRY] [-e {optimized,single,multi}] [-p CUSTOM_PROCESSOR]               
                  [--no-json-output] [--request-parameters ...]                                                                                              
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
                        type of extractor used for streaming blocks from the Firehose endpoint (default: optimized)
  -p CUSTOM_PROCESSOR, --custom-processor CUSTOM_PROCESSOR
                        relative import path to a custom block processing function located in the "block_processors" module (default: None)
  --no-json-output      don't try to convert block processor output to JSON (default: False)
  --request-parameters ...
                        optional keyword arguments (key=val) sent with the gRPC request (must match .proto definition, will override any parameters set in
                        the config) (default: None)
```

The period's *start* and *end* accepts either a block number or a [ISO-like formatted date time](https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat). By default, the extracted data will be stored in a `.jsonl` file inside the [`jsonl/`](jsonl/) directory.

A [`.pylintrc`](.pylintrc) file is provided if you want to run [Pylint](https://pypi.org/project/pylint/):
```console
(.venv) user@dev-eosnation:~/Documents/eos-blockchain-data$ pylint pyfirehose --rcfile=.pylintrc
```

## Editing configuration files

The settings values are stored in a `config.hjson` file located in the [`pyfirehose/`](pyfirehose/) folder. A sample file is provided as [`sample.config.hjson`](pyfirehose/sample.config.hjson) that you can rename after adding your API keys.

For using [EOSNation](https://eosnation.io) based endpoints, go to https://dfuse.eosnation.io/ and create a free account for registering an API key.
For using [StreamingFast](https://streamingfast.io) based endpoints, go to https://app.streamingfast.io/ and create a free account for registering an API key.

Replace the placeholder values with the optained API keys in the config file:
```json
"auth": {
  "eosnation": {
    "api_key": "<YOUR_API_KEY>",
    "endpoint": "https://auth.eosnation.io/v1/auth/issue"
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

To communicate with the gRPC endpoint, Python objects are generated using `.proto` template files that describes the kind of data the client and server are going to manipulate. Those Python objects are already provided in the [`proto/generated/`](pyfirehose/proto/generated/) folder, however if you want to generate them yourself, you can run the following commands:
```console
(.venv) foo@bar:~/eos-blockchain-data$ pip install grpcio-tools
(.venv) foo@bar:~/eos-blockchain-data$ cd pyfirehose/proto
(.venv) foo@bar:~/eos-blockchain-data/pyfirehose/proto$ python -m grpc_tools.protoc -I. --python_out=generated/ --grpc_python_out=generated/ $(find . -iname *.proto)
```

or use the provided script [`build_proto.sh`](pyfirehose/proto/build_proto.sh).

*Note: if you encounter some `ModuleNotFound` errors, you might have to edit the generated files for fixing local imports by prefixing them with `proto.generated.`.*

### gRPC endpoints support

#### Currently implemented

Below is a list of the gRPC endpoints which have a default ready-to-use [stub config](pyfirehose/config/) and [processor](pyfirehose/block_processors) available for extracting blocks. All data available in the gRPC block response (as defined in their respective [`.proto` files](pyfirehose/proto/)) will be available upon completion.

| Auth provider | Blockchain          | Block protobuf        | gRPC endpoint                        |
|---------------|---------------------|-----------------------|--------------------------------------|
| eosnation     | EOS                 | sf.firehose.v2.stream | eos.firehose.eosnation.io:9001       |
| eosnation     | EOS                 | dfuse.eosio.codec.v1  | eos.firehose.eosnation.io:9000       |
| eosnation     | WAX                 | dfuse.eosio.codec.v1  | wax.firehose.eosnation.io:9000       |
| eosnation     | Kylin               | dfuse.eosio.codec.v1  | kylin.firehose.eosnation.io:9000     |
| eosnation     | Jungle4             | dfuse.eosio.codec.v1  | jungle4.firehose.eosnation.io:9000   |

#### Pending implementation

| Auth provider | Blockchain          | Block protobuf      | gRPC endpoint                        |
|---------------|---------------------|---------------------|--------------------------------------|
| streamingfast | Ethereum Mainnet    | sf.ethereum.type.v2 | mainnet.eth.streamingfast.io:443     |
| streamingfast | Görli               | sf.ethereum.type.v2 | goerli.eth.streamingfast.io:443      |
| streamingfast | Polygon Mainnet     | sf.ethereum.type.v2 | polygon.streamingfast.io:443         |
| streamingfast | BNB                 | sf.ethereum.type.v2 | bnb.streamingfast.io:443             |
| streamingfast | Near Mainnet        | sf.near.type.v1     | mainnet.near.streamingfast.io:443    |
| streamingfast | Near Testnet        | sf.near.type.v1     | testnet.near.streamingfast.io:443    |
| streamingfast | Solana Mainnet-beta | sf.solana.type.v1   | mainnet.sol.streamingfast.io:443     |
| streamingfast | Arweave Mainnet     | sf.arweave.type.v1  | mainnet.arweave.streamingfast.io:443 |
| streamingfast | Aptos Testnet       | aptos.extractor.v1  | testnet.aptos.streamingfast.io:443   |

## Writing custom block processors (Firehose v1)

For even more control over the data extracted, the extraction process uses a modular approach for manipulating `Block` objects coming from the Firehose gRPC stream. A block processing function is used for extracting the data into `Dict` objects that are later stored in a `.jsonl` file at the end of the process. Customizing which data is extracted is the objective of writing a custom block processor. The default behavior is documented in the [`eos_block_processor`](pyfirehose/block_processors/default.py#L15) function.

In order to write custom block processing functions, some conditions must be respected:
- The function signature should strictly follow the following model: `func(codec_pb2.Block) -> Dict` (you can disable the signature check with the `--disable-signature-check` flag, however this is not recommended and might break the script if your function isn't parsing the block data as expected).
- The function should act as a **generator** (using the `yield` keyword) to return the dictionary data.
- The function should be placed inside a seperate `.py` file in the [`block_processors`](pyfirehose/block_processors/) module.

A typical template for parsing the block data would look like the following:
```python
for transaction_trace in block.filtered_transaction_traces: # Gets every filtered TransactionTrace from a Block
  for action_trace in transaction_trace.action_traces: # Gets every ActionTrace within a TransactionTrace
    if not action_trace.filtering_matched: # Only keep 'transfer' actions that matched the filters
      continue

    data = {}
    
    # Process the data...

    yield data # Make the function act as a generator
```

For documentation about `Block`, `TransactionTrace`, `ActionTrace` or other objects and their properties, please refer to the [`codec.proto`](pyfirehose/proto/codec.proto) file.

You can then use custom block processors through the command-line using the `--custom-processor` argument and providing the relative import path **from the `block_processors` submodule**. 

For example, let's say you've implemented a custom function `my_block_processor` in `custom.py`. The `custom.py` script should reside at the root or in a subdirectory inside the `block_processors` folder (let's say it's at the root for this example). You would then pass the argument as `--custom-processor custom.my_block_processor`. The script will locate it inside the `block_processors` module and use the `my_block_processor` function to parse block data and extract it to the output file.

## Additional information

### Using Firehose v1 filters

The `eos_firehose_v1` gRPC endpoint uses *include* and *exclude* filters for selecting blocks of interest directly within the gRPC block stream.
An example for extracting *transfer* information related to certain accounts is available in the [`producerpay.hjson`](pyfirehose/config/dfuse/producerpay.hjson) stub config file.

For full documentation about the syntax and variables available in the filter expressions, see the [Firehose documentation](https://github.com/streamingfast/playground-firehose-eosio-go#query-language).

*Note: the Firehose v1 is getting deprecated and will soon be replaced by the [Firehose v2](https://github.com/streamingfast/proto/blob/develop/sf/firehose/v2/firehose.proto) version.*

## Example

### Input

```console
(.venv) foo@bar:~/eos-blockchain-data$ python pyfirehose 272368521 272369521 --quiet --log logs/eosio_pay.log --out jsonl/out.jsonl
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