from __future__ import unicode_literals
import youtube_dl
from yet.config import config
import threading
from pathlib import Path


class MyLogger(object):
    # TODO add file logger
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class YtdlWrapper():

    def __init__(self, hook, ytconfig):
        self.hook = hook
        self.config = ytconfig
        self.output_path = self.config.get('output_path', fallback=config.get_videos_dir())
        self.extension = self.config.get('video_format', fallback='mp4')
        self.ydl_opts = {
            'format': 'bestvideo[ext={ex}]+bestaudio[ext=m4a]/best[ext={ex}]/best'.format(ex=self.extension),
            'outtmpl': self.output_path + '%(title)s.%(ext)s',
            # 'postprocessors': [{
            #     'key': 'FFmpegExtractAudio',
            #     'preferredcodec': 'mp3',
            #     'preferredquality': '192',
            # }],
            'logger': MyLogger(),
            'progress_hooks': [self.hook]}

    def get(self, url_list):
        thread = threading.Thread(target=self.start_t, args=(url_list,))
        thread.setDaemon(True)
        thread.start()

    def start_t(self, url_list: list):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            for u in url_list:
                info = ydl.extract_info(u, download=False)
                name = self.output_path + u'{title}.{ext}'.format(title=info['title'], ext=self.extension)
                if Path(name).is_file():
                    self.hook({'status': 'exists'})
                    url_list.remove(u)
            try:
                ydl.download(url_list)
            except Exception:
                self.hook({'status': 'error'})
                # TODO add logger
