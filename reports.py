from task_manager import load_tasks
from datetime import datetime

def show_productivity_report(period="daily"):
    tasks = load_tasks()
    today = datetime.today().date()
    
    completed = 0
    total = 0
    for task in tasks:
        if not task.due:
            continue
        try:
            task_date = datetime.strptime(task.due, "%Y-%m-%d").date()
            if (period == "daily" and task_date == today) or \
               (period == "weekly" and (today - task_date).days <= 7) or \
                (period == "monthly" and task_date.month == today.month and task_date.year == today.year):
                total += 1
                if task.completed:
                    completed += 1
        except:
            continue
    
    print(f"\n📈 {period.capitalize()} Productivity Report")
    print(f"Completed: {completed}/{total} tasks ({(completed/total)*100 if total else 0:.2f}%)")
