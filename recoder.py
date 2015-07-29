# -*- coding: utf-8 -*-
TOUCH = r'touch'
FLICK = r'flick'
DISPLAY_WIDTH = 480.0
DISPLAY_HEIGHT = 800.0
FOLDER = ''
BEGGINTIME = 0.0

class POINT():
    def __init__(self, x,y):
        self.x = x
        self.y = y

#touch x,y
#flick x1,y1-x2,y2
#comments: #
#times 50*flick x1,y1-x2,y2
#sleep 0.5