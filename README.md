AW-tools

用于alienware风扇控制，以及功耗模式选择。

## 编译说明

1. 需在环境中添加PyAWTool变量到本机所在python根目录（python安装不再赘述）requires-python = ">=3.8"
2. vs2022编译目录下AWToolSDK内项目，生成目录会在项目根目录.venv/DLLs目录下
3. python 安装PyQt5>=5.15.10, numpy, pyperclip, pyinstaller
4. 命令行执行pyinstaller /path/to/project/awtools.spec

## License

本项目遵循GPLv3开源协议，禁止用于商业。
