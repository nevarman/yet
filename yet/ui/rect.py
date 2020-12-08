

class Rect():
    def __init__(self, *args, **kwargs):
        rect = kwargs.get('rect')
        if rect:
            self.w = rect.w
            self.h = rect.h
            self.x = rect.x
            self.y = rect.y
        else:
            self.w = args[0]
            self.h = args[1]
            self.x = args[2]
            self.y = args[3]
