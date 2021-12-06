#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: LifeProTips
Module		: bot
Purpose   	: Download tips from Reddit and send to Twitter
Version		: 0.1.7 beta
Status 		: Development

Modified	: 2021 Dec 4
Created   	: 2020 Mar 04
Author		: Burak Tokman
Email 		: buraktokman@hotmail.com
Copyright 	: 2021, Bulrosa OU
Licence   	: EULA
			  Unauthorized copying of this file, via any medium is strictly prohibited,
			  proprietary and confidential
#-------------------------------------------------------------------------------
'''

from pathlib import Path
from colorama import Fore, Back, Style
import twitter
import sys
import time
import praw
sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import logz
import utilz
import aws


# ------ CONFIG --------------------------------
'''
Reddit Dev > https://www.reddit.com/prefs/apps
https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html
'''
WORK_DIR = str(Path(Path(__file__).parents[0])) + '/'
CONFIG = {	'reddit-account-file': WORK_DIR + 'inc/account-reddit.json',
			'config-file': WORK_DIR + 'inc/config.json',
			'tweet-file': WORK_DIR + 'tweets.txt',
			'tweet-count': 6,
			}
HASHTAGS = ['tips', 'life']


# ------ MAIN ----------------------------------
def main():
	# CONFIGURE
	global CONFIG
	
	# LOAD CONFIG
	CONFIG = utilz.load_json(CONFIG, CONFIG['reddit-account-file'])
	CONFIG = utilz.load_json(CONFIG, CONFIG['config-file'])


	# ------ FETCH REDDIT --------------------------
	reddit = praw.Reddit(client_id=CONFIG['personal_key'],
						client_secret=CONFIG['secret_key'],
						user_agent=CONFIG['name'],
						username=CONFIG['username'],
						password=CONFIG['password'])
						
	time_start = time.time()
	print(f"{logz.timestamp()}{Fore.GREEN} REDDIT → FETCH → {Style.RESET_ALL}Downloading...")

	reddit_posts = []
	for submission in reddit.subreddit("LifeProTips").top(time_filter='day', limit=CONFIG['tweet-count']):

		# REPLACE 'LPT'
		rep = {"LPT ": "", "LPT: ": ""}
		text = utilz.replace_all(submission.title, rep)

		# CAPITALIZE 1st
		text = text[:1].upper() + text[1:]
		
		# ADD TO LIST
		post = {'id': submission.id,
				'title': text,
				'content': submission.selftext,
				'flair': submission.link_flair_text}
		reddit_posts.append(post)
	

	# ------ DOWNLOAD HISTORY  ---------------------
	r = aws.s3_download()

	# ------ CHECK HISTORY  ------------------------
	with open(CONFIG['tweet-file']) as f:
		temp_str = f.read() #readlines()
	tweets_history = temp_str.split('\n\n')

	# SELECT NEW POSTS
	tweets_to_send = []
	for reddit_post in reddit_posts:
		if reddit_post['title'] not in tweets_history:
			tweets_history.append(reddit_post['title'])
			tweets_to_send.append(reddit_post)
			
			# INCOMPLETE
			break



	# ------ AUTH TWITTER --------------------------
	api = twitter.create_api()

	# ------ SEND TWEET ---------------------------
	# SELECT HASHTAG -- INCOMLETE!

	# SEND
	print(f"{logz.timestamp()}{Fore.MAGENTA} TWEET → {Style.RESET_ALL}Sending...")
	send_status = False
	while not send_status:
		twitter_response = api.update_status(tweets_to_send[0]['title'])
		print(f"response: {twitter_response}")
		try:
			twitter_response.id
			send_status = True
		except Exception as e:
			print(f"{logz.timestamp()}{Fore.RED} TWEET → ERROR → {Style.RESET_ALL}Cannot tweet! Trying again in 3sec.\n{e}")
			time.sleep(3)

		# ------ CREATE THREAD IF LONG TIP  ------------
		# INCOMPLETE!
		# if len(tweets_to_send[0]['content']) > 140:	
	

	# # ------ WRITE TO TXT  -------------------------
	# tweet = ''
	# with open(CONFIG['tweet-file'], 'w') as filehandle:
	# 	for tweet in tweets_history:
	# 		filehandle.write('%s\n' % tweet)

	# ------ WRITE TO S3  --------------------------
	#aws.s3_upload(CONFIG['tweet-file'])

	# ------ WRITE TO DYNAMO  ----------------------
	print(f"{logz.timestamp()}{Fore.YELLOW} AWS → DYNAMO → {Style.RESET_ALL}Inserting...")
	[aws.dynamodb_put_item(CONFIG['dynamodb-table'], tweet) for tweet in tweets_to_send]
	# for tweet in tweets_to_send:
	# 	r = aws.dynamodb_put_item(CONFIG['dynamodb-table'], tweet)
	# 	print(f"response: {r}")
	# 	exit()


	# ------ DONE  ---------------------------------
	

# ------ START  -----------------------------

if __name__ == '__main__':
	main()