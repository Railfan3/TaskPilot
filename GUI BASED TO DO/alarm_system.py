# alarm_system.py
import time
from datetime import datetime
import platform
import winsound
from task_data import load_tasks
from task_utils import parse_task_datetime


def alarm_system():
    while True:
        try:
            now = datetime.now()
            tasks = load_tasks()
            for task in tasks:
                if task.due and task.time and not task.completed:
                    try:
                        task_time = parse_task_datetime(task.due, task.time)
                        remaining = task_time - now
                        if 0 <= remaining.total_seconds() <= 60:
                            print(f"\n🔔 Alarm: '{task.title}' at {task_time.strftime('%Y-%m-%d %I:%M %p')}!")
                            if platform.system() == "Windows":
                                winsound.Beep(1500, 500)
                    except Exception as e:
                        print(f"⚠️ Alarm error: {e}")
        except Exception as ex:
            print(f"⚠️ Alarm System Crash: {ex}")
        time.sleep(30)
