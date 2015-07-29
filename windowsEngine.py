# -*- coding: utf-8 -*-
from engineBase import *
from factoryBase import *
from ctypes import *
import dataDef
import recoder
import time
import os,shutil,win32gui, win32ui, win32con, win32api
import logging


NumberOfIntermediatePoints = 10
    
def getFactory():
    return WindowsFactory()
    
class WindowsFactory(EngineFactory):
    def __init__(self):
        pass
    
    def MakeEngine(self):
        return WindowsEngine()    

class WindowsEngine(EngineBase):
    def __init__(self, *args, **kwargs):
        try:
            self.hwnd = win32gui.FindWindow('XDE_LCDWindow',None)
            rect = win32gui.GetWindowRect(self.hwnd)
            self.w = rect[2] - rect[0]
            self.h = rect[3] - rect[1]
        except Exception,e:
            MoniterDev=win32api.EnumDisplayMonitors(None,None)
            self.w = MoniterDev[0][2][2]
            self.h = MoniterDev[0][2][3]
            self.hwnd = 0
            print e
        
        FORMAT = '%(asctime)-15s %(message)s'
        LOG_FILENAME= "%s/log.txt" %recoder.FOLDER
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format=FORMAT)
    
    def click(self, _point):
        
        logging.debug(" %.2f Click(%s,%s)" %((time.time()-recoder.BEGGINTIME), _point.x, _point.y))
        point = self._transformPosition(_point)
        #move cursor
        windll.user32.SetCursorPos(point.x, point.y)
        #send down and up event
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, point.x, point.y)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, point.x, point.y)
        
        
        
    def flick(self, _start, _end):
    
        logging.debug(" %.2f Flick from(%s,%s)to(%s,%s)" %((time.time()-recoder.BEGGINTIME), _start.x, _start.y, _end.x, _end.y))
        start = self._transformPosition(_start)
        end = self._transformPosition(_end)
        list = self._getIntermediatePoints(start, end)  
        startPoint = list[0]
        endPoint = list[-1]
        
        windll.user32.SetCursorPos(startPoint.x, startPoint.y)
        #send down event
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, startPoint.x,  startPoint.y)
        time.sleep(0.01)
        
        for p in list:
            windll.user32.SetCursorPos(p.x, p.y)
            time.sleep(0.01)
            endPoint = p
        if(endPoint != end):
            endPoint = end
            
        windll.user32.SetCursorPos(endPoint.x, endPoint.y)
        time.sleep(0.01)
        #send up event
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, endPoint.x, endPoint.y) 
        
    def press(self, _point, t):
        point = self._transformPosition(in_point)
        #move cursor
        windll.user32.SetCursorPos(point.x, point.y)
        #send down and up event
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, point.x, point.y)
        time.sleep(t)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, point.x, point.y)

    def wait(self, t):
        time.sleep(t)
        
    def snapShot(self):
        # hwndDC = win32gui.GetWindowDC(self.hwnd)     
        # mfcDC=win32ui.CreateDCFromHandle(hwndDC) 
        # saveDC=mfcDC.CreateCompatibleDC() 
        # saveBitMap = win32ui.CreateBitmap() 
        # saveBitMap.CreateCompatibleBitmap(mfcDC, self.w, self.h) 
        # saveDC.SelectObject(saveBitMap) 
        # saveDC.BitBlt((0,0),(self.w, self.h) , mfcDC, (0,0), win32con.SRCCOPY)
        # tempfilename = win32api.GetTempFileName(".","")[0]
        # bmpname = tempfilename +'.bmp'
        # saveBitMap.SaveBitmapFile(saveDC, bmpname) 
        # if os.path.isfile(bmpname):
            # newfle = r"%s/%s.bmp" %(recoder.FOLDER, time.strftime('%m%d_%H%M%S',time.localtime(time.time())))
            # shutil.copy(bmpname, newfle)
            # os.remove(bmpname)
        # if os.path.isfile(tempfilename):
            # os.remove(tempfilename)
        # logging.debug(" %.2f Capture a picture %s" %((time.time()-recoder.BEGGINTIME), newfle))
        # return bmpname
        
        self._fullScreenshots()
    
    def back(self):
        pass
    
    
    def _getIntermediatePoints(self, start, end):
        list = []
        for i in range(0,NumberOfIntermediatePoints):
            ratio = (i + 1.0) / (NumberOfIntermediatePoints + 1.0);
            x = (start.x + (int) (ratio * (end.x - start.x)))
            y = (start.y + (int) (ratio * (end.y - start.y)))
            point = dataDef.Point(x,y)
            list.append(point)
        return list
        
    
    def _getEmuPositon(self):
    
        pwin=win32gui.FindWindow('XDE_LCDWindow',None)
        rect = win32gui.GetWindowRect(pwin)
        return rect    
        
    def _transformPosition(self, point):
        offset = self._getEmuPositon()
        scaleRatio = recoder.DISPLAY_WIDTH/(offset[2] - offset[0])
        point.x = int(point.x/scaleRatio + offset[0])
        point.y = int(point.y/scaleRatio + offset[1])
        return point 
        
    def _fullScreenshots(self):
        hwnd = 0
        hwndDC = win32gui.GetWindowDC(hwnd) 
        mfcDC=win32ui.CreateDCFromHandle(hwndDC) 
        saveDC=mfcDC.CreateCompatibleDC() 
        saveBitMap = win32ui.CreateBitmap() 
        MoniterDev=win32api.EnumDisplayMonitors(None,None)
        w = MoniterDev[0][2][2]
        h = MoniterDev[0][2][3]
        print w,h
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h) 
        saveDC.SelectObject(saveBitMap) 
        saveDC.BitBlt((0,0),(w, h) , mfcDC, (0,0), win32con.SRCCOPY) 
        tempfilename = win32api.GetTempFileName(".","")[0]
        bmpname = tempfilename +'.bmp'
        saveBitMap.SaveBitmapFile(saveDC, bmpname) 
        if os.path.isfile(bmpname):
            newfle = r"%s/%s.bmp" %(recoder.FOLDER, time.strftime('%m%d_%H%M%S',time.localtime(time.time())))
            shutil.copy(bmpname, newfle)
            os.remove(bmpname)
        if os.path.isfile(tempfilename):
            os.remove(tempfilename)
        logging.debug(" %.2f Capture a picture %s" %((time.time()-recoder.BEGGINTIME), newfle))
        return bmpname
        
        
    
    
if __name__ == '__main__':
    def test1():
        f = getFactory()
        e = f.MakeEngine()
        a = dataDef.Point(0, 350)
        b = dataDef.Point(1000, 350)
        e.flick(a, b)
    a = f.MakeEngine()
    b = f.MakeEngine()
    print a
    print b
        
    