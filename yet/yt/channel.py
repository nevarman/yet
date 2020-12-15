
import urllib.request as urllib2
import xmltodict


class Entry():

    def __init__(self, entry):
        self.title = entry['title']
        self.link = entry['link']['@href']
        self.published = entry['published'].replace("T", " / ")
        self.updated = entry['updated'].replace("T", " / ")
        self.thumbnail = entry['media:group']['media:thumbnail']['@url']
        self.description = entry['media:group']['media:description'].replace(
            '\n', '')
        self.views = entry['media:group']['media:community']['media:statistics']['@views']
        self.read = False

    def __str__(self):
        return self.title

    def get_extended_info(self) -> list:
        return [self.title, self.description, "Published:%s" % (self.published),
                "Updated:%s" % (self.updated), "Views:%s" % (self.views)]


class Feed():

    def __init__(self, data):
        self.data = data
        self.author = self.data['feed']['author']['name']
        self.url = self.data['feed']['author']['uri']
        # entries
        entries = []
        for i in self.data['feed']['entry']:
            entry = Entry(i)
            # TODO check cache read
            entries.append(entry)
        self.entries = entries


class Channel():

    def __init__(self, id):
        self.channel_id = id
        self.feed = self.load_feed()
        self.url = self.feed.url
        self.author = self.feed.author
        self.entries = self.feed.entries

    def load_feed(self):
        uri = 'https://www.youtube.com/feeds/videos.xml?channel_id=%s' % self.channel_id
        with urllib2.urlopen(uri) as response:
            data = response.read()
            data = xmltodict.parse(data)
            return Feed(data)

    def __str__(self):
        return self.author

    def __len__(self):
        return len(self.author)


class Subsriptions():

    def __init__(self, channel_ids: list, callback=None):
        self.channel_ids = channel_ids
        self.subsriptions = []
        self.callback = callback
        for i in range(len(channel_ids)):
            # print("%i/%i - Fetching feed id:%s" %
            #       (i, len(channel_ids), channel_ids[i]), end="\r")
            self.subsriptions.append(Channel(channel_ids[i]))
            # send callback
            if self.callback is not None:
                self.callback(i + 1, len(channel_ids), self.get_sorted_subsriptions())

    def get_sorted_subsriptions(self):
        return sorted(
            self.subsriptions, key=lambda Channel: str(Channel))

    def get_channel(self, id) -> Channel:
        if id > len(self.subsriptions) - 1 or id < 0:
            raise IndexError('id should be in range of subs list')
        return self.subsriptions[id]
