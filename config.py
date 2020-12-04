import os
import json
from pathlib import Path

SUBS_PATH = os.path.join(Path.home(), ".config", "ytrss", "subscriptions.json")

def get_videos_dir():
    return os.path.join(Path.home(), "Videos/")

def get_subs_json():

    try:
        with open(SUBS_PATH) as f:
            return json.load(f)
        # Do something with the file
    except IOError:
        print("%s not found!" %SUBS_PATH )


def get_channel_ids()->list:

    json = get_subs_json()
    channels = []
    for i in json:
        resource = (i['snippet']['resourceId'])
        if resource['kind'] == 'youtube#channel':
            channels.append(resource['channelId'])
    return channels
