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
$ # Edit sample config file with editor of your choice to add your API keys
$ cd pyfirehose
$ vim pyfirehose/sample.config.hjson
$ # Rename to config.hjson
$ mv pyfirehose/sample.config.hjson pyfirehose/config.hjson
$ # Create and activate virtual environnement
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ # Install dependencies and run the program as a module
(.venv) $ pip install -r requirements.txt
(.venv) $ python -m pyfirehose -h
usage: __main__.py [-h] [-c CONFIG] [-s STUB] [-o OUT_FILE] [-l [LOG]] [-q] [-g GRPC_ENTRY] [-e {optimized,single,multi}] [-p CUSTOM_PROCESSOR]
                   [--no-json-output] [--overwrite-log] [--request-parameters ...]
                   start end

Extract any data from the blockchain. Powered by Firehose (https://firehose.streamingfast.io/) and Substreams (https://substreams.streamingfast.io).

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
                        name of a custom block processing function located in the "block_processors.processors" module (default: default_processor)
  --no-json-output      don't try to convert block processor output to JSON (default: False)
  --overwrite-log       overwrite log file, erasing its content (default is to append) (default: False)
  --request-parameters ...
                        optional keyword arguments (key=val) sent with the gRPC request (must match .proto definition, will override any parameters set in
                        the config) (default: None)
```

The period's *start* and *end* accepts either a block number or a [ISO-like formatted date time](https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat). By default, the extracted data will be stored in a `.jsonl` file inside the [`jsonl/`](jsonl/) directory.

A [`.pylintrc`](.pylintrc) file is provided if you want to run [Pylint](https://pypi.org/project/pylint/):
```console
(.venv) $ pylint pyfirehose --rcfile=.pylintrc
```

Auto-generated documentation can be browsed [here](https://pinax-network.github.io/pyfirehose/docs).

## Configuration files

To manage the list of blockchain data providers and the specific settings for individual gRPC connections, *PyFirehose* uses two kind of configuration files (written in [Hjson](https://hjson.github.io/), an extended JSON format notably allowing comments to be added).

### *Main* configuration file

This file holds the list of endpoints serving data using either *Firehose*, *Substreams* or both. It specifies which *authentication* endpoint to use and adds a few details describing each endpoint as well as some other settings like the requests' cache duration, etc (see comments).

The most important part is to fill the `api_key` setting by registering an API key (with a *free* account) for each authentication endpoint you plan on using:
- For using [**Dfuse**](https://dfuse.eosnation.io) based endpoints, go to https://dfuse.eosnation.io/.
- For using [**Pinax**](https://pinax.network/) based endpoints, go to https://pinax.network/.
- For using [**StreamingFast**](https://www.streamingfast.io/) based endpoints, go to https://app.streamingfast.io/.

Then edit the `pyfirehose/config.hjson` file:
```json
{
  // Authentication endpoints for issuing JWT tokens
  "auth": {
    "dfuse": {
      "api_key": "<YOUR_API_KEY>",
      "endpoint": "https://auth.eosnation.io/v1/auth/issue"
    },
    "pinax": {
      "api_key": "<YOUR_API_KEY>",
      "endpoint": "https://auth.pinax.network/v1/auth/issue"
    },
    "streamingfast": {
      "api_key": "<YOUR_API_KEY>",
      "endpoint": "https://auth.streamingfast.io/v1/auth/issue"
    }
  },
  ...
}
```

If you want to add your own provider, you can create a new entry in the `grpc` array like so:
```json
{
  "id": "<unique identifier for the endpoint>",
  "auth": "<authentication endpoint to use>", // One of the entry in the "auth" object
  "chain": "<descriptive text for the targeted blockchain>",
  "stub": "<a path or json object for the default stub configuration to use with this endpoint>",
  "url": "<gRPC endpoint address>", // Usually in the form "ip:port"
},
```

*Coming soon : managing auth and data providers using the config UI tool (see below).*

### *Stub* configuration files

A stub configuration file describe a particular way to run a gRPC stream for querying blockchain data from an endpoint. They specify the objects that will be manipulated, the request parameters to send as well as the data to filter into the final output. As such, you can have *multiple* stub configs for an endpoint, each dedicated to extract some particular data.

Here's an example of a stub config dedicated to a substream:
```json
{
  "base": "sf.substreams.v1", // Package of the protofile holding the gRPC objects
  "service": "Stream", // Service to use on the gRPC endpoint
  "method": "Blocks", // Method of the service to use
  "request": {
    "object": "Request", // Request object of the method
    "params": {
      "output_modules": [ // Substream output parameter
        "map_block",
      ],
      "modules" : "pyfirehose/proto/common.spkg" // Substream package describing the data format
    }
  },
  "response": {
    "object": "Response", // Response object of the method
    "params": {} // Output filter (empty will get ALL the fields from the gRPC JSON response)
  }
}
```

Stub configuration files can be easily managed and edited using the config UI tool (see below).

### Using the config UI tool

This is still a *Work-In-Progress* but right now you can fully add and edit stub configuration files easily using the UI interface to specify all the parameters required.

[![PyFirehose ethereum data extraction demo](https://user-images.githubusercontent.com/550895/214672801-de39738a-ca8e-461b-8552-da7f97eeb816.png)](https://user-images.githubusercontent.com/23462475/214952950-256b73cc-3f2a-469f-911b-aaae00f8629c.mp4)

## Block processors

For even more control over the data extracted, the extraction process uses a modular approach for manipulating response objects coming from a gRPC stream. A block processing function is used for extracting the data that is later stored in the output file at the end of the block extraction process.

Several [block processors](pyfirehose/block_processors/processors.py) are available by default:
- `default_processor` will output *all* the data (filtered according to the stub config) from the gRPC response.
- `default_substream_processor` should be used with a substream and will output the data (filtered according to the stub config) from each of the output module in the gRPC response.
- `filtered_block_processor` will output the data (filtered according to the stub config) using the legacy [FirehoseV1](https://github.com/streamingfast/playground-firehose-eosio-go#query-language) filtering system.

All three will output the response data in JSON, with the final data being compiled in a JSONL file (one line for each response parsed). 

### Writing a custom block processor

Customizing the format of the data extracted is the main goal of writing a custom block processor.

In order to write custom block processing functions, some conditions must be respected:
- The function should be placed inside the [`processors.py`](pyfirehose/block_processors/processors.py) file (avoid name conflicts with existing functions).
- The function should act as a **generator** (using the `yield` keyword) to return the data. A dictionary is the preferred format, but it could be any format (specify the `--no-json-output` flag if you don't want to convert the final output to JSON).
- The **first parameter** of the function should take the raw data extracted from the gRPC stream (Google protobuf [`Message`](https://googleapis.dev/python/protobuf/latest/google/protobuf/message.html#google.protobuf.message.Message) type).

You can use the `_filter_data` function to apply the filters defined in the stub config to the output and process it further from here. Or you can directly get all the content from the response using the `MessageToJson` function. See other block processors in the [`processors.py`](pyfirehose/block_processors/processors.py) file for details and instructions.

You can then use a custom block processor through the command-line using the `--custom-processor` (or `-p`) argument and providing the name of the function.

For example, let's say you've implemented a custom function `my_block_processor` in `processors.py`. You would then pass the argument as `--custom-processor my_block_processor`. The script will locate it inside the `processors.py` module and use the `my_block_processor` function to parse block data and extract it to the output file.
