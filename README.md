# نظام إدارة المهام (CLI)

```markdown
# 📝 To-Do List CLI System

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)

نظام متكامل لإدارة المهام عبر سطر الأوامر مع ميزات متقدمة:

## ✨ المميزات
- إضافة/تعديل/حذف المهام
- تصفية حسب (الحالة، الأولوية، الفئة)
- دعم تخزين SQLite/JSON
- واجهة سهلة الاستخدام

## 🚀 التشغيل
```bash
cd task_manager
python cli.py
```

## 🔧 الأوامر الأساسية
| الأمر | الوصف | مثال |
|-------|-------|-------|
| `add` | إضافة مهمة | `python cli.py add` |
| `list` | عرض المهام | `python cli.py list` |
| `complete` | إكمال مهمة | `python cli.py complete 1` |
| `delete` | حذف مهمة | `python cli.py delete 1` |

## 📂 الهيكلة
```
task_manager/
├── cli.py
├── storage.py
├── models.py
└── config.py
```

📜 الترخيص: MIT
```

هذا الملف المختصر يحتوي على:
1. عنوان رئيسي مع أيقونة
2. شارة إصدار بايثون
3. قسم المميزات مع أيقونات
4. قسم التشغيل مع الأوامر
5. جدول الأوامر الأساسية
6. هيكلة الملفات المختصرة
7. نوع الترخيص

Developed by Qusai Gamal Al-Absi
