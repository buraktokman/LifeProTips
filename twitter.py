#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: LifeProTips
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
import sys
import json
import tweepy
sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import utilz
import logging
logger = logging.getLogger()



# ------ CONFIG --------------------------------
WORK_DIR = str(Path(Path(__file__).parents[0])) + '/'
CONFIG = {'config-file': WORK_DIR + 'inc/config.json'}
'''
https://developer.twitter.com/en/docs/basics/rate-limiting
https://developer.twitter.com/en/portal/products/elevated
'''


# ------ MAIN ----------------------------------
def create_api():
	global CONFIG

	# ----------------------------------------------

		#	#	#	#	#	#	#	#	#	#	#
		#										#
		#			AUTH TWITTER 				#
		#										#
		#	#	#	#	#	#	#	#	#	#	#

	print(f"TWITTER → AUTH → Authorizing")

	# LOAD CONFIG
	CONFIG = utilz.load_json(CONFIG, WORK_DIR + CONFIG['twitter-account-file'])


	# ------ AUTH TWITTER --------------------------
	auth = tweepy.OAuthHandler(CONFIG['consumer-key'], CONFIG['consumer-secret'])
	auth.set_access_token(CONFIG['access-token'], CONFIG['access-token-secret'])
	api = tweepy.API(auth)

	# Create API object
	# Print a message and wait if the rate limit is exceeded
	api = tweepy.API(auth, wait_on_rate_limit=True,
							wait_on_rate_limit_notify=True)
	try:
		api.verify_credentials()
		# print("TWITTER → AUTH → OK")
	except Exception as e:
		print("TWITTER → ERROR Authentication failed")
		logger.error("Error creating API", exc_info=True)
		raise e

	logger.info("API created")
	return api


if __name__ == '__main__':
	r = create_api()
	print(r)

