# EOS - Blockchain Data for Analytics (Python version)

> Aggregates historical EOS blockchains data & outputs result into JSONL format (using [dfuse **Firehose**](https://dfuse.eosnation.io/))

[![Pylint](https://github.com/Krow10/eos-blockchain-data/actions/workflows/pylint.yml/badge.svg)](https://github.com/Krow10/eos-blockchain-data/actions/workflows/pylint.yml)

[![Extract Firehose](https://github.com/Krow10/eos-blockchain-data/actions/workflows/firehose_daily_extraction.yml/badge.svg)](https://github.com/Krow10/eos-blockchain-data/actions/workflows/firehose_daily_extraction.yml)
[![Update Index](https://github.com/Krow10/eos-blockchain-data/actions/workflows/update_index_notebook.yml/badge.svg)](https://github.com/Krow10/eos-blockchain-data/actions/workflows/update_index_notebook.yml)
[![Deploy Website](https://github.com/Krow10/eos-blockchain-data/actions/workflows/static.yml/badge.svg)](https://github.com/Krow10/eos-blockchain-data/actions/workflows/static.yml)

**Supported chains:**
- [x] EOS
- [x] Jungle4
- [x] Kylin
- [x] WAX
- [ ] Telos
- [ ] UX

**TODO:**
* Cleanup multi-channel extractor
* Test perfomance between extractors
* Add architectures description
* Add more examples to README.md
* Drop the generator requirement for block processors (?)
* Investigate functools and other more abstract modules for block processor modularity (?)
  + Possibility of 3 stages:
  + Pre-processing (e.g. load some API data)
  + Process (currently implemented)
  + Post-processing (e.g. adding more data to transactions)


## Github Actions workflow

This repo uses Github actions to automatically fetch transactions related to EOS block producer's (BP) addresses payments, parse them and generate a [Sankey chart](https://en.wikipedia.org/wiki/Sankey_diagram) for visualizing the flow of funds. Below is a flow diagram showing what the actual pipeline looks like:

![Github actions workflow pipeline](github_actions_workflow.png)

You can see the rendered chart [here](https://krow10.github.io/eos-blockchain-data/) at the bottom of the page.

## Quickstart

```console
foo@bar:~$ git clone git@github.com:Krow10/eos-blockchain-data.git
foo@bar:~$ cd eos-blockchain-data
foo@bar:~/eos-blockchain-data$ nano pyfirehose/sample.env # Edit sample .env file with editor of your choice and add your DFUSE_API_TOKEN
foo@bar:~/eos-blockchain-data$ mv pyfirehose/sample.env pyfirehose/.env # Rename to .env
```

### Environment variables

[Sample `.env` file](pyfirehose/sample.env):
```env
# [REQUIRED] Authentication to Firehose endpoint (see https://docs.dfuse.eosnation.io/platform/dfuse-cloud/authentication/)
DFUSE_TOKEN=<DFUSE_API_TOKEN>

# [OPTIONAL] Endpoint for getting authentication token
AUTH_ENDPOINT="https://auth.eosnation.io/v1/auth/issue"

# [OPTIONAL] Endpoint for querying block numbers from date
DFUSE_GRAPHQL_ENDPOINT="https://eos.dfuse.eosnation.io/graphql"

# [OPTIONAL] Maximum block size (in KB) for blocks returned by the Firehose stream 
# Note that blocks bigger than the limit will make the workers throw a `grpc.aio.AioRpcError`
MAX_RECV_BLOCK_SIZE=10240 # 10MB
```

Follow the instructions on the [dFuse documentation website](https://docs.dfuse.eosnation.io/platform/dfuse-cloud/authentication/#types-of-keys) to generate an API key and copy it to your `.env` file (the JWT token authentication is handled by the [script](pyfirehose/utils.py#L71) itself).

### Python

```console
foo@bar:~/eos-blockchain-data$ python3 -m venv .venv # Create virtual environnement
foo@bar:~/eos-blockchain-data$ source .venv/bin/activate # Activate virtual environnement
(.venv) foo@bar:~/eos-blockchain-data$ pip install -r requirements.txt # Install dependencies
(.venv) foo@bar:~/eos-blockchain-data$ python pyfirehose -h
usage: pyfirehose [-h] [-c {eos,wax,kylin,jungle4}] [-o OUT_FILE] [-l [LOG]] [-q] [-x CUSTOM_EXCLUDE_EXPR] [-i CUSTOM_INCLUDE_EXPR]                           
                  [-e {simple,single,multi}] [-p CUSTOM_PROCESSOR] [--disable-signature-check]
                  start end                                           

Extract any data from the blockchain. Powered by Firehose (https://eos.firehose.eosnation.io/).                                      

positional arguments:  
  start                 period start as a date (iso-like format) or a block number                                 
  end                   period end as a date (iso-like format) or a block number             

options:                        
  -h, --help            show this help message and exit
  -c {eos,wax,kylin,jungle4}, --chain {eos,wax,kylin,jungle4}                                                             
                        target blockchain (default: eos)
  -o OUT_FILE, --out-file OUT_FILE                                                                                                      
                        output file path (default: jsonl/{chain}_{start}_to_{end}.jsonl)
  -l [LOG], --log [LOG]                                                                                                          
                        log debug information to log file (can specify the full path) (default: logs/{datetime}.log)
  -q, --quiet           disable console logging (default: False)                                      
  -x CUSTOM_EXCLUDE_EXPR, --custom-exclude-expr CUSTOM_EXCLUDE_EXPR
                        custom filter for the Firehose stream to exclude transactions (default: None)
  -i CUSTOM_INCLUDE_EXPR, --custom-include-expr CUSTOM_INCLUDE_EXPR    
                        custom filter for the Firehose stream to tag included transactions (default: None)
  -e {simple,single,multi}, --extractor {simple,single,multi}
                        type of extractor used for streaming blocks from the Firehose endpoint (default: simple)
  -p CUSTOM_PROCESSOR, --custom-processor CUSTOM_PROCESSOR
                        relative import path to a custom block processing function located in the "block_processors" module (default: None)
  --disable-signature-check                                                                                                    
                        disable signature checking for the custom block processing function (default: False)
```

The period's *start* and *end* accepts either a block number or a [ISO-like formatted date time](https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat). By default, the extracted data will be stored in a `.jsonl` file inside the [`jsonl/`](jsonl/) directory.

A [`.pylintrc`](.pylintrc) file is provided if you want to run [Pylint](https://pypi.org/project/pylint/):
```console
(.venv) user@dev-eosnation:~/Documents/eos-blockchain-data$ pylint pyfirehose --rcfile=.pylintrc
```

### Protobuf

To communicate with the gRPC endpoint, Python object are generated through the use of `.proto` file templates that describes the kind of data the client and server are going to manipulate. Those Python object are already provided in the [`proto/`](pyfirehose/proto/) folder, however if you want to generate them yourself, you can run the following commands:
```console
(.venv) foo@bar:~/eos-blockchain-data$ pip install grpcio-tools
(.venv) foo@bar:~/eos-blockchain-data$ cd pyfirehose
(.venv) foo@bar:~/eos-blockchain-data/pyfirehose$ python -m grpc_tools.protoc -Iproto --python_out=proto/ --grpc_python_out=proto/ proto/*.proto
```

*Note: if you encounter some `ModuleNotFound` errors, you might have to edit the files for fixing the imports by prefixing them with `proto.`.*

## Using Firehose filters

By default, the script include **every** transaction from the targeted blocks. You can speed up the process by filtering the blocks sent by the Firehose stream using *include* or *exclude* statements.

Let's say you just wanted outgoing transactions from certain accounts. You could use the `--custom-include-expr` argument like so:
```console
(.venv) foo@bar:~/eos-blockchain-data$ python pyfirehose $START $END -i "receiver == '${TARGET}' && data['from'] == '${TARGET}' && action == 'transfer'"
```
This specifies that only *transfer* transactions *from* the `TARGET` should be included in the resulting `.jsonl` file.

You could also write it using the `--custom-exclude-expr` argument:
```console
(.venv) foo@bar:~/eos-blockchain-data$ python pyfirehose $START $END -x "receiver == '${TARGET}' && data['to'] == '${TARGET}' && action == 'transfer'"
```

For full documentation about the syntax and variables available in the filter expressions, see the [Firehose documentation](https://github.com/streamingfast/playground-firehose-eosio-go#query-language).

*Note: a simpler interface will be provided for common use cases such as extracting transactions of specific accounts from the blockchain.*
*See scripts in the [scripts/](scripts/) folder for more examples.*

## Writing custom block processors

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

## Example

### Input

```console
(.venv) foo@bar:~/eos-blockchain-data$ python pyfirehose 272368521 272369521 -i "receiver in ['eosio.vpay', 'eosio.bpay'] && action == 'transfer'" --quiet --log logs/eosio_pay.log --out jsonl/out.jsonl
```

### Output (jsonl/out.jsonl)

```jsonl
{"account": "eosio.bpay", "date": "2022-10-10 00:00:12", "timestamp": 1665360012, "amount": "40.1309", "token": "EOS", "from": "eosio", "to": "eosio.bpay", "block_num": 272368521, "transaction_id": "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75", "memo": "fund per-block bucket", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.vpay", "date": "2022-10-10 00:00:12", "timestamp": 1665360012, "amount": "120.3927", "token": "EOS", "from": "eosio", "to": "eosio.vpay", "block_num": 272368521, "transaction_id": "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75", "memo": "fund per-vote bucket", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.bpay", "date": "2022-10-10 00:00:12", "timestamp": 1665360012, "amount": "343.8791", "token": "EOS", "from": "eosio.bpay", "to": "aus1genereos", "block_num": 272368521, "transaction_id": "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75", "memo": "producer block pay", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.vpay", "date": "2022-10-10 00:00:12", "timestamp": 1665360012, "amount": "675.7402", "token": "EOS", "from": "eosio.vpay", "to": "aus1genereos", "block_num": 272368521, "transaction_id": "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75", "memo": "producer vote pay", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.bpay", "date": "2022-10-10 00:02:56", "timestamp": 1665360176, "amount": "13.7532", "token": "EOS", "from": "eosio", "to": "eosio.bpay", "block_num": 272368850, "transaction_id": "22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6", "memo": "fund per-block bucket", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.vpay", "date": "2022-10-10 00:02:56", "timestamp": 1665360176, "amount": "41.2596", "token": "EOS", "from": "eosio", "to": "eosio.vpay", "block_num": 272368850, "transaction_id": "22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6", "memo": "fund per-vote bucket", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.bpay", "date": "2022-10-10 00:02:56", "timestamp": 1665360176, "amount": "344.5057", "token": "EOS", "from": "eosio.bpay", "to": "newdex.bp", "block_num": 272368850, "transaction_id": "22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6", "memo": "producer block pay", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.vpay", "date": "2022-10-10 00:02:56", "timestamp": 1665360176, "amount": "698.0213", "token": "EOS", "from": "eosio.vpay", "to": "newdex.bp", "block_num": 272368850, "transaction_id": "22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6", "memo": "producer vote pay", "contract": "eosio.token", "action": "transfer"}
```

### Log file sample (logs/eosio_pay.log)

```
T+203 [DEBUG] Script arguments: Namespace(start=272368521, end=272369521, chain='eos', out_file='jsonl/out.jsonl', log='logs/eosio_pay.log', quiet=True, custom_exclude_expr=None, custom_include_expr="receiver in ['eosio.vpay', 'eosio.bpay'] && action == 'transfer'", custom_processor=None, disable_signature_check=False)
T+204 [DEBUG] Using selector: EpollSelector
T+204 [*] Streaming 1000 blocks on EOS chain...
T+204 [DEBUG] Using AsyncIOEngine.POLLER as I/O engine
T+205 [*] [Task-02] 0 tasks running | polling every 0.100000s | 1000 blocks remaining in block pool
T+306 [*] [Task-02] 1 tasks running | polling every 0.100000s | 900 blocks remaining in block pool
T+306 [DEBUG] [Task-03] Starting streaming blocks from #272368921 to #272369020...
T+407 [*] [Task-02] 2 tasks running | polling every 0.100000s | 800 blocks remaining in block pool
T+407 [DEBUG] [Task-06] Starting streaming blocks from #272369121 to #272369220...
T+508 [*] [Task-02] 3 tasks running | polling every 0.100000s | 700 blocks remaining in block pool
T+508 [DEBUG] [Task-09] Starting streaming blocks from #272368821 to #272368920...
T+609 [*] [Task-02] 4 tasks running | polling every 0.100000s | 600 blocks remaining in block pool
T+609 [DEBUG] [Task-12] Starting streaming blocks from #272369021 to #272369120...
T+710 [*] [Task-02] 5 tasks running | polling every 0.100000s | 500 blocks remaining in block pool
T+710 [DEBUG] [Task-15] Starting streaming blocks from #272368721 to #272368820...
T+811 [*] [Task-02] 6 tasks running | polling every 0.100000s | 400 blocks remaining in block pool
T+811 [DEBUG] [Task-18] Starting streaming blocks from #272369421 to #272369520...
T+912 [*] [Task-02] 7 tasks running | polling every 0.100000s | 300 blocks remaining in block pool
T+913 [DEBUG] [Task-21] Starting streaming blocks from #272368621 to #272368720...
T+1013  [*] [Task-02] 8 tasks running | polling every 0.100000s | 200 blocks remaining in block pool
T+1013  [DEBUG] [Task-24] Starting streaming blocks from #272369321 to #272369420...
T+1019  [DEBUG] [Task-18] Getting block number #272369421 (99 blocks remaining)...
T+1114  [*] [Task-02] 9 tasks running | polling every 0.100000s | 100 blocks remaining in block pool
T+1114  [DEBUG] [Task-27] Starting streaming blocks from #272368521 to #272368620...
T+1130  [DEBUG] [Task-21] Getting block number #272368621 (99 blocks remaining)...
T+1169  [DEBUG] [Task-24] Getting block number #272369321 (99 blocks remaining)...
T+1214  [*] [Task-02] 10 tasks running | polling every 0.100000s | 0 blocks remaining in block pool
T+1215  [DEBUG] [Task-30] Starting streaming blocks from #272369221 to #272369320...
T+1315  [!] [Task-02] No more blocks in block pool, stopping spawner task NOW...
T+1550  [DEBUG] [Task-27] Getting block number #272368521 (99 blocks remaining)...
T+1705  [DEBUG] [Task-27] Getting block number #272368522 (98 blocks remaining)...
T+1820  [DEBUG] [Task-09] Getting block number #272368821 (99 blocks remaining)...
T+2088  [DEBUG] [Task-24] Getting block number #272369322 (98 blocks remaining)...
T+2092  [DEBUG] [Task-24] Getting block number #272369323 (97 blocks remaining)...
T+2095  [DEBUG] [Task-24] Getting block number #272369324 (96 blocks remaining)...
T+2099  [DEBUG] [Task-24] Getting block number #272369325 (95 blocks remaining)...
T+2101  [DEBUG] [Task-24] Getting block number #272369326 (94 blocks remaining)...
T+2102  [DEBUG] [Task-24] Getting block number #272369327 (93 blocks remaining)...
T+2106  [DEBUG] [Task-24] Getting block number #272369328 (92 blocks remaining)...
T+2118  [DEBUG] [Task-27] Getting block number #272368523 (97 blocks remaining)...
T+2118  [DEBUG] [Task-27] Getting block number #272368524 (96 blocks remaining)...
T+2122  [DEBUG] [Task-27] Getting block number #272368525 (95 blocks remaining)...
T+2126  [DEBUG] [Task-27] Getting block number #272368526 (94 blocks remaining)...
T+2126  [DEBUG] [Task-06] Getting block number #272369121 (99 blocks remaining)...
T+2163  [DEBUG] [Task-09] Getting block number #272368822 (98 blocks remaining)...
T+2165  [DEBUG] [Task-09] Getting block number #272368823 (97 blocks remaining)...
T+2168  [DEBUG] [Task-09] Getting block number #272368824 (96 blocks remaining)...
T+2171  [DEBUG] [Task-24] Getting block number #272369329 (91 blocks remaining)...
[...]
T+13152 [*] Finished block streaming, got 1000 blocks [SUCCESS]
T+13165 [DEBUG] Data: {'account': 'eosio.bpay', 'date': '2022-10-10 00:02:56', 'timestamp': 1665360176, 'amount': '13.7532', 'token': 'EOS', 'from': 'eosio', 'to': 'eosio.bpay', 'block_num': 272368850, 'transaction_id': '22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6', 'memo': 'fund per-block bucket', 'contract': 'eosio.token', 'action': 'transfer'}
T+13165 [DEBUG] Data: {'account': 'eosio.vpay', 'date': '2022-10-10 00:02:56', 'timestamp': 1665360176, 'amount': '41.2596', 'token': 'EOS', 'from': 'eosio', 'to': 'eosio.vpay', 'block_num': 272368850, 'transaction_id': '22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6', 'memo': 'fund per-vote bucket', 'contract': 'eosio.token', 'action': 'transfer'}
T+13165 [DEBUG] Data: {'account': 'eosio.bpay', 'date': '2022-10-10 00:02:56', 'timestamp': 1665360176, 'amount': '344.5057', 'token': 'EOS', 'from': 'eosio.bpay', 'to': 'newdex.bp', 'block_num': 272368850, 'transaction_id': '22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6', 'memo': 'producer block pay', 'contract': 'eosio.token', 'action': 'transfer'}
T+13165 [DEBUG] Data: {'account': 'eosio.vpay', 'date': '2022-10-10 00:02:56', 'timestamp': 1665360176, 'amount': '698.0213', 'token': 'EOS', 'from': 'eosio.vpay', 'to': 'newdex.bp', 'block_num': 272368850, 'transaction_id': '22b736b6662a5fae94b4e37b11d6c9fa324b4a85d434da9afd92227913aa8dc6', 'memo': 'producer vote pay', 'contract': 'eosio.token', 'action': 'transfer'}
T+13168 [DEBUG] Data: {'account': 'eosio.bpay', 'date': '2022-10-10 00:00:12', 'timestamp': 1665360012, 'amount': '40.1309', 'token': 'EOS', 'from': 'eosio', 'to': 'eosio.bpay', 'block_num': 272368521, 'transaction_id': 'e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75', 'memo': 'fund per-block bucket', 'contract': 'eosio.token', 'action': 'transfer'}
T+13168 [DEBUG] Data: {'account': 'eosio.vpay', 'date': '2022-10-10 00:00:12', 'timestamp': 1665360012, 'amount': '120.3927', 'token': 'EOS', 'from': 'eosio', 'to': 'eosio.vpay', 'block_num': 272368521, 'transaction_id': 'e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75', 'memo': 'fund per-vote bucket', 'contract': 'eosio.token', 'action': 'transfer'}
T+13168 [DEBUG] Data: {'account': 'eosio.bpay', 'date': '2022-10-10 00:00:12', 'timestamp': 1665360012, 'amount': '343.8791', 'token': 'EOS', 'from': 'eosio.bpay', 'to': 'aus1genereos', 'block_num': 272368521, 'transaction_id': 'e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75', 'memo': 'producer block pay', 'contract': 'eosio.token', 'action': 'transfer'}
T+13168 [DEBUG] Data: {'account': 'eosio.vpay', 'date': '2022-10-10 00:00:12', 'timestamp': 1665360012, 'amount': '675.7402', 'token': 'EOS', 'from': 'eosio.vpay', 'to': 'aus1genereos', 'block_num': 272368521, 'transaction_id': 'e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75', 'memo': 'producer vote pay', 'contract': 'eosio.token', 'action': 'transfer'}
T+13171 [*] Finished block processing, wrote 8 rows of data to jsonl/out.jsonl [SUCCESS]
```