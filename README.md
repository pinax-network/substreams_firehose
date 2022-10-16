# EOS - Blockchain Data for Analytics

[![Firehose](https://github.com/EOS-Nation/eos-blockchain-data/actions/workflows/firehose.yml/badge.svg)](https://github.com/EOS-Nation/eos-blockchain-data/actions/workflows/firehose.yml)

> Aggregates historical EOS blockchain data & outputs result into JSONL format (using [dfuse **Firehose**](https://dfuse.eosnation.io/))

## Chains

- [x] EOS
- [ ] Telos
- [ ] WAX
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
usage: main.py [-h] [--max-tasks [MAX_TASKS]] [--debug] [--no-log] accounts [accounts ...] block_start block_end

Search the blockchain for transfer transactions targeting specific accounts over a given period. Powered by Firehose (https://eos.firehose.eosnation.io/).

positional arguments:
  accounts              target account(s) (single or space-separated)
  block_start           starting block number
  block_end             ending block number

optional arguments:
  -h, --help            show this help message and exit
  --max-tasks [MAX_TASKS]
                        maximum number of concurrent tasks running for block streaming (default: 20)
  --debug               log debug information to log file (found in logs/) (default: False)
  --no-log              disable console logging (default: False)
```

The transactions will be listed in a `.jsonl` file inside the [`jsonl/`](jsonl/) directory.

## Example

### Input

```console
(.venv) foo@bar:~/eos-blockchain-data$ python main.py eosio.bpay 272368521 272368621 --debug
```

### Output (jsonl/eosio.bpay_272368521_to_272368621.jsonl)

```jsonl
{"account": "eosio.bpay", "date": 1665360012, "amount": "40.1309", "token": "EOS", "amountCAD": 0, "token/CAD": 0, "from": "eosio", "to": "eosio.bpay", "blockNum": 272368521, "trxID": "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75", "memo": "fund per-block bucket", "contract": "eosio.token", "action": "transfer"}
{"account": "eosio.bpay", "date": 1665360012, "amount": "343.8791", "token": "EOS", "amountCAD": 0, "token/CAD": 0, "from": "eosio.bpay", "to": "aus1genereos", "blockNum": 272368521, "trxID": "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75", "memo": "producer block pay", "contract": "eosio.token", "action": "transfer"}
```

### Log file sample (logs/{datetime}.log)

```
T+306   [DEBUG] Using selector: EpollSelector
T+306   [DEBUG] Initializing backend: None jwt_token
T+306   [DEBUG] Initializing SQLitePickleDict with serializer: <requests_cache.serializers.pipeline.SerializerPipeline object at 0x7d5c7f5ea940>
T+306   [DEBUG] Opening connection to /home/user/Documents/eos-blockchain-data/jwt_token.sqlite:responses
T+307   [DEBUG] Initializing SQLiteDict with serializer: <requests_cache.serializers.pipeline.SerializerPipeline object at 0x7d5c7f5ea940>
T+307   [DEBUG] Opening connection to /home/user/Documents/eos-blockchain-data/jwt_token.sqlite:redirects
T+307   [*] Getting JWT token...
T+310   [DEBUG] Cache directives from request headers: {}
T+314   [DEBUG] {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiaHR0cHM6Ly9kZnVzZS5lb3NuYXRpb24uaW8vIl0sImV4cCI6MTY2NjAyNTA4NiwiaWF0IjoxNjY1OTM4Njg2LCJpc3MiOiJodHRwczovL2FwaS5kZnVzZS5lb3NuYXRpb24uaW8vdjEvIiwic3ViIjoidWlkOjU1NDIzMjMuZW9zbiIsImFwaV9rZXlfaWQiOiIxNjY1NTE2MDU2NTYwIiwicXVvdGEiOjEyMCwicmF0ZSI6MTAsIm5ldHdvcmtzIjpbeyJuYW1lIjoiZW9zIiwicXVvdGEiOjEyMCwicmF0ZSI6MTB9LHsibmFtZSI6IndheCIsInF1b3RhIjoxMjAsInJhdGUiOjEwfSx7Im5hbWUiOiJreWxpbiIsInF1b3RhIjoxMjAsInJhdGUiOjEwfSx7Im5hbWUiOiJqdW5nbGU0IiwicXVvdGEiOjEyMCwicmF0ZSI6MTB9LHsibmFtZSI6IndheHRlc3QiLCJxdW90YSI6MTIwLCJyYXRlIjoxMH0seyJuYW1lIjoib3JlIiwicXVvdGEiOjEyMCwicmF0ZSI6MTB9LHsibmFtZSI6Im9yZXN0YWdlIiwicXVvdGEiOjEyMCwicmF0ZSI6MTB9LHsibmFtZSI6InRlc3RuZXQiLCJxdW90YSI6MTIwLCJyYXRlIjoxMH0seyJuYW1lIjoidGVsb3MiLCJxdW90YSI6MTIwLCJyYXRlIjoxMH0seyJuYW1lIjoidGVsb3N0ZXN0IiwicXVvdGEiOjEyMCwicmF0ZSI6MTB9XX0.fGF356vGsMZc2vlCagC4f8ZXMpQcPXtiOsDjW2-i6iE', 'expires_at': 1666025086}
T+314   [*] Got JWT token (cached) [SUCCESS]
T+315   [*] Streaming 100 blocks for transfer information related to ['eosio.bpay'] (running 20 workers)...
T+315   [DEBUG] Using AsyncIOEngine.POLLER as I/O engine
T+316   [DEBUG] [Task-2] Starting streaming blocks from 272368521 to 272368526...
T+317   [DEBUG] [Task-3] Starting streaming blocks from 272368526 to 272368531...
T+317   [DEBUG] [Task-4] Starting streaming blocks from 272368531 to 272368536...
T+317   [DEBUG] [Task-5] Starting streaming blocks from 272368536 to 272368541...
T+317   [DEBUG] [Task-6] Starting streaming blocks from 272368541 to 272368546...
T+317   [DEBUG] [Task-7] Starting streaming blocks from 272368546 to 272368551...
T+317   [DEBUG] [Task-8] Starting streaming blocks from 272368551 to 272368556...
T+318   [DEBUG] [Task-9] Starting streaming blocks from 272368556 to 272368561...
T+318   [DEBUG] [Task-10] Starting streaming blocks from 272368561 to 272368566...
T+318   [DEBUG] [Task-11] Starting streaming blocks from 272368566 to 272368571...
T+318   [DEBUG] [Task-12] Starting streaming blocks from 272368571 to 272368576...
T+318   [DEBUG] [Task-13] Starting streaming blocks from 272368576 to 272368581...
T+318   [DEBUG] [Task-14] Starting streaming blocks from 272368581 to 272368586...
T+318   [DEBUG] [Task-15] Starting streaming blocks from 272368586 to 272368591...
T+318   [DEBUG] [Task-16] Starting streaming blocks from 272368591 to 272368596...
T+318   [DEBUG] [Task-17] Starting streaming blocks from 272368596 to 272368601...
T+318   [DEBUG] [Task-18] Starting streaming blocks from 272368601 to 272368606...
T+319   [DEBUG] [Task-19] Starting streaming blocks from 272368606 to 272368611...
T+319   [DEBUG] [Task-20] Starting streaming blocks from 272368611 to 272368616...
T+319   [DEBUG] [Task-21] Starting streaming blocks from 272368616 to 272368621...
T+1138  [*] [Task-21] Parsing block number #272368616 (5 blocks remaining)...
T+1138  [*] [Task-2] Parsing block number #272368521 (5 blocks remaining)...
T+1150  [DEBUG] [Task-2] action_trace=receiver: "eosio"
receipt {
  receiver: "eosio"
  digest: "bd12f2112f822a408d33fdef62e1d882ac823d8c37908c91254afe9d347a3b01"
  global_sequence: 356879133833
  auth_sequence {
    account_name: "aus1genereos"
    sequence: 1059537
  }
  recv_sequence: 346189547
  code_sequence: 18
  abi_sequence: 19
}
action {
  account: "eosio"
  name: "claimrewards"
  authorization {
    actor: "aus1genereos"
    permission: "claimer"
  }
  json_data: "{\"owner\":\"aus1genereos\"}"
  raw_data: "\200\251\272j*\026\2606"
}
elapsed: 230
transaction_id: "e34893fbf5c1ed8bd639b4b395fa546102b6708fbd45e4dcd0d9c2a3fc144b75"
block_num: 272368521
producer_block_id: "103c03898849d5d54fe2174119c6ae34d4cb5772328e64bee85da1c39eb583ba"
block_time {
  seconds: 1665360012
}
action_ordinal: 1
[...]
```