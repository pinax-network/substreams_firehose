"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1afirehose/annotations.proto\x12\x08firehose\x1a google/protobuf/descriptor.proto:4\n\x08required\x12\x1d.google.protobuf.FieldOptions\x18\xc9\xd9\x04 \x01(\x08\x88\x01\x01B9Z7github.com/streamingfast/pbgo/sf/firehose/v1;pbfirehoseb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'firehose.annotations_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(required)
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z7github.com/streamingfast/pbgo/sf/firehose/v1;pbfirehose'