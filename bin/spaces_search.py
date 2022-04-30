#!/usr/bin/env python
import requests
import getopt
import os
import traceback
import sys
import json
import logging
import threading
import time
from datetime import datetime, timedelta

sys.path.insert(1,'../lib/')
import lib

def usage():
    print("./spaces_search.py -r rate -c config -i input -t input_type")


def main(argv):
    try:
        (opts,args)=getopt.getopt(argv, "hi:t:r:c:", ["help"])
        timeout=120  # default
        input_type=""
        config=""
        input=""

        for (opt,arg) in opts:
            if (opt in ("-h", "-help")):
                usage()
                sys.exit()
            elif (opt=="-r"):
                timeout=int(arg)
            elif (opt=="-t"):
                input_type=str(arg)
            elif (opt=="-c"):
                config=str(arg)
            elif (opt=="-i"):
                input=str(arg)
            else:
                usage()
                sys.exit()
    except:
        traceback.print_exc()

    conf=lib.get_config(config)

    if input_type=="file":
        with open(conf.get('ETC_DIR')+"/"+input) as f:
            topic_list=[line.rstrip() for line in f]
    elif input_type=="text":
        topic_list=input.split(",")
    else:
        raise Exception("-> -> -> -> -> -> -> -> -> -> -> -> -> invalid input_type parameter...exiting...")

    t1=threading.Thread(target=lib.topic_search, name="topic_search", args=(conf.get("BEARER_TOKEN"),topic_list,timeout,))
    t1.start()


if __name__ == "__main__":
    main(sys.argv[1:])
