from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    due_date: Optional[str] = None
    priority: int = 1  # 1: منخفض، 2: متوسط، 3: عالي
    category: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    def __str__(self):
        status = "✓" if self.completed else "✗"
        priority_map = {1: "⬇️ منخفض", 2: "↔️ متوسط", 3: "⬆️ عالي"}
        due_info = f" | 📅 {self.due_date}" if self.due_date else ""
        category_info = f" | 🏷️ {self.category}" if self.category else ""
        return (
            f"{self.id:03d}. [{status}] {self.title}"
            f"{due_info}{category_info} | {priority_map.get(self.priority, '')}"
        )