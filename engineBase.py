# -*- coding: utf-8 -*-
class EngineBase(object):
    def __new__(cls,*args,**kw):
        if not hasattr(cls,"_instance"):
            orig = super(EngineBase,cls)
            cls._instance = orig.__new__(cls,*args,**kw)
        return cls._instance 
    
    def __init__(self,*args, **kwargs):
        pass 
    
    def click(self, x, y):
        pass
    
    def flick(self, x1, y1, x2, y2):
        pass
    
    def press(self, x, y, time):
        pass
    
    def wait(self, time):
        pass
    
    def snapShot(self):
        pass
        
if __name__ == "__main__":
    class A(EngineBase):
        def __init__(self):
            pass
    class B(EngineBase):
        def __init__(self):
            pass     
    base = EngineBase()
            
    test1 = A()
    test2 = B()
    print test1 ,test2