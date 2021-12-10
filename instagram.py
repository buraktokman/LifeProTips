#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: LifeProTips
Module		: instagram
Purpose   	: Create PNG image and post on Instagram
Source		: https://github.com/buraktokman/LifeProTips
Version		: 0.1.4 beta
Status 		: Development

Modified	: 2021 Dec 9
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
from PIL import Image, ImageFont, ImageDraw 
from colorama import Fore, Back, Style
import random
import sys
from instagrapi import Client
sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import logz
import utilz



# ------ CONFIG --------------------------------
WORK_DIR = str(Path(Path(__file__).parents[0])) + '/'
CONFIG = {'config-file': WORK_DIR + 'inc/config.json'}
'''
DOCS
https://adw0rd.github.io/instagrapi/usage-guide/media.html
https://towardsdatascience.com/adding-text-on-image-using-python-2f5bf61bf448
'''


# ------ MAIN ----------------------------------
def main():
	# CONFIGURE
	global CONFIG

	# LOAD CONFIG
	print(f"{logz.timestamp()}{Fore.MAGENTA} INSTA → INIT → {Style.RESET_ALL}Loading configuration")
	CONFIG = utilz.load_json(CONFIG, CONFIG['config-file'])
	CONFIG = utilz.load_json(CONFIG, WORK_DIR + CONFIG['instagram-account-file'])
	hashtags = utilz.load_hashtags(WORK_DIR + CONFIG['hashtag-file'])


	# ------ CREATE POST --------------------------
	# OPEN IMAGE
	img = Image.open("res/white_1080x1080.png")
	# SELECT FONT
	title_font = ImageFont.truetype("res/open-sans.ttf", 32)

	title_text = "If you're low on funds and need to eat... A grocery store rotisserie chicken, a big head of broccoli and a box of pasta will feed you for 3 days for about 10 bucks. Free condiment packets for the chicken. Can easily spend 10 on a single small meal, or make it go further."
	title_text = title_text.replace('. ', '\n')
	# CREATE DRAW OBJECT
	image_editable = ImageDraw.Draw(img)
	# DRAW TEXT
	image_editable.text((15,15), title_text, (41, 41, 41, 1))#, font=title_font)
	# SAVE
	img.save("out/result.jpg", optimize=True, quality=80)
	exit()


	# ------ AUTH INSTA ---------------------------
	cl = Client()
	cl.login(CONFIG['insta-password'], CONFIG['insta-pasword'])

	# ------ SEND POST ----------------------------
	print(f"{logz.timestamp()}{Fore.MAGENTA} INSTA → {Style.RESET_ALL}Sending...")
	caption = content['title'] + '\n' + content['content']

	# photo_path  = 
	cl.photo_upload(path=Path("out/new_picture.jpg"),
					caption=caption)


	# ------ ADD HASHTAGS AS REPLY ----------------
	# PICK 3
	hashtag = random.choice(hashtags, k=3)
	# DD HASHTAG
	hashtag_text = ''
	for hashtag in hashtag:
		hashtag_text += ' #' + hashtag

	# REPLY
	# INCOMPLETE
	

	

	# ------ DONE  --------------------------------
	print(f'{logz.timestamp()}{Fore.MAGENTA} INSTA → DONE → Completed')



# ------ START  -----------------------------
if __name__ == '__main__':
	main()
	