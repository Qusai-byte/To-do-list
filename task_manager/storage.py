import json
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from models import Task
from config import DB_PATH, JSON_PATH, DEFAULT_STORAGE

class Storage:
    def __init__(self, storage_type: str = DEFAULT_STORAGE):
        self.storage_type = storage_type
        if storage_type == "sqlite":
            self.db_path = DB_PATH
            self._init_sqlite()
        elif storage_type == "json":
            self.json_path = JSON_PATH
            self._init_json()
    
    def _init_sqlite(self):
        """تهيئة قاعدة بيانات SQLite"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                due_date TEXT,
                priority INTEGER DEFAULT 1,
                category TEXT
            )
        """)
        self.conn.commit()
    
    def _init_json(self):
        """تهيئة ملف JSON"""
        if not self.json_path.exists():
            with open(self.json_path, "w") as f:
                json.dump([], f)
    
    def add_task(self, task: Task) -> Task:
        """إضافة مهمة جديدة"""
        if self.storage_type == "sqlite":
            self.cursor.execute("""
                INSERT INTO tasks (title, description, completed, created_at, due_date, priority, category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                task.title, task.description, task.completed, task.created_at, 
                task.due_date, task.priority, task.category
            ))
            task.id = self.cursor.lastrowid
            self.conn.commit()
            return task
        
        elif self.storage_type == "json":
            tasks = self.get_all_tasks()
            new_id = max(t.id for t in tasks) + 1 if tasks else 1
            task.id = new_id
            tasks.append(task)
            self._save_json(tasks)
            return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """الحصول على مهمة بواسطة المعرف"""
        if self.storage_type == "sqlite":
            self.cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = self.cursor.fetchone()
            if row:
                return Task(*row)
            return None
        
        elif self.storage_type == "json":
            tasks = self.get_all_tasks()
            for task in tasks:
                if task.id == task_id:
                    return task
            return None
    
    def get_all_tasks(self) -> List[Task]:
        """الحصول على جميع المهام"""
        if self.storage_type == "sqlite":
            self.cursor.execute("SELECT * FROM tasks")
            return [Task(*row) for row in self.cursor.fetchall()]
        
        elif self.storage_type == "json":
            try:
                with open(self.json_path, "r") as f:
                    tasks_data = json.load(f)
                return [Task.from_dict(task) for task in tasks_data]
            except (FileNotFoundError, json.JSONDecodeError):
                return []
    
    def update_task(self, task: Task) -> bool:
        """تحديث مهمة"""
        if self.storage_type == "sqlite":
            self.cursor.execute("""
                UPDATE tasks SET 
                title = ?, description = ?, completed = ?, 
                due_date = ?, priority = ?, category = ?
                WHERE id = ?
            """, (
                task.title, task.description, task.completed,
                task.due_date, task.priority, task.category, task.id
            ))
            self.conn.commit()
            return self.cursor.rowcount > 0
        
        elif self.storage_type == "json":
            tasks = self.get_all_tasks()
            for i, t in enumerate(tasks):
                if t.id == task.id:
                    tasks[i] = task
                    self._save_json(tasks)
                    return True
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """حذف مهمة"""
        if self.storage_type == "sqlite":
            self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        
        elif self.storage_type == "json":
            tasks = self.get_all_tasks()
            original_count = len(tasks)
            tasks = [t for t in tasks if t.id != task_id]
            if len(tasks) < original_count:
                self._save_json(tasks)
                return True
            return False
    
    def search_tasks(self, query: str) -> List[Task]:
        """بحث في المهام"""
        tasks = self.get_all_tasks()
        query = query.lower()
        return [
            t for t in tasks 
            if query in t.title.lower() or 
               (t.description and query in t.description.lower()) or
               (t.category and query in t.category.lower())
        ]
    
    def filter_tasks(self, completed: Optional[bool] = None, 
                    priority: Optional[int] = None,
                    category: Optional[str] = None) -> List[Task]:
        """تصفية المهام"""
        tasks = self.get_all_tasks()
        
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        
        if priority is not None:
            tasks = [t for t in tasks if t.priority == priority]
        
        if category is not None:
            tasks = [t for t in tasks if t.category and t.category.lower() == category.lower()]
        
        return tasks
    
    def _save_json(self, tasks: List[Task]):
        """حفظ المهام إلى ملف JSON"""
        with open(self.json_path, "w") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=2)
    
    def __del__(self):
        """تنظيف الموارد عند الإغلاق"""
        if self.storage_type == "sqlite":
            self.conn.close()