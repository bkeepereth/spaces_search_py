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

bearer_token = ""

def create_headers(bearer_token):
    headers = {
        "Authorization": "Bearer {}".format(bearer_token),
        "User-Agent": "v2SpacesSearchPython"
    }
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    #print(response.status_code)

    if (response.status_code != 200):
        raise Exception(response.status_code, response.text)
    return response.json()


def topic_search(argv):
    print(argv)

    topic_list=[]

    while True:
        for x in topic_list:
            try:
                search_url="https://api.twitter.com/2/spaces/search"

                query_params={'query':x,
                    'space.fields':'title,started_at',
                    'expansions':'creator_id,host_ids,speaker_ids'}

                headers=create_headers(bearer_token)
                json_response=connect_to_endpoint(search_url,headers,query_params)
           
                #print(json_response)

                spaces=json_response['data']
                users=json_response['includes']['users']

                for i in range(len(spaces)):
                    title=spaces[i]['title']
                    host_ids=spaces[i]['host_ids']
                    creator_id=spaces[i]['creator_id']
                    speaker_ids=spaces[i]['speaker_ids']
                    space_id=spaces[i]['id']
                    started_at=spaces[i]['started_at']
                
                    start_dt=datetime(
                        int(started_at[:4]),
                        int(started_at[5:7]),
                        int(started_at[8:10]),
                        int(started_at[11:13]),
                        int(started_at[14:16]),
                        int(started_at[17:19]))

                    print('''----------------------------------------------------------------+++++
'''+title+'''
'''+started_at+'''
''')
                    for user in users:
                        if user['id']==creator_id:
                            print("  Host: "+user['name']+" // "+user['username'])
                        elif user['id'] in host_ids:
                            print("    Co-Host: "+user['name']+" // "+user['username'])
                        elif user['id'] in speaker_ids:
                            print("      Speaker: "+user['name']+" // "+user['username'])

                    print('''\n=> https://twitter.com/i/spaces/'''+str(space_id)+'''/peek
=> Started: -'''+str(datetime.utcnow()-start_dt)[:7])
            except:
                #traceback.print_exc()
                pass

        print('''----------------------------------------------------------------+++++''')
        time.sleep(120)


def main(argv):
    t1=threading.Thread(target=topic_search, name="topic_search", args=(argv,))
    t1.start()


if __name__ == "__main__":
    main(sys.argv[1:])
