from dataclasses import dataclass
from datetime import datetime
from dataclasses import field

@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    created_at: datetime = field(default_factory = datetime.now)