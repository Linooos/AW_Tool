import sys
import AWToolSDK.x64.Debug.AWToolSDK as aw
import ctypes

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("This script must be run as admin")
        exit()
    fanctrl = aw.FanControl()
    print("APICHECK",fanctrl.checkAPI(0))

