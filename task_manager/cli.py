import sys
import os
import argparse
from datetime import datetime
# إضافة مسار المجلد الحالي إلى مسار بايثون
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# استيرادات مباشرة
from storage import Storage
from models import Task
from utils import print_tasks_table, print_task_details, validate_date, get_user_input
from config import APP_NAME, VERSION, AUTHOR, DEFAULT_STORAGE

class TaskManagerCLI:
    def __init__(self, storage_type: str = DEFAULT_STORAGE):
        self.storage = Storage(storage_type)
        self.storage_type = storage_type
    
    def add_task(self, args):
        """إضافة مهمة جديدة"""
        title = get_user_input("عنوان المهمة: ")
        if not title:
            print("العنوان مطلوب!")
            return
        
        description = get_user_input("وصف المهمة (اختياري): ", "")
        due_date = get_user_input("تاريخ الاستحقاق (YYYY-MM-DD, اختياري): ", "")
        
        if due_date and not validate_date(due_date):
            print("صيغة التاريخ غير صحيحة! يجب أن تكون YYYY-MM-DD")
            due_date = ""
        
        priority = get_user_input("الأولوية (1-منخفض, 2-متوسط, 3-عالي, الافتراضي 1): ", "1")
        try:
            priority = int(priority)
            if priority not in (1, 2, 3):
                raise ValueError
        except ValueError:
            print("الأولوية يجب أن تكون 1, 2, أو 3. تم تعيينها إلى 1.")
            priority = 1
        
        category = get_user_input("الفئة (اختياري): ", "")
        
        task = Task(
            id=0,  # سيتم تعيينه تلقائياً
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category=category
        )
        
        new_task = self.storage.add_task(task)
        print(f"\nتمت إضافة المهمة بنجاح:")
        print_task_details(new_task)
    
    def list_tasks(self, args):
        """عرض جميع المهام"""
        tasks = self.storage.get_all_tasks()
        print_tasks_table(tasks, "جميع المهام")
    
    def show_task(self, args):
        """عرض تفاصيل مهمة محددة"""
        if not args.task_id:
            print("يجب تحديد معرف المهمة")
            return
        
        task = self.storage.get_task(args.task_id)
        if task:
            print_task_details(task)
        else:
            print(f"لم يتم العثور على مهمة بالمعرف #{args.task_id}")
    
    def complete_task(self, args):
        """تمييز مهمة كمكتملة"""
        if not args.task_id:
            print("يجب تحديد معرف المهمة")
            return
        
        task = self.storage.get_task(args.task_id)
        if task:
            if task.completed:
                print(f"المهمة #{task.id} مكتملة بالفعل")
            else:
                task.completed = True
                self.storage.update_task(task)
                print(f"تم تمييز المهمة #{task.id} كمكتملة")
        else:
            print(f"لم يتم العثور على مهمة بالمعرف #{args.task_id}")
    
    def delete_task(self, args):
        """حذف مهمة"""
        if not args.task_id:
            print("يجب تحديد معرف المهمة")
            return
        
        if self.storage.delete_task(args.task_id):
            print(f"تم حذف المهمة #{args.task_id}")
        else:
            print(f"لم يتم العثور على مهمة بالمعرف #{args.task_id}")
    
    def update_task(self, args):
        """تحديث مهمة"""
        if not args.task_id:
            print("يجب تحديد معرف المهمة")
            return
        
        task = self.storage.get_task(args.task_id)
        if not task:
            print(f"لم يتم العثور على مهمة بالمعرف #{args.task_id}")
            return
        
        print("اترك الحقل فارغاً للحفاظ على القيمة الحالية")
        print_task_details(task)
        
        title = get_user_input("العنوان الجديد: ", task.title)
        description = get_user_input("الوصف الجديد: ", task.description)
        due_date = get_user_input("تاريخ الاستحقاق الجديد (YYYY-MM-DD): ", task.due_date)
        
        if due_date and not validate_date(due_date):
            print("صيغة التاريخ غير صحيحة! يجب أن تكون YYYY-MM-DD")
            due_date = task.due_date
        
        priority = get_user_input("الأولوية الجديدة (1-منخفض, 2-متوسط, 3-عالي): ", str(task.priority))
        try:
            priority = int(priority)
            if priority not in (1, 2, 3):
                raise ValueError
        except ValueError:
            print("الأولوية يجب أن تكون 1, 2, أو 3. تم الحفاظ على القيمة الحالية.")
            priority = task.priority
        
        category = get_user_input("الفئة الجديدة: ", task.category)
        
        # تحديث المهمة
        task.title = title
        task.description = description
        task.due_date = due_date
        task.priority = priority
        task.category = category
        
        if self.storage.update_task(task):
            print("\nتم تحديث المهمة بنجاح:")
            print_task_details(task)
        else:
            print("فشل تحديث المهمة")
    
    def search_tasks(self, args):
        """بحث في المهام"""
        if not args.query:
            print("يجب تقديم نص للبحث")
            return
        
        tasks = self.storage.search_tasks(args.query)
        print_tasks_table(tasks, f"نتائج البحث عن '{args.query}'")
    
    def filter_tasks(self, args):
        """تصفية المهام"""
        completed = None
        if args.completed == "yes":
            completed = True
        elif args.completed == "no":
            completed = False
        
        priority = None
        if args.priority:
            try:
                priority = int(args.priority)
                if priority not in (1, 2, 3):
                    raise ValueError
            except ValueError:
                print("الأولوية يجب أن تكون 1, 2, أو 3. سيتم تجاهل عامل التصفية.")
                priority = None
        
        tasks = self.storage.filter_tasks(
            completed=completed,
            priority=priority,
            category=args.category
        )
        
        # بناء عنوان التصفية
        title_parts = []
        if completed is not None:
            title_parts.append("مكتملة" if completed else "غير مكتملة")
        if priority:
            title_parts.append(f"الأولوية {priority}")
        if args.category:
            title_parts.append(f"الفئة '{args.category}'")
        
        title = "المهام المصفاة: " + ", ".join(title_parts) if title_parts else "المهام المصفاة"
        print_tasks_table(tasks, title)
    
    def run(self):
        """تشغيل الواجهة الرئيسية"""
        parser = argparse.ArgumentParser(
            description=f"{APP_NAME} v{VERSION}",
            epilog=f"بواسطة {AUTHOR}"
        )
        subparsers = parser.add_subparsers(title="الأوامر", dest="command")
        
        # إضافة مهمة
        add_parser = subparsers.add_parser("add", help="إضافة مهمة جديدة")
        add_parser.set_defaults(func=self.add_task)
        
        # عرض المهام
        list_parser = subparsers.add_parser("list", help="عرض جميع المهام")
        list_parser.set_defaults(func=self.list_tasks)
        
        # عرض مهمة
        show_parser = subparsers.add_parser("show", help="عرض تفاصيل مهمة")
        show_parser.add_argument("task_id", type=int, help="معرف المهمة")
        show_parser.set_defaults(func=self.show_task)
        
        # إكمال مهمة
        complete_parser = subparsers.add_parser("complete", help="تمييز مهمة كمكتملة")
        complete_parser.add_argument("task_id", type=int, help="معرف المهمة")
        complete_parser.set_defaults(func=self.complete_task)
        
        # حذف مهمة
        delete_parser = subparsers.add_parser("delete", help="حذف مهمة")
        delete_parser.add_argument("task_id", type=int, help="معرف المهمة")
        delete_parser.set_defaults(func=self.delete_task)
        
        # تحديث مهمة
        update_parser = subparsers.add_parser("update", help="تحديث مهمة")
        update_parser.add_argument("task_id", type=int, help="معرف المهمة")
        update_parser.set_defaults(func=self.update_task)
        
        # بحث
        search_parser = subparsers.add_parser("search", help="بحث في المهام")
        search_parser.add_argument("query", help="نص البحث")
        search_parser.set_defaults(func=self.search_tasks)
        
        # تصفية
        filter_parser = subparsers.add_parser("filter", help="تصفية المهام")
        filter_parser.add_argument("--completed", choices=["yes", "no"], help="عرض المهام المكتملة أو غير المكتملة")
        filter_parser.add_argument("--priority", type=int, choices=[1, 2, 3], help="تصفية حسب الأولوية (1-3)")
        filter_parser.add_argument("--category", help="تصفية حسب الفئة")
        filter_parser.set_defaults(func=self.filter_tasks)
        
        # معلومات النسخة
        parser.add_argument("-v", "--version", action="version", version=f"{APP_NAME} v{VERSION}")
        
        # نوع التخزين
        parser.add_argument("--storage", choices=["json", "sqlite"], default=DEFAULT_STORAGE, 
                          help=f"نوع التخزين (افتراضي: {DEFAULT_STORAGE})")
        
        args = parser.parse_args()
        
        if hasattr(args, "storage"):
            self.storage_type = args.storage
            self.storage = Storage(args.storage)
        
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()

if __name__ == "__main__":
    cli = TaskManagerCLI()
    cli.run()