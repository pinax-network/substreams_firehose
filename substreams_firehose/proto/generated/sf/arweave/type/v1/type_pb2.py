"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsf/arweave/type/v1/type.proto\x12\x12sf.arweave.type.v1"\x17\n\x06BigInt\x12\r\n\x05bytes\x18\x01 \x01(\x0c"\xe1\x04\n\x05Block\x12\x0b\n\x03ver\x18\x01 \x01(\r\x12\x12\n\nindep_hash\x18\x02 \x01(\x0c\x12\r\n\x05nonce\x18\x03 \x01(\x0c\x12\x16\n\x0eprevious_block\x18\x04 \x01(\x0c\x12\x11\n\ttimestamp\x18\x05 \x01(\x04\x12\x15\n\rlast_retarget\x18\x06 \x01(\x04\x12(\n\x04diff\x18\x07 \x01(\x0b2\x1a.sf.arweave.type.v1.BigInt\x12\x0e\n\x06height\x18\x08 \x01(\x04\x12\x0c\n\x04hash\x18\t \x01(\x0c\x12\x0f\n\x07tx_root\x18\n \x01(\x0c\x12,\n\x03txs\x18\x0b \x03(\x0b2\x1f.sf.arweave.type.v1.Transaction\x12\x13\n\x0bwallet_list\x18\x0c \x01(\x0c\x12\x13\n\x0breward_addr\x18\r \x01(\x0c\x12%\n\x04tags\x18\x0e \x03(\x0b2\x17.sf.arweave.type.v1.Tag\x12/\n\x0breward_pool\x18\x0f \x01(\x0b2\x1a.sf.arweave.type.v1.BigInt\x12.\n\nweave_size\x18\x10 \x01(\x0b2\x1a.sf.arweave.type.v1.BigInt\x12.\n\nblock_size\x18\x11 \x01(\x0b2\x1a.sf.arweave.type.v1.BigInt\x123\n\x0fcumulative_diff\x18\x12 \x01(\x0b2\x1a.sf.arweave.type.v1.BigInt\x12\x18\n\x10hash_list_merkle\x18\x14 \x01(\x0c\x12.\n\x03poa\x18\x15 \x01(\x0b2!.sf.arweave.type.v1.ProofOfAccess"R\n\rProofOfAccess\x12\x0e\n\x06option\x18\x01 \x01(\t\x12\x0f\n\x07tx_path\x18\x02 \x01(\x0c\x12\x11\n\tdata_path\x18\x03 \x01(\x0c\x12\r\n\x05chunk\x18\x04 \x01(\x0c"\xbd\x02\n\x0bTransaction\x12\x0e\n\x06format\x18\x01 \x01(\r\x12\n\n\x02id\x18\x02 \x01(\x0c\x12\x0f\n\x07last_tx\x18\x03 \x01(\x0c\x12\r\n\x05owner\x18\x04 \x01(\x0c\x12%\n\x04tags\x18\x05 \x03(\x0b2\x17.sf.arweave.type.v1.Tag\x12\x0e\n\x06target\x18\x06 \x01(\x0c\x12,\n\x08quantity\x18\x07 \x01(\x0b2\x1a.sf.arweave.type.v1.BigInt\x12\x0c\n\x04data\x18\x08 \x01(\x0c\x12-\n\tdata_size\x18\t \x01(\x0b2\x1a.sf.arweave.type.v1.BigInt\x12\x11\n\tdata_root\x18\n \x01(\x0c\x12\x11\n\tsignature\x18\x0b \x01(\x0c\x12*\n\x06reward\x18\x0c \x01(\x0b2\x1a.sf.arweave.type.v1.BigInt""\n\x03Tag\x12\x0c\n\x04name\x18\x01 \x01(\x0c\x12\r\n\x05value\x18\x02 \x01(\x0cBQZOgithub.com/streamingfast/firehose-arweave/types/pb/sf/arweave/type/v1;pbarweaveb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sf.arweave.type.v1.type_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZOgithub.com/streamingfast/firehose-arweave/types/pb/sf/arweave/type/v1;pbarweave'
    _BIGINT._serialized_start = 53
    _BIGINT._serialized_end = 76
    _BLOCK._serialized_start = 79
    _BLOCK._serialized_end = 688
    _PROOFOFACCESS._serialized_start = 690
    _PROOFOFACCESS._serialized_end = 772
    _TRANSACTION._serialized_start = 775
    _TRANSACTION._serialized_end = 1092
    _TAG._serialized_start = 1094
    _TAG._serialized_end = 1128