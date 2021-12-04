#! usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: Project JaaS
Module		: twitter
Purpose   	: Twitter API
Version		: 0.1.1 beta
Status 		: Development

Modified	: 2021 Dec 4
Created   	: 2020 Mar 04
Author		: Burak Tokman
Email 		: buraktokman@hotmail.com
Copyright 	: 2021, Bulrosa OU
Licence   	: EULA
			  Unauthorized copying of this file, via any medium is strictly prohibited
			  Proprietary and confidential
#-------------------------------------------------------------------------------
'''

from pathlib import Path
from colorama import Fore, Back, Style
import os
import sys
import time
import logging
import tweepy
sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import logz
import utilz

logger = logging.getLogger()

# Twitter Dev > https://developer.twitter.com
# https://developer.twitter.com/en/docs/basics/rate-limiting

WORK_DIR = str(Path(Path(__file__).parents[0])) + '/'
CONFIG = {	'config-file': WORK_DIR + 'inc/config',
			'twitter-account-file': WORK_DIR + 'inc/account-twitter.json',
			}


def create_api():
	global CONFIG

	# LOAD .JSON CONFIG
	CONFIG = utilz.load_json(CONFIG, CONFIG['twitter-account-file'])

	# ----------------------------------------------

		#	#	#	#	#	#	#	#	#	#	#
		#										#
		#			AUTH TWITTER 				#
		#										#
		#	#	#	#	#	#	#	#	#	#	#

	print(f"{logz.timestamp()}{Fore.MAGENTA} TWITTER → AUTH → {Style.RESET_ALL}Authorizing to Twitter", end="")

	# Authenticate to Twitter
	auth = tweepy.OAuthHandler(CONFIG['consumer-key'], CONFIG['consumer-secret'])
	auth.set_access_token(CONFIG['access-token'], CONFIG['access-token-secret'])

	# Create API object
	# Print a message and wait if the rate limit is exceeded
	api = tweepy.API(auth, wait_on_rate_limit=True,
							wait_on_rate_limit_notify=True)
	try:
		api.verify_credentials()
		print("OK")
	except Exception as e:
		print("Error during authentication")
		logger.error("Error creating API", exc_info=True)
		raise e

	logger.info("API created")
	return api


if __name__ == '__main__':
	r = create_api()
	print(r)

