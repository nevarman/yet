from ui.window import Window
from yt.channel import Subsriptions
from config import config
from config.videoscache import VideosCache


def main():
    try:
        channel_ids = config.get_channel_ids()
    except FileNotFoundError:
        return

    try:
        yetconfig = config.YetConfig()
    except config.YetConfigException:
        return

    videoscache = VideosCache(yetconfig.get_section("common").getint("clean_cache", fallback=0))
    window = Window(None, yetconfig=yetconfig, videoscache=videoscache)
    Subsriptions(channel_ids, window.update_model)
    window.run()


if __name__ == '__main__':
    main()
