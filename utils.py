# -*- coding: utf-8 -*-

import pythoncom, pyHook 
import win32gui
import recoder
import time

global BEGGINTIME
global FILE

t = time.time()
print time.localtime(t)
print time.strftime('%m-%d-%M-%S',time.localtime(time.time()))

DOWN_POSITION_X = ''
DISPLAY_WIDTH = recoder.DISPLAY_WIDTH
DISPLAY_HEIGHT = recoder.DISPLAY_HEIGHT

def getEmuPositon():
    
    pwin=win32gui.FindWindow('XDE_LCDWindow',None)
    rect = win32gui.GetWindowRect(pwin)
    return rect

def transformPosition(x, y):
    
    offset = getEmuPositon()
    scaleRatio = DISPLAY_WIDTH/(offset[2] - offset[0])

    x = int((x - offset[0])*scaleRatio)
    y = int((y - offset[1])*scaleRatio)
    
    return (x, y)

def transformPosition2(point):
    
    offset = getEmuPositon()
    scaleRatio = DISPLAY_WIDTH/(offset[2] - offset[0])

    point.x = int((point.x - offset[0])*scaleRatio)
    point.y = int((point.y - offset[1])*scaleRatio)
    
    return point


def OnMouseEvent(event):

    global BEGGINTIME 
    global FILE
    if event.MessageName == 'mouse left down':
        recoder.X = event.Position[0]
        recoder.Y = event.Position[1]
    
    elif event.MessageName == 'mouse left up':
        if ((recoder.X == event.Position[0]) and (recoder.Y == event.Position[1])):
            print "it is a click event"
            #print 'before transform : ', event.Position
            #print 'after transform: ', transformPosition(event.Position[0],event.Position[1])
            temp = transformPosition(event.Position[0],event.Position[1])
            FILE.write("I tap on screen %s from the left and %s from the top\n" %(temp[0],temp[1]))
            t = time.time()  
            FILE.write("I wait %.2f seconds\n" %(t - BEGGINTIME))
            BEGGINTIME = t
        else:
            print "flick from",(recoder.X,recoder.Y), 'to', event.Position
            start = transformPosition(recoder.X,recoder.Y)
            end = transformPosition(event.Position[0],event.Position[1])
            FILE.write("I flick from (%s,%s) to (%s,%s)\n" %(start[0],start[1],end[0],end[1]))
            t = time.time()  
            print (t - BEGGINTIME)
            FILE.write("I wait %.2f seconds\n" %(t - BEGGINTIME))
            BEGGINTIME = t
    elif event.MessageName == 'mouse middle down':
            FILE.write("take a picture\n")
            t = time.time()  
            FILE.write("I wait %.2f seconds\n" %(t - BEGGINTIME))
            BEGGINTIME = t
            

    # 返回 True 可将事件传给其它处理程序，否则停止传播事件
    return True

if __name__ == '__main__':
    
    fileName = time.strftime('%m%d_%M%S',time.localtime(time.time()))
    BEGGINTIME = time.time()
    FILE = open(fileName,'a')
    downPosition = ()
    # 创建钩子管理对象
    hm = pyHook.HookManager()
    # 监听所有鼠标事件
    hm.MouseAll = OnMouseEvent # 等效于hm.SubscribeMouseAll(OnMouseEvent)
    # 开始监听鼠标事件
    hm.HookMouse()
    # 一直监听，直到手动退出程序
    pythoncom.PumpMessages()