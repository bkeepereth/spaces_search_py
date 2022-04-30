#!/usr/bin/env python
import requests
import getopt
import os
import traceback
import sys
import json
import threading
import time
from datetime import datetime, timedelta

import xml.etree.ElementTree as ET

def get_config(file_name):
    if (file_name=="" or file_name==None):
        raise Exception(str(datetime.datetime.now())+"|get_config|file_name is invalid|file_name="+str(file_name))

    result=dict()
    root=ET.parse(file_name).getroot()
    for prop in root.findall('property'):
        result[prop.find('name').text]=prop.find('value').text

    return result


def create_headers(bearer_token):
    headers = {
        "Authorization": "Bearer {}".format(bearer_token),
        "User-Agent": "v2SpacesSearchPython"
    }
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)

    if (response.status_code != 200):
        raise Exception(response.status_code, response.text)
    return response.json()


def topic_search(bearer_token, topic_list, timeout):
    while True:
        ids=list()
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

                    if space_id not in ids:  # added to prevent dups / run
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

                        ids.append(space_id)
            except:
                #traceback.print_exc()
                pass

        print('''----------------------------------------------------------------+++++''')
        time.sleep(timeout)

