from todo.models import Task
from datetime import datetime


def add_task(tasks: list[Task], title: str) -> Task:
    task = Task(max([item.id for item in tasks], default=0) + 1, title)
    tasks.append(task)
    return task


def list_tasks(tasks: list[Task]) -> list[Task]:
    return tasks


def search_task(tasks: list[Task], task_id: int) -> Task | None:
    for item in tasks:
        if item.id == task_id:
            return item


def mark_done(tasks: list[Task], task_id: int) -> bool:
    for item in tasks:
        if item.id == task_id:
            item.done = True
            item.completed_at = datetime.now()
            return True
    return False


def delete_task(tasks: list[Task], task_id: int) -> bool:
    for item in tasks:
        if item.id == task_id:
            tasks.remove(item)
            return True
    return False
