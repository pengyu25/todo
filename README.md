这是一个简单的代办清单工具

功能：通过命令实现任务的增、删、改、查，已完成本地json的持久化

用法:
    todo add(添加任务)                              todo add "买菜"
    todo list(打印剩余任务及其完成情况)               todo done 
    todo done(标记任务已完成，参数为任务标号)         todo done 1
    todo delete(从代办列表中删除任务，参数为任务标号)  todo delete 1
    todo clear(清空代办列表)                         todo clear
安装: 
    方式一(uv安装):
        # 1. 安装 uv(如果还没有)
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"   # Windows
        # (macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh)

        # 2. 获取源码
        git clone <你的仓库地址> todo
        cd todo

        # 3. 安装成全局命令
        uv tool install .

        # 4. 验证(在任意目录都能跑)
        todo --help
    
    方式二(pip安装):
        # 前提:已有 Python 3.13+
        git clone <https://github.com/pengyu25/todo> todo
        cd todo
        pip install .
        todo --help

删除:
    uv tool uninstall todo
