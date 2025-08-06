📋 TaskPilot GUI - Professional To-Do List Manager
TaskPilot GUI is an advanced desktop-based To-Do List Manager developed using PyQt6. Designed for productivity-focused individuals, it offers a clean and intuitive interface for managing tasks with categories, priorities, due dates, alarms, and encrypted storage — all within a visually responsive dashboard.

🌟 Key Features
🖥️ Modern and responsive PyQt6 GUI

➕ Add, edit, and delete tasks easily

📂 Filter tasks by category and status

⏰ Built-in alarm/notification system for reminders

🔐 Secure, encrypted local JSON storage

📊 Daily/Weekly productivity reports

🔁 Support for recurring tasks

📅 Due date tracking with countdown timers

🧭 Sidebar navigation (optional dashboard)

🌙 Light/dark-friendly gradient UI

🛠️ Tech Stack
Frontend: PyQt6 (QWidgets, QVBox/QHBox Layouts, QTabWidget, QScrollArea)

Backend: Python

Storage: Encrypted JSON (custom encryption.py)

Utilities: Task management, alarms, CLI fallback mode

🚀 Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/taskpilot-gui.git
cd taskpilot-gui
Install dependencies:

bash
Copy
Edit
pip install PyQt6
Optionally install plyer for desktop notifications:

bash
Copy
Edit
pip install plyer
▶️ How to Run
bash
Copy
Edit
python taskpilot_gui.py
📂 Project Structure
pgsql
Copy
Edit
taskpilot-gui/
│
├── taskpilot_gui.py       # Main GUI application
├── add_task_dialog.py     # Dialog window for adding new tasks
├── task_manager.py        # Load/save task logic
├── task_data.py           # Task model and serialization
├── alarm_system.py        # Alarm/notification logic
├── encryption.py          # Secure encryption for task files
├── reports.py             # Daily/weekly report generator
├── task_utils.py          # Utility functions
├── assets/                # Icons & UI resources
└── tasks/                 # Encrypted task files per user
🧭 App Overview
🔐 Login System
Each user has their own encrypted task storage for privacy and separation.

🧱 Dashboard Features
Add task (with title, due date, category, status, priority)

View tasks with filters

Sidebar/tab-based navigation

Notifications for upcoming tasks

📅 Filter & Organize
Filter tasks by category

Switch between Pending, Completed, or All Tasks

🔐 Security
Tasks are encrypted using a basic XOR-based encryption (custom logic in encryption.py)

Per-user task isolation with tasks/{username}_tasks.json

💡 Planned Enhancements
🌙 Dark Mode Toggle

🌐 Cloud sync & multi-device support

📆 Google Calendar integration

🧠 Smart reminders using AI

📥 Import/Export (CSV, JSON)

🧑‍🤝‍🧑 Collaboration features



📄 License
This project is licensed under the MIT License.
