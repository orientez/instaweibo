#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import ConfigParser
import os
import json
import logging
import time

logging.basicConfig(filename='weibo.log',level=logging.INFO)


def pp_json(json_str):
    print json.dumps(json.loads(json_str), indent=4)


def post_image(key_word, image_file):
    logging.info("posting " + image_file)
    d = {'source': app_key, 'status': key_word}
    payload = {'pic': open(image_file, 'rb')}
    r = requests.post(http_url, data=d, files=payload, auth=(username, password))
    logging.debug(pp_json(r.text))

key_word = u'#美臀课# #秋裤美臀# #美臀诱惑# #我是美臀控# #腿臀训练#'.encode('utf-8')
cfg = ConfigParser.ConfigParser()
cfg.read("/opt/.weibo/weibo.conf")
username = cfg.get("DEFAULT",'user')
password = cfg.get("DEFAULT",'passwd')
app_key = cfg.get("DEFAULT",'app_key')

http_url = "https://upload.api.weibo.com/2/statuses/upload.json"
image_file = '1484626614980930268.jpg'

for insta in os.listdir("./images"):
    tmp_key_word = '#' + insta + '# ' + key_word
    insta_path = "./images/" + insta
    print tmp_key_word
    for image_file in os.listdir(insta_path):
        file_path = insta_path + "/" + image_file
        print file_path

        post_image(tmp_key_word, file_path)
        time.sleep(1)
        logging.info("deleting " + image_file)
        os.remove(file_path)

# delete image after upload


'''
endpoint = "https://api.weibo.com/2/statuses/update.json"
payload = {'source': app_key, 'status': 'api test xxxx'}
r = requests.post(endpoint, data=payload, auth=(user, passwd))
'''