"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"antelope/eosio/token/v1/test.proto\x12\x17antelope.eosio.token.v1\x1a\x1fgoogle/protobuf/timestamp.proto"\x1a\n\x07Account\x12\x0f\n\x07account\x18\x01 \x01(\x0c"\'\n\rCurrencyStats\x12\x16\n\x0ecurrency_stats\x18\x01 \x01(\x0c"G\n\x0eTransferEvents\x125\n\x05items\x18\x01 \x03(\x0b2&.antelope.eosio.token.v1.TransferEvent"\xe6\x01\n\rTransferEvent\x12\x11\n\tblock_num\x18\x01 \x01(\r\x12-\n\ttimestamp\x18\x02 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x0e\n\x06trx_id\x18\x03 \x01(\t\x12\x16\n\x0eaction_ordinal\x18\x04 \x01(\r\x12\x0f\n\x07account\x18\x05 \x01(\t\x12\x0f\n\x07symcode\x18\x06 \x01(\t\x12\x11\n\tprecision\x18\x07 \x01(\r\x12\x0c\n\x04from\x18\x08 \x01(\t\x12\n\n\x02to\x18\t \x01(\t\x12\x0e\n\x06amount\x18\n \x01(\x03\x12\x0c\n\x04memo\x18\x0b \x01(\tb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'antelope.eosio.token.v1.test_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ACCOUNT._serialized_start = 96
    _ACCOUNT._serialized_end = 122
    _CURRENCYSTATS._serialized_start = 124
    _CURRENCYSTATS._serialized_end = 163
    _TRANSFEREVENTS._serialized_start = 165
    _TRANSFEREVENTS._serialized_end = 236
    _TRANSFEREVENT._serialized_start = 239
    _TRANSFEREVENT._serialized_end = 469