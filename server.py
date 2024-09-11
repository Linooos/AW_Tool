import pyAWToolSDK as aw
import math

fanCfgs = list()
fanCount = None
fanCtrl: aw.Fan_controller = None


def getRPM(index):
    if index >= fanCount:
        return -1
    return fanCtrl.getFanRPM(index)


def getFanBoost(index):
    if index >= fanCount:
        return -1
    return fanCtrl.getFanBoost(index)


def setFansBoost(index, value):
    if value > 100: return -1
    if index >= fanCount: return -1
    byte = int((float(value) / 100.0) * 0xFF)
    #print("byte:"+str(byte))
    #fanCtrl.unlockFanControl()
    return fanCtrl.setFan(index, byte)


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


print("initial SDK")
initSDK()

if __name__ == "__main__":
    # for i in range(fanCount):
    #     setFansBoost(i,0)
    #     #fanCtrl.setFan(i, 0)
    # g = aw.Graphic_Controller()
    # print(g.setGraphicOptimus(True))
    # for i in fanCfgs:
    #     print(i.type)
    # pass
    for i in range(fanCount):
        print(fanCtrl.getFanBoost(i))

