"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&sf/solana/serumhist/v1/serumhist.proto\x12\x16sf.solana.serumhist.v1\x1a\x1fgoogle/protobuf/timestamp.proto"1\n\x0fGetFillsRequest\x12\x0e\n\x06trader\x18\x01 \x01(\x0c\x12\x0e\n\x06market\x18\x02 \x01(\x0c"M\n\rFillsResponse\x12*\n\x04fill\x18\x01 \x03(\x0b2\x1c.sf.solana.serumhist.v1.Fill\x12\x10\n\x08has_more\x18\x02 \x01(\x08"5\n\x11TrackOrderRequest\x12\x0e\n\x06market\x18\x01 \x01(\x0c\x12\x10\n\x08order_id\x18\x02 \x01(\t"\xf8\x04\n\x0fOrderTransition\x12E\n\x0eprevious_state\x18\x01 \x01(\x0e2-.sf.solana.serumhist.v1.OrderTransition.State\x12D\n\rcurrent_state\x18\x02 \x01(\x0e2-.sf.solana.serumhist.v1.OrderTransition.State\x12F\n\ntransition\x18\x03 \x01(\x0e22.sf.solana.serumhist.v1.OrderTransition.Transition\x12,\n\x05order\x18\x04 \x01(\x0b2\x1d.sf.solana.serumhist.v1.Order\x120\n\nadded_fill\x18\x05 \x01(\x0b2\x1c.sf.solana.serumhist.v1.Fill\x12<\n\x0ccancellation\x18\x06 \x01(\x0b2&.sf.solana.serumhist.v1.InstructionRef"\x84\x01\n\x05State\x12\x11\n\rSTATE_UNKNOWN\x10\x00\x12\x12\n\x0eSTATE_APPROVED\x10\x01\x12\x18\n\x14STATE_CANCEL_PENDING\x10\x02\x12\x13\n\x0fSTATE_CANCELLED\x10\x03\x12\x11\n\rSTATE_PARTIAL\x10\x04\x12\x12\n\x0eSTATE_EXECUTED\x10\x05"k\n\nTransition\x12\x0e\n\nTRANS_INIT\x10\x00\x12\x12\n\x0eTRANS_ACCEPTED\x10\x01\x12\x13\n\x0fTRANS_CANCELLED\x10\x02\x12\x10\n\x0cTRANS_FILLED\x10\x03\x12\x12\n\x0eTRANS_EXECUTED\x10\x04"\x97\x01\n\x0eInstructionRef\x12\x11\n\tblock_num\x18\x01 \x01(\x04\x12\x0e\n\x06trx_id\x18\x02 \x01(\x0c\x12\x0f\n\x07trx_idx\x18\x03 \x01(\r\x12\x10\n\x08inst_idx\x18\x04 \x01(\r\x12\x10\n\x08block_id\x18\x05 \x01(\x0c\x12-\n\ttimestamp\x18\x06 \x01(\x0b2\x1a.google.protobuf.Timestamp"K\n\nCheckpoint\x12\x1e\n\x16last_written_block_num\x18\x01 \x01(\x04\x12\x1d\n\x15last_written_block_id\x18\x02 \x01(\x0c"\x98\x03\n\x04Fill\x12\x0e\n\x06trader\x18\x01 \x01(\x0c\x12\x0e\n\x06market\x18\x02 \x01(\x0c\x12\x10\n\x08order_id\x18\x03 \x01(\t\x12*\n\x04side\x18\x04 \x01(\x0e2\x1c.sf.solana.serumhist.v1.Side\x12\r\n\x05maker\x18\x05 \x01(\x08\x12\x17\n\x0fnative_qty_paid\x18\x06 \x01(\x04\x12\x1b\n\x13native_qty_received\x18\x07 \x01(\x04\x12\x1c\n\x14native_fee_or_rebate\x18\x08 \x01(\x04\x121\n\x08fee_tier\x18\t \x01(\x0e2\x1f.sf.solana.serumhist.v1.FeeTier\x12-\n\ttimestamp\x18\n \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x11\n\tblock_num\x18\x14 \x01(\x04\x12\x10\n\x08block_id\x18\x18 \x01(\x0c\x12\x0e\n\x06trx_id\x18\x19 \x01(\x0c\x12\x0f\n\x07trx_idx\x18\x15 \x01(\r\x12\x10\n\x08inst_idx\x18\x16 \x01(\r\x12\x15\n\rorder_seq_num\x18\x17 \x01(\x04"\xc1\x02\n\x05Order\x12\x0b\n\x03num\x18\x01 \x01(\x04\x12\x0e\n\x06market\x18\x02 \x01(\x0c\x12\x0e\n\x06trader\x18\x03 \x01(\x0c\x12*\n\x04side\x18\x04 \x01(\x0e2\x1c.sf.solana.serumhist.v1.Side\x12\x13\n\x0blimit_price\x18\x05 \x01(\x04\x12\x14\n\x0cmax_quantity\x18\x06 \x01(\x04\x12/\n\x04type\x18\x07 \x01(\x0e2!.sf.solana.serumhist.v1.OrderType\x12+\n\x05fills\x18\n \x03(\x0b2\x1c.sf.solana.serumhist.v1.Fill\x12\x11\n\tblock_num\x18\x14 \x01(\x04\x12\x10\n\x08block_id\x18\x18 \x01(\x0c\x12\x0e\n\x06trx_id\x18\x19 \x01(\x0c\x12\x0f\n\x07trx_idx\x18\x15 \x01(\r\x12\x10\n\x08inst_idx\x18\x16 \x01(\r*\x18\n\x04Side\x12\x07\n\x03BID\x10\x00\x12\x07\n\x03ASK\x10\x01*O\n\x07FeeTier\x12\x08\n\x04Base\x10\x00\x12\x08\n\x04SRM2\x10\x01\x12\x08\n\x04SRM3\x10\x02\x12\x08\n\x04SRM4\x10\x03\x12\x08\n\x04SRM5\x10\x04\x12\x08\n\x04SRM6\x10\x05\x12\x08\n\x04MSRM\x10\x06*>\n\tOrderType\x12\t\n\x05LIMIT\x10\x00\x12\x17\n\x13IMMEDIATE_OR_CANCEL\x10\x01\x12\r\n\tPOST_ONLY\x10\x022w\n\x11SerumOrderTracker\x12b\n\nTrackOrder\x12).sf.solana.serumhist.v1.TrackOrderRequest\x1a\'.sf.solana.serumhist.v1.OrderTransition0\x012j\n\x0cSerumHistory\x12Z\n\x08GetFills\x12\'.sf.solana.serumhist.v1.GetFillsRequest\x1a%.sf.solana.serumhist.v1.FillsResponseBVZTgithub.com/streamingfast/firehose-solana/types/pb/sf/solana/serumhist/v1;pbserumhistb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sf.solana.serumhist.v1.serumhist_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZTgithub.com/streamingfast/firehose-solana/types/pb/sf/solana/serumhist/v1;pbserumhist'
    _SIDE._serialized_start = 1885
    _SIDE._serialized_end = 1909
    _FEETIER._serialized_start = 1911
    _FEETIER._serialized_end = 1990
    _ORDERTYPE._serialized_start = 1992
    _ORDERTYPE._serialized_end = 2054
    _GETFILLSREQUEST._serialized_start = 99
    _GETFILLSREQUEST._serialized_end = 148
    _FILLSRESPONSE._serialized_start = 150
    _FILLSRESPONSE._serialized_end = 227
    _TRACKORDERREQUEST._serialized_start = 229
    _TRACKORDERREQUEST._serialized_end = 282
    _ORDERTRANSITION._serialized_start = 285
    _ORDERTRANSITION._serialized_end = 917
    _ORDERTRANSITION_STATE._serialized_start = 676
    _ORDERTRANSITION_STATE._serialized_end = 808
    _ORDERTRANSITION_TRANSITION._serialized_start = 810
    _ORDERTRANSITION_TRANSITION._serialized_end = 917
    _INSTRUCTIONREF._serialized_start = 920
    _INSTRUCTIONREF._serialized_end = 1071
    _CHECKPOINT._serialized_start = 1073
    _CHECKPOINT._serialized_end = 1148
    _FILL._serialized_start = 1151
    _FILL._serialized_end = 1559
    _ORDER._serialized_start = 1562
    _ORDER._serialized_end = 1883
    _SERUMORDERTRACKER._serialized_start = 2056
    _SERUMORDERTRACKER._serialized_end = 2175
    _SERUMHISTORY._serialized_start = 2177
    _SERUMHISTORY._serialized_end = 2283