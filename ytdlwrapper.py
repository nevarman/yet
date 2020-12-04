from __future__ import unicode_literals
import youtube_dl
import config
import threading
from pathlib import Path


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class YtdlWrapper():

    def __init__(self, hook):
        self.hook = hook
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': config.get_videos_dir() + '%(title)s.%(ext)s',
            # 'postprocessors': [{
            #     'key': 'FFmpegExtractAudio',
            #     'preferredcodec': 'mp3',
            #     'preferredquality': '192',
            # }],
            'logger': MyLogger(),
            'progress_hooks': [self.hook]}

    
    def get(self, url):
        thread = threading.Thread(target=self.start_t, args=[url,])
        thread.setDaemon(True)
        thread.start()


    def start_t(self, url):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(url, download = False)
            name = config.get_videos_dir() + u'%s.mp4' % info['title']
            if Path(name).is_file():
                self.hook({'status':'exists'})
            else:
                ydl.download([url])
