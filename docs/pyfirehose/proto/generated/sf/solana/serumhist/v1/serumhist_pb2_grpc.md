# Serumhist Pb2 Grpc

[Eos-blockchain-data Index](../../../../../../../README.md#eos-blockchain-data-index) /
[Pyfirehose](../../../../../../index.md#pyfirehose) /
[Pyfirehose](../../../../../../index.md#pyfirehose) /
[Generated](../../../../index.md#generated) /
[Generated](../../../../index.md#generated) /
[Generated](../../../../index.md#generated) /
[Generated](../../../../index.md#generated) /
[V1](./index.md#v1) /
Serumhist Pb2 Grpc

> Auto-generated documentation for [pyfirehose.proto.generated.sf.solana.serumhist.v1.serumhist_pb2_grpc](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py) module.

- [Serumhist Pb2 Grpc](#serumhist-pb2-grpc)
  - [SerumHistory](#serumhistory)
    - [SerumHistory.GetFills](#serumhistorygetfills)
  - [SerumHistoryServicer](#serumhistoryservicer)
    - [SerumHistoryServicer().GetFills](#serumhistoryservicer()getfills)
  - [SerumHistoryStub](#serumhistorystub)
  - [SerumOrderTracker](#serumordertracker)
    - [SerumOrderTracker.TrackOrder](#serumordertrackertrackorder)
  - [SerumOrderTrackerServicer](#serumordertrackerservicer)
    - [SerumOrderTrackerServicer().TrackOrder](#serumordertrackerservicer()trackorder)
  - [SerumOrderTrackerStub](#serumordertrackerstub)
  - [add_SerumHistoryServicer_to_server](#add_serumhistoryservicer_to_server)
  - [add_SerumOrderTrackerServicer_to_server](#add_serumordertrackerservicer_to_server)

## SerumHistory

[Show source in serumhist_pb2_grpc.py:109](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L109)

Missing associated documentation comment in .proto file.

#### Signature

```python
class SerumHistory(object):
    ...
```

### SerumHistory.GetFills

[Show source in serumhist_pb2_grpc.py:112](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L112)

#### Signature

```python
@staticmethod
def GetFills(
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



## SerumHistoryServicer

[Show source in serumhist_pb2_grpc.py:85](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L85)

Missing associated documentation comment in .proto file.

#### Signature

```python
class SerumHistoryServicer(object):
    ...
```

### SerumHistoryServicer().GetFills

[Show source in serumhist_pb2_grpc.py:88](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L88)

Missing associated documentation comment in .proto file.

#### Signature

```python
def GetFills(self, request, context):
    ...
```



## SerumHistoryStub

[Show source in serumhist_pb2_grpc.py:69](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L69)

Missing associated documentation comment in .proto file.

#### Signature

```python
class SerumHistoryStub(object):
    def __init__(self, channel):
        ...
```



## SerumOrderTracker

[Show source in serumhist_pb2_grpc.py:48](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L48)

Missing associated documentation comment in .proto file.

#### Signature

```python
class SerumOrderTracker(object):
    ...
```

### SerumOrderTracker.TrackOrder

[Show source in serumhist_pb2_grpc.py:51](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L51)

#### Signature

```python
@staticmethod
def TrackOrder(
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



## SerumOrderTrackerServicer

[Show source in serumhist_pb2_grpc.py:24](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L24)

Missing associated documentation comment in .proto file.

#### Signature

```python
class SerumOrderTrackerServicer(object):
    ...
```

### SerumOrderTrackerServicer().TrackOrder

[Show source in serumhist_pb2_grpc.py:27](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L27)

Missing associated documentation comment in .proto file.

#### Signature

```python
def TrackOrder(self, request, context):
    ...
```



## SerumOrderTrackerStub

[Show source in serumhist_pb2_grpc.py:8](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L8)

Missing associated documentation comment in .proto file.

#### Signature

```python
class SerumOrderTrackerStub(object):
    def __init__(self, channel):
        ...
```



## add_SerumHistoryServicer_to_server

[Show source in serumhist_pb2_grpc.py:95](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L95)

#### Signature

```python
def add_SerumHistoryServicer_to_server(servicer, server):
    ...
```



## add_SerumOrderTrackerServicer_to_server

[Show source in serumhist_pb2_grpc.py:34](https://github.com/Krow10/eos-blockchain-data/blob/main/pyfirehose/proto/generated/sf/solana/serumhist/v1/serumhist_pb2_grpc.py#L34)

#### Signature

```python
def add_SerumOrderTrackerServicer_to_server(servicer, server):
    ...
```


