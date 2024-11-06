import subprocess

command = "Import-Module DellBIOSProvider; dir DellSmbios:\\"

# 使用 subprocess 模块运行 PowerShell 命令
result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)

# 输出结果
result = result.stdout

resultList = result.split("\n")
for i in range(3):
    resultList.pop(0)
print(resultList[0].split("  "))