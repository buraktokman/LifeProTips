#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: LifeProTips
Module		: bot
Purpose   	: Download tips from Reddit and send to Twitter
Version		: 0.1.2 beta
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
		rep = {"LPT ": "", "LPT: ": ""}
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
	print(f'{logz.timestamp()}{Fore.GREEN} BOT → NEW TIP → {Style.RESET_ALL}{tweets_to_send[0]["title"]}')


	# ------ AUTH TWITTER --------------------------
	api = twitter.create_api()

	# ------ SEND TWEET ---------------------------
	# SELECT HASHTAG -- INCOMLETE!

	# SEND
	print(f"{logz.timestamp()}{Fore.MAGENTA} TWEET → {Style.RESET_ALL}Sending...")
	twitter_response = api.update_status(status=tweets_to_send[0]['title'])
	# READ RESPONSE TO JSON
	#twitter_response = json.dumps(twitter_response._json)
	twitter_response = twitter_response._json
	print(f"1 - responseTYpe:\n{type(twitter_response)}")
	print(f"1 - response:\n{twitter_response}")

	# try:
	# 	twitter_response.id
	# 	send_status = True
	# except Exception as e:
	# 	print(f"{logz.timestamp()}{Fore.RED} TWEET → ERROR → {Style.RESET_ALL}Cannot tweet! Trying again in 3sec.\n{e}")
	# 	time.sleep(3)

	# ------ CREATE THREAD IF LONG CONTENT  --------

	# REMOVE THIS
	tweets_to_send[0]['content'] = '''There is some great advice out there on personal finance for saving. I believe building a strong foundation for retirement (savings, IRAs, 401ks, etc.) is definitely something everyone should work on. I also agree that an emergency fund is important. All that said, make sure to take some chances as well, especially before you get older, get married, and have kids. You don’t have to buy luxury cars, take 10 exotic trips, or buy a million dollar house. One thing you should do is pick somewhere you have always wanted to go, save up, and get there, no matter what. Don’t skimp on the little things either. Make sure to take whatever time you need, plan it out, go to nice restaurants, see the sights, and stay in a nice hotel. A lot of my friends have waited and waited for those trips, thinking they would do it eventually. Some thought before they had kids, others on their honeymoon, and some when “they made enough money to justify it”. Most of them never got the chance. Some had kids early/unexpectedly, others married at the court house and didn’t want a honeymoon, some cancelled their honeymoons because of the pandemic, and others keep pushing the goal posts further on “how much they need to make to go to ____”. One trip, even an expensive one won’t break most people. It could also be the most amazing experience of your life. I got lucky and got to do mine when I was in college as part of a study abroad. I took loans out for it, worked OT at two retail jobs that semester, and didn’t have the loans paid back until I turned 30, but I have no regrets. It expanded my worldview, left me with some unbelievable memories, and made me a better person.'''

	# INCOMPLETE!
	if tweets_to_send[0]['content'] != '':
		print(f"{logz.timestamp()}{Fore.MAGENTA} TWEET → {Style.RESET_ALL}Long tip. Creating tweet thread")

		# SPLIT TO SENTENCES
		sentences = tweets_to_send[0]['content'].split('.')
		# REMOVE EMPTY SENTENCES
		sentences = [x.lstrip().rstrip() for x in sentences if x != '']

		# CONSTRUCT TWEET
		tweet_text = ''
		for sentence in sentences:
			if (len(tweet_text) + len(sentence)) < CONFIG['tweet-length']:
				tweet_text += sentence + '. '
			else:
				# TWEET
				print(f'---\n{tweet_text}')
				twitter_response = api.update_status(status=tweet_text,
														in_reply_to_status_id=twitter_response['id'], #auto_populate_reply_metadata=True
														)
				# READ RESPONSE TO JSON
				twitter_response = twitter_response._json
				print(f'2 response:\n{twitter_response}')
				# ADD CURRENT SENTENCE
				tweet_text = sentence + '. '

		# TWEET LAST GROUP
		print(f'===\n{tweet_text}')


	# # ------ WRITE TO TXT  -------------------------
	# tweet = ''
	# with open(CONFIG['tweet-file'], 'w') as filehandle:
	# 	for tweet in tweets_history:
	# 		filehandle.write('%s\n' % tweet)

	# ------ WRITE TO S3  --------------------------
	# aws.s3_upload(CONFIG['bucket-name'], WORK_DIR + CONFIG['tweet-file'])

	# ------ WRITE TO DYNAMO  ----------------------
	# print(f"{logz.timestamp()}{Fore.YELLOW} AWS → DYNAMO → {Style.RESET_ALL}Inserting...")
	# [aws.dynamodb_put_item(CONFIG['dynamodb-table'], tweet) for tweet in tweets_to_send]
	# for tweet in tweets_to_send:
	# 	r = aws.dynamodb_put_item(CONFIG['dynamodb-table'], tweet)
	# 	# print(f"response: {r}")

	# ------ DONE  ---------------------------------
	print(f'{logz.timestamp()}{Fore.GREEN} BOT → DONE → Completed')



# ------ START  -----------------------------
if __name__ == '__main__':
	main()