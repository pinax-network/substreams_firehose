"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsf/firehose/v2/firehose.proto\x12\x0esf.firehose.v2\x1a\x19google/protobuf/any.proto"\x8f\x03\n\x12SingleBlockRequest\x12F\n\x0cblock_number\x18\x03 \x01(\x0b2..sf.firehose.v2.SingleBlockRequest.BlockNumberH\x00\x12V\n\x15block_hash_and_number\x18\x04 \x01(\x0b25.sf.firehose.v2.SingleBlockRequest.BlockHashAndNumberH\x00\x12;\n\x06cursor\x18\x05 \x01(\x0b2).sf.firehose.v2.SingleBlockRequest.CursorH\x00\x12(\n\ntransforms\x18\x06 \x03(\x0b2\x14.google.protobuf.Any\x1a\x1a\n\x0bBlockNumber\x12\x0b\n\x03num\x18\x01 \x01(\x04\x1a/\n\x12BlockHashAndNumber\x12\x0b\n\x03num\x18\x01 \x01(\x04\x12\x0c\n\x04hash\x18\x02 \x01(\t\x1a\x18\n\x06Cursor\x12\x0e\n\x06cursor\x18\x01 \x01(\tB\x0b\n\treference":\n\x13SingleBlockResponse\x12#\n\x05block\x18\x01 \x01(\x0b2\x14.google.protobuf.Any"\x8f\x01\n\x07Request\x12\x17\n\x0fstart_block_num\x18\x01 \x01(\x03\x12\x0e\n\x06cursor\x18\x02 \x01(\t\x12\x16\n\x0estop_block_num\x18\x03 \x01(\x04\x12\x19\n\x11final_blocks_only\x18\x04 \x01(\x08\x12(\n\ntransforms\x18\n \x03(\x0b2\x14.google.protobuf.Any"g\n\x08Response\x12#\n\x05block\x18\x01 \x01(\x0b2\x14.google.protobuf.Any\x12&\n\x04step\x18\x06 \x01(\x0e2\x18.sf.firehose.v2.ForkStep\x12\x0e\n\x06cursor\x18\n \x01(\t*G\n\x08ForkStep\x12\x0e\n\nSTEP_UNSET\x10\x00\x12\x0c\n\x08STEP_NEW\x10\x01\x12\r\n\tSTEP_UNDO\x10\x02\x12\x0e\n\nSTEP_FINAL\x10\x032G\n\x06Stream\x12=\n\x06Blocks\x12\x17.sf.firehose.v2.Request\x1a\x18.sf.firehose.v2.Response0\x012Y\n\x05Fetch\x12P\n\x05Block\x12".sf.firehose.v2.SingleBlockRequest\x1a#.sf.firehose.v2.SingleBlockResponseB9Z7github.com/streamingfast/pbgo/sf/firehose/v2;pbfirehoseb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sf.firehose.v2.firehose_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z7github.com/streamingfast/pbgo/sf/firehose/v2;pbfirehose'
    _FORKSTEP._serialized_start = 789
    _FORKSTEP._serialized_end = 860
    _SINGLEBLOCKREQUEST._serialized_start = 77
    _SINGLEBLOCKREQUEST._serialized_end = 476
    _SINGLEBLOCKREQUEST_BLOCKNUMBER._serialized_start = 362
    _SINGLEBLOCKREQUEST_BLOCKNUMBER._serialized_end = 388
    _SINGLEBLOCKREQUEST_BLOCKHASHANDNUMBER._serialized_start = 390
    _SINGLEBLOCKREQUEST_BLOCKHASHANDNUMBER._serialized_end = 437
    _SINGLEBLOCKREQUEST_CURSOR._serialized_start = 439
    _SINGLEBLOCKREQUEST_CURSOR._serialized_end = 463
    _SINGLEBLOCKRESPONSE._serialized_start = 478
    _SINGLEBLOCKRESPONSE._serialized_end = 536
    _REQUEST._serialized_start = 539
    _REQUEST._serialized_end = 682
    _RESPONSE._serialized_start = 684
    _RESPONSE._serialized_end = 787
    _STREAM._serialized_start = 862
    _STREAM._serialized_end = 933
    _FETCH._serialized_start = 935
    _FETCH._serialized_end = 1024