#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: LifeProTips
Module		: aws
Purpose   	: Manage AWS services
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

from pathlib import Path
from colorama import Fore, Back, Style
from boto3.dynamodb.conditions import Key
import sys
import json
import boto3
#sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import logz
import utilz


# ------ CONFIG --------------------------------
WORK_DIR = str(Path(Path(__file__).parents[1])) + '/'
INC_DIR = WORK_DIR + '/inc/'


# ----------------------------------------------

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			S3 			 				#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

def s3_download(bucket_name, file_name):
	''' Download from S3
	'''
	print(f"{logz.timestamp()}{Fore.YELLOW} AWS → S3 → {Style.RESET_ALL}Downloading...")

	try:
		s3 = boto3.resource('s3')
		s3.Bucket(bucket_name).download_file(file_name.split('/')[-1],
												WORK_DIR + '/res/' + file_name) #2nd arg. is s3 path
		return True
	except Exception as e:
		print(f"{logz.timestamp()}{Fore.RED} AWS → S3 → ERROR → {Style.RESET_ALL}Cannot download!\n{e}")
		return False


def s3_upload(bucket_name, file_path):
	''' Upload to S3
	'''
	print(f"{logz.timestamp()}{Fore.YELLOW} AWS → S3 → {Style.RESET_ALL}Uploading...")

	# s3 = boto3.resource('s3')
	# for bucket in s3.buckets.all():
	# 	print(bucket.name)
	try:
		s3 = boto3.resource('s3')
		#s3.Bucket(CONFIG['bucket-name']).put_object(key=s3_path, body=file_object)
		# upload_file(Filename, Bucket, Key, ExtraArgs=None, Callback=None, Config=None)
		s3.meta.client.upload_file(file_path,
									bucket_name,
									file_path.split('/')[-1]) # filename as Key
		return True
	except Exception as e:
		print(f"{logz.timestamp()}{Fore.RED} AWS → S3 → ERROR → {Style.RESET_ALL}Cannot upload!\n{e}")
		return False

def s3_get_buckets():
	''' Get buckets from S3
	'''
	try:
		s3 = boto3.resource('s3')
		for bucket in s3.buckets.all():
			print(bucket.name)
		return True
	except Exception as e:
		print(f"{logz.timestamp()}{Fore.RED} AWS → S3 → ERROR → {Style.RESET_ALL}Cannot get buckets!\n{e}")
		return False


def lambda_handler(event, context):
    string = "dfghj"
    encoded_string = string.encode("utf-8")

    bucket_name = "s3bucket"
    file_name = "hello.txt"
    s3_path = "100001/20180223/" + file_name

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)



# ----------------------------------------------

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			SNS 			 			#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

def sns_get_topic(topic_name):
	''' Get topic from SNS
	'''
	try:
		sns = boto3.client('sns')
		response = sns.get_topic_attributes(TopicArn=topic_name)
		return response
	except Exception as e:
		print(f"{logz.timestamp()}{Fore.RED} AWS → SNS → ERROR → {Style.RESET_ALL}Cannot get topic!\n{e}")
		return False



# ----------------------------------------------

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			DYNAMODB 			 		#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

def dynamodb_get_item(table_name, key):
	''' Get item from DynamoDB
		{'Key': value}
	'''
	try:
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table(table_name)
		response = table.get_item(
			Key=key
		 	# Key={'id': {'S': key}}
			# Key={'id': key, 'flair': None}
			)
		# response = table.query(
		# 	#IndexName='id',
		# 	KeyConditionExpression=Key('id').eq(key)
		# 	)
		return response['Item']
	except Exception as e:
		print(f"{logz.timestamp()}{Fore.RED} AWS → DYNAMO → ERROR → {Style.RESET_ALL}Item not found → response: {e}")
		return False


def dynamodb_get_all(table_name):
	''' Get all items from DynamoDB
	'''
	try:
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table(table_name)
		response = table.scan()
		return response['Items']
	except Exception as e:
		print(f"{logz.timestamp()}{Fore.RED} AWS → DYNAMO → ERROR → {Style.RESET_ALL}Cannot get all\n{e}")
		return False


