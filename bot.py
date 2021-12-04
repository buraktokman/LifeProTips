#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: LifeProTips
Module		: reddit
Purpose   	: Reddit API Wrapper
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
import twitter
import sys
import time
import json
import re
import praw
sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import logz
import utilz
import aws_storage


# Reddit Dev > https://www.reddit.com/prefs/apps
# https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html

WORK_DIR = str(Path(Path(__file__).parents[0])) + '/'
CONFIG = {	'reddit-account-file': WORK_DIR + 'inc/account-reddit.json',
			'tweet-file': WORK_DIR + 'tweets.txt',
			'tweet-count': 6,
			}

HASHTAGS = ['tips', 'life']


# ------ MAIN ----------------------------------
def main():
	# CONFIGURE
	global CONFIG
	
	# LOAD .JSON CONFIG
	CONFIG = utilz.load_json(CONFIG, CONFIG['reddit-account-file'])


	# ------ FETCH REDDIT --------------------------
	reddit = praw.Reddit(client_id=CONFIG['personal_key'],
						client_secret=CONFIG['secret_key'],
						user_agent=CONFIG['name'],
						username=CONFIG['username'],
						password=CONFIG['password'])
						
	time_start = time.time()
	print(f"{logz.timestamp()}{Fore.GREEN} REDDIT → FETCH → {Style.RESET_ALL}Downloading...")

	tweets = []
	for submission in reddit.subreddit("LifeProTips").top(time_filter='day', limit=CONFIG['tweet-count']):
		
		# REPLACE 'LPT'
		rep = {"LPT ": "", "LPT: ": ""}
		text = utilz.replace_all(submission.title, rep)

		# CAPITALIZE 1st
		text = text[:1].upper() + text[1:]
		print(text) #submission.title
		
		# ADD TO LIST
		tweets.append(text)


	# ------ WRITE TO S3  --------------------------
	aws_storage.lambda_handler(tweets)
	tweet = ''
	with open(CONFIG['tweet-file'], 'w') as filehandle:
		for tweet in tweets:
			filehandle.write('%s\n' % tweet)
	

	# ------ AUTH TWITTER --------------------------
	api = twitter.create_api()


	# ------ SEND TWEETS ---------------------------
	print('Loading tweet drafts')
	
	with open(CONFIG['tweet-file']) as f:
		temp_str = f.read() #readlines()
	# file = open(CONFIG['tweet-file'])
	# temp_str = file.read()#.replace("\n", " ")
	# file.close()
	tweets = temp_str.split('\n\n')

	for tweet in tweets:

		# SELECT HASHTAG -- INCOMLETE!
		
		# SEND
		print(f"Sending...")
		send_status = False
		while not send_status:
			twitter_response = api.update_status(tweet)
			print(f"response: {twitter_response}")
			try:
				twitter_response.id
				send_status = True
			except Exception as e:
				print(f"ERROR - Trying again in 3sec. > {e}")


		# ------ WRITE TO FILE  ------------------------
		tweet = ''
		with open(CONFIG['tweet-file'], 'w') as filehandle:
			for tweet in tweets:
				filehandle.write('%s\n' % tweet)

		# ------ SLEEP  --------------------------------
		#time.sleep(CONFIG['sleep'])

	# ------ DONE  ---------------------------------
	

# ------ START  -----------------------------

if __name__ == '__main__':
	main()