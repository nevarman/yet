from .scrollablewidget import ScrollableWidget


class InfoWidget(ScrollableWidget):

    def __init__(self, window, content, header, rect, config):
        super().__init__(window, content, header, rect, config)

    def update_content(self, content):
        new_content = []
        for i in content:
            new_content.extend(self._wrap(
                i, self.rect.w - self._TEXT_WRAP_PADDING))
            new_content.append('')
        self.content = new_content
        self.bottom = len(self.content)
        self.current = 0
        self.display()

    def _wrap(self, s, w):
        return [s[i:i + w].strip() for i in range(0, len(s), w)]
