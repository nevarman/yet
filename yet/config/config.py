import os
import json
import configparser
import ast
from pathlib import Path

CONFIG_PATH = os.path.join(Path.home(), ".config", "yet")
SUBS_PATH = os.path.join(CONFIG_PATH, "subscriptions.json")
CONFIG_FILE_PATH = os.path.join(CONFIG_PATH, "yet.conf")
CONFIG_FALLBACK_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "yet.conf")


def get_videos_dir():
    return os.path.join(Path.home(), "Videos/")


def _get_subs_json():
    """ Reads subscriptions json file """
    try:
        with open(SUBS_PATH) as f:
            return json.load(f)
    except IOError:
        print("%s not found!" % SUBS_PATH)
        return None


def get_channel_ids() -> list:
    """ Returns channel ids from youtube export data """
    json = _get_subs_json()
    if json is None:
        # TODO look for simple text maybe
        raise FileNotFoundError
    channels = [i['snippet']['resourceId']['channelId']
                for i in json if i['snippet']['resourceId']['kind'] == 'youtube#channel']
    return channels


class YetConfigException(Exception):
    pass


class YetConfig(object):
    """
    Configuration for yet
    """

    CONFIG_KEY_COMMON = 'common'
    CONFIG_KEY_YT = 'youtube-dl'
    CONFIG_KEY_KEYBINDINGS = 'keybindings'
    CONFIG_KEY_WIDGET_SUBS = 'subswidget'
    CONFIG_KEY_WIDGET_VIDEO = 'videoswidget'
    CONFIG_KEY_WIDGET_INFO = 'infowidget'
    CONFIG_KEY_WIDGET_BAR = 'infobar'

    def __init__(self):
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read(CONFIG_FILE_PATH)
        if len(self.config.sections()) == 0:
            # check fallback config
            print("Can't find config file {home}. Using default {d}".format(
                home=CONFIG_FILE_PATH, d=CONFIG_FALLBACK_PATH))
            self.config.read(CONFIG_FALLBACK_PATH)
            if len(self.config.sections()) == 0:
                raise YetConfigException("Can't parse or locate config file.")

    def get_section(self, section_key) -> configparser.SectionProxy:
        """
        Returns section proxy, if key is not available raises YetConfigException
        """
        if not self.config.has_section(section_key):
            raise YetConfigException(
                "Config file doesn't contain section: {key}".format(key=section_key))
        return self.config[section_key]

    def get_keybinding(self, key) -> list:
        """
        Returns keybindings for a given key.

        >>> binding = get_keybinding("download")
        [100]
        """
        if not self.config.has_section(self.CONFIG_KEY_KEYBINDINGS):
            raise YetConfigException(
                "Config file doesn't contain section: {key}".format(key=self.CONFIG_KEY_KEYBINDINGS))

        section = self.config[self.CONFIG_KEY_KEYBINDINGS]
        keys = []
        for k in ast.literal_eval(section[key]):
            keys.append(k if type(k) is int else ord(k))
        return keys
