"""
# What is substreams_firehose ?

*substreams_firehose* is a data extraction tool leveraging the power of [**Firehose**](https://firehose.streamingfast.io/) \
and [**Substreams**](https://substreams.streamingfast.io) innovative technologies for accessing any blockchain-related data.

It acts as an easy-to-use interface to communicate with gRPC endpoints, simplifying the process of extracting data that matters to *you*.

Using a flexible approach, you can review and select which information to extract from these endpoints in the final output \
(JSONL is the default but it's entierly up to you how the data looks like at the end). You can then use this data to power \
other applications or for your own purpose.

See the [README.md](https://github.com/pinax-network/substreams_firehose#readme) file for more details.

# Background

In order to make the best out of this tool, you should be familiar with the underlying technologies it leverages.

## Firehose

From the StreamingFast team (core developers of the technology) [documentation](https://firehose.streamingfast.io/):
> The product provides previously unseen capabilities and speeds for indexing blockchain data using a files-based and \
streaming-first approach.

For any blockchain supported by *Firehose*, an instrumented blockchain node is runned to forward data that it receives and generates \
to other [*Firehose* components](https://firehose.streamingfast.io/architecture/components). The end user can then access this data \
by querying a [gRPC server](https://firehose.streamingfast.io/architecture/components/grpc-server).

## Substreams

*Substreams* are the evolution of *Firehose* nodes that aims to be highly composable, reusable, inter-connected and fast for accessing \
subsets of data. As putted in the [documentation](https://substreams.streamingfast.io/):
> Substreams enables developers to write Rust modules, composing data streams alongside the community, and provides extremely \
high-performance indexing by virtue of parallelization, in a streaming-first fashion.

> Substreams have all the benefits of StreamingFast Firehose, like low-cost caching and archiving of blockchain data, high \
throughput processing, and cursor-based reorgs handling.

The difference mostly lies in the server-side implementation with Substreams making the most of parallelization for indexing data.

The end user is still served by a gRPC endpoint although several middleman-services that transforms the data first \
(called [sinks](https://substreams.streamingfast.io/#network-model-diagram)) are available.

## gRPC streams

As you can see, both technologies uses the [*gRPC*](https://grpc.io/) protocol for streaming data out of their components.

gRPC makes data transfers fast and efficient by serializing it to raw binary data before sending it on the network. It uses \
protocol buffers (shortened to *protobufs*) to describe the format of the binary data, allowing the server and client to encode \
and decode it the same way.

As such, both needs the same *protobufs* in order to know how to handle the data.

These are stored in `.proto` files and are usually \
supplied by the server-side developer team to allow any clients to use it. Some servers can also implement a *reflection service* that \
can be queried for retrieving information about the available *protobufs*.

## gRPC in the context of Firehose/Substreams

With this information in mind, you can see that in order to extract blockchain data from a *Firehose* or *Substreams* gRPC endpoint, \
one must first know about what kind of data is served and available for extraction (again, described by *protobufs*).

*Substreams* makes it very easy as it provides [`.spkg` package files](https://substreams.streamingfast.io/reference-and-specs/packages) \
that includes all that information (and more for use by the server-side components). That means, **in order to communicate \
with a substream you must first provide the right package file for that substream** (which is usually bundled in the releases \
of the source code repo).

In both cases, you still need to have the `.proto` files definitions to be able to make requests and parse responses when communicating \
with an endpoint. A set of default *protobufs* are included with the tool to be used with the default endpoints provided \
(see [`substreams_firehose/proto`](https://github.com/pinax-network/substreams_firehose/tree/main/substreams_firehose/proto)).

# Using the substreams_firehose CLI tool

The package is designed to be run from the command-line as a python module. You can see the list of available options with the following \
command:
```console
(.venv) $ python -m substreams_firehose -h
```

The basic usage is to select a gRPC endpoint from the list stored in the \
[main configuration file](https://github.com/pinax-network/substreams_firehose#main-configuration-file) \
(`substreams_firehose/config.hjson` by default) with the `--grpc-entry` or `-g` flag. You can browse the list of data endpoints and see \
which blockchain they index by running the TUI configuration tool:
```console
(.venv) $ python -m substreams_firehose.config
```

Once you know which blockchain data you want to extract, simply specify a block range to get the relevant data. By default, every data \
available for each block from the endpoint will be extracted to a JSONL file, one line per block processed.

You can customize which data gets extracted by using the TUI configuration tool to edit \
[stub configuration files](https://github.com/pinax-network/substreams_firehose#stub-configuration-files) \
that will store all the information related to the extraction process. This makes it easy to manage different extraction goals for \
the same endpoint (e.g on Ethereum, you can have one config for getting only gas prices and another one for ether value transactions).

## Detailed example: extracting data from the Ethereum blockchain

Looking at our main configuration file, we have a [StreamingFast endpoint](https://mainnet.eth.streamingfast.io/) dedicated to storing \
block data from the Ethereum mainnet blockchain:
```json
"grpc": [
    ...,
    {
        "id": "eth_mainnet",
        "auth": "streamingfast",
        "chain": "Ethereum Mainnet",
        "compression": "gzip",
        "url": "mainnet.eth.streamingfast.io:443"
    },
    ...
]
```

We can pass the `id` to the `--grpc-entry` option of the CLI to query this endpoint. We'll use a range of 100 blocks and output \
to a `.jsonl` file:
```console
(.venv) $ python -m substreams_firehose 16608400 16608499 -g eth_mainnet -o eth.jsonl
```

This produces the following output (if you have setup your own API key from [StreamingFast](https://app.streamingfast.io/), see \
the [video](https://user-images.githubusercontent.com/23462475/219525336-9f44cba8-2db3-400f-a5cc-26fee10b9266.mp4) for how to set it \
from the TUI):
```console
(.venv) $ 2023-02-17 20:49:09:T+179 [*] Getting JWT token...
(.venv) $ 2023-02-17 20:49:09:T+183 [*] Got JWT token (cached) [SUCCESS]
(.venv) $ 2023-02-17 20:49:09:T+184 [*] Streaming 100 blocks on Ethereum Mainnet chain (running 25 workers)...
(.venv) $ 2023-02-17 20:49:09:T+185 [*] Getting JWT token...
(.venv) $ 2023-02-17 20:49:09:T+186 [*] Got JWT token (cached) [SUCCESS]
(.venv) $ 2023-02-17 20:49:10:T+1342 [*] Block streaming done !
(.venv) $ 2023-02-17 20:49:22:T+12718 [*] Finished block processing, parsed 100 rows of data [SUCCESS]
(.venv) $ 2023-02-17 20:49:26:T+16581 [*] Wrote 100 rows of data to eth.jsonl [SUCCESS]
```

And the data will look like this (note that block numbers won't necessary be in ascending order as the extraction process uses multiple \
parallel tasks):
```json
{"@type": "type.googleapis.com/sf.ethereum.type.v2.Block", "ver": 3, "hash": "uxC01u3G38h/xNX7SYHu42R52iLjCeFliGJNszdLvAo=", \
"number": "16608436",
{"@type": "type.googleapis.com/sf.ethereum.type.v2.Block", "ver": 3, "hash": "5CiKWxLLvYFbUAkc90Tm1ROiw+k7SegYTXqMiLmZROo=", \
"number": "16608437",
{"@type": "type.googleapis.com/sf.ethereum.type.v2.Block", "ver": 3, "hash": "IPM5K72Dm4keiGVpYxN+4s7zzA2Jb83WfyfEdVKprAs=", \
"number": "16608438",
{"@type": "type.googleapis.com/sf.ethereum.type.v2.Block", "ver": 3, "hash": "Z7MlgQ2db4LbKrn9FLSDICherJAvv+/oqwiiS8WFwlw=", \
"number": "16608469",
{"@type": "type.googleapis.com/sf.ethereum.type.v2.Block", "ver": 3, "hash": "lT6h0fagzxQLZmRTeYWcZ2bxqGPrdaprTEBF36Q0xvM=", \
"number": "16608470",
...
```

At this point you could further transform this data for whatever use you might want but there is still a **sizeable** volume of it \
to process (~165MB total).

Instead, we can write a stub configuration file to filter out only the data that we want to use, directly from the gRPC output.

To do that, start the TUI configuration tool:
```console
(.venv) $ python -m substreams_firehose.config
```

- On the main screen, bring up the main menu by pressing `[CTRL+X]` and select `Edit stub configuration`.
- Choose the previously used endpoint `Ethereum Mainnet (mainnet.eth.streamingfast.io:443)`.
- Select a location to save the stub configuration file (we'll assume to be in `substreams_firehose/config/firehose/eth.hjson`).
- Select the *Firehose V2* service named `sf.firehose.v2.Stream`.
- Only one method `Blocks` should be available, press `[OK]`.
- On the inputs screen, you can select to only include final blocks (meaning \
[finalized](https://www.alchemy.com/overviews/ethereum-commitment-levels) blocks in the context of Ethereum) in the output.
This doesn't apply here as we are already far enough into the past.
- Now, on the outputs screen, this is the important part. Choose the right type of blocks that this endpoint handles (namely \
`sf.ethereum.type.v2.Block` in our case) and **select below the output fields that you want to keep in the final output**.
Here's what fields we'll select for this example :
    + *hash*
    + *number*
    + *transaction_traces*
        + *to*
        + *value*
        + *type*
        + *hash*
        + *from*
        + *status*

Next you'll see a summary of what the stub configuration file will look like:
```json
{
    "base": "sf.firehose.v2",
    "service": "Stream",
    "method": "Blocks",
    "request": {
        "object": "Request",
        "params": {
            "final_blocks_only": false
        }
    },
    "response": {
        "object": "Response",
        "params": {
            "hash": "True",
            "number": "True",
            "transaction_traces": {
                "to": "True",
                "value": "True",
                "type": "True",
                "hash": "True",
                "from": "True",
                "status": "True"
            }
        }
    }
}
```

Press `[OK]` to confirm.

To use it, simply pass it to the CLI tool with the `--stub` or `-s` argument:
```console
(.venv) $ python -m substreams_firehose 14128200 14128299 -g eth_mainnet -o eth.jsonl -s substreams_firehose/config/firehose/eth.hjson
```

Now, the file size should have reduced to about 3.9MB (a -97% decrease !) and contains the following data:
```json
{"hash": "uxC01u3G38h/xNX7SYHu42R52iLjCeFliGJNszdLvAo=", "number": "16608436", "transaction_traces": ...}
{"hash": "5CiKWxLLvYFbUAkc90Tm1ROiw+k7SegYTXqMiLmZROo=", "number": "16608437", "transaction_traces": ...}
{"hash": "IPM5K72Dm4keiGVpYxN+4s7zzA2Jb83WfyfEdVKprAs=", "number": "16608438", "transaction_traces": ...}
{"hash": "Z7MlgQ2db4LbKrn9FLSDICherJAvv+/oqwiiS8WFwlw=", "number": "16608469", "transaction_traces": ...}
{"hash": "lT6h0fagzxQLZmRTeYWcZ2bxqGPrdaprTEBF36Q0xvM=", "number": "16608470", "transaction_traces": ...}
...
```

This is great but you'll notice that the values don't quite match what you will find from a block explorer like \
[Etherscan](https://etherscan.io) for example. This is because the values from this endpoint are returned encoded in `Base64`.

Now, you could have a script or some other tool to decrypt this data for you but if you know some Python, you can write a \
[custom block processor](https://github.com/pinax-network/substreams_firehose#block-processors) directly for use by the tool.

To do that, we implement a function inside the `substreams_firehose/block_processors/processor.py` module:
```python
from base64 import b64decode
def ethereum_processor(data: Message) -> Iterator[dict]:
    # Use the available internal `_filter_data` function to apply the filtering from the stub configuration
    block_data = _filter_data(data, StubConfig.RESPONSE_PARAMETERS)

    # Decode the data using the `base64` package
    block_data['hash'] = f'0x{b64decode(block_data["hash"]).hex()}'

    try:
        for transaction in block_data['transaction_traces']:
            for key, value in transaction.items():
                if key in ['hash', 'to', 'from']:
                    # Decode those addresses
                    transaction[key] = f'0x{b64decode(value).hex()}'
                elif key == 'value':
                    # The value here is converted from WEI to ETHER
                    # Notice the additional field `bytes` present as well
                    # You can notice it from the response and in the `sf.ethereum.type.v2.Block` proto file
                    transaction[key] = f'{int.from_bytes(b64decode(value["bytes"])) / 10**18}'
    except KeyError:
        # Sometimes no transactions might be recorded for a block and it will contain only `eth_call` instructions.
        pass

    # Important to yield the parsed block as every block processor function must act as a generator
    yield block_data
```

You'll notice the signature of the function which takes the raw gRPC message from the stream and **yields** a dictionary with the \
parsed data.

A utility function called `_filter_data` is available for applying the output fields filter set in the stub configuration file passed \
as CLI argument.

Finally, we get the data that we want with the following format:
```json
{
    "hash": "0x953ea1d1f6a0cf140b66645379859c6766f1a863eb75aa6b4c4045dfa434c6f3",
    "number": "16608470",
    "transaction_traces": [
        {
            "to": "0xdce67033ce64b923a00faedbd897736faa3f4930",
            "value": "0.083756",
            "hash": "0x57d348451af8a0264f7771629ed0878d7bd25845c318d970740f7f1c4c07462b",
            "from": "0x4103c267fba03a1df4fe84bc28092d629fa3f422",
            "status": "SUCCEEDED"
        },
        ...
    ]
}
...
```

Hopefully you now have a better idea of the capabilities of the tool and its usage to start creating your own stubs and eventual \
block processors !

*PS: As a little easter egg, if you search for the tx hash `0xbd72f4953024f5720d9e47cccdc869d64afcce331a9169ce5d3e1334c3b1af4c`, \
you'll witness some shady money laundering operation attributed to the \
[Wormhole bridge exploiter](https://etherscan.io/tx/0xbd72f4953024f5720d9e47cccdc869d64afcce331a9169ce5d3e1334c3b1af4c). More info \
on that story [here](https://www.certik.com/resources/blog/1kDYgyBcisoD2EqiBpHE5l-wormhole-bridge-exploit-incident-analysis) and \
[here](https://cointelegraph.com/news/wormhole-hacker-moves-another-46m-of-stolen-funds) \
if you're interested ;)*

# Using substreams_firehose as a library

*TODO: talk about block extractors / processors*
"""
