from ui.window import Window
from yt.channel import Subsriptions
from config import config


def main():
    try:
        channel_ids = config.get_channel_ids()
    except FileNotFoundError:
        return

    try:
        yetconfig = config.YetConfig()
    except config.YetConfigException:
        return

    window = Window(None, yetconfig=yetconfig)
    Subsriptions(channel_ids, window.update_model)
    window.run()


if __name__ == '__main__':
    main()
