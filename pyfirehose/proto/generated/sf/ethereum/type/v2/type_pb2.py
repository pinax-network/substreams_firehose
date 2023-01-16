"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1esf/ethereum/type/v2/type.proto\x12\x13sf.ethereum.type.v2\x1a\x1fgoogle/protobuf/timestamp.proto"\xed\x02\n\x05Block\x12\x0b\n\x03ver\x18\x01 \x01(\x05\x12\x0c\n\x04hash\x18\x02 \x01(\x0c\x12\x0e\n\x06number\x18\x03 \x01(\x04\x12\x0c\n\x04size\x18\x04 \x01(\x04\x120\n\x06header\x18\x05 \x01(\x0b2 .sf.ethereum.type.v2.BlockHeader\x120\n\x06uncles\x18\x06 \x03(\x0b2 .sf.ethereum.type.v2.BlockHeader\x12A\n\x12transaction_traces\x18\n \x03(\x0b2%.sf.ethereum.type.v2.TransactionTrace\x12;\n\x0fbalance_changes\x18\x0b \x03(\x0b2".sf.ethereum.type.v2.BalanceChange\x125\n\x0ccode_changes\x18\x14 \x03(\x0b2\x1f.sf.ethereum.type.v2.CodeChangeJ\x04\x08(\x10)J\x04\x08)\x10*J\x04\x08*\x10+"C\n\x0fHeaderOnlyBlock\x120\n\x06header\x18\x05 \x01(\x0b2 .sf.ethereum.type.v2.BlockHeader"\xa2\x01\n\rBlockWithRefs\x12\n\n\x02id\x18\x01 \x01(\t\x12)\n\x05block\x18\x02 \x01(\x0b2\x1a.sf.ethereum.type.v2.Block\x12D\n\x16transaction_trace_refs\x18\x03 \x01(\x0b2$.sf.ethereum.type.v2.TransactionRefs\x12\x14\n\x0cirreversible\x18\x04 \x01(\x08"!\n\x0fTransactionRefs\x12\x0e\n\x06hashes\x18\x01 \x03(\x0c"A\n\rUnclesHeaders\x120\n\x06uncles\x18\x01 \x03(\x0b2 .sf.ethereum.type.v2.BlockHeader"(\n\x08BlockRef\x12\x0c\n\x04hash\x18\x01 \x01(\x0c\x12\x0e\n\x06number\x18\x02 \x01(\x04"\xe7\x03\n\x0bBlockHeader\x12\x13\n\x0bparent_hash\x18\x01 \x01(\x0c\x12\x12\n\nuncle_hash\x18\x02 \x01(\x0c\x12\x10\n\x08coinbase\x18\x03 \x01(\x0c\x12\x12\n\nstate_root\x18\x04 \x01(\x0c\x12\x19\n\x11transactions_root\x18\x05 \x01(\x0c\x12\x14\n\x0creceipt_root\x18\x06 \x01(\x0c\x12\x12\n\nlogs_bloom\x18\x07 \x01(\x0c\x12/\n\ndifficulty\x18\x08 \x01(\x0b2\x1b.sf.ethereum.type.v2.BigInt\x125\n\x10total_difficulty\x18\x11 \x01(\x0b2\x1b.sf.ethereum.type.v2.BigInt\x12\x0e\n\x06number\x18\t \x01(\x04\x12\x11\n\tgas_limit\x18\n \x01(\x04\x12\x10\n\x08gas_used\x18\x0b \x01(\x04\x12-\n\ttimestamp\x18\x0c \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x12\n\nextra_data\x18\r \x01(\x0c\x12\x10\n\x08mix_hash\x18\x0e \x01(\x0c\x12\r\n\x05nonce\x18\x0f \x01(\x04\x12\x0c\n\x04hash\x18\x10 \x01(\x0c\x125\n\x10base_fee_per_gas\x18\x12 \x01(\x0b2\x1b.sf.ethereum.type.v2.BigInt"\x17\n\x06BigInt\x12\r\n\x05bytes\x18\x01 \x01(\x0c"\xb6\x06\n\x10TransactionTrace\x12\n\n\x02to\x18\x01 \x01(\x0c\x12\r\n\x05nonce\x18\x02 \x01(\x04\x12.\n\tgas_price\x18\x03 \x01(\x0b2\x1b.sf.ethereum.type.v2.BigInt\x12\x11\n\tgas_limit\x18\x04 \x01(\x04\x12*\n\x05value\x18\x05 \x01(\x0b2\x1b.sf.ethereum.type.v2.BigInt\x12\r\n\x05input\x18\x06 \x01(\x0c\x12\t\n\x01v\x18\x07 \x01(\x0c\x12\t\n\x01r\x18\x08 \x01(\x0c\x12\t\n\x01s\x18\t \x01(\x0c\x12\x10\n\x08gas_used\x18\n \x01(\x04\x128\n\x04type\x18\x0c \x01(\x0e2*.sf.ethereum.type.v2.TransactionTrace.Type\x125\n\x0baccess_list\x18\x0e \x03(\x0b2 .sf.ethereum.type.v2.AccessTuple\x124\n\x0fmax_fee_per_gas\x18\x0b \x01(\x0b2\x1b.sf.ethereum.type.v2.BigInt\x12=\n\x18max_priority_fee_per_gas\x18\r \x01(\x0b2\x1b.sf.ethereum.type.v2.BigInt\x12\r\n\x05index\x18\x14 \x01(\r\x12\x0c\n\x04hash\x18\x15 \x01(\x0c\x12\x0c\n\x04from\x18\x16 \x01(\x0c\x12\x13\n\x0breturn_data\x18\x17 \x01(\x0c\x12\x12\n\npublic_key\x18\x18 \x01(\x0c\x12\x15\n\rbegin_ordinal\x18\x19 \x01(\x04\x12\x13\n\x0bend_ordinal\x18\x1a \x01(\x04\x12;\n\x06status\x18\x1e \x01(\x0e2+.sf.ethereum.type.v2.TransactionTraceStatus\x128\n\x07receipt\x18\x1f \x01(\x0b2\'.sf.ethereum.type.v2.TransactionReceipt\x12(\n\x05calls\x18  \x03(\x0b2\x19.sf.ethereum.type.v2.Call"O\n\x04Type\x12\x13\n\x0fTRX_TYPE_LEGACY\x10\x00\x12\x18\n\x14TRX_TYPE_ACCESS_LIST\x10\x01\x12\x18\n\x14TRX_TYPE_DYNAMIC_FEE\x10\x02"4\n\x0bAccessTuple\x12\x0f\n\x07address\x18\x01 \x01(\x0c\x12\x14\n\x0cstorage_keys\x18\x02 \x03(\x0c"\x86\x01\n\x1cTransactionTraceWithBlockRef\x124\n\x05trace\x18\x01 \x01(\x0b2%.sf.ethereum.type.v2.TransactionTrace\x120\n\tblock_ref\x18\x02 \x01(\x0b2\x1d.sf.ethereum.type.v2.BlockRef"\x81\x01\n\x12TransactionReceipt\x12\x12\n\nstate_root\x18\x01 \x01(\x0c\x12\x1b\n\x13cumulative_gas_used\x18\x02 \x01(\x04\x12\x12\n\nlogs_bloom\x18\x03 \x01(\x0c\x12&\n\x04logs\x18\x04 \x03(\x0b2\x18.sf.ethereum.type.v2.Log"h\n\x03Log\x12\x0f\n\x07address\x18\x01 \x01(\x0c\x12\x0e\n\x06topics\x18\x02 \x03(\x0c\x12\x0c\n\x04data\x18\x03 \x01(\x0c\x12\r\n\x05index\x18\x04 \x01(\r\x12\x12\n\nblockIndex\x18\x06 \x01(\r\x12\x0f\n\x07ordinal\x18\x07 \x01(\x04"\xe2\x07\n\x04Call\x12\r\n\x05index\x18\x01 \x01(\r\x12\x14\n\x0cparent_index\x18\x02 \x01(\r\x12\r\n\x05depth\x18\x03 \x01(\r\x120\n\tcall_type\x18\x04 \x01(\x0e2\x1d.sf.ethereum.type.v2.CallType\x12\x0e\n\x06caller\x18\x05 \x01(\x0c\x12\x0f\n\x07address\x18\x06 \x01(\x0c\x12*\n\x05value\x18\x07 \x01(\x0b2\x1b.sf.ethereum.type.v2.BigInt\x12\x11\n\tgas_limit\x18\x08 \x01(\x04\x12\x14\n\x0cgas_consumed\x18\t \x01(\x04\x12\x13\n\x0breturn_data\x18\r \x01(\x0c\x12\r\n\x05input\x18\x0e \x01(\x0c\x12\x15\n\rexecuted_code\x18\x0f \x01(\x08\x12\x0f\n\x07suicide\x18\x10 \x01(\x08\x12H\n\x10keccak_preimages\x18\x14 \x03(\x0b2..sf.ethereum.type.v2.Call.KeccakPreimagesEntry\x12;\n\x0fstorage_changes\x18\x15 \x03(\x0b2".sf.ethereum.type.v2.StorageChange\x12;\n\x0fbalance_changes\x18\x16 \x03(\x0b2".sf.ethereum.type.v2.BalanceChange\x127\n\rnonce_changes\x18\x18 \x03(\x0b2 .sf.ethereum.type.v2.NonceChange\x12&\n\x04logs\x18\x19 \x03(\x0b2\x18.sf.ethereum.type.v2.Log\x125\n\x0ccode_changes\x18\x1a \x03(\x0b2\x1f.sf.ethereum.type.v2.CodeChange\x123\n\x0bgas_changes\x18\x1c \x03(\x0b2\x1e.sf.ethereum.type.v2.GasChange\x12\x15\n\rstatus_failed\x18\n \x01(\x08\x12\x17\n\x0fstatus_reverted\x18\x0c \x01(\x08\x12\x16\n\x0efailure_reason\x18\x0b \x01(\t\x12\x16\n\x0estate_reverted\x18\x1e \x01(\x08\x12\x15\n\rbegin_ordinal\x18\x1f \x01(\x04\x12\x13\n\x0bend_ordinal\x18  \x01(\x04\x12?\n\x11account_creations\x18! \x03(\x0b2$.sf.ethereum.type.v2.AccountCreation\x1a6\n\x14KeccakPreimagesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x01J\x04\x08\x1b\x10\x1cJ\x04\x08\x1d\x10\x1eJ\x04\x082\x103J\x04\x083\x104J\x04\x08<\x10="d\n\rStorageChange\x12\x0f\n\x07address\x18\x01 \x01(\x0c\x12\x0b\n\x03key\x18\x02 \x01(\x0c\x12\x11\n\told_value\x18\x03 \x01(\x0c\x12\x11\n\tnew_value\x18\x04 \x01(\x0c\x12\x0f\n\x07ordinal\x18\x05 \x01(\x04"\x87\x05\n\rBalanceChange\x12\x0f\n\x07address\x18\x01 \x01(\x0c\x12.\n\told_value\x18\x02 \x01(\x0b2\x1b.sf.ethereum.type.v2.BigInt\x12.\n\tnew_value\x18\x03 \x01(\x0b2\x1b.sf.ethereum.type.v2.BigInt\x129\n\x06reason\x18\x04 \x01(\x0e2).sf.ethereum.type.v2.BalanceChange.Reason\x12\x0f\n\x07ordinal\x18\x05 \x01(\x04"\xb8\x03\n\x06Reason\x12\x12\n\x0eREASON_UNKNOWN\x10\x00\x12\x1c\n\x18REASON_REWARD_MINE_UNCLE\x10\x01\x12\x1c\n\x18REASON_REWARD_MINE_BLOCK\x10\x02\x12\x1e\n\x1aREASON_DAO_REFUND_CONTRACT\x10\x03\x12\x1d\n\x19REASON_DAO_ADJUST_BALANCE\x10\x04\x12\x13\n\x0fREASON_TRANSFER\x10\x05\x12\x1a\n\x16REASON_GENESIS_BALANCE\x10\x06\x12\x12\n\x0eREASON_GAS_BUY\x10\x07\x12!\n\x1dREASON_REWARD_TRANSACTION_FEE\x10\x08\x12\x1b\n\x17REASON_REWARD_FEE_RESET\x10\x0e\x12\x15\n\x11REASON_GAS_REFUND\x10\t\x12\x18\n\x14REASON_TOUCH_ACCOUNT\x10\n\x12\x19\n\x15REASON_SUICIDE_REFUND\x10\x0b\x12\x1b\n\x17REASON_SUICIDE_WITHDRAW\x10\r\x12 \n\x1cREASON_CALL_BALANCE_OVERRIDE\x10\x0c\x12\x0f\n\x0bREASON_BURN\x10\x0f"U\n\x0bNonceChange\x12\x0f\n\x07address\x18\x01 \x01(\x0c\x12\x11\n\told_value\x18\x02 \x01(\x04\x12\x11\n\tnew_value\x18\x03 \x01(\x04\x12\x0f\n\x07ordinal\x18\x04 \x01(\x04"3\n\x0fAccountCreation\x12\x0f\n\x07account\x18\x01 \x01(\x0c\x12\x0f\n\x07ordinal\x18\x02 \x01(\x04"v\n\nCodeChange\x12\x0f\n\x07address\x18\x01 \x01(\x0c\x12\x10\n\x08old_hash\x18\x02 \x01(\x0c\x12\x10\n\x08old_code\x18\x03 \x01(\x0c\x12\x10\n\x08new_hash\x18\x04 \x01(\x0c\x12\x10\n\x08new_code\x18\x05 \x01(\x0c\x12\x0f\n\x07ordinal\x18\x06 \x01(\x04"\x9e\x05\n\tGasChange\x12\x11\n\told_value\x18\x01 \x01(\x04\x12\x11\n\tnew_value\x18\x02 \x01(\x04\x125\n\x06reason\x18\x03 \x01(\x0e2%.sf.ethereum.type.v2.GasChange.Reason\x12\x0f\n\x07ordinal\x18\x04 \x01(\x04"\xa2\x04\n\x06Reason\x12\x12\n\x0eREASON_UNKNOWN\x10\x00\x12\x0f\n\x0bREASON_CALL\x10\x01\x12\x14\n\x10REASON_CALL_CODE\x10\x02\x12\x19\n\x15REASON_CALL_DATA_COPY\x10\x03\x12\x14\n\x10REASON_CODE_COPY\x10\x04\x12\x17\n\x13REASON_CODE_STORAGE\x10\x05\x12\x1c\n\x18REASON_CONTRACT_CREATION\x10\x06\x12\x1d\n\x19REASON_CONTRACT_CREATION2\x10\x07\x12\x18\n\x14REASON_DELEGATE_CALL\x10\x08\x12\x14\n\x10REASON_EVENT_LOG\x10\t\x12\x18\n\x14REASON_EXT_CODE_COPY\x10\n\x12\x1b\n\x17REASON_FAILED_EXECUTION\x10\x0b\x12\x18\n\x14REASON_INTRINSIC_GAS\x10\x0c\x12\x1f\n\x1bREASON_PRECOMPILED_CONTRACT\x10\r\x12!\n\x1dREASON_REFUND_AFTER_EXECUTION\x10\x0e\x12\x11\n\rREASON_RETURN\x10\x0f\x12\x1b\n\x17REASON_RETURN_DATA_COPY\x10\x10\x12\x11\n\rREASON_REVERT\x10\x11\x12\x18\n\x14REASON_SELF_DESTRUCT\x10\x12\x12\x16\n\x12REASON_STATIC_CALL\x10\x13\x12\x1c\n\x18REASON_STATE_COLD_ACCESS\x10\x14*N\n\x16TransactionTraceStatus\x12\x0b\n\x07UNKNOWN\x10\x00\x12\r\n\tSUCCEEDED\x10\x01\x12\n\n\x06FAILED\x10\x02\x12\x0c\n\x08REVERTED\x10\x03*Y\n\x08CallType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x08\n\x04CALL\x10\x01\x12\x0c\n\x08CALLCODE\x10\x02\x12\x0c\n\x08DELEGATE\x10\x03\x12\n\n\x06STATIC\x10\x04\x12\n\n\x06CREATE\x10\x05BOZMgithub.com/streamingfast/firehose-ethereum/types/pb/sf/ethereum/type/v2;pbethb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sf.ethereum.type.v2.type_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZMgithub.com/streamingfast/firehose-ethereum/types/pb/sf/ethereum/type/v2;pbeth'
    _CALL_KECCAKPREIMAGESENTRY._options = None
    _CALL_KECCAKPREIMAGESENTRY._serialized_options = b'8\x01'
    _TRANSACTIONTRACESTATUS._serialized_start = 5285
    _TRANSACTIONTRACESTATUS._serialized_end = 5363
    _CALLTYPE._serialized_start = 5365
    _CALLTYPE._serialized_end = 5454
    _BLOCK._serialized_start = 89
    _BLOCK._serialized_end = 454
    _HEADERONLYBLOCK._serialized_start = 456
    _HEADERONLYBLOCK._serialized_end = 523
    _BLOCKWITHREFS._serialized_start = 526
    _BLOCKWITHREFS._serialized_end = 688
    _TRANSACTIONREFS._serialized_start = 690
    _TRANSACTIONREFS._serialized_end = 723
    _UNCLESHEADERS._serialized_start = 725
    _UNCLESHEADERS._serialized_end = 790
    _BLOCKREF._serialized_start = 792
    _BLOCKREF._serialized_end = 832
    _BLOCKHEADER._serialized_start = 835
    _BLOCKHEADER._serialized_end = 1322
    _BIGINT._serialized_start = 1324
    _BIGINT._serialized_end = 1347
    _TRANSACTIONTRACE._serialized_start = 1350
    _TRANSACTIONTRACE._serialized_end = 2172
    _TRANSACTIONTRACE_TYPE._serialized_start = 2093
    _TRANSACTIONTRACE_TYPE._serialized_end = 2172
    _ACCESSTUPLE._serialized_start = 2174
    _ACCESSTUPLE._serialized_end = 2226
    _TRANSACTIONTRACEWITHBLOCKREF._serialized_start = 2229
    _TRANSACTIONTRACEWITHBLOCKREF._serialized_end = 2363
    _TRANSACTIONRECEIPT._serialized_start = 2366
    _TRANSACTIONRECEIPT._serialized_end = 2495
    _LOG._serialized_start = 2497
    _LOG._serialized_end = 2601
    _CALL._serialized_start = 2604
    _CALL._serialized_end = 3598
    _CALL_KECCAKPREIMAGESENTRY._serialized_start = 3514
    _CALL_KECCAKPREIMAGESENTRY._serialized_end = 3568
    _STORAGECHANGE._serialized_start = 3600
    _STORAGECHANGE._serialized_end = 3700
    _BALANCECHANGE._serialized_start = 3703
    _BALANCECHANGE._serialized_end = 4350
    _BALANCECHANGE_REASON._serialized_start = 3910
    _BALANCECHANGE_REASON._serialized_end = 4350
    _NONCECHANGE._serialized_start = 4352
    _NONCECHANGE._serialized_end = 4437
    _ACCOUNTCREATION._serialized_start = 4439
    _ACCOUNTCREATION._serialized_end = 4490
    _CODECHANGE._serialized_start = 4492
    _CODECHANGE._serialized_end = 4610
    _GASCHANGE._serialized_start = 4613
    _GASCHANGE._serialized_end = 5283
    _GASCHANGE_REASON._serialized_start = 4737
    _GASCHANGE_REASON._serialized_end = 5283