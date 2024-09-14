fanCfgs = list()
fanCount = None

if __name__ == "__main__":
    # check ADMIN

    # Add path
    import sys, os

    sys.path.append(os.path.split(os.path.abspath(__file__))[0] + "\\uiprofile")

    # load UI
    import uiprofile.window as window

    window.startUi()
