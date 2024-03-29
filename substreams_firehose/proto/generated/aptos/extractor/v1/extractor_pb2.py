"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....aptos.util.timestamp import timestamp_pb2 as aptos_dot_util_dot_timestamp_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"aptos/extractor/v1/extractor.proto\x12\x12aptos.extractor.v1\x1a$aptos/util/timestamp/timestamp.proto"\x94\x01\n\x05Block\x122\n\ttimestamp\x18\x01 \x01(\x0b2\x1f.aptos.util.timestamp.Timestamp\x12\x0e\n\x06height\x18\x02 \x01(\x04\x125\n\x0ctransactions\x18\x03 \x03(\x0b2\x1f.aptos.extractor.v1.Transaction\x12\x10\n\x08chain_id\x18\x04 \x01(\r"\xcd\x04\n\x0bTransaction\x122\n\ttimestamp\x18\x01 \x01(\x0b2\x1f.aptos.util.timestamp.Timestamp\x12\x0f\n\x07version\x18\x02 \x01(\x04\x121\n\x04info\x18\x03 \x01(\x0b2#.aptos.extractor.v1.TransactionInfo\x12\r\n\x05epoch\x18\x04 \x01(\x04\x12\x14\n\x0cblock_height\x18\x05 \x01(\x04\x12=\n\x04type\x18\x06 \x01(\x0e2/.aptos.extractor.v1.Transaction.TransactionType\x12F\n\x0eblock_metadata\x18\x07 \x01(\x0b2,.aptos.extractor.v1.BlockMetadataTransactionH\x00\x129\n\x07genesis\x18\x08 \x01(\x0b2&.aptos.extractor.v1.GenesisTransactionH\x00\x12J\n\x10state_checkpoint\x18\t \x01(\x0b2..aptos.extractor.v1.StateCheckpointTransactionH\x00\x123\n\x04user\x18\n \x01(\x0b2#.aptos.extractor.v1.UserTransactionH\x00"R\n\x0fTransactionType\x12\x0b\n\x07GENESIS\x10\x00\x12\x12\n\x0eBLOCK_METADATA\x10\x01\x12\x14\n\x10STATE_CHECKPOINT\x10\x02\x12\x08\n\x04USER\x10\x03B\n\n\x08txn_data"Y\n\x12TransactionTrimmed\x122\n\ttimestamp\x18\x01 \x01(\x0b2\x1f.aptos.util.timestamp.Timestamp\x12\x0f\n\x07version\x18\x02 \x01(\x04"\xb8\x01\n\x18BlockMetadataTransaction\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05round\x18\x02 \x01(\x04\x12)\n\x06events\x18\x03 \x03(\x0b2\x19.aptos.extractor.v1.Event\x12#\n\x1bprevious_block_votes_bitvec\x18\x04 \x01(\x0c\x12\x10\n\x08proposer\x18\x05 \x01(\t\x12\x1f\n\x17failed_proposer_indices\x18\x06 \x03(\r"n\n\x12GenesisTransaction\x12-\n\x07payload\x18\x01 \x01(\x0b2\x1c.aptos.extractor.v1.WriteSet\x12)\n\x06events\x18\x02 \x03(\x0b2\x19.aptos.extractor.v1.Event"\x1c\n\x1aStateCheckpointTransaction"y\n\x0fUserTransaction\x12;\n\x07request\x18\x01 \x01(\x0b2*.aptos.extractor.v1.UserTransactionRequest\x12)\n\x06events\x18\x02 \x03(\x0b2\x19.aptos.extractor.v1.Event"\x97\x01\n\x05Event\x12)\n\x03key\x18\x01 \x01(\x0b2\x1c.aptos.extractor.v1.EventKey\x12\x17\n\x0fsequence_number\x18\x02 \x01(\x04\x12*\n\x04type\x18\x03 \x01(\x0b2\x1c.aptos.extractor.v1.MoveType\x12\x10\n\x08type_str\x18\x05 \x01(\t\x12\x0c\n\x04data\x18\x04 \x01(\t"\x9b\x02\n\x0fTransactionInfo\x12\x0c\n\x04hash\x18\x01 \x01(\x0c\x12\x19\n\x11state_change_hash\x18\x02 \x01(\x0c\x12\x17\n\x0fevent_root_hash\x18\x03 \x01(\x0c\x12"\n\x15state_checkpoint_hash\x18\x04 \x01(\x0cH\x00\x88\x01\x01\x12\x10\n\x08gas_used\x18\x05 \x01(\x04\x12\x0f\n\x07success\x18\x06 \x01(\x08\x12\x11\n\tvm_status\x18\x07 \x01(\t\x12\x1d\n\x15accumulator_root_hash\x18\x08 \x01(\x0c\x123\n\x07changes\x18\t \x03(\x0b2".aptos.extractor.v1.WriteSetChangeB\x18\n\x16_state_checkpoint_hash"<\n\x08EventKey\x12\x17\n\x0fcreation_number\x18\x01 \x01(\x04\x12\x17\n\x0faccount_address\x18\x02 \x01(\t"\xa0\x02\n\x16UserTransactionRequest\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x17\n\x0fsequence_number\x18\x02 \x01(\x04\x12\x16\n\x0emax_gas_amount\x18\x03 \x01(\x04\x12\x16\n\x0egas_unit_price\x18\x04 \x01(\x04\x12B\n\x19expiration_timestamp_secs\x18\x05 \x01(\x0b2\x1f.aptos.util.timestamp.Timestamp\x127\n\x07payload\x18\x06 \x01(\x0b2&.aptos.extractor.v1.TransactionPayload\x120\n\tsignature\x18\x07 \x01(\x0b2\x1d.aptos.extractor.v1.Signature"\x96\x02\n\x08WriteSet\x12A\n\x0ewrite_set_type\x18\x01 \x01(\x0e2).aptos.extractor.v1.WriteSet.WriteSetType\x12>\n\x10script_write_set\x18\x02 \x01(\x0b2".aptos.extractor.v1.ScriptWriteSetH\x00\x12>\n\x10direct_write_set\x18\x03 \x01(\x0b2".aptos.extractor.v1.DirectWriteSetH\x00":\n\x0cWriteSetType\x12\x14\n\x10SCRIPT_WRITE_SET\x10\x00\x12\x14\n\x10DIRECT_WRITE_SET\x10\x01B\x0b\n\twrite_set"W\n\x0eScriptWriteSet\x12\x12\n\nexecute_as\x18\x01 \x01(\t\x121\n\x06script\x18\x02 \x01(\x0b2!.aptos.extractor.v1.ScriptPayload"y\n\x0eDirectWriteSet\x12<\n\x10write_set_change\x18\x01 \x03(\x0b2".aptos.extractor.v1.WriteSetChange\x12)\n\x06events\x18\x02 \x03(\x0b2\x19.aptos.extractor.v1.Event"\xc7\x04\n\x0eWriteSetChange\x125\n\x04type\x18\x01 \x01(\x0e2\'.aptos.extractor.v1.WriteSetChange.Type\x129\n\rdelete_module\x18\x02 \x01(\x0b2 .aptos.extractor.v1.DeleteModuleH\x00\x12=\n\x0fdelete_resource\x18\x03 \x01(\x0b2".aptos.extractor.v1.DeleteResourceH\x00\x12@\n\x11delete_table_item\x18\x04 \x01(\x0b2#.aptos.extractor.v1.DeleteTableItemH\x00\x127\n\x0cwrite_module\x18\x05 \x01(\x0b2\x1f.aptos.extractor.v1.WriteModuleH\x00\x12;\n\x0ewrite_resource\x18\x06 \x01(\x0b2!.aptos.extractor.v1.WriteResourceH\x00\x12>\n\x10write_table_item\x18\x07 \x01(\x0b2".aptos.extractor.v1.WriteTableItemH\x00"\x81\x01\n\x04Type\x12\x11\n\rDELETE_MODULE\x10\x00\x12\x13\n\x0fDELETE_RESOURCE\x10\x01\x12\x15\n\x11DELETE_TABLE_ITEM\x10\x02\x12\x10\n\x0cWRITE_MODULE\x10\x03\x12\x12\n\x0eWRITE_RESOURCE\x10\x04\x12\x14\n\x10WRITE_TABLE_ITEM\x10\x05B\x08\n\x06change"i\n\x0cDeleteModule\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\x16\n\x0estate_key_hash\x18\x02 \x01(\x0c\x120\n\x06module\x18\x03 \x01(\x0b2 .aptos.extractor.v1.MoveModuleId"|\n\x0eDeleteResource\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\x16\n\x0estate_key_hash\x18\x02 \x01(\x0c\x12/\n\x04type\x18\x03 \x01(\x0b2!.aptos.extractor.v1.MoveStructTag\x12\x10\n\x08type_str\x18\x04 \x01(\t"y\n\x0fDeleteTableItem\x12\x16\n\x0estate_key_hash\x18\x01 \x01(\x0c\x12\x0e\n\x06handle\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\x121\n\x04data\x18\x04 \x01(\x0b2#.aptos.extractor.v1.DeleteTableData"0\n\x0fDeleteTableData\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x10\n\x08key_type\x18\x02 \x01(\t"l\n\x0bWriteModule\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\x16\n\x0estate_key_hash\x18\x02 \x01(\x0c\x124\n\x04data\x18\x03 \x01(\x0b2&.aptos.extractor.v1.MoveModuleBytecode"\x89\x01\n\rWriteResource\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\x16\n\x0estate_key_hash\x18\x02 \x01(\x0c\x12/\n\x04type\x18\x03 \x01(\x0b2!.aptos.extractor.v1.MoveStructTag\x12\x10\n\x08type_str\x18\x04 \x01(\t\x12\x0c\n\x04data\x18\x05 \x01(\t"R\n\x0eWriteTableData\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x10\n\x08key_type\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\x12\x12\n\nvalue_type\x18\x04 \x01(\t"w\n\x0eWriteTableItem\x12\x16\n\x0estate_key_hash\x18\x01 \x01(\x0c\x12\x0e\n\x06handle\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\x120\n\x04data\x18\x04 \x01(\x0b2".aptos.extractor.v1.WriteTableData"\xc2\x03\n\x12TransactionPayload\x129\n\x04type\x18\x01 \x01(\x0e2+.aptos.extractor.v1.TransactionPayload.Type\x12J\n\x16entry_function_payload\x18\x02 \x01(\x0b2(.aptos.extractor.v1.EntryFunctionPayloadH\x00\x12;\n\x0escript_payload\x18\x03 \x01(\x0b2!.aptos.extractor.v1.ScriptPayloadH\x00\x12H\n\x15module_bundle_payload\x18\x04 \x01(\x0b2\'.aptos.extractor.v1.ModuleBundlePayloadH\x00\x12@\n\x11write_set_payload\x18\x05 \x01(\x0b2#.aptos.extractor.v1.WriteSetPayloadH\x00"Q\n\x04Type\x12\x1a\n\x16ENTRY_FUNCTION_PAYLOAD\x10\x00\x12\x12\n\x0eSCRIPT_PAYLOAD\x10\x01\x12\x19\n\x15MODULE_BUNDLE_PAYLOAD\x10\x02B\t\n\x07payload"\x96\x01\n\x14EntryFunctionPayload\x125\n\x08function\x18\x01 \x01(\x0b2#.aptos.extractor.v1.EntryFunctionId\x124\n\x0etype_arguments\x18\x02 \x03(\x0b2\x1c.aptos.extractor.v1.MoveType\x12\x11\n\targuments\x18\x03 \x03(\t"U\n\x12MoveScriptBytecode\x12\x10\n\x08bytecode\x18\x01 \x01(\x0c\x12-\n\x03abi\x18\x02 \x01(\x0b2 .aptos.extractor.v1.MoveFunction"\x8e\x01\n\rScriptPayload\x124\n\x04code\x18\x01 \x01(\x0b2&.aptos.extractor.v1.MoveScriptBytecode\x124\n\x0etype_arguments\x18\x02 \x03(\x0b2\x1c.aptos.extractor.v1.MoveType\x12\x11\n\targuments\x18\x03 \x03(\t"N\n\x13ModuleBundlePayload\x127\n\x07modules\x18\x01 \x03(\x0b2&.aptos.extractor.v1.MoveModuleBytecode"S\n\x12MoveModuleBytecode\x12\x10\n\x08bytecode\x18\x01 \x01(\x0c\x12+\n\x03abi\x18\x02 \x01(\x0b2\x1e.aptos.extractor.v1.MoveModule"\xcc\x01\n\nMoveModule\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x121\n\x07friends\x18\x03 \x03(\x0b2 .aptos.extractor.v1.MoveModuleId\x12;\n\x11exposed_functions\x18\x04 \x03(\x0b2 .aptos.extractor.v1.MoveFunction\x12/\n\x07structs\x18\x05 \x03(\x0b2\x1e.aptos.extractor.v1.MoveStruct"\xcd\x02\n\x0cMoveFunction\x12\x0c\n\x04name\x18\x01 \x01(\t\x12?\n\nvisibility\x18\x02 \x01(\x0e2+.aptos.extractor.v1.MoveFunction.Visibility\x12\x10\n\x08is_entry\x18\x03 \x01(\x08\x12M\n\x13generic_type_params\x18\x04 \x03(\x0b20.aptos.extractor.v1.MoveFunctionGenericTypeParam\x12,\n\x06params\x18\x05 \x03(\x0b2\x1c.aptos.extractor.v1.MoveType\x12,\n\x06return\x18\x06 \x03(\x0b2\x1c.aptos.extractor.v1.MoveType"1\n\nVisibility\x12\x0b\n\x07PRIVATE\x10\x00\x12\n\n\x06PUBLIC\x10\x01\x12\n\n\x06FRIEND\x10\x02"\xe3\x01\n\nMoveStruct\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tis_native\x18\x02 \x01(\x08\x122\n\tabilities\x18\x03 \x03(\x0e2\x1f.aptos.extractor.v1.MoveAbility\x12K\n\x13generic_type_params\x18\x04 \x03(\x0b2..aptos.extractor.v1.MoveStructGenericTypeParam\x123\n\x06fields\x18\x05 \x03(\x0b2#.aptos.extractor.v1.MoveStructField"f\n\x1aMoveStructGenericTypeParam\x124\n\x0bconstraints\x18\x01 \x03(\x0e2\x1f.aptos.extractor.v1.MoveAbility\x12\x12\n\nis_phantom\x18\x02 \x01(\x08"K\n\x0fMoveStructField\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x04type\x18\x02 \x01(\x0b2\x1c.aptos.extractor.v1.MoveType"T\n\x1cMoveFunctionGenericTypeParam\x124\n\x0bconstraints\x18\x01 \x03(\x0e2\x1f.aptos.extractor.v1.MoveAbility"\xee\x02\n\x08MoveType\x12+\n\x04type\x18\x01 \x01(\x0e2\x1d.aptos.extractor.v1.MoveTypes\x12.\n\x06vector\x18\x03 \x01(\x0b2\x1c.aptos.extractor.v1.MoveTypeH\x00\x123\n\x06struct\x18\x04 \x01(\x0b2!.aptos.extractor.v1.MoveStructTagH\x00\x12"\n\x18generic_type_param_index\x18\x05 \x01(\rH\x00\x12?\n\treference\x18\x06 \x01(\x0b2*.aptos.extractor.v1.MoveType.ReferenceTypeH\x00\x12\x14\n\nunparsable\x18\x07 \x01(\tH\x00\x1aJ\n\rReferenceType\x12\x0f\n\x07mutable\x18\x01 \x01(\x08\x12(\n\x02to\x18\x02 \x01(\x0b2\x1c.aptos.extractor.v1.MoveTypeB\t\n\x07content"B\n\x0fWriteSetPayload\x12/\n\twrite_set\x18\x01 \x01(\x0b2\x1c.aptos.extractor.v1.WriteSet"Q\n\x0fEntryFunctionId\x120\n\x06module\x18\x01 \x01(\x0b2 .aptos.extractor.v1.MoveModuleId\x12\x0c\n\x04name\x18\x02 \x01(\t"-\n\x0cMoveModuleId\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t"y\n\rMoveStructTag\x12\x0f\n\x07address\x18\x01 \x01(\t\x12\x0e\n\x06module\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x129\n\x13generic_type_params\x18\x04 \x03(\x0b2\x1c.aptos.extractor.v1.MoveType"\xc0\x02\n\tSignature\x120\n\x04type\x18\x01 \x01(\x0e2".aptos.extractor.v1.Signature.Type\x127\n\x07ed25519\x18\x02 \x01(\x0b2$.aptos.extractor.v1.Ed25519SignatureH\x00\x12B\n\rmulti_ed25519\x18\x03 \x01(\x0b2).aptos.extractor.v1.MultiEd25519SignatureH\x00\x12>\n\x0bmulti_agent\x18\x04 \x01(\x0b2\'.aptos.extractor.v1.MultiAgentSignatureH\x00"7\n\x04Type\x12\x0b\n\x07ED25519\x10\x00\x12\x11\n\rMULTI_ED25519\x10\x01\x12\x0f\n\x0bMULTI_AGENT\x10\x02B\x0b\n\tsignature"9\n\x10Ed25519Signature\x12\x12\n\npublic_key\x18\x01 \x01(\x0c\x12\x11\n\tsignature\x18\x02 \x01(\x0c"o\n\x15MultiEd25519Signature\x12\x13\n\x0bpublic_keys\x18\x01 \x03(\x0c\x12\x12\n\nsignatures\x18\x02 \x03(\x0c\x12\x11\n\tthreshold\x18\x03 \x01(\r\x12\x1a\n\x12public_key_indices\x18\x04 \x03(\r"\xb0\x01\n\x13MultiAgentSignature\x124\n\x06sender\x18\x01 \x01(\x0b2$.aptos.extractor.v1.AccountSignature\x12"\n\x1asecondary_signer_addresses\x18\x02 \x03(\t\x12?\n\x11secondary_signers\x18\x03 \x03(\x0b2$.aptos.extractor.v1.AccountSignature"\xfd\x01\n\x10AccountSignature\x127\n\x04type\x18\x01 \x01(\x0e2).aptos.extractor.v1.AccountSignature.Type\x127\n\x07ed25519\x18\x02 \x01(\x0b2$.aptos.extractor.v1.Ed25519SignatureH\x00\x12B\n\rmulti_ed25519\x18\x03 \x01(\x0b2).aptos.extractor.v1.MultiEd25519SignatureH\x00"&\n\x04Type\x12\x0b\n\x07ED25519\x10\x00\x12\x11\n\rMULTI_ED25519\x10\x01B\x0b\n\tsignature*\x96\x01\n\tMoveTypes\x12\x08\n\x04Bool\x10\x00\x12\x06\n\x02U8\x10\x01\x12\x07\n\x03U64\x10\x02\x12\x08\n\x04U128\x10\x03\x12\x0b\n\x07Address\x10\x04\x12\n\n\x06Signer\x10\x05\x12\n\n\x06Vector\x10\x06\x12\n\n\x06Struct\x10\x07\x12\x14\n\x10GenericTypeParam\x10\x08\x12\r\n\tReference\x10\t\x12\x0e\n\nUnparsable\x10\n*5\n\x0bMoveAbility\x12\x08\n\x04COPY\x10\x00\x12\x08\n\x04DROP\x10\x01\x12\t\n\x05STORE\x10\x02\x12\x07\n\x03KEY\x10\x03BMZKgithub.com/streamingfast/firehose-aptos/types/pb/aptos/extractor/v1;pbaptosb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aptos.extractor.v1.extractor_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZKgithub.com/streamingfast/firehose-aptos/types/pb/aptos/extractor/v1;pbaptos'
    _MOVETYPES._serialized_start = 7779
    _MOVETYPES._serialized_end = 7929
    _MOVEABILITY._serialized_start = 7931
    _MOVEABILITY._serialized_end = 7984
    _BLOCK._serialized_start = 97
    _BLOCK._serialized_end = 245
    _TRANSACTION._serialized_start = 248
    _TRANSACTION._serialized_end = 837
    _TRANSACTION_TRANSACTIONTYPE._serialized_start = 743
    _TRANSACTION_TRANSACTIONTYPE._serialized_end = 825
    _TRANSACTIONTRIMMED._serialized_start = 839
    _TRANSACTIONTRIMMED._serialized_end = 928
    _BLOCKMETADATATRANSACTION._serialized_start = 931
    _BLOCKMETADATATRANSACTION._serialized_end = 1115
    _GENESISTRANSACTION._serialized_start = 1117
    _GENESISTRANSACTION._serialized_end = 1227
    _STATECHECKPOINTTRANSACTION._serialized_start = 1229
    _STATECHECKPOINTTRANSACTION._serialized_end = 1257
    _USERTRANSACTION._serialized_start = 1259
    _USERTRANSACTION._serialized_end = 1380
    _EVENT._serialized_start = 1383
    _EVENT._serialized_end = 1534
    _TRANSACTIONINFO._serialized_start = 1537
    _TRANSACTIONINFO._serialized_end = 1820
    _EVENTKEY._serialized_start = 1822
    _EVENTKEY._serialized_end = 1882
    _USERTRANSACTIONREQUEST._serialized_start = 1885
    _USERTRANSACTIONREQUEST._serialized_end = 2173
    _WRITESET._serialized_start = 2176
    _WRITESET._serialized_end = 2454
    _WRITESET_WRITESETTYPE._serialized_start = 2383
    _WRITESET_WRITESETTYPE._serialized_end = 2441
    _SCRIPTWRITESET._serialized_start = 2456
    _SCRIPTWRITESET._serialized_end = 2543
    _DIRECTWRITESET._serialized_start = 2545
    _DIRECTWRITESET._serialized_end = 2666
    _WRITESETCHANGE._serialized_start = 2669
    _WRITESETCHANGE._serialized_end = 3252
    _WRITESETCHANGE_TYPE._serialized_start = 3113
    _WRITESETCHANGE_TYPE._serialized_end = 3242
    _DELETEMODULE._serialized_start = 3254
    _DELETEMODULE._serialized_end = 3359
    _DELETERESOURCE._serialized_start = 3361
    _DELETERESOURCE._serialized_end = 3485
    _DELETETABLEITEM._serialized_start = 3487
    _DELETETABLEITEM._serialized_end = 3608
    _DELETETABLEDATA._serialized_start = 3610
    _DELETETABLEDATA._serialized_end = 3658
    _WRITEMODULE._serialized_start = 3660
    _WRITEMODULE._serialized_end = 3768
    _WRITERESOURCE._serialized_start = 3771
    _WRITERESOURCE._serialized_end = 3908
    _WRITETABLEDATA._serialized_start = 3910
    _WRITETABLEDATA._serialized_end = 3992
    _WRITETABLEITEM._serialized_start = 3994
    _WRITETABLEITEM._serialized_end = 4113
    _TRANSACTIONPAYLOAD._serialized_start = 4116
    _TRANSACTIONPAYLOAD._serialized_end = 4566
    _TRANSACTIONPAYLOAD_TYPE._serialized_start = 4474
    _TRANSACTIONPAYLOAD_TYPE._serialized_end = 4555
    _ENTRYFUNCTIONPAYLOAD._serialized_start = 4569
    _ENTRYFUNCTIONPAYLOAD._serialized_end = 4719
    _MOVESCRIPTBYTECODE._serialized_start = 4721
    _MOVESCRIPTBYTECODE._serialized_end = 4806
    _SCRIPTPAYLOAD._serialized_start = 4809
    _SCRIPTPAYLOAD._serialized_end = 4951
    _MODULEBUNDLEPAYLOAD._serialized_start = 4953
    _MODULEBUNDLEPAYLOAD._serialized_end = 5031
    _MOVEMODULEBYTECODE._serialized_start = 5033
    _MOVEMODULEBYTECODE._serialized_end = 5116
    _MOVEMODULE._serialized_start = 5119
    _MOVEMODULE._serialized_end = 5323
    _MOVEFUNCTION._serialized_start = 5326
    _MOVEFUNCTION._serialized_end = 5659
    _MOVEFUNCTION_VISIBILITY._serialized_start = 5610
    _MOVEFUNCTION_VISIBILITY._serialized_end = 5659
    _MOVESTRUCT._serialized_start = 5662
    _MOVESTRUCT._serialized_end = 5889
    _MOVESTRUCTGENERICTYPEPARAM._serialized_start = 5891
    _MOVESTRUCTGENERICTYPEPARAM._serialized_end = 5993
    _MOVESTRUCTFIELD._serialized_start = 5995
    _MOVESTRUCTFIELD._serialized_end = 6070
    _MOVEFUNCTIONGENERICTYPEPARAM._serialized_start = 6072
    _MOVEFUNCTIONGENERICTYPEPARAM._serialized_end = 6156
    _MOVETYPE._serialized_start = 6159
    _MOVETYPE._serialized_end = 6525
    _MOVETYPE_REFERENCETYPE._serialized_start = 6440
    _MOVETYPE_REFERENCETYPE._serialized_end = 6514
    _WRITESETPAYLOAD._serialized_start = 6527
    _WRITESETPAYLOAD._serialized_end = 6593
    _ENTRYFUNCTIONID._serialized_start = 6595
    _ENTRYFUNCTIONID._serialized_end = 6676
    _MOVEMODULEID._serialized_start = 6678
    _MOVEMODULEID._serialized_end = 6723
    _MOVESTRUCTTAG._serialized_start = 6725
    _MOVESTRUCTTAG._serialized_end = 6846
    _SIGNATURE._serialized_start = 6849
    _SIGNATURE._serialized_end = 7169
    _SIGNATURE_TYPE._serialized_start = 7101
    _SIGNATURE_TYPE._serialized_end = 7156
    _ED25519SIGNATURE._serialized_start = 7171
    _ED25519SIGNATURE._serialized_end = 7228
    _MULTIED25519SIGNATURE._serialized_start = 7230
    _MULTIED25519SIGNATURE._serialized_end = 7341
    _MULTIAGENTSIGNATURE._serialized_start = 7344
    _MULTIAGENTSIGNATURE._serialized_end = 7520
    _ACCOUNTSIGNATURE._serialized_start = 7523
    _ACCOUNTSIGNATURE._serialized_end = 7776
    _ACCOUNTSIGNATURE_TYPE._serialized_start = 7101
    _ACCOUNTSIGNATURE_TYPE._serialized_end = 7139