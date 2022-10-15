import asyncio
import grpc
import json
import logging
import multiprocessing
import os
import pandas as pd
import requests

from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from proto import bstream_pb2, bstream_pb2_grpc, codec_pb2
from requests_cache import CachedSession
from typing import List, Dict

load_dotenv(find_dotenv())

# Old laptop speed, home internet, 20 workers: ~ 200 blocks/s
async def run(accounts: List[str], period_start: int, period_end: int):
	async def stream_blocks(accounts: List[str], period_start: int, period_end: int) -> List[Dict]:
		transactions = []
		filter_exp = ' '.join(["receiver == '" + account + ("' ||" if accounts.index(account) + 1 - len(accounts) else "'") for account in accounts]) # Example: receiver == "a" || receiver == "b"
		
		logging.debug(f'[{asyncio.current_task().get_name()}] Starting streaming blocks from {period_start} to {period_end}...')
		async for response in stub.Blocks(bstream_pb2.BlocksRequestV2(
			start_block_num=period_start,
			stop_block_num=period_end,
			fork_steps=["STEP_IRREVERSIBLE"],
			include_filter_expr=f"({filter_exp}) && action == 'transfer'", # TODO: Figure out if filter is really working
			exclude_filter_expr="action == '*'"
		)):
			b = codec_pb2.Block()
			response.block.Unpack(b)
			logging.info(f'[{asyncio.current_task().get_name()}] Parsing block number #{b.number} ({period_end - b.number} blocks remaining)...')
			for transaction_trace in b.filtered_transaction_traces:
				for action_trace in transaction_trace.action_traces:
					logging.debug(f'[{asyncio.current_task().get_name()}] action_trace={action_trace}')
					
					action = action_trace.action
					try:
						json_data = json.loads(action.json_data)
					except Exception as e:
						logging.warning(f'Could not parse action (trxid={action_trace.transaction_id}): {e}\n')
						continue
					
					if action.name != 'transfer': # Skip non-transfer actions
						continue

					if action_trace.receiver not in accounts: # Filter only transfers involving target accounts
						continue

					data = {}
					data['account'] = action_trace.receiver
					data['date'] = action_trace.block_time.seconds # TODO: Convert UNIX to Date
					data['amount'], data['token'] = json_data['quantity'].split(' ')
					data['amountCAD'] = 0
					data['token/CAD'] = 0
					data['from'] = json_data['from']
					data['to'] = json_data['to']
					data['blockNum'] = transaction_trace.block_num
					data['trxID'] = action_trace.transaction_id
					data['memo'] = json_data['memo']
					data['contract'] = action.account
					data['action'] = action.name

					transactions.append(data)
		logging.info(f'[{asyncio.current_task().get_name()}] Done !\n')
		return transactions

	creds = grpc.composite_channel_credentials(grpc.ssl_channel_credentials(), grpc.access_token_call_credentials(jwt))
	block_diff = period_end - period_start
	max_tasks = block_diff if block_diff < 20 else 20 # Max 20 workers
	split = block_diff//max_tasks
	
	logging.info(f'Starting streaming {block_diff} blocks for transfer informations related to {accounts} (running {max_tasks} workers)')
	console_handler.terminator = '\r'

	async with grpc.aio.secure_channel('eos.firehose.eosnation.io:9000', creds) as secure_channel:
		stub = bstream_pb2_grpc.BlockStreamV2Stub(secure_channel)
		tasks = []

		for i in range(max_tasks):
			tasks.append(asyncio.create_task(stream_blocks(accounts, period_start + i*split, period_start + (i+1)*split)))

		data = []
		for t in tasks:
			data += await t
		
	filename = f'jsonl\\{"_".join(accounts)}_{period_start}_to_{period_end}.jsonl'
	with open(filename, 'w') as f:
		for entry in data:
			json.dump(entry, f)
			f.write('\n')
	
	console_handler.terminator = '\n'
	logging.info(f'Finished streaming, wrote {len(data)} rows of data to {filename} [SUCCESS]')

if __name__ == "__main__":
	# file_handler = logging.FileHandler("logs\\" + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + ".log", mode='w') # Unique log files
	file_handler = logging.FileHandler("logs\\" + datetime.today().strftime('%Y-%m-%d') + ".log", mode='w') # Daily log files

	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.INFO)

	logging.basicConfig(
		handlers=[file_handler, console_handler],
		level=logging.DEBUG,
		format='T+%(relativeCreated)d\t%(levelname)s %(message)s',
		force=True
	)

	logging.addLevelName(logging.DEBUG, '[DEBUG]')
	logging.addLevelName(logging.INFO, '[*]')
	logging.addLevelName(logging.WARNING, '[!]')
	logging.addLevelName(logging.ERROR, '[ERROR]')
	logging.addLevelName(logging.CRITICAL, '[CRITICAL]')

	session = CachedSession(
		'jwt_token',
		expire_after=timedelta(days=1),
		allowable_methods=['GET', 'POST'],
	)

	headers = {'Content-Type': 'application/json',}
	data = f'{{"api_key":"{os.environ.get("DFUSE_TOKEN")}"}}'

	logging.info('Getting JWT token...')
	# Cache JWT response (for up to 24 hours)
	response = session.post('https://auth.eosnation.io/v1/auth/issue', headers=headers, data=data)
	if (response.status_code == 200):
		logging.debug(response.json())
		jwt = response.json()['token']
	else:
		logging.error(f'Could not load JWT token: {response.text}')
		exit(-1)
	logging.info(f'Got JWT token ({"cached" if response.from_cache else "new"}) [SUCCESS]')

	accounts = ['eosio.vpay', 'eosio.bpay']
	# period_start = 272541202 # 2022-10-11T00:00:00Z
	# period_end = 272713628 # 2022-10-11T23:59:59Z
	period_start = 272368521
	period_end = 272540290

	asyncio.run(run(accounts, period_start, period_end))

	"""
		Pandas dataframe
		================

		Account | Date | Amount | Token | AmountCAD | Token/CAD | From | To | BlockNum | TrxID | Memo | Contract | Action | Data 
		-------------------------------------------------------------------------------------------------------------------------
	"""

	# results = response.json()['data']['searchTransactionsBackward']['results']
	# rows = []
	# for r in results:
	# 	row = {}
	# 	for t in r['trace']['matchingActions']:
	# 		row['Account'] = account_name
	# 		row['Date'] = r['trace']['block']['timestamp'] # TODO: Format date
	# 		row['Amount'], row['Token'] = t['json']['quantity'].split(' ')
	# 		row['AmountCAD'] = 0 # TODO: Calculate price from pair quote
	# 		row['Token/CAD'] = 0 # TODO: Fetch historical price from API
	# 		row['From'] = t['json']['from']
	# 		row['To'] = t['json']['to']
	# 		row['BlockNum'] = r['trace']['block']['num']
	# 		row['TrxID'] = r['trace']['id']
	# 		row['Memo'] = t['json']['memo']
	# 		row['Contract'] = t['account']
	# 		row['Action'] = t['name']
	# 		row['Data'] = '' # TODO: Use ?
	# 		rows.append(row)

	# df = pd.DataFrame(rows)
	# print(df)
	# df.to_csv(f'csv\\{account_name}_{period_start.split("T")[0]}_to_{period_end.split("T")[0]}.csv', index=False)