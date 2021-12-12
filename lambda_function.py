#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project     : LifeProTips
Module      : lambda_function
Purpose     : AWS Lambda function handler
Source      : https://github.com/buraktokman/LifeProTips
Version     : 0.1.5 beta
Status      : Development

Modified    : 2021 Dec 12
Created     : 2021 Dec 4
Author      : Burak Tokman
Email       : buraktokman@hotmail.com
Copyright   : 2021, Bulrosa OU
Licence     : EULA
              Unauthorized copying of this file, via any medium is strictly prohibited,
              proprietary and confidential
#---
import os
import sys
import json
import subprocess
import bot

def lambda_handler(event, context):
    print("Hello, lambda handler in progress.")

   	# INSTALL MODULES
    # print("Installing modules...")
    # install_modules()

    # START
    print('Initiating bot.py')
    bot.main()
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

# def install_modules():
#     print("Installing modules...")
#     # subprocess.call(['pip3', 'install', '-r', 'requirements.txt'
#     #                             '-t /tmp/',
#     #                             '--no-cache-dir'])
#     subprocess.call('pip install -r requirements-t /tmp/ --no-cache-dir'.split(),
#                         stdout=subprocess.DEVNULL,
#                         stderr=subprocess.DEVNULL)
#     sys.path.insert(1, '/tmp/')
 