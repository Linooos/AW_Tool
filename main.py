
#sys.path.append(os.path.split(os.path.abspath(__file__))[0]+"\\AWToolSDK\\x64\\Debug")
#sys.path.append(os.path.split(os.path.abspath(__file__))[0]+"\\AWToolSDK\\x64\\Release")
fanCfgs = list()
fanCount = None

if __name__ == "__main__":
    # check ADMIN
    import ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("This script must be run as admin")
        exit()

    # Add path
    import sys,os
    sys.path.append(os.path.split(os.path.abspath(__file__))[0] + "\\uiprofile")

    # #initSDk



    # load UI
    import uiprofile.window as window
    import SDK
    window.startUi()
