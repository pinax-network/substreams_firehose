"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&sf/cosmos/transform/v1/transform.proto\x12\x16sf.cosmos.transform.v1"\xe7\x01\n\x0eCombinedFilter\x12C\n\x12event_type_filters\x18\x01 \x03(\x0b2\'.sf.cosmos.transform.v1.EventTypeFilter\x12G\n\x14event_origin_filters\x18\x02 \x03(\x0b2).sf.cosmos.transform.v1.EventOriginFilter\x12G\n\x14message_type_filters\x18\x03 \x03(\x0b2).sf.cosmos.transform.v1.MessageTypeFilter"&\n\x0fEventTypeFilter\x12\x13\n\x0bevent_types\x18\x01 \x03(\t"*\n\x11EventOriginFilter\x12\x15\n\revent_origins\x18\x01 \x03(\t"*\n\x11MessageTypeFilter\x12\x15\n\rmessage_types\x18\x01 \x03(\tBPZNgithub.com/figment-networks/proto-cosmos/pb/sf/cosmos/transform/v1;pbtransformb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sf.cosmos.transform.v1.transform_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZNgithub.com/figment-networks/proto-cosmos/pb/sf/cosmos/transform/v1;pbtransform'
    _COMBINEDFILTER._serialized_start = 67
    _COMBINEDFILTER._serialized_end = 298
    _EVENTTYPEFILTER._serialized_start = 300
    _EVENTTYPEFILTER._serialized_end = 338
    _EVENTORIGINFILTER._serialized_start = 340
    _EVENTORIGINFILTER._serialized_end = 382
    _MESSAGETYPEFILTER._serialized_start = 384
    _MESSAGETYPEFILTER._serialized_end = 426