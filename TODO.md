# TODO

## Config tool

- Correct type editing and checking
  + .spkg, list of output modules for substreams
- Better stub config handling
  + Possibility to create new stub from template

## Pyfirehose

- Rework block processing for imports
- Clean-up and fix multi-channel extractor
- Add more examples to README.md
- Support for external block processing
- Performance tests and comparison
- Investigate functools and other more abstract modules for block processor modularity (?)
  + Possibility of 3 stages:
  + Pre-processing (e.g. load some API data)
  + Process (currently implemented)
  + Post-processing (e.g. adding more data to transactions)