from .widget import Widget
import curses
import textwrap


class InfoBar(Widget):
    ''' Info bar widget '''

    def __init__(self, window, content, header, rect, config):
        super().__init__(window, content, header, rect, config)
        self.info_text = ""
        self.progress = 1.0
        self.color = curses.color_pair(config.getint('fg', fallback=4)) | curses.A_REVERSE
        self.colorprogress = curses.color_pair(config.getint('progressbg', fallback=0)) | curses.A_REVERSE

    def set_info_text(self, text, progress=1.0):
        self.info_text = text
        self.progress = progress
        self.display()

    def display(self):
        self.subwindow.erase()
        text = textwrap.shorten(self.info_text, self.rect.w - 2)
        text += ' ' * (self.rect.w - len(text) - 2)
        try:
            length = len(text)
            done = int((length * self.progress))
            self.subwindow.addstr(0, 1, text[0:done], self.color)
            self.subwindow.addstr(0, 1 + done, text[done:length], self.colorprogress)
        except curses.error:
            # TODO log
            pass

        self.subwindow.refresh()
