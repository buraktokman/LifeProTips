#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: LifeProTips
Module		: bot
Purpose   	: Download tips from Reddit and send to Twitter
Source		: https://github.com/buraktokman/LifeProTips
Version		: 0.1.5 beta
Status 		: Development

Modified	: 2021 Dec 4
Created   	: 2021 Dec 4
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
import random
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
'''
Subreddit
https://www.reddit.com/r/LifeProTips/top/

Reddit Dev > https://www.reddit.com/prefs/apps
https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html
'''



# ------ MAIN ----------------------------------
def main():
	# CONFIGURE
	global CONFIG

	# LOAD CONFIG
	print(f"{logz.timestamp()}{Fore.GREEN} REDDIT → INIT → {Style.RESET_ALL}Loading configuration")
	CONFIG = utilz.load_json(CONFIG, CONFIG['config-file'])
	CONFIG = utilz.load_json(CONFIG, WORK_DIR + CONFIG['reddit-account-file'])
	hashtags = utilz.load_hashtags(WORK_DIR + CONFIG['hashtag-file'])


	# ------ FETCH REDDIT --------------------------
	reddit = praw.Reddit(client_id=CONFIG['personal_key'],
						client_secret=CONFIG['secret_key'],
						user_agent=CONFIG['name'],
						username=CONFIG['username'],
						password=CONFIG['password'])

	print(f"{logz.timestamp()}{Fore.GREEN} REDDIT → FETCH → {Style.RESET_ALL}Downloading posts")

	reddit_posts = []
	for submission in reddit.subreddit("LifeProTips").top(time_filter='day', limit=CONFIG['tweet-count']):

		# REPLACE
		rep = {"LPT:": "", "LPT : ": "", "Lpt:": "", "LPT Request:": "", "LPT": ""}
		text = utilz.replace_all(submission.title, rep)
		if "icons8" in submission.title:
			submission.title = "Mod Pick"
		# STRIP
		text = text.rstrip().lstrip()
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
	print(f'{logz.timestamp()}{Fore.GREEN} BOT → HISTORY → {Style.RESET_ALL}Checking history from DynamoDB')
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
			#break

	print(f"{logz.timestamp()}{Fore.GREEN} BOT → SHOW → {Style.RESET_ALL}New tips")
	print(f'{Fore.YELLOW}ID\t{Fore.GREEN}LEN\t{Fore.MAGENTA}FLAIR / TITLE{Style.RESET_ALL}')
	for item in tweets_to_send:
		print(f'{item["id"]}\t{len(item["title"])}\t{Fore.CYAN}({item["flair"]}){Style.RESET_ALL} {item["title"][:60]}...')
	
	print(f'{logz.timestamp()}{Fore.GREEN} BOT → SELECTED → {Style.RESET_ALL}{tweets_to_send[0]["id"]}')

	# --- INCOMPLETE - REMOVE THIS! ----
	# ONLY FIRST TIP
	tweet_to_send = tweets_to_send[0]

	# print(tweet_to_send)
	# exit()

	# ------ AUTH TWITTER --------------------------
	api = twitter.create_api()

	# ------ SEND TWEET ---------------------------
	# ADD HASHTAG
	hashtag = random.choice(hashtags)
	tweet_text = tweet_to_send['title']
	if len(tweet_text) + len(hashtag) + 1 < CONFIG['tweet-length']:
		tweet_text += ' #' + hashtag
	print(f"{logz.timestamp()}{Fore.MAGENTA} TWEET → {Style.RESET_ALL}Sending...")
	twitter_response = api.update_status(status=tweet_text)
	
	# READ RESPONSE TO JSON
	#twitter_response = json.dumps(twitter_response._json)
	twitter_response = twitter_response._json
	# print(f"1 - response:\n{twitter_response}")

	# LIKE TWEET
	# api.create_favorite(twitter_response._json['id'])

	try:
		twitter_response['id']
	except Exception as e:
		print(f"{logz.timestamp()}{Fore.RED} TWEET → ERROR → {Style.RESET_ALL}Cannot tweet! Trying again in 3sec.\n{e}")
		time.sleep(3)

	# ------ CREATE THREAD IF LONG CONTENT  --------
	if tweet_to_send['content'] != '':
		print(f"{logz.timestamp()}{Fore.MAGENTA} TWEET → {Style.RESET_ALL}Long tip, creating tweet thread")

		# SPLIT
		tweets = utilz.split_to_tweets(tweet_to_send['content'], CONFIG['tweet-length'])

		# TWEET
		print(f'{Fore.YELLOW}LEN\t{Fore.MAGENTA}TWEET{Style.RESET_ALL}')
		for tweet in tweets:

			# CHECK IF SENTENCE IS LONGER THAN 240
			#
			# INCOMPLETE !!!
			#
			if len(tweet) > CONFIG['tweet-length']:
				print(f"{Fore.RED}ERROR{Style.RESET_ALL} Tweet is too long!")
				continue

			twitter_response = api.update_status(status=tweet, in_reply_to_status_id=twitter_response['id'])
			# READ RESPONSE TO JSON
			twitter_response = twitter_response._json
			# print(f'response:\n{twitter_response}')
			print(f'{len(tweet)}\t{tweet[:60]}...')
			
			# LIKE TWEET
			# api.create_favorite(twitter_response._json['id'])


	# # ------ WRITE TO TXT  -------------------------
	# tweet = ''
	# with open(WORK_DIR + CONFIG['tweet-file'], 'w') as filehandle:
	# 	for tweet in tweets_history:
	# 		filehandle.write('%s\n' % tweet)

	# ------ WRITE TO S3  --------------------------
	# aws.s3_upload(CONFIG['bucket-name'], WORK_DIR + CONFIG['tweet-file'])

	# ------ WRITE TO DYNAMO  ----------------------
	print(f"{logz.timestamp()}{Fore.YELLOW} AWS → DYNAMO → {Style.RESET_ALL}Inserting...")
	# [aws.dynamodb_put_item(CONFIG['dynamodb-table'], tweet) for tweet in tweets_to_send]
	for tweet in [tweet_to_send]:
		r = aws.dynamodb_put_item(CONFIG['dynamodb-table'], tweet)
		print(f"dynamo response: {r}")


	# ------ DONE  ---------------------------------
	print(f'{logz.timestamp()}{Fore.GREEN} BOT → DONE → Completed')



# ------ START  -----------------------------
if __name__ == '__main__':
	main()
	