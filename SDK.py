import pyAWToolSDK as aw
import json

fanCfgs = list()
fanCount = None
fanCtrl: aw.Fan_controller = None

powerCfgs = list()
powerCtrl: aw.Power_controller = None
powerCount = None
globalConfig = dict()


def readConfig():
    global globalConfig
    try:
        with open('config.json', 'r') as file:
            globalConfig = json.load(file)
    except FileNotFoundError:
        saveConfig()
    except json.JSONDecodeError:
        print(f"文件 config.json 不是有效的 JSON 文件。")
        exit(-1)


def saveConfig():
    with open('config.json', 'w') as file:
        json.dump(globalConfig, file, indent=4)


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
    return fanCtrl.setFan(index, byte)


def initSDK():
    global fanCfgs, fanCount, fanCtrl, powerCtrl, powerCount, powerCfgs
    # Initialize SDK
    fanCtrl = aw.Fan_controller()  # fans control
    fanCount = fanCtrl.getFansCount()  # fans count

    powerCtrl = aw.Power_controller()  # power 控制器
    powerCount = powerCtrl.getPowersCount()  # 获取power数量

    # load info config from SDK
    for i in range(fanCount):
        info = aw.Fan_info()  # 作为引用参数传递 数据结构
        fanCtrl.getFan(i, info)
        fanCfgs.append(info)

    for i in range(powerCount):
        powerCfgs.append(powerCtrl.getPower(i))  # 创建power列表

    # 读取配置文件
    readConfig()

    # 为文件设置不同模式命名

    if not globalConfig.get('globalSetting'):
        globalConfig['globalSetting'] = {}
    if not globalConfig['globalSetting'].get('powerName'):
        globalConfig['globalSetting']['powerName'] = {"0": "自定义模式",
                                                      '160': "均衡模式",
                                                      '161': "性能模式",
                                                      '162': "电池模式",
                                                      '163': "安静模式",
                                                      '164': "满速模式"}
    saveConfig()




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
    # for i in range(fanCount):
    #     print(fanCtrl.getFanBoost(i))

    for i in range(powerCtrl.getPowersCount()):
        print(f"Power {i}:{powerCtrl.getPower(i)}")

    print(f"current power :{powerCtrl.getCurPower(True)}")
    powerCtrl.setPower(163, True)
    print(f"current power :{powerCtrl.getCurPower(True)}")
