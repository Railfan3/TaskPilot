✅ TaskPilot - CLI To-Do List Manager
TaskPilot is a powerful and secure command-line based To-Do List Manager designed for productivity-focused users. With features like task categorization, priority levels, due dates, notifications, and encrypted storage, TaskPilot helps you organize your daily tasks efficiently — all from your terminal.

📌 Features
✅ Add, View, and Remove Tasks via CLI

📂 Categorize tasks by project, type, or context

⚙️ Set priority levels and due dates

🔒 Encrypted JSON storage for task safety

🕑 Alarm and notification support for upcoming deadlines

📊 Daily/Weekly productivity reports

🔁 Support for recurring tasks (e.g., daily meetings)

📅 Calendar-friendly structure

⏳ Countdown timers for urgent tasks

🚀 Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/taskpilot-cli.git
cd taskpilot-cli
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies (if any):

bash
Copy
Edit
pip install -r requirements.txt
For basic use, no external libraries are required unless using alarms or encryption modules.

🛠️ Usage
Run the main script:

bash
Copy
Edit
python cli_main.py
🧭 Available Commands (Sample Navigation):
Action	Command Example
Add a task	add
View tasks	view
Remove a task	remove
Mark as completed	done
Filter by category	filter --category Work
View due today	due today
Show reports	report daily
Export to file	export tasks.json

🔐 Encryption
Tasks are securely stored in an encrypted JSON file. Encryption logic is handled via encryption.py.
You can update the encryption key logic inside the initialize_encryption() function.

📦 File Structure
pgsql
Copy
Edit
taskpilot-cli/
│
├── cli_main.py         # CLI entry point
├── task_manager.py     # Core task operations
├── task_data.py        # Task data model & storage
├── encryption.py       # File encryption support
├── reports.py          # Productivity report generator
├── alarm_system.py     # Optional alarm/notification
├── tasks.json          # Encrypted task storage
└── README.md
🌟 Coming Soon
📥 Import tasks from CSV or JSON

📆 Google Calendar integration

🌐 Web-based dashboard (PyQt6 / React UI)

🧠 AI-based task priority suggestions


📄 License
This project is licensed under the MIT License.
This project is licensed under the MIT License.

