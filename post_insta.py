#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import ConfigParser
import os
import json
import logging
import time
import threading

logging.basicConfig(filename='/tmp/weibo.log',level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s')
cfg = ConfigParser.ConfigParser()
cfg.read("/opt/.weibo/weibo.conf")
username = cfg.get("DEFAULT", 'user')
password = cfg.get("DEFAULT", 'passwd')
app_key = cfg.get("DEFAULT", 'app_key')
http_url = "https://upload.api.weibo.com/2/statuses/upload.json"


def pp_json(json_str):
    print json.dumps(json.loads(json_str), indent=4)


def post_image(key_word, image_file):
    logging.info("posting " + image_file)
    d = {'source': app_key, 'status': key_word}
    payload = {'pic': open(image_file, 'rb')}
    r = requests.post(http_url, data=d, files=payload, auth=(username, password))
    # r.raise_for_status()
    logging.info("removing " + image_file)
    os.remove(image_file)
    # pp_json(r.text)
    logging.debug(r.text)


def post_insta_images(insta_path, key_word):
    for image_file in os.listdir(insta_path):
        file_path = insta_path + "/" + image_file
        post_image(key_word, file_path)
        time.sleep(60 * 60)


def main():
    key_word = u'#美臀课# #秋裤美臀# #我是美臀控# #腿臀训练#'.encode('utf-8')
    threads = []
    instas = os.listdir("./images")
    for insta in instas:
        tmp_key_word = '#' + insta + '# ' + key_word
        insta_path = "./images/" + insta
        print tmp_key_word
        t = threading.Thread(name=insta, target=post_insta_images, args=(insta_path, tmp_key_word,))
        threads.append(t)
        t.start()
        time.sleep(61)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
'''
endpoint = "https://api.weibo.com/2/statuses/update.json"
payload = {'source': app_key, 'status': 'api test xxxx'}
r = requests.post(endpoint, data=payload, auth=(user, passwd))
'''
