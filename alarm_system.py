from datetime import datetime, timedelta
from task_manager import load_tasks, save_tasks
from plyer import notification
import time
import os

def alarm_system():
    while True:
        now = datetime.now()
        tasks = load_tasks()
        updated = False

        for task in tasks:
            if not task.completed and task.due and task.time:
                try:
                    dt = datetime.strptime(f"{task.due} {task.time}", "%Y-%m-%d %I:%M %p")
                    if now.strftime("%Y-%m-%d %I:%M %p") == dt.strftime("%Y-%m-%d %I:%M %p"):
                        print(f"\n🔔 ALARM: '{task.title}' is due now!")
                        try:
                            notification.notify(
                                title="Task Reminder",
                                message=f"{task.title} is due now!",
                                timeout=10
                            )
                            if os.name == 'nt':
                                os.system('echo \a')
                        except:
                            pass

                        if task.recurring == "daily":
                            dt += timedelta(days=1)
                            task.due = dt.strftime("%Y-%m-%d")
                            updated = True
                        elif task.recurring == "weekly":
                            dt += timedelta(weeks=1)
                            task.due = dt.strftime("%Y-%m-%d")
                            updated = True
                except Exception as e:
                    print(f"⚠️ Error with alarm: {e}")

        if updated:
            save_tasks(tasks)
        time.sleep(30)
