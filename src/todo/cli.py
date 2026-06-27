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
    """标记一条任务已完成(传入参数为任务标号)，并显示用时"""
    tasks = storage.load()
    if core.mark_done(tasks, task_id):
        task = core.search_task(tasks, task_id)
        diff = task.completed_at - task.created_at
        storage.save(tasks)
        typer.echo(
            f"已将任务 #{task_id} 标记为完成，用时{int(diff.total_seconds() // 60)}分{int(diff.total_seconds() % 60)}秒"
        )
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
def clear() -> None:
    """清空代办清单"""
    if not typer.confirm("确定要清空所有任务吗?"):
        raise typer.Exit()
    storage.save([])
    typer.echo("已清空所有任务")


@app.command("list")
def show() -> None:
    """打印所有任务信息"""
    tasks = storage.load()
    if not tasks:
        typer.echo("还没有任务")
        return
    for item in tasks:
        mark = "✓" if item.done else " "
        done_time = item.completed_at if item.completed_at else "未完成"
        typer.echo(
            f"[{mark}] #{item.id} {item.title}，创建时间：{item.created_at}, 完成时间：{done_time}"
        )
