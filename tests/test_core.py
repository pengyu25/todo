from todo import core


def test_add_task():
    tasks = []
    task = core.add_task(tasks, "买菜")
    assert task.done is False
    assert task.id == 1
    assert task.title == "买菜"
    assert len(tasks) == 1


def test_mark_done():
    tasks = []
    task = core.add_task(tasks, "买菜")
    assert core.mark_done(tasks, 1) is True
    assert task.done is True
    assert core.mark_done(tasks, 999) is False


def test_delete_task():
    tasks = []
    core.add_task(tasks, "买菜")
    assert core.delete_task(tasks, 1) is True
    assert core.delete_task(tasks, 999) is False
    assert len(tasks) == 0
