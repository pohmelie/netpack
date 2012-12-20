from ctypes import *


au3 = windll.AutoItX3
au3.AU3_Init()
#au3.AU3_WinMinimizeAll()
au3.AU3_WinWaitActive.args = (c_wchar_p, c_wchar_p, c_long)
au3.AU3_WinWaitActive("Diablo", "", 0)
print("here")
