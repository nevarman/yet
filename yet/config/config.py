import os
import json
from pathlib import Path

# TODO what happens in windows
SUBS_PATH = os.path.join(Path.home(), ".config", "yet", "subscriptions.json")


def get_videos_dir():
    return os.path.join(Path.home(), "Videos/")


def get_subs_json():

    try:
        with open(SUBS_PATH) as f:
            return json.load(f)
    except IOError:
        print("%s not found!" % SUBS_PATH)
        return None


def get_channel_ids() -> list:

    json = get_subs_json()
    if json is None:
        # TODO look for simple text
        pass
    channels = []
    for i in json:
        resource = (i['snippet']['resourceId'])
        if resource['kind'] == 'youtube#channel':
            channels.append(resource['channelId'])
    return channels
