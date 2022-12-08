# TODO
* Better protobuf generation
  - Fix generated python module import paths
    + https://github.com/protocolbuffers/protobuf/issues/1491
    + https://github.com/protocolbuffers/protobuf/issues/881
  - Add docs for need to specify full path in module import in .proto files
* Finish chain selection and stub creation
  - Handle multiple import dir for stub config
  - Automatic endpoint detection and proto definitions from gRPC reflection service
* Clean-up and fix multi-channel extractor
* Add more examples to README.md
* Support for external block processing
* Performance tests and comparison
* NEXT BIG STEP:
  - .proto files are king: generate code for the whole pipeline from them
    + Make very robust proto folder handling and stub generation
  - Have a wrapper tool for creating stub configs
    + Select request parameters AND response fields to be extracted
  - Generate block processors
* Integrate Substreams as an alternative to Firehose (?)
  - Can the pipeline remain mostly the same ?
* Investigate functools and other more abstract modules for block processor modularity (?)
  - Possibility of 3 stages:
  - Pre-processing (e.g. load some API data)
  - Process (currently implemented)
  - Post-processing (e.g. adding more data to transactions)