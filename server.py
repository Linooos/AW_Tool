import pyAWToolSDK as aw

fanCfgs = list()
fanCount = None
fanCtrl = None


def initSDK():
    global fanCfgs, fanCount, fanCtrl
    # Initialize SDK
    fanCtrl = aw.Fan_controller()  # fans control
    fanCount = fanCtrl.getFansCount()  # fans count

    # load fan config from SDK
    for i in range(fanCount):
        info = aw.Fan_info()
        fanCtrl.getFan(i, info)
        fanCfgs.append(info)
