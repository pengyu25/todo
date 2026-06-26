# todo

一个简单的命令行待办清单工具。

## 功能

通过命令实现任务的增、删、改、查,数据以本地 JSON 文件持久化保存。

## 用法

| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `todo add` | 添加任务 | `todo add "买菜"` |
| `todo list` | 列出所有任务及完成情况 | `todo list` |
| `todo done` | 标记任务已完成(参数为任务编号) | `todo done 1` |
| `todo delete` | 从待办列表删除任务(参数为任务编号) | `todo delete 1` |
| `todo clear` | 清空所有任务 | `todo clear` |

加 `-v` / `--verbose` 可显示详细日志,例如 `todo --verbose list`。

## 安装

前提:Python 3.13+(使用 uv 安装时,可由 uv 自动提供 Python)。

### 方式一:使用 uv(推荐)

```bash
# 1. 安装 uv(如果还没有)
# Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS / Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 获取源码
git clone https://github.com/pengyu25/todo.git
cd todo

# 3. 安装成全局命令
uv tool install .

# 4. 验证(在任意目录都能运行)
todo --help
```

### 方式二:使用 pip

```bash
git clone https://github.com/pengyu25/todo.git
cd todo
pip install .
todo --help
```

## 卸载

```bash
uv tool uninstall todo
```
