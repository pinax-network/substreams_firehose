import json
import logging
import os
import pandas as pd
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from requests_cache import CachedSession

load_dotenv(find_dotenv())

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
		expire_after=timedelta(days=0),
		allowable_methods=['GET', 'POST'],
	)

	headers = {'Content-Type': 'application/json',}
	data = f'{{"api_key":"{os.environ.get("DFUSE_TOKEN")}"}}'

	# Cache JWT response (for up to 24 hours)
	response = session.post('https://auth.eosnation.io/v1/auth/issue', headers=headers, data=data)
	if (response.status_code == 200):
		logging.debug(response.json())
		jwt = response.json()['token']
	else:
		logging.error(f'Could not load JWT token: {response.text}')
		exit(-1)

	headers = {'Authorization': f'Bearer {jwt}'}
	session = CachedSession(
		'graphql_rest',
		expire_after=timedelta(minutes=30),
		allowable_methods=['GET', 'POST'],
	)

	account_name = 'eosnationftw'
	period_start = '2021-01-01T00:00:00Z' # TODO: Format to datetime
	period_end = '2021-01-02T00:00:00Z' # TODO: Format to datetime
	logging.info(f'Searching for transfer transactions involving "{account_name}" between {period_start} and {period_end}')

	query = """
	query ($start: Time!, $end: Time!) {
		low: blockIDByTime(time: $start) {
			num
			id
		}
		high: blockIDByTime(time: $end) {
			num
			id
		}
	}
	"""

	variables = {
		"start": period_start,
		"end": period_end
	}

	data = {
		"query": query,
		"variables": variables
	}

	logging.info('Querying for block range...')
	logging.debug(f'Query: {data}') # TODO: Pretty-print query to log file
	response = session.post('https://eos.dfuse.eosnation.io/graphql', headers=headers, data=json.dumps(data))
	if response.status_code == 200:
		logging.info(f'Got response: {response.json()}')
	else:
		logging.error(f'Could not fetch query data: {response.text}')
		exit(-1)

	query = """
	query ($query: String!, $cursor: String, $limit: Int64, $low: Int64, $high: Int64) {
		searchTransactionsBackward(query: $query, lowBlockNum: $low, highBlockNum: $high, limit: $limit, cursor: $cursor) {
			results {
				cursor
				trace {
					block {
						num
						id
						confirmed
						timestamp
						previous
					}
					id
					matchingActions {
						account
						name
						json
						seq
						receiver
					}
				}
			}
		}
	}"""

	variables = {
		"query": f'receiver:{account_name} action:transfer',
		"low": response.json()['data']['low']['num'],
		"high": response.json()['data']['high']['num'],
		"cursor": "",
		"limit": 0
	}
	
	data = {
		"query": query,
		"variables": variables
	}

	logging.info(f'Querying for transfer transactions for {int(response.json()["data"]["high"]["num"]) - int(response.json()["data"]["low"]["num"])} blocks...')
	logging.debug(f'Query: {data}') # TODO: Pretty-print query to log file
	response = session.post('https://eos.dfuse.eosnation.io/graphql', headers=headers, data=json.dumps(data))
	if response.status_code == 200:
		logging.info(f'Got response: {response.json()}')
	else:
		logging.error(f'Could not fetch query data: {response.text}')
		exit(-1)

	"""
		Pandas dataframe
		================

		Account | Date | Amount | Token | AmountCAD | Token/CAD | From | To | BlockNum | TrxID | Memo | Contract | Action | Data 
		-------------------------------------------------------------------------------------------------------------------------
	"""

	results = response.json()['data']['searchTransactionsBackward']['results']
	rows = []
	for r in results:
		row = {}
		for t in r['trace']['matchingActions']:
			row['Account'] = account_name
			row['Date'] = r['trace']['block']['timestamp'] # TODO: Format date
			row['Amount'], row['Token'] = t['json']['quantity'].split(' ')
			row['AmountCAD'] = 0 # TODO: Calculate price from pair quote
			row['Token/CAD'] = 0 # TODO: Fetch historical price from API
			row['From'] = t['json']['from']
			row['To'] = t['json']['to']
			row['BlockNum'] = r['trace']['block']['num']
			row['TrxID'] = r['trace']['id']
			row['Memo'] = t['json']['memo']
			row['Contract'] = t['account']
			row['Action'] = t['name']
			row['Data'] = '' # TODO: Use ?
			rows.append(row)

	df = pd.DataFrame(rows)
	print(df)
	df.to_csv(f'csv\\{account_name}_{period_start.split("T")[0]}_to_{period_end.split("T")[0]}.csv', index=False)