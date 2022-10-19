# EOS - Blockchain Data for Analytics (Python version)

[![Firehose](https://github.com/EOS-Nation/eos-blockchain-data/actions/workflows/firehose.yml/badge.svg)](https://github.com/EOS-Nation/eos-blockchain-data/actions/workflows/firehose.yml)

> Aggregates historical EOS blockchains data & outputs result into JSONL format (using [dfuse **Firehose**](https://dfuse.eosnation.io/))

## Chains

- [x] EOS
- [x] Jungle4
- [x] Kylin
- [x] WAX
- [ ] Telos
- [ ] UX

## Environment variables

[Sample `.env` file](sample.env):
```env
# [REQUIRED] Authentication to Firehose endpoint (see https://docs.dfuse.eosnation.io/platform/dfuse-cloud/authentication/)
DFUSE_TOKEN=<DFUSE_API_TOKEN>

# [OPTIONAL] Defines endpoints for getting authentication token and streaming blocks through gRPC connection
AUTH_ENDPOINT="https://auth.eosnation.io/v1/auth/issue"
GRPC_ENDPOINT="eos.firehose.eosnation.io:9000"
```

## Quickstart

```console
foo@bar:~$ git clone git@github.com:Krow10/eos-blockchain-data.git
foo@bar:~$ cd eos-blockchain-data
foo@bar:~/eos-blockchain-data$ nano sample.env # Edit sample .env file with editor of your choice and add your DFUSE_API_TOKEN
foo@bar:~/eos-blockchain-data$ mv sample.env .env # Rename to .env
```

### Python

```console
foo@bar:~/eos-blockchain-data$ python3 -m venv .venv # Create virtual environnement
foo@bar:~/eos-blockchain-data$ pip install -r requirements.txt # Install dependencies
foo@bar:~/eos-blockchain-data$ source .venv/bin/activate # Activate virtual environnement
(.venv) foo@bar:~/eos-blockchain-data$ python main.py -h
usage: main.py [-h] [-c {eos,wax,kylin,jungle4}] [-n MAX_TASKS] [-o OUT_FILE] [-l [LOG]] [-q] [-x CUSTOM_EXCLUDE_EXPR] [-i CUSTOM_INCLUDE_EXPR] [-p CUSTOM_PROCESSOR]
               [--disable-signature-check]
               accounts [accounts ...] block_start block_end

Search the blockchain for transactions targeting specific accounts over a given period. Powered by Firehose (https://eos.firehose.eosnation.io/).

positional arguments:
  accounts              target account(s) (single or space-separated)
  block_start           starting block number
  block_end             ending block number

optional arguments:
  -h, --help            show this help message and exit
  -c {eos,wax,kylin,jungle4}, --chain {eos,wax,kylin,jungle4}
                        target blockchain (default: eos)
  -n MAX_TASKS, --max-tasks MAX_TASKS
                        maximum number of concurrent tasks running for block streaming (default: 20)
  -o OUT_FILE, --out-file OUT_FILE
                        output file path (default: jsonl/{chain}_{accounts}_{start}_to_{end}.jsonl)
  -l [LOG], --log [LOG]
                        log debug information to log file (can specify the full path) (default: logs/{datetime}.log)
  -q, --quiet           disable console logging (default: False)
  -x CUSTOM_EXCLUDE_EXPR, --custom-exclude-expr CUSTOM_EXCLUDE_EXPR
                        custom filter for the Firehose stream to exclude transactions (default: None)
  -i CUSTOM_INCLUDE_EXPR, --custom-include-expr CUSTOM_INCLUDE_EXPR
                        custom filter for the Firehose stream to tag included transactions (default: None)
  -p CUSTOM_PROCESSOR, --custom-processor CUSTOM_PROCESSOR
                        relative import path to a custom block processing function located in the "block_processors" module (default: None)
  --disable-signature-check
                        disable signature checking for the custom block processing function (default: False)
```

The transactions will be listed in a `.jsonl` file inside the [`jsonl/`](jsonl/) directory.

### Protobuf

To communicate with the gRPC endpoint, Python object are generated through the use of `.proto` file templates that describes the kind of data the client and server are going to manipulate. Those Python object are already provided in the [`proto/`](proto/) folder, however if you want to generate them yourself, you can run the following commands:
```console
(.venv) foo@bar:~/eos-blockchain-data$ pip install grpcio-tools
(.venv) foo@bar:~/eos-blockchain-data$ python -m grpc_tools.protoc -Iproto --python_out=proto/ --grpc_python_out=proto/ proto/*.proto
```

## Using custom filters

By default, the script will look for all 'transfer' actions with the targeted accounts as the contract's 'receiver' (which can be different from the recipient of the transaction) meaning that all transactions 'from' and 'to' those adresses will be accounted for.

Let's say you just wanted outgoing transactions from certain accounts. You could use the `--custom-include-expr` argument like so:
```console
(.venv) foo@bar:~/eos-blockchain-data$ python main.py $TARGET $START $END --custom-include-expr "receiver == '${TARGET}' && data['from'] == '${TARGET}' && action == 'transfer'"
```
This specifies that only 'transfer' transactions 'from' the `TARGET` should be included in the resulting `.jsonl` file.

You could also write it using the `--custom-exclude-expr` taking advantage of the default transaction inclusion behavior:
```console
(.venv) foo@bar:~/eos-blockchain-data$ python main.py $TARGET $START $END --custom-exclude-expr "data['to'] == '${TARGET}'"
```
For reference about the default behavior, see [`main.py`](main.py#L89-L90).

For full documentation about the syntax and variables available in the filter expressions, see the [Firehose documentation](https://github.com/streamingfast/playground-firehose-eosio-go#query-language).

## Writing custom block processors

For even more control over the data extracted, the extraction process uses a modular approach for manipulating `Block` objects coming from the Firehose gRPC stream. A block processing function is used for extracting the data into `Dict` objects that are later stored in a `.jsonl` file at the end of the process. Customizing which data is extracted is the objective of writing a custom block processor. The default behavior is documented in the [`eos_block_processor`](block_processors/default.py#L15) function.

In order to write custom block processing functions, some conditions must be respected:
- The function signature should strictly follow the following model: `func(codec_pb2.Block) -> Dict`
- The function should act as a **generator** using the `yield` keyword to return the dictionary data.
- The function should be placed inside a seperate `.py` file in the [`block_processors`](block_processors/) module.

A typical template for parsing the block data would look like the following:
```python
for transaction_trace in block.filtered_transaction_traces: # Gets every filtered TransactionTrace from a Block
  for action_trace in transaction_trace.action_traces: # Gets every ActionTrace within a TransactionTrace
    if not action_trace.filtering_matched: # Only keep 'transfer' actions that concerns the targeted accounts
      continue

    data = {}
    
    # Process the data...

    yield data
```

For documentation about `Block`, `TransactionTrace`, `ActionTrace` or other objects and their properties, please refer to the [`codec.proto`](proto/codec.proto) file.

You can then use custom block processors through the command-line using the `--custom-processor` argument and providing the relative import path **from the `block_processors` module**. 

For example, let's say you've implemented a custom function `my_block_processor` in `custom.py`. The `custom.py` script should reside at the root or in a subdirectory inside the `block_processors` folder (let's say it's at the root for this example). You would then pass the argument as `--custom-processor custom.my_block_processor`. The script will locate it inside the `block_processors` module and use the `my_block_processor` function to parse block data and extract it to the `.jsonl` file.

## Example

### Input

```console
(.venv) foo@bar:~/eos-blockchain-data$ python main.py eosio.bpay 272368521 272368621 --quiet --log logs/eosio.bpay.log
```

### Output (jsonl/eos_eosio.bpay_272368521_to_272368621.jsonl)

```jsonl
{"account": "eosio.bpay", "date": "2022-10-10 00:00:12", "timestamp": 1665360012, "amount": "40.1309", "token": "EOS", "from": "eosio", "to": "eosio.bpay", "block_num": 272368521, "transaction_id": "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75", "memo": "fund per-block bucket", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.bpay", "date": "2022-10-10 00:00:12", "timestamp": 1665360012, "amount": "343.8791", "token": "EOS", "from": "eosio.bpay", "to": "aus1genereos", "block_num": 272368521, "transaction_id": "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75", "memo": "producer block pay", "contract": "eosio.token", "action": "transfer"}
```

### Log file sample (logs/eosio.bpay.log)

```
T+128 [DEBUG] Using selector: EpollSelector
T+139 [DEBUG] Initializing backend: None jwt_token
T+140 [DEBUG] Initializing SQLitePickleDict with serializer: <requests_cache.serializers.pipeline.SerializerPipeline object at 0x780d84fa60a0>
T+140 [DEBUG] Opening connection to /home/user/Documents/eos-blockchain-data/jwt_token.sqlite:responses
T+141 [DEBUG] Initializing SQLiteDict with serializer: <requests_cache.serializers.pipeline.SerializerPipeline object at 0x780d84fa60a0>
T+141 [DEBUG] Opening connection to /home/user/Documents/eos-blockchain-data/jwt_token.sqlite:redirects
T+142 [*] Getting JWT token...
T+145 [DEBUG] Cache directives from request headers: {}
T+147 [DEBUG] {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiaHR0cHM6Ly9kZnVzZS5lb3NuYXRpb24uaW8vIl0sImV4cCI6MTY2NjExMTYyMCwiaWF0IjoxNjY2MDI1MjIwLCJpc3MiOiJodHRwczovL2FwaS5kZnVzZS5lb3NuYXRpb24uaW8vdjEvIiwic3ViIjoidWlkOjU1NDIzMjMuZW9zbiIsImFwaV9rZXlfaWQiOiIxNjY1NTE2MDU2NTYwIiwicXVvdGEiOjEyMCwicmF0ZSI6MTAsIm5ldHdvcmtzIjpbeyJuYW1lIjoiZW9zIiwicXVvdGEiOjEyMCwicmF0ZSI6MTB9LHsibmFtZSI6IndheCIsInF1b3RhIjoxMjAsInJhdGUiOjEwfSx7Im5hbWUiOiJreWxpbiIsInF1b3RhIjoxMjAsInJhdGUiOjEwfSx7Im5hbWUiOiJqdW5nbGU0IiwicXVvdGEiOjEyMCwicmF0ZSI6MTB9LHsibmFtZSI6IndheHRlc3QiLCJxdW90YSI6MTIwLCJyYXRlIjoxMH0seyJuYW1lIjoib3JlIiwicXVvdGEiOjEyMCwicmF0ZSI6MTB9LHsibmFtZSI6Im9yZXN0YWdlIiwicXVvdGEiOjEyMCwicmF0ZSI6MTB9LHsibmFtZSI6InRlc3RuZXQiLCJxdW90YSI6MTIwLCJyYXRlIjoxMH0seyJuYW1lIjoidGVsb3MiLCJxdW90YSI6MTIwLCJyYXRlIjoxMH0seyJuYW1lIjoidGVsb3N0ZXN0IiwicXVvdGEiOjEyMCwicmF0ZSI6MTB9XX0.3qhISRS8mSYGfEx4kGSBL9qpkPyjAtBOzDkb6is_yzI', 'expires_at': 1666111620}
T+147 [*] Got JWT token (cached) [SUCCESS]
T+147 [*] Streaming 100 blocks on EOS chain for transfer information related to ['eosio.bpay'] (running 20 concurrent tasks)...
T+147 [DEBUG] Using AsyncIOEngine.POLLER as I/O engine
T+148 [DEBUG] [Task-2] Starting streaming blocks from 272368521 to 272368526 using "eos_block_processor"...
T+148 [DEBUG] [Task-3] Starting streaming blocks from 272368526 to 272368531 using "eos_block_processor"...
T+148 [DEBUG] [Task-4] Starting streaming blocks from 272368531 to 272368536 using "eos_block_processor"...
T+148 [DEBUG] [Task-5] Starting streaming blocks from 272368536 to 272368541 using "eos_block_processor"...
T+148 [DEBUG] [Task-6] Starting streaming blocks from 272368541 to 272368546 using "eos_block_processor"...
T+148 [DEBUG] [Task-7] Starting streaming blocks from 272368546 to 272368551 using "eos_block_processor"...
T+148 [DEBUG] [Task-8] Starting streaming blocks from 272368551 to 272368556 using "eos_block_processor"...
T+148 [DEBUG] [Task-9] Starting streaming blocks from 272368556 to 272368561 using "eos_block_processor"...
T+148 [DEBUG] [Task-10] Starting streaming blocks from 272368561 to 272368566 using "eos_block_processor"...
T+148 [DEBUG] [Task-11] Starting streaming blocks from 272368566 to 272368571 using "eos_block_processor"...
T+148 [DEBUG] [Task-12] Starting streaming blocks from 272368571 to 272368576 using "eos_block_processor"...
T+148 [DEBUG] [Task-13] Starting streaming blocks from 272368576 to 272368581 using "eos_block_processor"...
T+148 [DEBUG] [Task-14] Starting streaming blocks from 272368581 to 272368586 using "eos_block_processor"...
T+149 [DEBUG] [Task-15] Starting streaming blocks from 272368586 to 272368591 using "eos_block_processor"...
T+149 [DEBUG] [Task-16] Starting streaming blocks from 272368591 to 272368596 using "eos_block_processor"...
T+149 [DEBUG] [Task-17] Starting streaming blocks from 272368596 to 272368601 using "eos_block_processor"...
T+149 [DEBUG] [Task-18] Starting streaming blocks from 272368601 to 272368606 using "eos_block_processor"...
T+149 [DEBUG] [Task-19] Starting streaming blocks from 272368606 to 272368611 using "eos_block_processor"...
T+149 [DEBUG] [Task-20] Starting streaming blocks from 272368611 to 272368616 using "eos_block_processor"...
T+149 [DEBUG] [Task-21] Starting streaming blocks from 272368616 to 272368621 using "eos_block_processor"...
T+707 [*] [Task-18] Parsing block number #272368601 (5 blocks remaining)...
T+708 [DEBUG] [Task-18] block=id: "103c03d9d318fb6aa7bf78966f0eff520897ce8df9f391d750449a2599e3dc0d"
number: 272368601
version: 1
header {
  timestamp {
    seconds: 1665360052
  }
  producer: "okcapitalbp1"
  previous: "103c03d807a546d324323f49e63dffd4871f5440404a52edf1b19f85fa7551d0"
  transaction_mroot: "p\023\030\224;#\334\201<\236^+z\262\360\252\307:k\207\\Z\363\364\021\366&\256XV\335\347"
  action_mroot: "\267W\223J\233\3664\305\177\267d\213s\007c\247\326\243hu\200J\006@y\360\345 *z\317\210"
  schedule_version: 2041
}
producer_signature: "SIG_K1_KmNN2Ctneg2T5VV8PDNsw4c7JkSCce5eMGw4tq345adDb4KXvsENAKY9DqYHeLnfqf869DePZRmoxN43wUhHR4wBtAWFx6"
dpos_proposed_irreversible_blocknum: 272368437
dpos_irreversible_blocknum: 272368269
blockroot_merkle {
[...]
```