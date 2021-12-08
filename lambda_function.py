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
 