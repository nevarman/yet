
import urllib.request as urllib2
import xmltodict


class Entry:

    def __init__(self, entry):
        self.title = entry['title']
        self.link = entry['link']['@href']
        self.published = entry['published'].replace("T", " / ") if entry['published'] is not None else "-"
        self.updated = entry['updated'].replace("T", " / ") if entry['updated'] is not None else "-"
        self.thumbnail = entry['media:group']['media:thumbnail']['@url']
        self.description = entry['media:group']['media:description'].replace(
                '\n', '') if entry['media:group']['media:description'] is not None else "No information..."
        self.views = entry['media:group']['media:community']['media:statistics']['@views']
        self.read = False

    def __str__(self):
        return self.title

    def get_extended_info(self) -> list:
        return [self.title, self.description, f"Published:{self.published}",
                f"Updated:{self.updated}", f"Views:{self.views}"]


class Feed:

    def __init__(self, data: dict):
        self.data = data
        self.entries = []
        feed = self.data.get('feed')
        if feed is None:
            return
        # infos
        self.author = feed['author']['name']
        self.url = feed['author']['uri']
        # entries
        e = feed.get('entry')
        if e is None:
            return
        for i in e:
            entry = Entry(i)
            # TODO check cache read
            self.entries.append(entry)


class Channel:

    def __init__(self, c_id):
        self.channel_id = c_id
        self.feed = self.load_feed()
        self.url = self.feed.url
        self.author = self.feed.author
        self.entries = self.feed.entries

    def load_feed(self):
        uri = f'https://www.youtube.com/feeds/videos.xml?channel_id={self.channel_id}'
        with urllib2.urlopen(uri) as response:
            data = response.read()
            data = xmltodict.parse(data)
            return Feed(data)

    def __str__(self):
        return self.author

    def __len__(self):
        return len(self.author)


class Subscriptions:

    def __init__(self, channel_ids: list, callback=None):
        self.channel_ids = channel_ids
        self.subscriptions = []
        self.callback = callback
        for i in range(len(channel_ids)):
            channel = Channel(channel_ids[i])
            if len(channel.entries) > 0:
                self.subscriptions.append(channel)
            # send callback
            if self.callback is not None:
                self.callback(i + 1, len(channel_ids), self.get_sorted_subscriptions())

    def get_sorted_subscriptions(self):
        return sorted(
            self.subscriptions, key=lambda ch: str(ch))

    def get_channel(self, c_id) -> Channel:
        if c_id > len(self.subscriptions) - 1 or c_id < 0:
            raise IndexError('id should be in range of subs list')
        return self.subscriptions[c_id]
