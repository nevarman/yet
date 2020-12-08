from .scrollablewidget import ScrollableWidget
import textwrap


class InfoWidget(ScrollableWidget):

    def __init__(self, window, content, header, rect, box=True):
        super().__init__(window, content, header, rect, box)

    def update_content(self, content):
        cache = content.copy()
        for i in range(len(content)):
            content.insert(i * 2, ' ')
        cache = content.copy()
        for i in range(len(cache)):
            item = cache[i]
            index = cache.index(item)
            subline = textwrap.wrap(str(item), self.rect.w - 10)
            if(len(subline) > 1):
                content.pop(index)
                content[index:index] = subline

        self.content = content
        self.bottom = len(self.content)
        self.display()
