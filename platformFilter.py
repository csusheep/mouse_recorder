# -*- coding: utf-8 -*-
import platform

osName = platform.system()
if(osName == 'Windows'):
    import windowsEngine as engine
elif(osName == 'Linux'):
    import linuxEngine as engine
elif(osName == 'Darwin'):
    import macEngine as engine
   
        
if __name__ == "__main__":
    
    print(platform.system())