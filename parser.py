# -*- coding: utf-8 -*-
from command import *
import os
import re
import time
import utils
import recoder
import win32gui
from dataDef import *

DISPLAY_WIDTH = 480.0

class ParserBase(object):
    def __init__(self):
        pass
    
    def getScript(self, script):
        pass
    
    def parser(self):
        pass
    
    
class SimpleParser(ParserBase):
    
    def __init__(self):
        self.macro = MacroCommand()
        self.script = []
    
    def getScript(self, script):
        
        if os.path.exists(script):
            try:
                f = open(script,'r')
                self.script = f.readlines()
            except Exception,e:
                print e
            finally:
                if (f):
                    f.close()
            
    def parser(self):
        
        click = re.compile("I tap on screen (\d+) from the left and (\d+) from the top")
        wait = re.compile("I wait (\d+\.?\d*) seconds")
        flick = re.compile("I flick from \((\d+),(\d+)\) to \((\d+),(\d+)\)")
        back = re.compile("I go back")
        snapshot = re.compile("take a picture")
        
        flickUpTimes = re.compile("I flick up (\d+) times")
        
        num = re.compile("(\d+)")
        
        for line in self.script:
            line = line.strip()
            if(click.match(line)):
                list = num.findall(line)
                tempCommand = ClickCommand(Point(list[0],list[1]))
                self.macro.Add(tempCommand)
            elif(wait.match(line)):
                list = num.findall(line)
                if (list[0] < 1.5):
                    list[0] = 1.5
                    # 。。。。。
                tempCommand = WaitCommand(float(list[0])+0.5)
                self.macro.Add(tempCommand)
            elif(flick.match(line)):
                list = num.findall(line)
                tempCommand = FlickCommand(Point(list[0],list[1]),Point(list[2],list[3]))
                self.macro.Add(tempCommand)
            elif(back.match(line)):
                tempCommand = BackCommand()
                self.macro.Add(tempCommand)
            elif(snapshot.match(line)):
                tempCommand = SnapShotCommand()
                self.macro.Add(tempCommand)
            elif(flickUpTimes.match(line)):
                times = num.findall(line)
                for i in range(0,int(times[0])):
                    tempCommand = FlickCommand(Point(97,400),Point(97,261))
                    self.macro.Add(tempCommand)
                
    def run(self):
        self.macro.Execute()
        
    def _getEmuPositon(self):
    
        pwin=win32gui.FindWindow('XDE_LCDWindow',None)
        rect = win32gui.GetWindowRect(pwin)
        return rect    
        
    def _transformPosition(self,point):
        
        offset = self._getEmuPositon()
        scaleRatio = DISPLAY_WIDTH/(offset[2] - offset[0])
        point.x = int(point.x/scaleRatio + offset[0])
        point.y = int(point.y/scaleRatio + offset[1])
        return point        
            
if __name__ == "__main__":
    
    import logging
    
    if not os.path.exists('./result'):
        print  "not result folder"
        os.mkdir('./result')
    
    if os.path.exists('./result'):
        locationStr = './result' + '/' + time.strftime('%m%d_%H%M%S',time.localtime(time.time()))
        os.mkdir(locationStr)
        
        recoder.FOLDER = locationStr
        recoder.BEGGINTIME = time.time()

        file = "script.txt"
        parser = SimpleParser()
        parser.getScript(file)
        parser.parser()
        parser.run()
