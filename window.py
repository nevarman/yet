import curses
import curses.textpad
import textwrap
from channel import Subsriptions
from ytdlwrapper import YtdlWrapper
from channel import Subsriptions
import webbrowser
from threading import Thread, Event


class Screen(object):
    UP = -1
    DOWN = 1
    CURRENT = -1

    def __init__(self, window, items, header='', width=0, begin_x=0, box=True):
        self.window = window
        self.height, self.width = self.window.getmaxyx()
        self.items = items
        self.max_lines = curses.LINES - 4
        self.top = 0
        self.bottom = len(self.items)
        self.current = 0
        self.selectcallback = None
        # header text
        self.header = header
        # calculate width
        self.width = max(max(len(ele) for ele in self.items),
                         len(self.header)) + 4 if width == 0 else width
        self.header = header + ' '*(self.width - len(header) - 4)
        # create sub window
        self.subwindow = self.window.subwin(
            self.height - 1, self.width, 0, begin_x)
        self.box = box
        self.is_current = False

    def set_window_params(self, width, height, x):
        self.width = max(max(len(ele) for ele in self.items),
                         len(self.header)) + 4 if width == 0 else width
        self.height = height
        # create sub window
        if self.subwindow:
            self.subwindow.clear()
        self.subwindow = self.window.subwin(self.height - 1, self.width, 0, x)

    def update_content(self, content):
        self.items = content
        self.CURRENT = -1
        self.current = 0
        self.bottom = len(self.items)
        self.subwindow.refresh()

    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""
        # next cursor position after scrolling
        next_line = self.current + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        if (direction == self.DOWN) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom):
            self.top += direction
            return
        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        # Scroll down
        # next cursor position is above max lines, and absolute position of next cursor could not touch the bottom
        if (direction == self.DOWN) and (next_line < self.max_lines) and (self.top + next_line < self.bottom):
            self.current = next_line
            return

    def display(self):
        """Display the items on window"""
        self.subwindow.erase()
        if self.box:
            self.subwindow.box()
        # header
        self.subwindow.addstr(
            1, 2, self.header[0:self.width-4], curses.color_pair(3))

        if self.items == None or len(self.items) == 0:
            return

        for idx, item in enumerate(self.items[self.top:self.top + self.max_lines]):
            # Highlight the current cursor line
            color = curses.color_pair(
                2) if idx == self.current and self.is_current else curses.color_pair(1)
            self.subwindow.addstr(
                idx+2, 2, textwrap.shorten(str(item), self.width - 5), color)

        self.subwindow.refresh()

        # Send index
        if(self.CURRENT != self.current + self.top and self.selectcallback):
            self.CURRENT = self.current + self.top
            self.selectcallback(self.current + self.top)

    def set_current(self, current=True):
        self.is_current = current

    def set_listener(self, listener):
        self.selectcallback = listener


class InfoScreen(Screen):

    def __init__(self, window, items, header='', width=0, begin_x=0, box=True):
        super(InfoScreen, self).__init__(
            window, items, header, width, begin_x, box)

    def display(self):
        """Display the items on window"""
        self.subwindow.erase()

        if self.box:
            self.subwindow.box()

        self.subwindow.addstr(
            1, 2, self.header[0:self.width-4], curses.color_pair(3))

        if self.items == None or len(self.items) == 0:
            return

        for idx, item in enumerate(self.items[self.top:self.top + self.max_lines - 2]):
            # Highlight the current cursor line
            color = curses.color_pair(
                2) if idx == self.current and self.is_current else curses.color_pair(1)
            t = textwrap.shorten(str(item), self.width)
            self.subwindow.addstr(idx+2, 2, t, color)

        self.subwindow.refresh()

        # Send index
        if(self.CURRENT != self.current + self.top and self.selectcallback):
            self.CURRENT = self.current + self.top
            self.selectcallback(self.current + self.top)

    def update_content(self, content):
        cache = content.copy()
        for i in range(len(content)):
            content.insert(i*2, ' ')
        cache = content.copy()
        for i in range(len(cache)):
            item = cache[i]
            index = cache.index(item)
            subline = textwrap.wrap(str(item), self.width - 10)
            if(len(subline) > 1):
                content.pop(index)
                content[index:index] = subline

        self.items = content
        self.bottom = len(self.items)
        self.subwindow.refresh()


