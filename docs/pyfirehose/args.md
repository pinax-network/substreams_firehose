# Args

[Pyfirehose Index](../README.md#pyfirehose-index) /
[Pyfirehose](./index.md#pyfirehose) /
Args

> Auto-generated documentation for [pyfirehose.args](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/args.py) module.

- [Args](#args)
  - [check_period](#check_period)
  - [parse_arguments](#parse_arguments)

## check_period

[Show source in args.py:12](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/args.py#L12)

Convert the specified period argument, from an integer or a date, to a block number.

#### Arguments

- `arg_period` - A period argument from the ArgumentParser.

#### Returns

An integer representing the corresponding block number.

#### Raises

- `ArgumentTypeError` - If the period cannot be parsed.

#### Signature

```python
def check_period(arg_period: str) -> int:
    ...
```



## parse_arguments

[Show source in args.py:35](https://github.com/Krow10/pyfirehose/blob/main/pyfirehose/args.py#L35)

Setup the command line interface and return the parsed arguments.

#### Returns

A Namespace object containing the parsed arguments.

#### Signature

```python
def parse_arguments() -> argparse.Namespace:
    ...
```


