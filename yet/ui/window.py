from .infobar import InfoBar
from .rect import Rect
from .scrollablewidget import ScrollableWidget
from .videoswidget import VideosWidget
from .infowidget import InfoWidget
from .widget import Focusable
# from yet.yt.channel import Subsriptions
from yt.ytdlwrapper import YtdlWrapper
import curses
import curses.textpad


class Window(object):

    def __init__(self, model=None, yetconfig=None):

        self.yetconfig = yetconfig
        self.video_index = 0
        self.download = False
        self.subs_widget = None
        self.videos_screen = None
        self.info_screen = None
        self.infobar = None
        self.widget_placement = [0.2, 0.4, 0.4]

        self.window = self.init_curses()
        self.model = model
        # create widgets
        self.widgets = self.init_widgets()

    def init_curses(self):
        window = curses.initscr()
        window.keypad(True)
        curses.noecho()
        curses.cbreak()
        window.nodelay(False)
        # curses.halfdelay(20)
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        self.console_height, self.console_width = window.getmaxyx()
        return window

    def init_widgets(self):
        widgets = []
        # Subs window
        w = round(self.console_width * self.widget_placement[0])
        rect = Rect(w, self.console_height - 1, 0, 0)
        self.subs_widget = ScrollableWidget(self.window,
                                            None,
                                            'Subscriptions', rect,
                                            self.yetconfig.get_section(self.yetconfig.CONFIG_KEY_WIDGET_SUBS))
        widgets.append(self.subs_widget)
        self.subs_widget.set_listener(self._on_select_subs)

        # Videos
        w = round(self.console_width * self.widget_placement[1])
        rect2 = Rect(w, self.console_height - 1, rect.w, 0)
        self.videos_widget = VideosWidget(self.window,
                                          [],
                                          'Videos', rect2,
                                          self.yetconfig.get_section(self.yetconfig.CONFIG_KEY_WIDGET_VIDEO))
        self.videos_widget.set_listener(self._on_select_video)
        widgets.append(self.videos_widget)

        # Info
        w = self.console_width - rect.w - rect2.w
        rect3 = Rect(w, self.console_height - 1, rect2.x + rect2.w, 0)
        self.info_widget = InfoWidget(self.window,
                                      [],
                                      'Info', rect3,
                                      self.yetconfig.get_section(self.yetconfig.CONFIG_KEY_WIDGET_INFO))
        widgets.append(self.info_widget)

        recti = Rect(self.console_width, 1, 0, self.console_height - 1)
        self.infobar = InfoBar(self.window, None, None, recti,
                               self.yetconfig.get_section(self.yetconfig.CONFIG_KEY_WIDGET_BAR))
        widgets.append(self.infobar)

        # current screen subs
        self.screen_index = 0
        for i in widgets:
            i.display()

        return widgets

    def update_model(self, i, total, model):
        self.model = model
        self.subs_widget.update_content(model)
        self.infobar.set_info_text(
            "Fetching feed %d/%d" % (i, total), float(i) / total)
        if i == total:
            self.infobar.set_info_text(
                "Welcome to yet! Select a video to download. Press Q to exit.")
            # set focused
            self.subs_widget.set_focused(True)

    def destroy(self):
        self.window.clear()
        self.window.refresh()
        del self.window
        curses.endwin()

    def run(self):
        """Continue running the TUI until get interrupted"""
        try:
            self._main_loop()
        except KeyboardInterrupt:
            pass
        finally:
            self.destroy()

    def _main_loop(self):
        """Waiting an input
        and run a proper method according to type of input"""
        while True:
            # input
            ch = self.window.getch()
            if ch in self.yetconfig.get_keybinding("exit"):  # EXIT
                break
            elif ch in self.yetconfig.get_keybinding("up"):
                self._scroll_widget(-1)
            elif ch in self.yetconfig.get_keybinding("down"):
                self._scroll_widget(1)
            elif ch in self.yetconfig.get_keybinding("left"):
                self._focus_next_widget(-1)
            elif ch in self.yetconfig.get_keybinding("right"):
                self._focus_next_widget(1)
            elif ch == curses.KEY_RESIZE:
                self.resize()
            elif ch in self.yetconfig.get_keybinding("selectvideo"):
                self.videos_widget.select_video()
            elif ch in self.yetconfig.get_keybinding("open"):
                self.videos_widget.open_in_browser()
            elif ch in self.yetconfig.get_keybinding("download"):
                self.yt_download()

    def resize(self):
        # Recalculate
        height, width = self.window.getmaxyx()
        if width != self.console_width or height != self.console_height:
            self.window.erase()
            curses.resizeterm(height, width)
            self.window.refresh()
            # set new values
            self.console_width = width
            self.console_height = height

            # subs widget
            rect = Rect(rect=self.subs_widget.rect)
            rect.w = round(self.console_width * self.widget_placement[0])
            rect.h = self.console_height - 1
            self.subs_widget.resize(rect)

            # video
            rect2 = Rect(rect=self.videos_widget.rect)
            rect2.w = round(self.console_width * self.widget_placement[1])
            rect2.h = self.console_height - 1
            rect2.x = rect.w
            self.videos_widget.resize(rect2)

            # info
            rect3 = Rect(rect=self.info_widget.rect)
            rect3.w = self.console_width - rect.w - rect2.w
            rect3.h = self.console_height - 1
            rect3.x = rect2.w + rect2.x
            self.info_widget.resize(rect3)

            # info bar down, h is always 1 , x is always 0
            rect4 = Rect(rect=self.infobar.rect)
            rect4.w = self.console_width
            rect4.y = self.console_height - 1
            self.infobar.resize(rect4)

            for i in self.widgets:
                i.display()

    def _scroll_widget(self, dir):
        w = self.widgets[self.screen_index]
        if isinstance(w, ScrollableWidget):
            w.scroll(dir)

    def _focus_next_widget(self, index):
        widgets = [i for i in self.widgets if isinstance(i, Focusable)]
        w = widgets[self.screen_index]
        if isinstance(w, Focusable):
            w.set_focused(False)
        # set index
        self.screen_index += index
        if self.screen_index < 0:
            self.screen_index = 0
        else:
            self.screen_index %= len(widgets)
        widgets[self.screen_index].set_focused(True)

    def _on_select_subs(self, index):
        # channel feed entries for videos
        channel = self.subs_widget.get_current_index_item()
        if channel is None:
            return
        self.videos_widget.update_content(channel.feed.entries)

    def _on_select_video(self, index):
        items = self.videos_widget.get_current_index_item().get_extended_info()
        self.info_widget.update_content(items)
        if not self.download:
            self.infobar.set_info_text(
                "Press D to download - O to open in browser - Space to add to the basket.")

    def yt_download(self):
        if self.download:
            return
        urls = self.videos_widget.get_urls_to_download()
        if urls is None:
            self.infobar.set_info_text("Select video/s to download...")
            return
        try:
            ytdl = YtdlWrapper(self._yt_hook)
            ytdl.get(urls)
            self.infobar.set_info_text("Checking library.")
        except Exception as e:
            # curses.endwin()
            print(str(e))
        finally:
            self.videos_widget.clear_selected_videos()

    def _yt_hook(self, d):
        ''' Callback function for ytdl'''

        if d['status'] == 'downloading':
            self.download = True
            perct = d['downloaded_bytes'] / d['total_bytes']
            self.infobar.set_info_text("Downloading ... Total bytes:%s Speed:%s ETA:%s" %
                                       (d['_total_bytes_str'],
                                        d['_speed_str'], d['_eta_str']),
                                       perct)
        elif d['status'] == 'error':
            self.download = False
            self.infobar.set_info_text("An error occured...")
        elif d['status'] == 'finished':
            self.download = False
            file = d['filename']
            self.infobar.set_info_text("Done...%s" % file)
        elif d['status'] == 'exists':
            self.infobar.set_info_text("Already in library.")
