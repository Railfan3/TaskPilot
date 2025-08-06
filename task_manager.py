# task_manager.py (Advanced CLI Task Manager - TaskPilot CLI)

import json
import os
import time
from datetime import datetime, timedelta
from encryption import encrypt_data, decrypt_data
import platform

if platform.system() == "Windows":
    import winsound

TASK_FILE = "storage/tasks.json"

class Task:
    def __init__(self, title, category="General", due=None, time=None, completed=False, recurring=None):
        self.title = title
        self.category = category
        self.due = due
        self.time = time
        self.completed = completed
        self.recurring = recurring

    def to_dict(self):
        return self.__dict__

def save_tasks(tasks):
    with open(TASK_FILE, "wb") as f:
        json_data = json.dumps([t.to_dict() for t in tasks])
        f.write(encrypt_data(json_data))

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "rb") as f:
        try:
            decrypted = decrypt_data(f.read())
            data = json.loads(decrypted)
            return [Task(**t) for t in data]
        except Exception:
            return []

def parse_task_datetime(date_str):
    date_formats = [
        "%Y-%m-%d",  # 2025-08-05
        "%d-%m-%Y",  # 05-08-2025
        "%d/%m/%Y",  # 05/08/2025
        "%m-%d-%Y",  # 08-05-2025
    ]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError("❌ Invalid date format. Use YYYY-MM-DD, DD-MM-YYYY, DD/MM/YYYY, or MM-DD-YYYY")
def parse_time(time_str):
    formats = ["%I:%M %p", "%H:%M", "%I.%M %p"]  # 12:30 PM, 23:30, 12.30 PM
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt).strftime("%I:%M %p")
        except ValueError:
            continue
    raise ValueError("Invalid time format. Try '12:30 PM', '23:30' or '12.30 PM'.")

def add_task():
    title = input("📝 Task Title: ")
    category = input("📂 Category (default: General): ") or "General"

    due = input("📅 Due Date (e.g., 2025-08-05, 05/08/2025 or leave blank): ").strip()
    if due:
        try:
            due = parse_task_datetime(due)
        except ValueError as e:
            print(f"❌ {e}")
            return
    else:
        due = None

    time_str = input("⏰ Due Time (e.g., 12:30 PM, 23:30 or leave blank): ").strip()
    if time_str:
        try:
            time_str = parse_time(time_str)
        except ValueError as e:
            print(f"❌ {e}")
            return
    else:
        time_str = None

    recurring = input("🔁 Recurring (daily/weekly/monthly/none): ").strip().lower()
    if recurring not in ["daily", "weekly", "monthly",]:
        recurring = None

    task = Task(title, category, str(due) if due else "", time_str if time_str else "", False, recurring)
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added successfully.")

def list_tasks(filter_category=None):
    tasks = load_tasks()
    if filter_category:
        tasks = [t for t in tasks if t.category.lower() == filter_category.lower()]

    for i, task in enumerate(tasks, 1):
        status = "✅" if task.completed else "❌"
        print(f"{i}. {task.title} [{task.category}] - {task.due or '-'} {task.time or ''} | {status}")

def complete_task():
    tasks = load_tasks()
    list_tasks()
    try:
        idx = int(input("Enter task number to complete: ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx].completed = True
            save_tasks(tasks)
            print("✅ Task marked as completed.")
    except:
        print("❗ Invalid input.")

def delete_task():
    tasks = load_tasks()
    list_tasks()
    try:
        idx = int(input("Enter task number to delete: ")) - 1
        if 0 <= idx < len(tasks):
            tasks.pop(idx)
            save_tasks(tasks)
            print("🗑️ Task deleted.")
    except:
        print("❗ Invalid input.")

def show_upcoming():
    tasks = load_tasks()
    now = datetime.now()
    for task in tasks:
        if task.due and task.time:
            try:
                task_time = parse_task_datetime(task.due, task.time)
                remaining = task_time - now
                if 0 <= remaining.total_seconds() <= 3600:
                    print(f"⏰ Upcoming: {task.title} at {task_time.strftime('%Y-%m-%d %I:%M %p')} ({remaining})")
                    if platform.system() == "Windows":
                        winsound.Beep(1500, 300)
            except Exception as e:
                print(f"⚠️ Error with alarm: {e}")

def handle_recurring_tasks():
    tasks = load_tasks()
    updated = False
    now = datetime.now()
    for task in tasks:
        if task.completed and task.recurring:
            try:
                due_time = parse_task_datetime(task.due, task.time)
                if task.recurring == "daily":
                    next_due = due_time + timedelta(days=1)
                elif task.recurring == "weekly":
                    next_due = due_time + timedelta(weeks=1)
                elif task.recurring == "monthly":
                    next_due = due_time + timedelta(days=30)

                else:
                    continue
                task.due = next_due.strftime("%Y-%m-%d")
                task.time = next_due.strftime("%I:%M %p")
                task.completed = False
                updated = True
            except:
                continue
    if updated:
        save_tasks(tasks)

def main():
    handle_recurring_tasks()
    show_upcoming()
    
    while True:
        print("\n=== TaskPilot CLI Menu ===")
        print("1. ➕ Add Task")
        print("2. 📋 List Tasks")
        print("3. ✅ Complete Task")
        print("4. 🗑️ Delete Task")
        print("5. 🚪 Exit")

        choice = input("👉 Choose: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            break
        else:
            print("❗ Invalid option.")

if __name__ == "__main__":
    main()