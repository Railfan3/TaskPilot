from task_data import load_tasks
from datetime import datetime, timedelta

def show_productivity_report(period="daily"):
    tasks = load_tasks()
    now = datetime.now()
    completed = 0
    total = 0

    if period == "daily":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "weekly":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        print("❗ Invalid period. Use 'daily' or 'weekly'.")
        return

    for task in tasks:
        if task.completed and task.timestamp >= start:
            completed += 1
        if task.timestamp >= start:
            total += 1

    print(f"\n📈 Productivity Report ({period.capitalize()}):")
    print(f"✅ Completed Tasks: {completed}")
    print(f"📋 Total Tasks: {total}")
    if total > 0:
        print(f"📊 Completion Rate: {round((completed / total) * 100, 2)}%")
    else:
        print("📊 No tasks in the selected period.")
