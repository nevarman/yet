from .widget import Widget
import curses
import textwrap


class InfoBar(Widget):
    ''' Info bar widget '''

    def __init__(self, window, content, header, rect, box=True):
        super().__init__(window, content, header, rect, box)
        self.info_text = "Welcome to yet! Select a video to download. Press Q to exit."
        self.progress = 1.0

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
            self.subwindow.attron(curses.color_pair(3))
            self.subwindow.addstr(0, 1, text[0:done])
            self.subwindow.attroff(curses.color_pair(3))

            self.subwindow.attron(curses.color_pair(4))
            self.subwindow.addstr(0, 1 + done, text[done:length])
            self.subwindow.attroff(curses.color_pair(4))
        except curses.error:
            pass

        self.subwindow.refresh()
