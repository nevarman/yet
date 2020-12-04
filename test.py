from __future__ import unicode_literals
import youtube_dl
from ytdlwrapper import YtdlWrapper

class MyLogger(object):
    def debug(self, msg):
        print(msg)
        pass

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if(d['status'] == 'downloading'):
        perct = d['downloaded_bytes'] / d['total_bytes']
        print(perct)
    if(d['status'] == 'exists'):
        print("YES")
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])
# ytdl = YtdlWrapper(my_hook)
# ytdl.start_t(('https://www.youtube.com/watch?v=przVUdwnm10'))

from channel import Subsriptions

s = Subsriptions()
