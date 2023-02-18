# Pinax - substreams_firehose

> Extract any data from the blockchain using gRPC-enabled endpoints (powered by [**Firehose**](https://firehose.streamingfast.io/) and [**Substreams**](https://substreams.streamingfast.io))

[![docs](https://github.com/pinax-network/substreams_firehose/actions/workflows/docs.yml/badge.svg)](https://github.com/pinax-network/substreams_firehose/actions/workflows/docs.yml) [![Pylint](https://github.com/pinax-network/substreams_firehose/actions/workflows/pylint.yml/badge.svg)](https://github.com/pinax-network/substreams_firehose/actions/workflows/pylint.yml)

## Overview

*substreams_firehose* is a data extraction tool leveraging the power of [**Firehose**](https://firehose.streamingfast.io/) and [**Substreams**](https://substreams.streamingfast.io) innovative technologies for accessing any blockchain-related data. It acts as an easy-to-use interface to communicate with gRPC endpoints, simplifying the process of extracting data that matters to *you*. 

Using a flexible approach, you can review and select which information to extract in the final output (JSONL is the default but it's entierly up to you how the data looks like at the end). You can then use this data to power other applications or for your own purpose.

## Quickstart

**Requires Python >= 3.7**

### Installing from PyPI

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install substreams_firehose 
```

### Installing from source

```console
$ git clone git@github.com:pinax-network/substreams_firehose.git
$ cd substreams_firehose
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
```

A [`.pylintrc`](.pylintrc) file is provided if you want to run [Pylint](https://pypi.org/project/pylint/):
```console
(.venv) $ pylint substreams_firehose --rcfile=.pylintrc
```

Auto-generated documentation can be browsed [here](https://pinax-network.github.io/substreams_firehose).

**Important: see the next section for how to setup your API keys.**

## Configuration files

To manage the list of blockchain data providers and the specific settings for individual gRPC connections, *substreams_firehose* uses two kind of configuration files (written in [Hjson](https://hjson.github.io/), an extended JSON format notably allowing comments to be added).

A TUI (Terminal User Interface) is available to manage (almost) all aspects of the configuration required for the tool. You can run it with the following command :
```console
(.venv) $ python -m substreams_firehose.config
```

Press `F1` on any screen of the TUI to access a help menu. For starter, you can bring the main menu on the starting screen by pressing `CTRL+X`.

*Note: the TUI requires your terminal emulator to support a 256 colors palette for syntax highlighting (if not, the tool still works you won't just see the pretty colors !). Check [here](https://github.com/termstandard/colors) if you're not sure that's the case.*

You can also edit any configuration file manually (stored under `.venv/lib/{PYTHON_VERSION}/site-packages/substreams_firehose/` with PyPI install) with the editor of your choice but beware it might break the application if edited incorrectly.

### *Main* configuration file

This file holds the list of endpoints serving data using either *Firehose*, *Substreams* or both. It specifies which *authentication* endpoint to use and adds a few details describing each endpoint as well as some other settings like the number of retries for failed blocks, etc. (see comments).

It is available in `.venv/lib/{PYTHON_VERSION}/site-packages/substreams_firehose/config.hjson` in the PyPI install. From source, you will want to copy the [`sample.config.hjson`](substreams_firehose/sample.config.hjson) file and rename it.

The most important part is to fill the `api_key` setting by registering an API key (with a *free* account) for each authentication endpoint you plan on using:
- For using [**Dfuse**](https://dfuse.eosnation.io) based endpoints, go to https://dfuse.eosnation.io/.
- For using [**Pinax**](https://pinax.network/) based endpoints, go to https://pinax.network/.
- For using [**StreamingFast**](https://www.streamingfast.io/) based endpoints, go to https://app.streamingfast.io/.

You can run the TUI configuration tool for setting your API keys. The tool will check that they are valid against the specified endpoint (hence why the `dummy` key used in the video below will fail to pass):

https://user-images.githubusercontent.com/23462475/219525336-9f44cba8-2db3-400f-a5cc-26fee10b9266.mp4

The TUI also allows you to add your own authentication providers and manage the list of data endpoints that you can query. 

### *Stub* configuration files

A stub configuration file describe a particular way to run a gRPC stream for querying blockchain data from an endpoint. They specify the objects that will be manipulated, the request parameters to send as well as the data to filter into the final output. As such, you can have *multiple* stub configs for an endpoint, each dedicated to extract some particular data.

Here's an example of a stub config dedicated to a substream:
```json5
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
      "modules" : "substreams_firehose/proto/common.spkg" // Substream package describing the data format
    }
  },
  "response": {
    "object": "Response", // Response object of the method
    "params": {} // Output filter (empty will get ALL the fields from the gRPC JSON response)
  }
}
```

Stub configuration files can be easily managed and edited using the TUI configuration tool. A step-by-step approach allows for easily filling all the required information to end up with a stub completely describing the extraction process for a given endpoint.

Here's a demo on how to setup a stub configuration for extracting gas prices data on the Ethereum mainnet and run it with the tool :

https://user-images.githubusercontent.com/23462475/219525512-9972ba67-eddb-4c1b-9946-92ec8a30202f.mp4

## Running the tool

`substreams_firehose` comes with a number of predefined endpoints, `.proto` files definitions and stub configurations to make it easy to use and not loose to much time setting up your own configurations.

From the TUI configuration tool starting screen (go back to the start of [Configuration files](#configuration-files) if you missed how to run it), you can see the list of available endpoints and the blockchain they target.

To extract data for a given block range, simply specify the `id` of an endpoint to the command-line tool. For example, to retrieve the latest 100 blocks data from the Ethereum main chain, you can run :
```console
(.venv) $ LAST_ETH_BLOCK=$(curl -s https://api.blockcypher.com/v1/eth/main | jq .height) && echo $LAST_ETH_BLOCK
(.venv) $ python -m substreams_firehose $(($LAST_ETH_BLOCK - 100)) $LAST_ETH_BLOCK --grpc-entry eth_mainnet --out-file jsonl/eth.jsonl
```
*Note: there is work-in-progress to allow specifying a date range instead of block numbers for the query, stay tuned !*

All the 100 latest block data will be stored in the `jsonl/eth.jsonl` file with one row for each block. If you have [`jq`](https://stedolan.github.io/jq/) installed, you can then preview the output with the following command :
```console
$ cat jsonl/eth.jsonl | jq --color-output | less --RAW-CONTROL-CHARS
```

To see all available options for the tool, run :
```console
(.venv) $ python -m substreams_firehose -h
```

## Block processors

For even more control over the data extracted, the extraction process uses a modular approach for manipulating response objects coming from a gRPC stream. A block processing function is used for extracting the data that is later stored in the output file at the end of the block extraction process.

Several [block processors](substreams_firehose/block_processors/processors.py) are available by default:
- `default_processor` will output *all* the data (filtered according to the stub config) from the gRPC response.
- `default_substream_processor` should be used with a **substream** and will output the data (filtered according to the stub config) from each of the output module in the gRPC response.
- `filtered_block_processor` will output the data (filtered according to the stub config) using the legacy [FirehoseV1](https://github.com/streamingfast/playground-firehose-eosio-go#query-language) filtering system.

All three will output the response data in JSON, with the final data being compiled in a JSONL file (one line for each response parsed). 

### Writing a custom block processor

Customizing the format of the data extracted is the main goal of writing a custom block processor.

In order to write custom block processing functions, some conditions must be respected:
- The function should be placed inside the [`processors.py`](substreams_firehose/block_processors/processors.py) file (avoid name conflicts with existing functions).
- The function should act as a **generator** (using the `yield` keyword) to return the data. A dictionary is the preferred format, but it could be any format (specify the `--no-json-output` flag if you don't want to convert the final output to JSON).
- The **first parameter** of the function should take the raw data extracted from the gRPC stream (Google protobuf [`Message`](https://googleapis.dev/python/protobuf/latest/google/protobuf/message.html#google.protobuf.message.Message) type).

You can use the `_filter_data` function to apply the filters defined in the stub config to the output and process it further from here. Or you can directly get all the content from the response using the `MessageToJson` function. See other block processors in the [`processors.py`](substreams_firehose/block_processors/processors.py) file for details and instructions.

You can then use a custom block processor through the command-line using the `--custom-processor` (or `-p`) argument and providing the name of the function. Also, if you do not want the final output to be converted to JSON before being sent to the output file, you can pass the `--no-json-output` flag.

For example, let's say you've implemented a custom function `my_block_processor` in `processors.py`. You would then pass the argument as `--custom-processor my_block_processor`. The script will locate it inside the `processors.py` module and use the `my_block_processor` function to parse block data and extract it to the output file.
