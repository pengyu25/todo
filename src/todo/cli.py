import typer
from todo import storage
from todo import core
import logging


app = typer.Typer()


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="显示详细日志"),
) -> None:
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
    )


@app.command()
def add(title: str) -> None:
    """添加一条新任务"""
    tasks = storage.load()
    core.add_task(tasks, title)
    storage.save(tasks)
    typer.echo(f'已添加"{title}"')


@app.command()
def done(task_id: int) -> None:
    """标记一条任务已完成(传入参数为任务标号)"""
    tasks = storage.load()
    if core.mark_done(tasks, task_id):
        storage.save(tasks)
        typer.echo(f"已将任务 #{task_id} 标记为完成")
    else:
        typer.echo(f"任务 #{task_id} 未找到", err=True)
        raise typer.Exit(code=1)


@app.command()
def delete(task_id: int) -> None:
    """将任务从待办列表中删除(参数为任务标号)"""
    tasks = storage.load()
    if core.delete_task(tasks, task_id):
        storage.save(tasks)
        typer.echo(f"已删除任务 #{task_id}")
    else:
        typer.echo(f"任务 #{task_id} 未找到", err=True)
        raise typer.Exit(code=1)


@app.command()
def clean() -> None:
    """清空代办清单"""
    tasks = storage.load()
    tasks = {}
    storage.save(tasks)


@app.command("list")
def show() -> None:
    """打印所有任务及其完成情况"""
    tasks = storage.load()
    if not tasks:
        typer.echo("还没有任务")
        return
    for item in tasks:
        mark = "✓" if item.done else " "
        typer.echo(f"[{mark}] #{item.id} {item.title}")
