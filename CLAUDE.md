# CLAUDE.md — 命令行待办清单(todo CLI)

## 这是什么

我(项目作者)是一名正在学习 Python 和 C++ 的学生,这是我的**第一个真正的项目**。
目标不是"做出一个能用的工具",而是**通过亲手完成它来提升自己的编程能力、积累工程实践经验**。

项目本体:一个命令行待办工具 —— 能添加任务、列出任务、标记完成、删除,数据存在本地 JSON 文件里。预计两三百行,但"麻雀虽小五脏俱全"。

## ⚠️ 最重要:你(AI)应该怎么帮我

我的能力只在一个地方生长:我自己卡住、思考、试错、最后解决的过程里。请据此协助。

**当导师/答疑/代码审查用(请这样做):**
- 我卡住时,解释"为什么这样写""这个报错是什么意思",给**思路提示**而不是直接给答案。
- 我自己写完一段后,帮我 review,告诉我"一个资深 Python 程序员会怎么重写这段"。
  - 我大概率会犯"用 Python 语法写 C++"的毛病(C++ 腔 Python),请重点帮我纠正。
- 讲解陌生概念、某个库/工具的惯用法。
- 需要时帮我出练习。

**不要这样做(这会偷走我的学习):**
- 不要一次性生成整个功能或整个项目让我复制粘贴。
- 不要在我没理解时就让我接受补全。
- 我报错时,不要直接替我改完;先帮我看懂我自己错在哪。

原则:**这个项目我坚持自己手写每一行,把你当随叫随到的导师,而不是代码生成器。**

## 一个完整项目要经历的八步(认知地图)

1. **定范围** —— 想清楚 MVP 做什么、不做什么,克制范围(目标:三天能跑起来的版本)。
2. **设计** —— 数据怎么表示、拆成哪些模块、模块间谁调用谁(纸上画即可)。
3. **搭骨架** —— 建目录、依赖管理、git init。
4. **迭代实现** —— 一个功能一个功能写,**永远保持程序能跑**。
5. **处理边界和错误** —— 真实世界输入是脏的(文件不存在、乱输入、数据损坏)。这是"项目级"与"作业级"的分水岭。
6. **测试** —— 写代码验证代码,而不是手动跑。
7. **打磨** —— 日志、统一风格、README。
8. **交付** —— 打包成别人(和三个月后的自己)能直接装来用的东西。

## 目录结构

```
todo/
├── pyproject.toml        # 项目元数据 + 依赖,用 uv 管理
├── README.md
├── src/
│   └── todo/
│       ├── __init__.py
│       ├── models.py     # Task 数据模型(dataclass)
│       ├── storage.py    # 读写 JSON 文件
│       ├── core.py       # 业务逻辑:增删查改
│       └── cli.py        # 命令行入口(typer)
└── tests/
    └── test_core.py      # pytest 测试
```

## 当前进度(最后更新:2026-06-26)

