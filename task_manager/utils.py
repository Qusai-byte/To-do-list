from datetime import datetime
from typing import List, Optional
from models import Task

def print_task_details(task: Task):
    """طباعة تفاصيل المهمة بشكل جميل"""
    print("\n" + "=" * 50)
    print(f"المهمة #{task.id}")
    print("=" * 50)
    print(f"العنوان: {task.title}")
    if task.description:
        print(f"الوصف: {task.description}")
    print(f"الحالة: {'مكتملة ✓' if task.completed else 'غير مكتملة ✗'}")
    print(f"تاريخ الإنشاء: {task.created_at}")
    if task.due_date:
        print(f"تاريخ الاستحقاق: {task.due_date}")
    priority_map = {1: "⬇️ منخفض", 2: "↔️ متوسط", 3: "⬆️ عالي"}
    print(f"الأولوية: {priority_map.get(task.priority, 'غير معروفة')}")
    if task.category:
        print(f"الفئة: 🏷️ {task.category}")
    print("=" * 50 + "\n")

def print_tasks_table(tasks: List[Task], title: str = "المهام"):
    """طباعة قائمة المهام في شكل جدول"""
    if not tasks:
        print("لا توجد مهام لعرضها.")
        return
    
    print(f"\n{title}:")
    print("=" * 80)
    print(f"{'ID':<5} | {'الحالة':<5} | {'العنوان':<30} | {'الاستحقاق':<12} | {'الفئة':<15} | {'الأولوية':<10}")
    print("-" * 80)
    
    for task in tasks:
        status = "✓" if task.completed else "✗"
        due_date = task.due_date if task.due_date else "لا يوجد"
        category = task.category if task.category else "بدون"
        priority_map = {1: "⬇️ منخفض", 2: "↔️ متوسط", 3: "⬆️ عالي"}
        priority = priority_map.get(task.priority, "غير معروف")
        
        print(f"{task.id:<5} | {status:<5} | {task.title[:28]:<30} | {due_date:<12} | {category[:13]:<15} | {priority:<10}")
    
    print("=" * 80)
    print(f"عدد المهام: {len(tasks)}\n")

def validate_date(date_str: str) -> bool:
    """التحقق من صحة التاريخ بصيغة YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_user_input(prompt: str, default: Optional[str] = None) -> str:
    """الحصول على إدخال المستخدم مع قيمة افتراضية"""
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    return input(prompt).strip()