#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: LifeProTips
Module		: utilz
Purpose   	: Module for utility functions
Source		: https://github.com/buraktokman/LifeProTips
Version		: 0.1.5 beta
Status 		: Development

Modified    : 2021 Dec 12
Created   	: 2021 Dec 4
Author		: Burak Tokman
Email 		: buraktokman@hotmail.com
Copyright 	: 2021, Bulrosa OU
Licence   	: EULA
			  Unauthorized copying of this file, via any medium is strictly prohibited,
			  proprietary and confidential
#-------------------------------------------------------------------------------
'''
import json



def load_json(dict_arg, json_path):
	'''Load .JSON config file
	'''
	# Opening JSON file
	with open(json_path) as json_file:
		data = json.load(json_file)
		dict_arg = merge_dicts(dict_arg, data)
		#CONFIG = {**CONFIG, **data} #CONFIG = CONFIG | data
		#print(dict_arg)

	return dict_arg


def load_hashtags(hashtag_path):
	'''Load hashtags from file
	'''
	# OPEN
	with open(hashtag_path) as hashtag_file:
		tweets = hashtag_file.read().splitlines()
	# RETURN
	return tweets


def merge_dicts(x, y):
	'''Merge two dictionaries
	'''
	z = x.copy()   # start with keys and values of x
	z.update(y)    # modifies z with keys and values of y
	return z


def replace_all(text, dic):
	'''Replace multiple strings.
	'''
	for i, j in dic.items():
		text = text.replace(i, j)
	return text


# ------ CREATE TWEET  -------------------------
def split_to_tweets(text, max_length):
	''' Split content to tweets
	'''
	tweets = []

	# INCOMPLETE!
	# . SPLIT AVOID LINKS

	# SPLIT
	sentences = text.split('.')
	# REMOVE EMPTY SENTENCES
	sentences = [x.lstrip().rstrip() for x in sentences if x != '']

	# CONSTRUCT TWEET
	tweet_text = ''
	for sentence in sentences:
		if (len(tweet_text) + len(sentence) + 2) < max_length :
			tweet_text += sentence + '. '
		else:
			# ADD TWEET
			tweets.append(tweet_text)
			# RESET - ADD CURRENT SENTENCE FOR NEXT ITER.
			tweet_text = sentence + '. '

	# ADD LAST TWEET
	# INCOMPLETE!
	if len(tweet_text) < max_length:
		tweets.append(tweet_text)

	# RETURN
	return tweets