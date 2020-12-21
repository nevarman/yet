from yet.ui.window import Window
from yet.yt.channel import Subsriptions
from yet.config import config
from yet.config.videoscache import VideosCache


def main():
    try:
        channel_ids = config.get_channel_ids()
    except FileNotFoundError:
        print("Using default channel...")
        channel_ids = ["UCLA_DiR1FfKNvjuUpBHmylQ"]

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
