from ui.window import Window
from yt.channel import Subsriptions
from config import config


def main():
    subs = Subsriptions(config.get_channel_ids())
    window = Window(subs)
    window.run()


if __name__ == '__main__':
    main()
