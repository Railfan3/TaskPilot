# task_data.py
import json
import os
from encryption import encrypt_data, decrypt_data
from task_utils import Task

TASK_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    try:
        with open(TASK_FILE, 'r') as f:
            encrypted = f.read()
            if encrypted.strip() == '':
                return []
            data = decrypt_data(encrypted)
            task_dicts = json.loads(data)
            return [Task.from_dict(t) for t in task_dicts]
    except Exception as e:
        print(f"❗ Failed to load tasks: {e}")
        return []

def save_tasks(tasks):
    try:
        data = json.dumps([t.to_dict() for t in tasks], indent=2)
        encrypted = encrypt_data(data)
        with open(TASK_FILE, 'w') as f:
            f.write(encrypted)
    except Exception as e:
        print(f"❗ Failed to save tasks: {e}")