def dynamodb_put_item(table_name, item):
	''' Put item to DynamoDB
	'''
	try:
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table(table_name)
		response = table.put_item(Item=item)
		return response
	except Exception as e:
		print(f"{logz.timestamp()}{Fore.RED} AWS → DYNAMO → ERROR → {Style.RESET_ALL}Cannot put item\n{e}")
		return False


def dynamodb_del_item(table_name, key):
	''' Delete item from DynamoDB
	'''
	try:
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table(table_name)
		response = table.delete_item(Key=key)
		return response
	except Exception as e:
		print(f"{logz.timestamp()}{Fore.RED} AWS → DYNAMO → ERROR → {Style.RESET_ALL}Cannot delete item\n{e}")
		return False



# ----------------------------------------------

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			EC2 			 			#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

def get_ec2_instances():
	''' Get all EC2 instances
	'''
	try:
		ec2 = boto3.resource('ec2')
		instances = ec2.instances.all()
		return instances
	except Exception as e:
		print(f"AWS → EC2 → ERROR → Cannot get instances!\n{e}")
		return False


def get_ec2_instances_all_regions():
	''' Get all EC2 instances in all regions
	'''
	try:
		ec2 = boto3.client('ec2')
		regions = ec2.describe_regions()
		all_instances = []
		for region in regions['Regions']:
			ec2 = boto3.resource('ec2', region_name=region['RegionName'])
			instances = ec2.instances.all()
			# all_instances.append({'region': region['RegionName'], 'instances': instances})
			for instance in instances:
				# print(instance.id, instance.instance_type)
				all_instances.append({'region': region, 'instance': instance})
		return all_instances
	except Exception as e:
		print(f"AWS → EC2 → ERROR → Cannot get instances!\n{e}")
		return False


def ec2_terminate_instance(instance_id):
	''' Terminate EC2 instance
	'''
	try:
		ec2 = boto3.resource('ec2')
		instance = ec2.Instance(instance_id)
		instance.terminate()
		return True
	except Exception as e:
		print(f"AWS → EC2 → ERROR → Cannot terminate instance!\n{e}")
		return False


def ec2_terminate_all_instances_in_all_regions():
	''' Terminate all EC2 instances in all regions
	'''
	try:
		ec2 = boto3.client('ec2')
		regions = ec2.describe_regions()
		for region in regions['Regions']:
			ec2 = boto3.resource('ec2', region_name=region['RegionName'])
			instances = ec2.instances.all()
			for instance in instances:
				instance.terminate()
		return True
	except Exception as e:
		print(f"AWS → EC2 → ERROR → Cannot terminate instances!\n{e}")
		return False



# ------ START  --------------------------------
if __name__ == '__main__':
	# upload('/Users/hummingbird/Workspace/Sandbox/Bot-LifeTips/tweets.txt')
	# s3_download('lifetips', 'tweets.txt')

	print('Connecting to AWS...')
	print('Fetching instances in all regions...')
	print('------')
	instance_list = get_ec2_instances_all_regions()
	print(f'REGION\t\t\tID\t\t\t\tIPv4 ADDRESS')
	for region in instance_list:
		# print(r)
		# print instance region and insntances
		# print(f'{region["region"]}\t\t{region["instances"].id}\t\t{region["instances"].public_ip_address}')
		# print(f'{region["region"]}\t\t{region["instances"]}')
		print(f'{region["region"]["RegionName"]}\t\t{region["instance"].id}\t\t{region["instance"].public_ip_address}')
		# for insntance in region['instances']:

		# print(f'{region.placement["AvailabilityZone"][:-1]}\t{r1.id}\t\t{r1.public_ip_address}')
		# # print(f"{r1.id}\t{r1.public_ip_address}")

	exit()

	item = {'id': 'r8vdza', 'title': "If you're at a hotel and have to call 911", 'flair': 'Miscellaneous'}
	dynamodb_put_item(CONFIG['dynamodb-table'], item)
	dynamodb_del_item(CONFIG['dynamodb-table'], {'tipId': '1'})

	key = {'id': 'r9dk8n', 'flair': 'Miscellaneous'}
	r = dynamodb_get_item('lifetips', key)
	print(r)
	exit()

	r = dynamodb_get_all('lifetips')
	for r2 in r:
		print(r2)
		print('-----')
	print(r)