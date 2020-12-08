from .widget import Widget, Focusable
import curses
import textwrap


class ScrollableWidget(Widget, Focusable):
    ''' Scrollable widget class'''
    UP = -1
    DOWN = 1

    def __init__(self, window, content, header, rect, box=True):
        super().__init__(
            window, content, header, rect, box)
        Focusable.__init__(self)
        self.top = 0
        self.bottom = len(self.content)
        self.max_lines = self.rect.h - 3
        self.current = 0
        self.selectcallback = None
        self.selected_color = curses.color_pair(2)

    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""

        if not self.is_focused:
            return

        current_index = self.get_current_index()
        # next cursor position after scrolling
        next_line = self.current + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        elif (direction == self.DOWN) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom):
            self.top += direction
        # Scroll up
        # current cursor position or top position is greater than 0
        elif (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
        # Scroll down
        # next cursor position is above max lines, and absolute position of next cursor could not touch the bottom
        elif (direction == self.DOWN) and (next_line < self.max_lines) and (self.top + next_line < self.bottom):
            self.current = next_line

        # Send index
        if(current_index != self.get_current_index() and self.selectcallback):
            self.selectcallback(self.get_current_index())

        self.display()

    def get_current_index(self):
        return self.current + self.top

    def get_current_index_item(self):
        return self.content[self.current + self.top]

    def update_content(self, content):
        super(ScrollableWidget, self).update_content(content)
        self.current = 0
        self.bottom = len(self.content)

    def set_listener(self, listener):
        self.selectcallback = listener

    def set_focused(self, focused):
        if focused == self.is_focused:
            return
        super().set_focused(focused)
        if self.selectcallback is not None:
            self.selectcallback(self.get_current_index())
        self.display()

    def resize(self, rect):
        super().resize(rect)
        self.max_lines = self.rect.h - 3

    def _draw_items(self):
        """Display the scrollable content on window"""
        # header
        start_y = self.draw_header()

        # draw items
        for index, item in enumerate(self.content[self.top:self.top + self.max_lines]):
            # Highlight the current cursor line
            color = self.selected_color if index == self.current and self.is_focused else self.color
            short_text = textwrap.shorten(str(item), self.rect.w - 4)
            # until the end of line
            short_text += " " * (self.rect.w - 2 - len(short_text))
            self.subwindow.addstr(
                index + start_y,
                1,
                short_text,
                color)