class Window(object):

    def __init__(self, model: Subsriptions):

        self.video_index = 0
        self.download = False
        self.console_width = 0
        self.console_height = 0
        self.info_text = "Select a video to download..."
        self.progress = 1.0

        self.window = self.init_curses()
        self.window.nodelay(False)
        self.model = model
        # create screens
        self.screens = self.init_screens()

    def init_curses(self):
        window = curses.initscr()
        window.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        return window

    def init_screens(self):
        screens = []
        self.console_height, self.console_width = self.window.getmaxyx()
        self.infobar = self.window.subwin(
            1, self.console_width, self.console_height-1, 0)
        # Subs window
        self.subs_screen = Screen(
            self.window, self.model.subsriptions, 'Subscriptions')
        screens.append(self.subs_screen)
        self.subs_screen.set_listener(self._on_select_subs)
        # Videos
        w = (int)((self.console_width - self.subs_screen.width)/2)
        self.videos_screen = Screen(
            self.window, [], 'Videos', w, self.subs_screen.width)
        screens.append(self.videos_screen)
        self.videos_screen.set_listener(self._on_select_video)
        # Info
        self.info_screen = InfoScreen(
            self.window, [], 'Info', w, self.subs_screen.width + w)
        screens.append(self.info_screen)

        # current screen subs
        self.screen_index = 0
        self.current_screen = self.subs_screen
        self.current_screen.set_current()
        return screens

    def run(self):
        """Continue running the TUI until get interrupted"""
        try:
            self._main_loop()
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()

    def _main_loop(self):
        """Waiting an input and run a proper method according to type of input"""
        while True:

            # Recalculate
            height, width = self.window.getmaxyx()
            if width != self.console_width or height != self.console_height:
                w = (int)((width - self.subs_screen.width)/2)
                self.subs_screen.set_window_params(
                    self.subs_screen.width, self.console_height, 0)
                self.videos_screen.set_window_params(
                    w, self.console_height, self.subs_screen.width)
                self.info_screen.set_window_params(
                    w, self.console_height, self.subs_screen.width + w)
                self.info_screen.update_content(self.info_screen.items)
                self.console_width = width
                self.console_height = height
                self.infobar = self.window.subwin(
                    1, self.console_width, self.console_height-1, 0)

            # ## Display
            self.redraw()

            # input
            ch = self.window.getch()
            if ch == curses.KEY_UP:
                self.current_screen.scroll(-1)
            elif ch == curses.KEY_DOWN:
                self.current_screen.scroll(1)
            elif ch == curses.KEY_LEFT:
                self.screen_index -= 1
                if self.screen_index < 0:
                    self.screen_index = len(self.screens) - 1
                self._set_next_screen(self.screen_index)
            elif ch == curses.KEY_RIGHT:
                self.screen_index += 1
                self.screen_index %= len(self.screens)
                self._set_next_screen(self.screen_index)
            elif ch == curses.ascii.ESC or ch == ord('q'):
                break
            elif ch == ord('o') and self._can_open_video():
                webbrowser.open_new_tab(
                    self.videos_screen.items[self.video_index].link)
            elif ch == ord('n') and self._can_open_video():
                self.yt_download(
                    self.videos_screen.items[self.video_index].link)

    def redraw(self):
        ''' Redraws screens and bar '''

        for i in self.screens:
            i.display()
        self._display_bar()
        self.window.refresh()

    def _can_open_video(self):
        return self.current_screen == self.info_screen or self.current_screen == self.videos_screen

    def _display_bar(self):
        # Render status bar
        self.infobar.clear()
        self.infobar.attron(curses.color_pair(3))
        text = textwrap.shorten(self.info_text, self.console_width-4)
        self.infobar.addstr(0, 1, text)
        bar = (int)((float)(self.console_width - len(text) - 2) * self.progress)
        self.infobar.addstr(0, len(text) + 1, ' ' * bar)
        self.infobar.attroff(curses.color_pair(3))
        self.infobar.refresh()

    def _set_next_screen(self, index):
        self.current_screen.set_current(False)
        self.current_screen = self.screens[index]
        self.current_screen.set_current()

    def _on_select_subs(self, index):
        items = self.model.get_channel(index).feed.entries
        self.videos_screen.update_content(items)
        pass

    def _on_select_video(self, index):
        self.info_text = "Press N to download - O to open in browser - Q to exit"
        self.video_index = index
        items = self.videos_screen.items[index].get_extended_info().split(
            '\n\t')
        self.info_screen.update_content(items)
        pass

    def yt_download(self, url):
        if self.download:
            return
        try:
            ytdl = YtdlWrapper(self._yt_hook)
            ytdl.get(str(url))
        except Exception:
            curses.endwin()

    def _yt_hook(self, d):
        ''' Callback function for ytdl'''

        if d['status'] == 'downloading':
            self.download = True
            perct = d['downloaded_bytes'] / d['total_bytes']
            self.progress = perct
            self.info_text = "Downloading..."
        elif d['status'] == 'error':
            self.info_text = "Some error occured..."
            self.download = False
        elif d['status'] == 'finished':
            file = d['filename']
            self.info_text = "Done...%s" % file
            self.download = False
        elif d['status'] == 'exists':
            self.info_text = "Already in library."
        self._display_bar()
