# Firehose Pb2 Grpc

[Eos-blockchain-data Index](../../../../../../README.md#eos-blockchain-data-index) /
[Pyfirehose](../../../../../index.md#pyfirehose) /
[Pyfirehose](../../../../../index.md#pyfirehose) /
[Generated](../../../index.md#generated) /
[Generated](../../../index.md#generated) /
[Generated](../../../index.md#generated) /
[V2](./index.md#v2) /
Firehose Pb2 Grpc

> Auto-generated documentation for [pyfirehose.proto.generated.sf.firehose.v2.firehose_pb2_grpc](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py) module.

- [Firehose Pb2 Grpc](#firehose-pb2-grpc)
  - [Fetch](#fetch)
    - [Fetch.Block](#fetchblock)
  - [FetchServicer](#fetchservicer)
    - [FetchServicer().Block](#fetchservicer()block)
  - [FetchStub](#fetchstub)
  - [Stream](#stream)
    - [Stream.Blocks](#streamblocks)
  - [StreamServicer](#streamservicer)
    - [StreamServicer().Blocks](#streamservicer()blocks)
  - [StreamStub](#streamstub)
  - [add_FetchServicer_to_server](#add_fetchservicer_to_server)
  - [add_StreamServicer_to_server](#add_streamservicer_to_server)

## Fetch

[Show source in firehose_pb2_grpc.py:109](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L109)

Missing associated documentation comment in .proto file.

#### Signature

```python
class Fetch(object):
    ...
```

### Fetch.Block

[Show source in firehose_pb2_grpc.py:112](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L112)

#### Signature

```python
@staticmethod
def Block(
    request,
    target,
    options=(),
    channel_credentials=None,
    call_credentials=None,
    insecure=False,
    compression=None,
    wait_for_ready=None,
    timeout=None,
    metadata=None,
):
    ...
```



## FetchServicer

[Show source in firehose_pb2_grpc.py:85](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L85)

Missing associated documentation comment in .proto file.

#### Signature

```python
class FetchServicer(object):
    ...
```

### FetchServicer().Block

[Show source in firehose_pb2_grpc.py:88](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L88)

Missing associated documentation comment in .proto file.

#### Signature

```python
def Block(self, request, context):
    ...
```



## FetchStub

[Show source in firehose_pb2_grpc.py:69](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L69)

Missing associated documentation comment in .proto file.

#### Signature

```python
class FetchStub(object):
    def __init__(self, channel):
        ...
```



## Stream

[Show source in firehose_pb2_grpc.py:48](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L48)

Missing associated documentation comment in .proto file.

#### Signature

```python
class Stream(object):
    ...
```

### Stream.Blocks

[Show source in firehose_pb2_grpc.py:51](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L51)

#### Signature

```python
@staticmethod
def Blocks(
    request,
    target,
    options=(),
    channel_credentials=None,
    call_credentials=None,
    insecure=False,
    compression=None,
    wait_for_ready=None,
    timeout=None,
    metadata=None,
):
    ...
```



## StreamServicer

[Show source in firehose_pb2_grpc.py:24](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L24)

Missing associated documentation comment in .proto file.

#### Signature

```python
class StreamServicer(object):
    ...
```

### StreamServicer().Blocks

[Show source in firehose_pb2_grpc.py:27](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L27)

Missing associated documentation comment in .proto file.

#### Signature

```python
def Blocks(self, request, context):
    ...
```



## StreamStub

[Show source in firehose_pb2_grpc.py:8](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L8)

Missing associated documentation comment in .proto file.

#### Signature

```python
class StreamStub(object):
    def __init__(self, channel):
        ...
```



## add_FetchServicer_to_server

[Show source in firehose_pb2_grpc.py:95](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L95)

#### Signature

```python
def add_FetchServicer_to_server(servicer, server):
    ...
```



## add_StreamServicer_to_server

[Show source in firehose_pb2_grpc.py:34](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/firehose/v2/firehose_pb2_grpc.py#L34)

#### Signature

```python
def add_StreamServicer_to_server(servicer, server):
    ...
```