- ✅ **第 0 步 · 环境与骨架** —— `uv init --package` 建好 src 布局;`pyproject.toml` 里加了 `[tool.uv] link-mode = "copy"`(跨盘 hardlink 警告);todo 已是**独立 git 仓库**(外层 `D:/Project` 的 `.gitignore` 忽略了 `/project/todo/`);分支 `main`;首次提交完成。
- ✅ **第 1 步 · 数据模型** —— `src/todo/models.py` 里 `Task` 写好:`id: int`、`title: str`、`done: bool = False`、`created_at: datetime = field(default_factory=datetime.now)`。(踩过的点:`field` 来自 `dataclasses` 不是 `datetime`;`default_factory` 传函数本身不加括号。)
- ✅ **第 2 步 · 核心逻辑** —— `src/todo/core.py` 四个函数全部完成并通过测试:`add_task(tasks, title) -> Task`(用 `max((t.id for t in tasks), default=0) + 1` 生成 id)、`list_tasks(tasks) -> list[Task]`(只 return,不 print)、`mark_done(tasks, task_id)`、`delete_task(tasks, task_id)`。全部带类型注解。**ruff 已装为 dev 依赖**,`ruff check` 通过、`ruff format` 已格式化。已提交。
- ✅ **第 3 步 · 持久化 `storage.py`** —— `save(tasks)`/`load()` 完成。`save`:`asdict` 转 dict、`datetime.isoformat()` 转字符串、`with open(... "w", encoding="utf-8")` + `json.dump(..., ensure_ascii=False)` 写文件。`load`:`json.load` 读回、`datetime.fromisoformat()` 还原时间、`Task(**item)` 解包还原对象。异常处理:`except FileNotFoundError` 返回 `[]`;`except json.JSONDecodeError as e: raise ValueError(...) from e`(异常链,交由上层 CLI 展示)。`DATA_FILE = Path("todos.json")`,已加进 `.gitignore`。三种边界(正常/缺失/损坏)已测通。(踩过的点:`isoformat` 是实例方法、`fromisoformat` 是类方法;load 误用 `"w"` 会清空文件;`fromisocalendar` ≠ `fromisoformat`。)
- ✅ **第 4 步 · 命令行界面 `cli.py`** —— `typer` app 完成,四个命令:`add`/`done`/`delete`/`list`(`@app.command("list")` + 函数名 `show` 避免撞内置)。每个命令编排 `storage.load → core.xxx → storage.save`。入口已改 `todo = "todo.cli:app"`,`uv run todo ...` 可用。`typer` 装为运行依赖。用户输出统一 `typer.echo`;找不到 id 时 `typer.echo(..., err=True)` 走 stderr + `raise typer.Exit(code=1)`。配套:`core.mark_done`/`delete_task` 改为返回 `bool`(找到并处理 True、否则 False)供 CLI 判断。(踩过的点:typer 单命令时不需敲命令名、补齐多命令即解决;`else: return False` 写进循环内导致只查第一条——"找遍都没有"必须等循环结束才能下结论。)
- 🔜 **第 5 步 · 日志 `logging`**(下一步)—— 把内部诊断信息从无/print 改为标准库 `logging`(注意:面向用户的 `typer.echo` 输出**不动**,日志是给开发者看的内部事件,如 load/save、未找到、异常)。理解 print 调试与 logging 的区别、日志级别(DEBUG/INFO/WARNING/ERROR)。

**已确立的约定/风格**:函数名 `snake_case`、动词_名词;参数列表用 `task_id` 不用 `id`;类型注解写 `list[Task]`(方括号);每完成一步用 `feat:`/`chore:` 提交一次,`git add` 后先 `git status` 再 commit。

## 实现顺序(从最熟的往外扩,每步逼自己学一个主题)

- **第 0 步 · 环境与骨架** → `uv init`、`pyproject.toml`、配 `ruff`、`git init`。先把架子立起来。
- **第 1 步 · 数据模型 `models.py`** → 用 `dataclass` 定义 `Task`(id、标题、是否完成、创建时间)。Pydantic 暂不用。
- **第 2 步 · 核心逻辑 `core.py`** → `add / list / mark_done / delete`,操作内存里的列表。纯逻辑,先建立信心。
- **第 3 步 · 持久化 `storage.py`** → 任务列表存成 JSON 再读回。同时撞上三个主题:`pathlib`(文件存哪)、`with` 上下文管理器、`try/except` 异常处理(文件不存在、JSON 损坏)。**最有营养的一步**。
- **第 4 步 · 命令行界面 `cli.py`** → 用 `typer` 把 core 包成命令:`todo add "买菜"`、`todo list`、`todo done 1`。
- **第 5 步 · 日志** → 把 `print` 换成 `logging`,理解真实项目为什么不用 print 调试。
- **第 6 步 · 测试 `test_core.py`** → 用 `pytest` 测核心逻辑。
- **第 7 步 · 打包** → 在 `pyproject.toml` 配 entry point,让 `todo` 成为终端里能直接敲的命令。

## 技术栈与约定

- 依赖/项目管理:**uv** + `pyproject.toml`
- 代码风格:**ruff**
- 数据建模:**dataclass**(Pydantic 留给以后需要校验外部输入的项目)
- CLI:**typer**
- 日志:标准库 **logging**
- 测试:**pytest**
- 版本控制:git
- **async 整个项目用不到,跳过**(等以后做并发网络请求那类项目再学)。
