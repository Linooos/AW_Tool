fanCfgs = list()
fanCount = None

file_path = None
file_name = None



if __name__ == "__main__":
    # check ADMIN

    # Add path
    import sys, os

    sys.path.append(os.path.split(os.path.abspath(__file__))[0] + "\\uiprofile")
    file_path = os.path.abspath(__file__)
    file_name = os.path.basename(file_path)

    # load UI
    import uiprofile.window as window

    window.startUi()
