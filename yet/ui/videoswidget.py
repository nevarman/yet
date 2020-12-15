from .scrollablewidget import ScrollableWidget
import textwrap
import curses


class VideosWidget(ScrollableWidget):

    def __init__(self, window, content, header, rect, box=True):
        super().__init__(window, content, header, rect, box)
        self.selected_videos = []

    def select_video(self):
        if not self.is_focused:
            return
        video = self.get_current_index_item()
        if video in self.selected_videos:
            self.selected_videos.remove(video)
        else:
            self.selected_videos.append(video)
        self.display()

    def clear_selected_videos(self):
        self.selected_videos = []
        self.display

    def get_urls_to_download(self):
        if len(self.selected_videos) > 0:
            return [str(feed.link) for feed in self.selected_videos]
        elif self.is_focused:
            return [str(self.get_current_index_item().link)]

        return None

    def _draw_items(self):
        # header
        start_y = self.draw_header()

        # draw items
        for index, item in enumerate(self.content[self.top:self.top + self.max_lines]):
            # Highlight the current cursor line
            color = self.selected_color if index == self.current else self.color
            item_text = '* ' + \
                str(item) if item in self.selected_videos else str(item)
            if item in self.selected_videos:
                color = color | curses.A_BOLD
            if item.read:
                color = color | curses.A_DIM
            short_text = textwrap.shorten(item_text, self.rect.w - self._TEXT_WRAP_PADDING)
            # until the end of line
            short_text += " " * (self.rect.w - 2 - len(short_text))
            self.subwindow.addstr(
                index + start_y,
                1,
                short_text,
                color)
