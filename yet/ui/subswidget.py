from .scrollablewidget import ScrollableWidget, Focusable


class SubsWidget(ScrollableWidget, Focusable):

    def __init__(self, window, content, header, rect, config, videos_cache):
        super().__init__(
            window, content, header, rect, config)
        self.cache = videos_cache

    def update_content(self, content, scroll_to_zero=True):
        # show only active content
        c = [channel for channel in content if not self.cache.contains_all(
            [i.link for i in channel.entries])]
        super().update_content(c, scroll_to_zero)

    def set_focused(self, focus):
        if focus:
            self.update_content(self.content, False)
        super().set_focused(focus)
