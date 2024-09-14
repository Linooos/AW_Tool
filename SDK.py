import os
import pyAWToolSDK as aw
import json

fanCfgs = list()
fanCount = None
fanCtrl: aw.Fan_controller = None
powerCfgs = list()
powerCtrl: aw.Power_controller = None
powerCount = None
globalConfig = dict()
configFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
isAPI: dict = None

'''json'''


def readConfig():
    global globalConfig
    try:
        with open(configFile, 'r') as file:
            globalConfig = json.load(file)
    except FileNotFoundError:
        saveConfig()
    except json.JSONDecodeError:
        print(f"文件 config.json 不是有效的 JSON 文件。")
        exit(-1)


def saveConfig():
    with open(configFile, 'w') as file:
        json.dump(globalConfig, file, indent=4)


def checkDict(dir: str, dict: dict):
    '''输入dict的键路径，解决嵌套字典输出keyerror问题'''
    dirList = dir.split('/')
    temp = dict
    for i in dirList:
        if temp is not dict:
            return -1
        if not temp.get(i):
            temp[i] = {}
        temp = temp[i]


def checkGCfg(dir: str):
    checkDict(dir, globalConfig)


'''fan'''


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


'''power'''


def getPower():
    """获取当前power值的index"""
    return powerCtrl.getCurPower(False)


def setPower(index):
    """设置当前index代表的power值为当前power"""
    return powerCtrl.setPower(index, False)


def setGMode(enable):
    return fanCtrl.setGMode(enable)


def checkAPI():
    global isAPI
    if isAPI is None:
        isAPI = {"isAlienware": True,
                 "isSupported": True,
                 "isTCC": True,
                 "isXMP": True,
                 "isGmode": True}
        for i in range(5):
            if aw.checkAPI(i) == -1:
                print(i)
                print(aw.checkAPI(i))
                isAPI[list(isAPI.keys())[i]] = False
    keylist = []
    for key, value in isAPI.items():
        if not value:
            keylist.append(key)
    return keylist


def initSDK():
    global fanCfgs, fanCount, fanCtrl, powerCtrl, powerCount, powerCfgs
    # Initialize SDK
    fanCtrl = aw.Fan_controller()  # fans control
    fanCount = fanCtrl.getFansCount()  # fans count
    checkAPI()
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
    # 打开文件并获取文件描述符
    readConfig()

    # 为文件设置不同模式命名
    checkGCfg('globalSetting')
    if not globalConfig['globalSetting'].get('powerName'):
        globalConfig['globalSetting']['powerName'] = {"0": "自定义模式",
                                                      '160': "均衡模式",
                                                      '161': "性能模式",
                                                      '162': "电池模式",
                                                      '163': "安静模式",
                                                      '164': "满速模式"}
    saveConfig()


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

    # for i in range(powerCtrl.getPowersCount()):
    #     print(f"Power {i}:{powerCtrl.getPower(i)}")
    #
    # print(f"current power :{powerCtrl.getCurPower(True)}")
    # powerCtrl.setPower(163, True)
    # print(f"current power :{powerCtrl.getCurPower(True)}")

    # print(getPower())
    # print(setPower(3))
    # print(getPower())
    # print(powerCfgs[3])

    # d = {}
    # checkDict("a",d)
    # checkDict("a", d)
    # print(f"d:{d}")
    #     powerCtrl.setPower(164,True)
    #     # print(powerCtrl.getCurPower(True))
    #     # powerCtrl.setPower(171, True)
    #     # print(powerCtrl.getCurPower(True))

    # setGMode(True)
    # os.system("pause")
    # print(powerCtrl.getCurPower(True))
    # setGMode(False)
    # print(powerCtrl.getCurPower(True))
    print(isAPI)
    print(checkAPI())
    for i in range(5):
        print(aw.checkAPI(i))
    os.system("pause")
