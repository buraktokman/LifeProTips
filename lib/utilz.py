#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: LifeProTips
Module		: logz
Purpose   	: Print timestamp
Version		: 0.1.1 beta
Status 		: Development

Modified	: 2021 Dec 04
Created   	: 2020 Mar 04
Author		: Burak Tokman
Email 		: buraktokman@hotmail.com
Copyright 	: 2021, Bulrosa OU
Licence   	: EULA
			  Unauthorized copying of this file, via any medium is strictly prohibited
			  Proprietary and confidential
#-------------------------------------------------------------------------------
'''
import json


def load_json(dict_arg, json_path):
	'''Load .JSON config file
	'''
	global CONFIG
	# Opening JSON file
	with open(json_path) as json_file:
		data = json.load(json_file)
		dict_arg = merge_dicts(dict_arg, data)
		#CONFIG = {**CONFIG, **data} #CONFIG = CONFIG | data
		#print(dict_arg)
	
	return dict_arg


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