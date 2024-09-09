
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
    import uiprofile.window as window
    import pyAWToolSDK as aw

    # Initialize SDK
    fanCtrl = aw.Fan_controller()  # fans control
    fanCount = fanCtrl.getFansCount()  # fans count

    # load fan config from SDK
    for i in range(fanCount):
        info = aw.Fan_info()
        fanCtrl.getFan(i, info)
        fanCfgs.append(info)

    # for i in fanCfgs:
    #     print(str(i)+"id："+str(i.id))
    #     print(str(i)+"id："+str(i.type))
    #     print("-------------------------------")

    # for i in range(fanCount):
    #     print(str(i) + "MAX：" + str(fanCtrl.getMAXFan(i)))
    #     print("-------------------------------")

    # load UI
    window.startUi()
