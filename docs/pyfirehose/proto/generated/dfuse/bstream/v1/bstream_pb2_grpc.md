# Bstream Pb2 Grpc

[Eos-blockchain-data Index](../../../../../../README.md#eos-blockchain-data-index) /
[Pyfirehose](../../../../../index.md#pyfirehose) /
[Pyfirehose](../../../../../index.md#pyfirehose) /
[Generated](../../../index.md#generated) /
[Generated](../../../index.md#generated) /
[Generated](../../../index.md#generated) /
[V1](./index.md#v1) /
Bstream Pb2 Grpc

> Auto-generated documentation for [pyfirehose.proto.generated.dfuse.bstream.v1.bstream_pb2_grpc](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py) module.

- [Bstream Pb2 Grpc](#bstream-pb2-grpc)
  - [BlockStream](#blockstream)
    - [BlockStream.Blocks](#blockstreamblocks)
  - [BlockStreamServicer](#blockstreamservicer)
    - [BlockStreamServicer().Blocks](#blockstreamservicer()blocks)
  - [BlockStreamStub](#blockstreamstub)
  - [BlockStreamV2](#blockstreamv2)
    - [BlockStreamV2.Blocks](#blockstreamv2blocks)
  - [BlockStreamV2Servicer](#blockstreamv2servicer)
    - [BlockStreamV2Servicer().Blocks](#blockstreamv2servicer()blocks)
  - [BlockStreamV2Stub](#blockstreamv2stub)
  - [add_BlockStreamServicer_to_server](#add_blockstreamservicer_to_server)
  - [add_BlockStreamV2Servicer_to_server](#add_blockstreamv2servicer_to_server)

## BlockStream

[Show source in bstream_pb2_grpc.py:48](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L48)

Missing associated documentation comment in .proto file.

#### Signature

```python
class BlockStream(object):
    ...
```

### BlockStream.Blocks

[Show source in bstream_pb2_grpc.py:51](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L51)

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



## BlockStreamServicer

[Show source in bstream_pb2_grpc.py:24](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L24)

Missing associated documentation comment in .proto file.

#### Signature

```python
class BlockStreamServicer(object):
    ...
```

### BlockStreamServicer().Blocks

[Show source in bstream_pb2_grpc.py:27](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L27)

Missing associated documentation comment in .proto file.

#### Signature

```python
def Blocks(self, request, context):
    ...
```



## BlockStreamStub

[Show source in bstream_pb2_grpc.py:8](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L8)

Missing associated documentation comment in .proto file.

#### Signature

```python
class BlockStreamStub(object):
    def __init__(self, channel):
        ...
```



## BlockStreamV2

[Show source in bstream_pb2_grpc.py:109](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L109)

Missing associated documentation comment in .proto file.

#### Signature

```python
class BlockStreamV2(object):
    ...
```

### BlockStreamV2.Blocks

[Show source in bstream_pb2_grpc.py:112](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L112)

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



## BlockStreamV2Servicer

[Show source in bstream_pb2_grpc.py:85](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L85)

Missing associated documentation comment in .proto file.

#### Signature

```python
class BlockStreamV2Servicer(object):
    ...
```

### BlockStreamV2Servicer().Blocks

[Show source in bstream_pb2_grpc.py:88](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L88)

Missing associated documentation comment in .proto file.

#### Signature

```python
def Blocks(self, request, context):
    ...
```



## BlockStreamV2Stub

[Show source in bstream_pb2_grpc.py:69](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L69)

Missing associated documentation comment in .proto file.

#### Signature

```python
class BlockStreamV2Stub(object):
    def __init__(self, channel):
        ...
```



## add_BlockStreamServicer_to_server

[Show source in bstream_pb2_grpc.py:34](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L34)

#### Signature

```python
def add_BlockStreamServicer_to_server(servicer, server):
    ...
```



## add_BlockStreamV2Servicer_to_server

[Show source in bstream_pb2_grpc.py:95](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/dfuse/bstream/v1/bstream_pb2_grpc.py#L95)

#### Signature

```python
def add_BlockStreamV2Servicer_to_server(servicer, server):
    ...
```


