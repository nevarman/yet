from yet.ui.window import Window
from yet.yt.channel import Subscriptions
from yet.config import config
from yet.config.videoscache import VideosCache


def main():
    try:
        channel_ids = config.get_channel_ids()
    except FileNotFoundError:
        print("Using default channel...")
        channel_ids = ["UCLA_DiR1FfKNvjuUpBHmylQ"]

    try:
        yet_config = config.YetConfig()
    except config.YetConfigException:
        return

    videos_cache = VideosCache(yet_config.get_section("common").getint("clean_cache", fallback=0))
    window = Window(None, yetconfig=yet_config, videoscache=videos_cache)
    Subscriptions(channel_ids, window.update_model)
    window.run()


if __name__ == '__main__':
    main()
