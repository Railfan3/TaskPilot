# task_manager.py

import os
import json
import platform
from datetime import datetime, timedelta
import platform

if platform.system() == "Windows":
    import winsound
else:
    winsound = None  # so you can still reference winsound safely

from task_data import Task, load_tasks, save_tasks
from task_utils import parse_date, parse_time, parse_task_datetime

# --- Add Task ---
def add_task():
    title = input("Ὅd Task Title: ")
    category = input("📂 Category (default: General): ") or "General"
    due_input = input("🗕️ Due Date (YYYY-MM-DD or DD-MM-YYYY or leave blank): ").strip()
    time_input = input("⏰ Due Time (e.g., 12:30 PM / 23:30 / 12.30am or leave blank): ").strip()
    recurring = input("🔁 Recurring (daily/weekly/none): ").strip().lower() or None

    due = None
    time_str = None

    if due_input:
        try:
            due = parse_date(due_input).strftime("%Y-%m-%d")
        except Exception as e:
            print(f"⚠️ Invalid date format: {e}")
            return

    if time_input:
        try:
            time_str = parse_time(time_input)
        except Exception as e:
            print(f"⚠️ Invalid time format: {e}")
            return

    if recurring not in ["daily", "weekly"]:
        recurring = None

    task = Task(title, category, due, time_str, False, recurring)
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added successfully.")

# --- View All Tasks ---
def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("❓ No tasks found.")
        return
    print("\n📅 Task List:")
    for idx, task in enumerate(tasks, 1):
        print(f"{idx}. {task.title} [{task.category}] - Due: {task.due or 'N/A'} {task.time or ''} Recurring: {task.recurring or 'No'}")

# --- Show Upcoming Within Hour ---
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

# --- Productivity Report ---
def generate_report():
    tasks = load_tasks()
    completed = sum(1 for task in tasks if task.completed)
    pending = len(tasks) - completed

    today = datetime.now().date()
    weekly = [t for t in tasks if t.due and datetime.strptime(t.due, "%Y-%m-%d").date() >= today - timedelta(days=7)]
    daily = [t for t in weekly if datetime.strptime(t.due, "%Y-%m-%d").date() == today]

    print("\n🌟 Productivity Report:")
    print(f"Total Tasks: {len(tasks)}")
    print(f"Completed: {completed}, Pending: {pending}")
    print(f"Today's Tasks: {len(daily)}, Last 7 Days: {len(weekly)}")

# --- Main CLI ---
def main():
    while True:
        print("""
🔹 Choose:
1. Add Task
2. View Tasks
3. Show Upcoming Tasks
4. Productivity Report
5. Exit
        """)
        choice = input("Enter choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            show_upcoming()
        elif choice == "4":
            generate_report()
        elif choice == "5":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
