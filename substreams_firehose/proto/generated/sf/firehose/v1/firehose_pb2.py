"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsf/firehose/v1/firehose.proto\x12\x0esf.firehose.v1\x1a\x19google/protobuf/any.proto"\x99\x02\n\x07Request\x12\x17\n\x0fstart_block_num\x18\x01 \x01(\x03\x12\x14\n\x0cstart_cursor\x18\r \x01(\t\x12\x16\n\x0estop_block_num\x18\x05 \x01(\x04\x12,\n\nfork_steps\x18\x08 \x03(\x0e2\x18.sf.firehose.v1.ForkStep\x12\x1f\n\x13include_filter_expr\x18\n \x01(\tB\x02\x18\x01\x12\x1f\n\x13exclude_filter_expr\x18\x0b \x01(\tB\x02\x18\x01\x12!\n\x19irreversibility_condition\x18\x11 \x01(\t\x12(\n\ntransforms\x18\x12 \x03(\x0b2\x14.google.protobuf.AnyJ\x04\x08\x0f\x10\x10J\x04\x08\x10\x10\x11"g\n\x08Response\x12#\n\x05block\x18\x01 \x01(\x0b2\x14.google.protobuf.Any\x12&\n\x04step\x18\x06 \x01(\x0e2\x18.sf.firehose.v1.ForkStep\x12\x0e\n\x06cursor\x18\n \x01(\t*\\\n\x08ForkStep\x12\x10\n\x0cSTEP_UNKNOWN\x10\x00\x12\x0c\n\x08STEP_NEW\x10\x01\x12\r\n\tSTEP_UNDO\x10\x02\x12\x15\n\x11STEP_IRREVERSIBLE\x10\x04"\x04\x08\x03\x10\x03"\x04\x08\x05\x10\x052G\n\x06Stream\x12=\n\x06Blocks\x12\x17.sf.firehose.v1.Request\x1a\x18.sf.firehose.v1.Response0\x01B9Z7github.com/streamingfast/pbgo/sf/firehose/v1;pbfirehoseb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sf.firehose.v1.firehose_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z7github.com/streamingfast/pbgo/sf/firehose/v1;pbfirehose'
    _REQUEST.fields_by_name['include_filter_expr']._options = None
    _REQUEST.fields_by_name['include_filter_expr']._serialized_options = b'\x18\x01'
    _REQUEST.fields_by_name['exclude_filter_expr']._options = None
    _REQUEST.fields_by_name['exclude_filter_expr']._serialized_options = b'\x18\x01'
    _FORKSTEP._serialized_start = 465
    _FORKSTEP._serialized_end = 557
    _REQUEST._serialized_start = 77
    _REQUEST._serialized_end = 358
    _RESPONSE._serialized_start = 360
    _RESPONSE._serialized_end = 463
    _STREAM._serialized_start = 559
    _STREAM._serialized_end = 630