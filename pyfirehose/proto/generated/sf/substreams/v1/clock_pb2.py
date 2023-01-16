"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1csf/substreams/v1/clock.proto\x12\x10sf.substreams.v1\x1a\x1fgoogle/protobuf/timestamp.proto"R\n\x05Clock\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06number\x18\x02 \x01(\x04\x12-\n\ttimestamp\x18\x03 \x01(\x0b2\x1a.google.protobuf.TimestampBFZDgithub.com/streamingfast/substreams/pb/sf/substreams/v1;pbsubstreamsb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sf.substreams.v1.clock_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZDgithub.com/streamingfast/substreams/pb/sf/substreams/v1;pbsubstreams'
    _CLOCK._serialized_start = 83
    _CLOCK._serialized_end = 165