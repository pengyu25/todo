from todo.models import Task
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
import json


DATA_FILE = Path("todos.json")


def save(tasks: list[Task]) -> None:
    data = [asdict(item) for item in tasks]
    for item in data:
        item["created_at"] = item["created_at"].isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def load() -> list[Task]:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        raise ValueError(f"数据文件{DATA_FILE} 已损坏，无法读取") from e
    for item in data:
        item["created_at"] = datetime.fromisoformat(item["created_at"])
    tasks = [Task(**item) for item in data]
    return tasks
