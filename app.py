import config
from window import Window
from channel import Subsriptions


def main():
    subs = Subsriptions()
    window = Window(subs)
    window.run()

if __name__ == '__main__':
    main()