# TODO

## Config tool

- Correct type editing and checking
  + .spkg, list of output modules for substreams
- Better editing
  + Get value back when entering edit mode
  + \<Escape\> key to go back without modification
- Better stub config handling
  + Select which one to edit
  + Possibility to create new
    * From other one as template

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