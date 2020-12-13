import curses
import curses.textpad
import textwrap


class Focusable():

    def __init__(self):
        self.is_focused = False

    def set_focused(self, focus):
        self.is_focused = focus


class Widget(object):
    _TEXT_WRAP_PADDING = 4

    def __init__(self, window, content, header, rect, config):
        self.window = window
        self.rect = rect
        self.content = content
        # header text
        self.header = header
        # create sub window
        self.subwindow = self.window.subwin(
            self.rect.h, self.rect.w, self.rect.y, self.rect.x)
        self.box = config.getboolean('box', fallback=False)
        self.color = curses.color_pair(config.getint('fg', fallback=11))
        self.header_color = curses.color_pair(
            config.getint('headerbg', fallback=12)) | curses.A_REVERSE | curses.A_BOLD | curses.A_UNDERLINE

    def update_content(self, content):
        self.content = content
        self.display()

    def resize(self, rect):
        ''' Resizes the current widget
        If widget doesn't fit window tries moving it
        '''
        self.subwindow.clear()
        self.subwindow.refresh()

        if rect.w != self.rect.w or rect.h != self.rect.h:
            try:
                self.subwindow.mvwin(rect.y, rect.x)
                self.subwindow.resize(rect.h, rect.w)
            except curses.error:
                # Not enough space for resizing...
                try:
                    self.subwindow.mvderwin(rect.y, rect.x)
                    self.subwindow.resize(rect.h, rect.w)
                except curses.error:
                    pass
                    # raise ValueError("Resizing Failed!")
        else:
            try:
                self.subwindow.mvwin(rect.y, rect.x)
            except curses.error:
                pass
        self.rect = rect
        self.subwindow.refresh()

    def redraw(self):
        ''' Erases all text and re displays '''
        self.subwindow.clear()
        self.display()

    def display(self):
        """ Display the content on window by erasing and adding the text again"""
        self.subwindow.erase()
        if self.content is None or len(self.content) == 0:
            return
        self._draw_items()
        self.subwindow.refresh()

    def draw_header(self):
        has_header = len(self.header) > 0
        if has_header:
            t = textwrap.shorten(self.header, self.rect.w - 2)
            lenght = max(0, (self.rect.w - 2 - len(t)))
            text = t + ' ' * lenght
            self.subwindow.addstr(1, 1, text, self.header_color)
        x = 2 if has_header else 1
        if self.box:
            try:
                self.subwindow.border()
                self.subwindow.refresh()
            except curses.error:
                pass
        return x

    def _draw_items(self):
        ''' Draws content and header '''
        # header
        start_x = self.draw_header()
        # draw items
        for index, item in enumerate(self.content[0:self.rect.h]):
            self.subwindow.addstr(
                index + start_x,
                2,
                textwrap.shorten(str(item), self.rect.w - self._TEXT_WRAP_PADDING),
                self.color)
