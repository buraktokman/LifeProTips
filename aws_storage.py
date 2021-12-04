#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: LifeProTips
Module		: aws_storage
Purpose   	: Manage S3 Bucket
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
import json
import boto3
sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import logz


CONFIG = {}
# https://stackoverflow.com/questions/48945389/how-could-i-use-aws-lambda-to-write-file-to-s3-python


# ------ MAIN ----------------------------------
def main():
	# CONFIGURE
	global CONFIG

	# ------ WRITE TO S3  --------------------------
	print(f"{logz.timestamp()}{Fore.YELLOW} AWS → S3 → {Style.RESET_ALL}Uploading...")

	s3 = boto3.resource('s3')
	for bucket in s3.buckets.all():
		print(bucket.name)

	# ------ DONE  ---------------------------------
	

def download():
	''' Download from S3
	'''
	pass


def upload():
	''' Upload to S3
	'''
	pass


def lambda_handler(event, context):
    string = "dfghj"
    encoded_string = string.encode("utf-8")

    bucket_name = "s3bucket"
    file_name = "hello.txt"
    s3_path = "100001/20180223/" + file_name

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)


if __name__ == '__main__':
	main()