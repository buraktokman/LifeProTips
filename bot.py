#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: LifeProTips
Module		: bot
Purpose   	: Download tips from Reddit and send to Twitter
Source		: https://github.com/buraktokman/LifeProTips
Version		: 0.1.3 beta
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
from re import sub
from colorama import Fore, Back, Style
import twitter
import sys
import time
import json
import praw
sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import logz
import utilz
import aws



# ------ CONFIG --------------------------------
WORK_DIR = str(Path(Path(__file__).parents[0])) + '/'
CONFIG = {'config-file': WORK_DIR + 'inc/config.json'}
HASHTAGS = ['tips', 'life']
'''
Reddit Dev > https://www.reddit.com/prefs/apps
https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html
'''



# ------ MAIN ----------------------------------
def main():
	# CONFIGURE
	global CONFIG

	# LOAD CONFIG
	CONFIG = utilz.load_json(CONFIG, CONFIG['config-file'])
	CONFIG = utilz.load_json(CONFIG, WORK_DIR + CONFIG['reddit-account-file'])


	# ------ FETCH REDDIT --------------------------
	reddit = praw.Reddit(client_id=CONFIG['personal_key'],
						client_secret=CONFIG['secret_key'],
						user_agent=CONFIG['name'],
						username=CONFIG['username'],
						password=CONFIG['password'])

	print(f"{logz.timestamp()}{Fore.GREEN} REDDIT → FETCH → {Style.RESET_ALL}Downloading...")

	reddit_posts = []
	for submission in reddit.subreddit("LifeProTips").top(time_filter='day', limit=CONFIG['tweet-count']):

		# REPLACE
		rep = {"LPT ": "", "LPT: ": "", "Lpt: ": ""}
		text = utilz.replace_all(submission.title, rep)
		if "icons8" in submission.title:
			submission.title = "Mod Pick"

		# CAPITALIZE 1st
		text = text[:1].upper() + text[1:]

		# ADD TO LIST
		post = {'id': submission.id,
				'title': text,
				'content': submission.selftext,
				'flair': submission.link_flair_text,
				'url': submission.url,
				'permalink': submission.permalink,
				'created_utc': int(submission.created_utc)}
		reddit_posts.append(post)


	# ------ DOWNLOAD HISTORY  ---------------------
	# r = aws.s3_download(CONFIG['bucket-name'], CONFIG['tweet-file'])

	# ------ CHECK HISTORY  ------------------------
	print(f'{logz.timestamp()}{Fore.GREEN} BOT → HISTORY → {Style.RESET_ALL}Checking...')
	with open(WORK_DIR + CONFIG['tweet-file']) as f:
		temp_str = f.read() #readlines()
	tweets_history = temp_str.split('\n')

	# SELECT NEW POSTS
	tweets_to_send = []
	for reddit_post in reddit_posts:
		key = {	'id': reddit_post['id'],
				'flair': reddit_post['flair']}

		# CHECK IN DYNAMODB
		r = aws.dynamodb_get_item(CONFIG['dynamodb-table'], key=key)
		# if reddit_post['title'] not in tweets_history:
		if r == False:
			line = f"{reddit_post['id']},{reddit_post['flair']}\n"
			tweets_history.append(reddit_post['title'])
			tweets_to_send.append(reddit_post)
			break
	print(f'{logz.timestamp()}{Fore.GREEN} BOT → NEW TIP → {Style.RESET_ALL}({tweets_to_send[0]["flair"]}) {tweets_to_send[0]["title"]}')
	if tweets_to_send[0]['content'] != '':
		print(f'{logz.timestamp()}{Fore.GREEN} BOT → NEW TIP → Content exist')


	# # ------ AUTH TWITTER --------------------------
	# api = twitter.create_api()

	# # ------ SEND TWEET ---------------------------
	# # SELECT HASHTAG -- INCOMLETE!

	# # SEND
	# print(f"{logz.timestamp()}{Fore.MAGENTA} TWEET → {Style.RESET_ALL}Sending...")
	# twitter_response = api.update_status(status=tweets_to_send[0]['title'])
	
	# # READ RESPONSE TO JSON
	# #twitter_response = json.dumps(twitter_response._json)
	# twitter_response = twitter_response._json
	# print(f"1 - response:\n{twitter_response}")

	# # LIKE TWEET
	# api.create_favorite(twitter_response._json['id'])

	# try:
	# 	twitter_response.id
	# 	send_status = True
	# except Exception as e:
	# 	print(f"{logz.timestamp()}{Fore.RED} TWEET → ERROR → {Style.RESET_ALL}Cannot tweet! Trying again in 3sec.\n{e}")
	# 	time.sleep(3)

	# # ------ CREATE THREAD IF LONG CONTENT  --------
	# if tweets_to_send[0]['content'] != '':
	# 	print(f"{logz.timestamp()}{Fore.MAGENTA} TWEET → {Style.RESET_ALL}Long tip. Creating tweet thread")

	# 	# SPLIT
	# 	tweets = utilz.split_to_tweets(tweets_to_send[0]['content'], CONFIG['tweet-length'])

	# 	# TWEET
	# 	for tweet in tweets:
	# 		print(f'#---------------\n{len(tweet)}\n{tweet}\n')
	# 		twitter_response = api.update_status(status=tweet, in_reply_to_status_id=twitter_response['id'])
	# 		# READ RESPONSE TO JSON
	# 		twitter_response = twitter_response._json
	# 		print(f'response:\n{twitter_response}')
			
	# 		# LIKE TWEET
	# 		api.create_favorite(twitter_response._json['id'])


	# # ------ WRITE TO TXT  -------------------------
	tweet = ''
	with open(WORK_DIR + CONFIG['tweet-file'], 'w') as filehandle:
		for tweet in tweets_history:
			filehandle.write('%s\n' % tweet)

	# ------ WRITE TO S3  --------------------------
	aws.s3_upload(CONFIG['bucket-name'], WORK_DIR + CONFIG['tweet-file'])

	# ------ WRITE TO DYNAMO  ----------------------
	print(f"{logz.timestamp()}{Fore.YELLOW} AWS → DYNAMO → {Style.RESET_ALL}Inserting...")
	[aws.dynamodb_put_item(CONFIG['dynamodb-table'], tweet) for tweet in tweets_to_send]
	for tweet in tweets_to_send:
		r = aws.dynamodb_put_item(CONFIG['dynamodb-table'], tweet)
		# print(f"response: {r}")

	# ------ DONE  ---------------------------------
	print(f'{logz.timestamp()}{Fore.GREEN} BOT → DONE → Completed')



# ------ START  -----------------------------
if __name__ == '__main__':
	main()
	