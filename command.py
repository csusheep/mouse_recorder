# -*- coding: utf-8 -*-
import utils
import platformFilter

class CommandBase(object):
    def __init__(self):
        self.factory = platformFilter.engine.getFactory()
        self.engine = self.factory.MakeEngine()
        print self.engine
    def Execute(self):
        pass
    
    
class ClickCommand(CommandBase):
    def __init__(self,point):
        CommandBase.__init__(self)
        self.point = point
    
    def Execute(self):
        self.engine.click(self.point)
    
    
class FlickCommand(CommandBase):
    def __init__(self, start, end):
        CommandBase.__init__(self)
        self.start = start
        self.end = end
    
    def Execute(self):
        self.engine.flick(self.start, self.end)

    
class PressCommand(CommandBase):   
    def __init__(self, point, t):
        CommandBase.__init__(self)
        self.point = point
        self.time = t
        
    def Execute(self):
        self.engine.press(self.point, self.time)
    
    
class WaitCommand(CommandBase):
    
    def __init__(self, time):
        CommandBase.__init__(self)
        self.time = float(time)
    
    def Execute(self):
        self.engine.wait(self.time)
        
        
class SnapShotCommand(CommandBase):        
    def Execute(self):
        self.engine.snapShot()
    
class BackCommand(CommandBase):    
    def Execute(self):
        self.engine.back()
        
class MacroCommand(CommandBase):
    def __init__(self):
        CommandBase.__init__(self)
        self.commands = []
    
    def Add(self,CommandBase):
        self.commands.append(CommandBase)
        print "adding" , CommandBase
    
    def Remove(self,CommandBase):
        try:
            self.commands.remove(CommandBase)
        except:
            print "The %s is not in command queue!"
    
    def Execute(self):
        for command in self.commands:
            try:
                command.Execute()
            except Exception,e :
                print e, command


#self testing
if __name__ == '__main__':
    
    #click = ClickCommand(500, 226)    
    import os,time,recoder
    if not os.path.exists('./result'):
        print  "not result folder"
        os.mkdir('./result')
    
    if os.path.exists('./result'):
        locationStr = './result' + '/' + time.strftime('%m%d_%H%M%S',time.localtime(time.time()))
        os.mkdir(locationStr)
        
        recoder.FOLDER = locationStr
        
        print locationStr
    #click.Execute()
    import dataDef
    A = dataDef.Point(450,226)
    B = dataDef.Point(5,98)
    C = dataDef.Point(200,500)
    
    flick = FlickCommand(A, B)
    click = ClickCommand(A)
    wait = WaitCommand(3)
    click2 = ClickCommand(C)
    press = PressCommand(A, 5)
    capture = SnapShotCommand()
    
    step = MacroCommand()
    step.Add(flick)
    step.Add(click)
    step.Add(wait)
    step.Add(click2)
    step.Add(press)
    step.Add(capture)
    
    step.Execute()
    
    
    
    