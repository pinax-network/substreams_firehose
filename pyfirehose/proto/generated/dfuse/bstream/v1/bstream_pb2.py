"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1edfuse/bstream/v1/bstream.proto\x12\x10dfuse.bstream.v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x19google/protobuf/any.proto"\xb1\x01\n\x0cBlockRequest\x12\r\n\x05burst\x18\x01 \x01(\x03\x12\x14\n\x0ccontent_type\x18\x02 \x01(\t\x123\n\x05order\x18\x03 \x01(\x0e2$.dfuse.bstream.v1.BlockRequest.Order\x12\x11\n\trequester\x18\x04 \x01(\t"4\n\x05Order\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07ORDERED\x10\x01\x12\r\n\tUNORDERED\x10\x02"6\n\x1bIrreversibleBlocksRequestV2\x12\x17\n\x0fstart_block_num\x18\x01 \x01(\x03"\xf3\x01\n\x0fBlocksRequestV2\x12\x17\n\x0fstart_block_num\x18\x01 \x01(\x03\x12\x14\n\x0cstart_cursor\x18\r \x01(\t\x12\x16\n\x0estop_block_num\x18\x05 \x01(\x04\x12.\n\nfork_steps\x18\x08 \x03(\x0e2\x1a.dfuse.bstream.v1.ForkStep\x12\x1b\n\x13include_filter_expr\x18\n \x01(\t\x12\x1b\n\x13exclude_filter_expr\x18\x0b \x01(\t\x12/\n\x07details\x18\x0f \x01(\x0e2\x1e.dfuse.bstream.v1.BlockDetails"p\n\x0fBlockResponseV2\x12#\n\x05block\x18\x01 \x01(\x0b2\x14.google.protobuf.Any\x12(\n\x04step\x18\x06 \x01(\x0e2\x1a.dfuse.bstream.v1.ForkStep\x12\x0e\n\x06cursor\x18\n \x01(\t"\xb6\x01\n\x06Cursor\x12)\n\x05block\x18\x01 \x01(\x0b2\x1a.dfuse.bstream.v1.BlockRef\x12.\n\nhead_block\x18\x02 \x01(\x0b2\x1a.dfuse.bstream.v1.BlockRef\x12\'\n\x03lib\x18\x03 \x01(\x0b2\x1a.dfuse.bstream.v1.BlockRef\x12(\n\x04step\x18\x04 \x01(\x0e2\x1a.dfuse.bstream.v1.ForkStep"\xdb\x01\n\x05Block\x12\x0e\n\x06number\x18\x01 \x01(\x04\x12\n\n\x02id\x18\x02 \x01(\t\x12\x13\n\x0bprevious_id\x18\x03 \x01(\t\x12-\n\ttimestamp\x18\x04 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x0f\n\x07lib_num\x18\x05 \x01(\x04\x120\n\x0cpayload_kind\x18\x06 \x01(\x0e2\x1a.dfuse.bstream.v1.Protocol\x12\x17\n\x0fpayload_version\x18\x07 \x01(\x05\x12\x16\n\x0epayload_buffer\x18\x08 \x01(\x0c"#\n\x08BlockRef\x12\x0b\n\x03num\x18\x01 \x01(\x04\x12\n\n\x02id\x18\x02 \x01(\t*\\\n\x08ForkStep\x12\x10\n\x0cSTEP_UNKNOWN\x10\x00\x12\x0c\n\x08STEP_NEW\x10\x01\x12\r\n\tSTEP_UNDO\x10\x02\x12\x15\n\x11STEP_IRREVERSIBLE\x10\x04"\x04\x08\x03\x10\x03"\x04\x08\x05\x10\x05*?\n\x0cBlockDetails\x12\x16\n\x12BLOCK_DETAILS_FULL\x10\x00\x12\x17\n\x13BLOCK_DETAILS_LIGHT\x10\x01*)\n\x08Protocol\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x07\n\x03EOS\x10\x01\x12\x07\n\x03ETH\x10\x022R\n\x0bBlockStream\x12C\n\x06Blocks\x12\x1e.dfuse.bstream.v1.BlockRequest\x1a\x17.dfuse.bstream.v1.Block0\x012a\n\rBlockStreamV2\x12P\n\x06Blocks\x12!.dfuse.bstream.v1.BlocksRequestV2\x1a!.dfuse.bstream.v1.BlockResponseV20\x01B5Z3github.com/dfuse-io/pbgo/dfuse/bstream/v1;pbbstreamb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dfuse.bstream.v1.bstream_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z3github.com/dfuse-io/pbgo/dfuse/bstream/v1;pbbstream'
    _FORKSTEP._serialized_start = 1152
    _FORKSTEP._serialized_end = 1244
    _BLOCKDETAILS._serialized_start = 1246
    _BLOCKDETAILS._serialized_end = 1309
    _PROTOCOL._serialized_start = 1311
    _PROTOCOL._serialized_end = 1352
    _BLOCKREQUEST._serialized_start = 113
    _BLOCKREQUEST._serialized_end = 290
    _BLOCKREQUEST_ORDER._serialized_start = 238
    _BLOCKREQUEST_ORDER._serialized_end = 290
    _IRREVERSIBLEBLOCKSREQUESTV2._serialized_start = 292
    _IRREVERSIBLEBLOCKSREQUESTV2._serialized_end = 346
    _BLOCKSREQUESTV2._serialized_start = 349
    _BLOCKSREQUESTV2._serialized_end = 592
    _BLOCKRESPONSEV2._serialized_start = 594
    _BLOCKRESPONSEV2._serialized_end = 706
    _CURSOR._serialized_start = 709
    _CURSOR._serialized_end = 891
    _BLOCK._serialized_start = 894
    _BLOCK._serialized_end = 1113
    _BLOCKREF._serialized_start = 1115
    _BLOCKREF._serialized_end = 1150
    _BLOCKSTREAM._serialized_start = 1354
    _BLOCKSTREAM._serialized_end = 1436
    _BLOCKSTREAMV2._serialized_start = 1438
    _BLOCKSTREAMV2._serialized_end = 1535