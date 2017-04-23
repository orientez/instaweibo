#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser
import os
from datetime import date
import logging
import threading

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

from instaLooter import InstaLooter


def fetcher(inst):
    logging.debug("fecthing " + inst)
    cur_dir = os.getcwd()
    inst_dir = cur_dir + "/images/"+inst
    if not os.path.exists(inst_dir):
        logging.debug("creating " + inst)
        os.mkdir(inst_dir)
    from_time = date(2015, 1, 1)
    to_time = date.today()
    looter = InstaLooter(profile=inst,directory=inst_dir)
    looter.download_pictures(media_count=20, timeframe=(to_time, from_time), new_only=True)


def main():
    cfg = ConfigParser.ConfigParser()
    cfg.read("/opt/.weibo/weibo.conf")
    insts = cfg.get("PROFILE", 'insts').split(',')
    print insts
    threads = []
    for inst in insts:
        t = threading.Thread(name=inst, target=fetcher, args=(inst,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__== "__main__":
    main()