from todo import storage, core
import pytest


def test_save_load_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "todos.json")
    assert storage.load() == []
    tasks = []
    core.add_task(tasks, "买菜")
    storage.save(tasks)
    loaded = storage.load()
    assert loaded == tasks


def test_load_corrupt_file(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "notexist.json")
    (tmp_path / "notexist.json").write_text("坏掉的内容{", encoding="UTF-8")
    with pytest.raises(ValueError):
        storage.load()
