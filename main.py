import json
import logging
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from requests_cache import CachedSession

load_dotenv(find_dotenv())

if __name__ == "__main__":
	file_handler = logging.FileHandler("logs\\" + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + ".log", mode='w')

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

	# Cache JWT response (for up to 24 hours)
	response = session.post('https://auth.eosnation.io/v1/auth/issue', headers=headers, data=data)
	if (response.status_code == 200):
		logging.debug(response.json())
		jwt = response.json()['token']
	else:
		logging.error("Could not load JWT token")
		exit(-1)

	headers = {'Authorization': f'Bearer {jwt}'}
	session = CachedSession(
		'graphql_rest',
		expire_after=timedelta(minutes=30),
		allowable_methods=['GET', 'POST'],
	)

	account_name = 'eosnationftw'
	period_start = '2022-09-22T12:12:24Z'
	period_end = '2022-09-23T12:12:23Z'
	logging.info(f'Searching for transfer transactions to "{account_name}" between {period_start} and {period_end}')

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
	response = session.post('https://eos.dfuse.eosnation.io/graphql', headers=headers, data=json.dumps(data))
	if response.status_code == 200:
		logging.info(f'Got response: {response.json()}')
	else:
		logging.warning("Could not fetch query data")

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
		"query": f"receiver:{account_name} action:transfer",
		"low": response.json()['data']['low']['num'],
		"high": response.json()['data']['high']['num'],
		"cursor": "",
		"limit": 0
	}
	
	data = {
		"query": query,
		"variables": variables
	}

	logging.info('Querying for transfer transactions...')
	response = session.post('https://eos.dfuse.eosnation.io/graphql', headers=headers, data=json.dumps(data))
	if response.status_code == 200:
		logging.info(f'Got response: {response.json()}')
	else:
		logging.warning("Could not fetch query data")