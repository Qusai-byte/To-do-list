import os
from pathlib import Path

# إعدادات النظام
APP_NAME = "نظام إدارة المهام المتطور"
VERSION = "1.0.0"
AUTHOR = "فريق التطوير"

# مسارات الملفات
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = BASE_DIR / "task_manager.db"
JSON_PATH = BASE_DIR / "tasks.json"

# إعدادات التخزين
DEFAULT_STORAGE = "sqlite"  # sqlite أو json