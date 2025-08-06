import sys
import json
import os
import hashlib
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QPushButton, QLabel, 
                            QLineEdit, QTextEdit, QComboBox, QDateEdit, 
                            QTimeEdit, QCheckBox, QListWidget, QListWidgetItem,
                            QTabWidget, QProgressBar, QMessageBox, QDialog,
                            QDialogButtonBox, QFrame, QScrollArea, QGroupBox,
                            QSystemTrayIcon, QMenu, QSplitter, QStackedWidget)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QDate, QTime, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QPixmap, QPainter, QBrush, QPen
from encryption import initialize_encryption, encrypt_data, decrypt_data

USERS_FILE = "storage/users.json"
TASK_FILE_TEMPLATE = "storage/tasks_{username}.json"

class UserManager:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    
    @staticmethod
    def save_user(username, password):
        os.makedirs("storage", exist_ok=True)
        users = UserManager.load_users()
        users[username] = {
            "password": UserManager.hash_password(password),
            "created_at": datetime.now().isoformat()
        }
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)
    
    @staticmethod
    def load_users():
        if not os.path.exists(USERS_FILE):
            return {}
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    
    @staticmethod
    def validate_user(username, password):
        users = UserManager.load_users()
        if username in users:
            return users[username]["password"] == UserManager.hash_password(password)
        
        return False
    
    @staticmethod
    def user_exists(username):
        users = UserManager.load_users()
        return username in users

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TaskPilot - Login")
        self.setFixedSize(450, 550)
        
        self.username = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        # Logo/Title
        title_label = QLabel("🚀 TaskPilot")
        title_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
        """)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle = QLabel("Professional Task Management")
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: rgba(255,255,255,0.9); margin-bottom: 30px;")
        layout.addWidget(subtitle)
        
        # Login form container
        form_container = QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background: rgba(255,255,255,0.95);
                border-radius: 20px;
                padding: 30px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        
        # Username
        username_label = QLabel("👤 Username:")
        username_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        username_label.setStyleSheet("color: black; margin-bottom: 5px; padding: 2px;")
        form_layout.addWidget(username_label)
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter your username...")
        self.username_edit.setStyleSheet("""
            QLineEdit {
                padding: 3px;
                border: 2px;
                border-radius: 2px;
                font-size: 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
        """)
        form_layout.addWidget(self.username_edit)
        
        # Password
        password_label = QLabel("🔒 Password:")
        password_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        password_label.setStyleSheet("color: black; margin-bottom: 5px; padding: 2px;")
        form_layout.addWidget(password_label)
        
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Enter your password...")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setStyleSheet("""
            QLineEdit {
                padding: 3px;
                border: 2px;
                border-radius: 2px;
                font-size: 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2) ;
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
        """)
        form_layout.addWidget(self.password_edit)
        
        # Password criteria
        criteria_label = QLabel("""
Password Requirements:
• Minimum 8 characters
• At least one uppercase letter
• At least one lowercase letter
• At least one number
• At least one special character (!@#$%^&*)
        """)
        criteria_label.setFont(QFont("Arial", 10))
        criteria_label.setStyleSheet("color: #666; background: #f8f9fa; padding: 10px; border-radius: 5px;")
        form_layout.addWidget(criteria_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.login_btn = QPushButton("🔑 Login")
        self.login_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold)
        )
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #20c997);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 2px 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #218838, stop:1 #1a9870);
            }
        """)
        self.login_btn.clicked.connect(self.login)
        button_layout.addWidget(self.login_btn)
        
        self.register_btn = QPushButton("📝 Register")
        self.register_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #138496);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 2px 3px;
                font-weight: bold;
                                       
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #138496, stop:1 #117a8b);
            }
        """)
        self.register_btn.clicked.connect(self.register)
        button_layout.addWidget(self.register_btn)
        
        form_layout.addLayout(button_layout)
        layout.addWidget(form_container)
        
        # Connect Enter key to login
        self.username_edit.returnPressed.connect(self.login)
        self.password_edit.returnPressed.connect(self.login)
        
    def validate_password(self, password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        if not any(c in "!@#$%^&*" for c in password):
            return False, "Password must contain at least one special character (!@#$%^&*)"
        return True, "Password is valid"
        
    def login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password!")
            return
            
        if UserManager.validate_user(username, password):
            self.username = username
            QMessageBox.information(self, "Success", f"Welcome back, {username}!")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Invalid username or password!")
            
    def register(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password!")
            return
            
        if len(username) < 3:
            QMessageBox.warning(self, "Error", "Username must be at least 3 characters long!")
            return
            
        is_valid, message = self.validate_password(password)
        if not is_valid:
            QMessageBox.warning(self, "Invalid Password", message)
            return
            
        if UserManager.user_exists(username):
            QMessageBox.warning(self, "Error", "Username already exists!")
            return
            
        UserManager.save_user(username, password)
        self.username = username
        QMessageBox.information(self, "Success", f"Account created successfully! Welcome, {username}!")
        self.accept()

class Task:
    def __init__(self, title, category="General", due=None, time=None, completed=False, recurring=None, priority="Medium"):
        self.title = title
        self.category = category
        self.due = due
        self.time = time
        self.completed = completed
        self.recurring = recurring
        self.priority = priority
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return self.__dict__

class TaskManager:
    @staticmethod

    

    def save_tasks(tasks, username):
        os.makedirs("storage", exist_ok=True)
        task_file = TASK_FILE_TEMPLATE.format(username=username)
        with open(task_file, "wb") as f:
            json_data = json.dumps([t.to_dict() for t in tasks])
            f.write(encrypt_data(json_data))

    @staticmethod
    def load_tasks(username):
        task_file = TASK_FILE_TEMPLATE.format(username=username)
        if not os.path.exists(task_file):
            return []
        try:
            with open(task_file, "rb") as f:
                decrypted = decrypt_data(f.read())
                data = json.loads(decrypted)
                return [Task(**t) for t in data]
        except Exception:
            return []
        






class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a67d8, stop:1 #6b46c1);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4c51bf, stop:1 #553c9a);
            }
        """)

class TaskCard(QFrame):
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.parent_widget = parent
        self.setup_ui()
        
    def setup_ui(self):
        self.setFrameStyle(QFrame.Shape.Box)
        self.setFixedHeight(160)
        
        # Color coding based on priority and status
        if self.task.completed:
            bg_color = "#d4edda"
            border_color = "#28a745"
            text_color = "#155724"
        elif self.task.priority == "High":
            bg_color = "#f8d7da"
            border_color = "#dc3545"
            text_color = "#721c24"
        elif self.task.priority == "Medium":
            bg_color = "#fff3cd"
            border_color = "#ffc107"
            text_color = "#856404"
        else:
            bg_color = "#d1ecf1"
            border_color = "#17a2b8"
            text_color = "#0c5460"
            
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 3px solid {border_color};
                border-radius: 15px;
                margin: 8px;
                padding: 12px;
            }}
            QFrame:hover {{
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
                transform: translateY(-3px);
                border-width: 4px;
            }}
            QLabel {{
                color: {text_color};
                font-weight: bold;
                background: transparent;
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Header with title and status
        header_layout = QHBoxLayout()
        
        # Status icon
        status_icon = "✅" if self.task.completed else "⏳"
        priority_icon = {"High": "🔴", "Medium": "🟡", "Low": "🔵"}
        
        title_label = QLabel(f"{status_icon} {priority_icon.get(self.task.priority, '🔵')} {self.task.title}")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet(f"""
            QLabel {{
                color: black;
                font-weight: bold;
                font-size: 14px;
                padding: 2px;
                                  
            }}
        """)
        header_layout.addWidget(title_label)
        
        # Complete button
        if not self.task.completed:
            complete_btn = QPushButton("✓ Complete")
            complete_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            complete_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #28a745, stop:1 #20c997);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 15px;
                    font-size: 11px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #218838, stop:1 #1a9870);
                }
            """)
            complete_btn.clicked.connect(self.complete_task)
            header_layout.addWidget(complete_btn)
        
        layout.addLayout(header_layout)
        
        # Details
        details_layout = QGridLayout()
        details_layout.setSpacing(6)
        
        # Format dates and times properly
        due_text = "No date"
        if self.task.due:
            try:
                due_date = datetime.strptime(self.task.due, "%Y-%m-%d")
                due_text = due_date.strftime("%B %d, %Y")
            except:
                due_text = self.task.due
                
        time_text = "No time"
        if self.task.time:
            time_text = self.task.time
        
        recurring_text = "None"
        if self.task.recurring:
            recurring_text = self.task.recurring.title()
        
        # Create detail labels with better styling
        category_label = QLabel(f"📂 Category: {self.task.category}")
        category_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        due_label = QLabel(f"📅 Due: {due_text}")
        due_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        time_label = QLabel(f"⏰ Time: {time_text}")
        time_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        priority_label = QLabel(f"⚡ Priority: {self.task.priority}")
        priority_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        recurring_label = QLabel(f"🔁 Recurring: {recurring_text}")
        recurring_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        details_layout.addWidget(category_label, 0, 0)
        details_layout.addWidget(due_label, 0, 1)
        details_layout.addWidget(time_label, 1, 0)
        details_layout.addWidget(priority_label, 1, 1)
        details_layout.addWidget(recurring_label, 2, 0, 1, 2)
        
        layout.addLayout(details_layout)
        
        # Delete button
        delete_btn = QPushButton("🗑️ Delete Task")
        delete_btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        delete_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #c82333);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c82333, stop:1 #bd2130);
            }
        """)
        delete_btn.clicked.connect(self.delete_task)
        layout.addWidget(delete_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
    def complete_task(self):
        self.task.completed = True
        if self.parent_widget:
            self.parent_widget.refresh_tasks()
            
    def delete_task(self):
        reply = QMessageBox.question(self, 'Delete Task', 
                                   f'Are you sure you want to delete "{self.task.title}"?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes and self.parent_widget:
            self.parent_widget.remove_task(self.task)

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Task")
        self.setFixedSize(600, 650)
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border-radius: 15px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("📝 Create New Task")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
                padding: 15px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
        """)
        layout.addWidget(title_label)
        
        # Form container
        form_container = QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #e9ecef;
                padding: 20px;
            }
        """)
        form_layout = QGridLayout(form_container)
        form_layout.setSpacing(15)
        
        # Improved styling
        label_style = """
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 14px;
                padding: 5px;
            }
        """
        
        input_style = """
            QLineEdit, QComboBox, QDateEdit, QTimeEdit {
                padding: 12px;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                font-size: 14px;
                background-color: #ffffff;
                color: #2c3e50;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus {
                border-color: #667eea;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
                background: #667eea;
                border-radius: 4px;
            }
            QDateEdit::drop-down, QTimeEdit::drop-down {
                background: #667eea;
                border: none;
                width: 30px;
                border-radius: 4px;
            }
        """
        
        # Task title (mandatory)
        title_lbl = QLabel("📌 Task Title: *")
        title_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_lbl.setStyleSheet(label_style + "color: #dc3545;")  # Red for mandatory
        form_layout.addWidget(title_lbl, 0, 0)
        
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter your task title here... (Required)")
        self.title_edit.setStyleSheet(input_style)
        form_layout.addWidget(self.title_edit, 0, 1)
        
        # Category (mandatory)
        cat_lbl = QLabel("📂 Category: *")
        cat_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        cat_lbl.setStyleSheet(label_style + "color: #dc3545;")  # Red for mandatory
        form_layout.addWidget(cat_lbl, 1, 0)
        
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.addItems(["General", "Work", "Personal", "Health", "Shopping", "Education"])
        self.category_combo.setStyleSheet("""
QComboBox {
        padding: 5px;
        border: 2px solid #ced4da;
        border-radius: 6px;
        background-color: white;
        color: black;
        font-size: 14px;
    }
    QComboBox QAbstractItemView {
        background-color: white;
        color: black;
        selection-background-color: #f8f9fa;
        selection-color: black;
    }
 """)
        form_layout.addWidget(self.category_combo, 1, 1)
        
        # Priority (mandatory)
        priority_lbl = QLabel("⚡ Priority: *")
        priority_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        priority_lbl.setStyleSheet(label_style + "color: #dc3545;")  # Red for mandatory  #dc3545
        form_layout.addWidget(priority_lbl, 2, 0)
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["High", "Medium", "Low"])
        self.priority_combo.setCurrentText("Medium",)
        self.priority_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
        border: 2px solid #ced4da;
        border-radius: 6px;
        background-color: white;
        color: black;
        font-size: 14px;
                                           }
        QComboBox QAbstractItemView {
        background-color: white;
        color: black;
        selection-background-color: #f8f9fa;
        selection-color: black;
           } """
            )
        

        form_layout.addWidget(self.priority_combo, 2, 1)
        
        # Due date
        date_lbl = QLabel("📅 Due Date:")
        date_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        date_lbl.setStyleSheet(label_style)
        form_layout.addWidget(date_lbl, 3, 0)
        
        date_container = QWidget()
        date_layout = QHBoxLayout(date_container)
        date_layout.setContentsMargins(0, 0, 0, 0)
        
        self.date_checkbox = QCheckBox("Set due date")
        self.date_checkbox.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.date_checkbox.setStyleSheet("""
            QCheckBox {
                color: #2c3e50;
                font-weight: bold;
                spacing: 8px;
                padding: 2px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #667eea;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #667eea;
            }
        """)
        
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setEnabled(False)
        self.date_edit.setStyleSheet(input_style)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("MMMM dd, yyyy")  # Better format
        self.date_checkbox.toggled.connect(self.date_edit.setEnabled)
        
        date_layout.addWidget(self.date_checkbox)
        date_layout.addWidget(self.date_edit)
        form_layout.addWidget(date_container, 3, 1)
        
        # Due time
        time_lbl = QLabel("⏰ Due Time:")
        time_lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        time_lbl.setStyleSheet(label_style)
        form_layout.addWidget(time_lbl, 4, 0)
        
        time_container = QWidget()
        time_layout = QHBoxLayout(time_container)
        time_layout.setContentsMargins(0, 0, 0, 0)
        
        self.time_checkbox = QCheckBox("Set due time")
        self.time_checkbox.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.time_checkbox.setStyleSheet("""
            QCheckBox {
                color: #2c3e50;
                font-weight: bold;
                spacing: 8px;
                padding: 2px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #667eea;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #667eea;
            }
        """)
        
        self.time_edit = QTimeEdit(QTime.currentTime())
        self.time_edit.setEnabled(False)
        self.time_edit.setStyleSheet(input_style)
        self.time_edit.setDisplayFormat("hh:mm AP")  # 12-hour format
        self.time_checkbox.toggled.connect(self.time_edit.setEnabled)
        
        time_layout.addWidget(self.time_checkbox)
        time_layout.addWidget(self.time_edit)
        form_layout.addWidget(time_container, 4, 1)
        
        # Recurring
        recurring_lbl = QLabel("🔁 Recurring:")
        recurring_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        recurring_lbl.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                                    font-weight: bold;
                                    font-size: 14px;
                                    padding: 5px;
                                    }""")
            
         
        form_layout.addWidget(recurring_lbl, 5, 0)
        
        self.recurring_combo = QComboBox()
        self.recurring_combo.addItems(["None", "Daily", "Weekly", "Monthly"])
        self.recurring_combo.setStyleSheet("""
            QComboBox {
                                          padding: 5px;
        border: 2px solid #ced4da;
        border-radius: 6px;
        background-color: white;
        color: black;
        font-size: 14px;
    }
    QComboBox QAbstractItemView {
        background-color: white;
        color: black;
        selection-background-color: #f8f9fa;
        selection-color: black;
    }"""
                                           )
        form_layout.addWidget(self.recurring_combo, 5, 1)
       
        
        # Mandatory fields note
        mandatory_note = QLabel("* Required fields")
        mandatory_note.setFont(QFont("Arial", 8, QFont.Weight.Bold))
        mandatory_note.setStyleSheet("color: #dc3545; margin-top: 10px; padding: 2px; font-style: italic; font-size: 8px;")
        form_layout.addWidget(mandatory_note, 6, 0, 1, 2)
        
        layout.addWidget(form_container)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.setStyleSheet("""
            QDialogButtonBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #20c997);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-weight: bold;
                font-size: 14px;
                margin: 5px;
                min-width: 120px;
            }
            QDialogButtonBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #218838, stop:1 #1a9870);
            }
            QDialogButtonBox QPushButton[text="Cancel"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #c82333);
            }
            QDialogButtonBox QPushButton[text="Cancel"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c82333, stop:1 #bd2130);
            }
        """)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def get_task_data(self):
        due_date = self.date_edit.date().toString("yyyy-MM-dd") if self.date_checkbox.isChecked() else None
        due_time = self.time_edit.time().toString("hh:mm AP") if self.time_checkbox.isChecked() else None
        recurring = self.recurring_combo.currentText() if self.recurring_combo.currentText() != "None" else None
        
        return {
            "title": self.title_edit.text().strip(),
            "category": self.category_combo.currentText(),
            "priority": self.priority_combo.currentText(),
            "due": due_date,
            "time": due_time,
            "recurring": recurring.lower() if recurring else None
        }

class ProductivityWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)



    








        
        # Title
        title = QLabel("📈 Productivity Dashboard")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("""
            QLabel {
                color: white;
                margin-bottom: 20px;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Stats container
        stats_widget = QWidget()
        stats_widget.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 15px;
                border: 3px solid #e9ecef;
                padding: 5px;
            }
        """)
        stats_layout = QGridLayout(stats_widget)
        stats_layout.setSpacing(15)
        
        # Progress bars
        self.daily_progress = QProgressBar()
        self.weekly_progress = QProgressBar()
        self.monthly_progress = QProgressBar()
        
        for progress in [self.daily_progress, self.weekly_progress, self.monthly_progress]:
            progress.setStyleSheet("""
                QProgressBar {
                    border: 3px solid #ddd;
                    border-radius: 10px;
                    text-align: center;
                    font-weight: bold;
                    font-size: 14px;
                    color: #2c3e50;
                    background-color: #f8f9fa;
                    min-height: 25px;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #667eea, stop:1 #764ba2);
                    border-radius: 7px;
                }
            """)
        
        # Progress labels
        daily_lbl = QLabel("📅 Daily Progress:")
        daily_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        daily_lbl.setStyleSheet("color: #2c3e50; font-weight: bold; padding: 5px;")
        stats_layout.addWidget(daily_lbl, 0, 0)
        stats_layout.addWidget(self.daily_progress, 0, 1)
        
        weekly_lbl = QLabel("📊 Weekly Progress:")
        weekly_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        weekly_lbl.setStyleSheet("color: #2c3e50; font-weight: bold; padding: 5px;")
        stats_layout.addWidget(weekly_lbl, 1, 0)
        stats_layout.addWidget(self.weekly_progress, 1, 1)
        
        monthly_lbl = QLabel("📈 Monthly Progress:")
        monthly_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        monthly_lbl.setStyleSheet("color: #2c3e50; font-weight: bold; padding: 5px;")
        stats_layout.addWidget(monthly_lbl, 2, 0)
        stats_layout.addWidget(self.monthly_progress, 2, 1)
        
        layout.addWidget(stats_widget)
        
        # Task statistics
        self.stats_label = QLabel()
        self.stats_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        self.stats_label.setStyleSheet("""
            QLabel {
                background: white;
                border: 3px solid #e9ecef;
                border-radius: 15px;
                padding: 25px;
                font-size: 14px;
                color: #2c3e50;
                font-weight: bold;
                line-height: 1.6;
            }
        """)
        layout.addWidget(self.stats_label)
        
    def update_stats(self, tasks):
        today = datetime.today().date()
        
        # Calculate statistics
        daily_completed = daily_total = 0
        weekly_completed = weekly_total = 0
        monthly_completed = monthly_total = 0
        
        for task in tasks:
            if not task.due:
                continue
                
            try:
                task_date = datetime.strptime(task.due, "%Y-%m-%d").date()
                
                # Daily stats
                if task_date == today:
                    daily_total += 1
                    if task.completed:
                        daily_completed += 1
                
                # Weekly stats
                if (today - task_date).days <= 7 and task_date <= today:
                    weekly_total += 1
                    if task.completed:
                        weekly_completed += 1
                
                # Monthly stats
                if task_date.month == today.month and task_date.year == today.year:
                    monthly_total += 1
                    if task.completed:
                        monthly_completed += 1
                        
            except:
                continue
        
        # Update progress bars
        self.daily_progress.setValue(int((daily_completed / daily_total * 100) if daily_total else 0))
        self.weekly_progress.setValue(int((weekly_completed / weekly_total * 100) if weekly_total else 0))
        self.monthly_progress.setValue(int((monthly_completed / monthly_total * 100) if monthly_total else 0))
        
        # Update statistics text
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.completed])
        pending_tasks = total_tasks - completed_tasks
        high_priority = len([t for t in tasks if t.priority == "High" and not t.completed])
        
        stats_text = f"""
📊 Overall Statistics:

Total Tasks: {total_tasks}
✅ Completed: {completed_tasks}
⏳ Pending: {pending_tasks}
🔴 High Priority Pending: {high_priority}

📅 Today: {daily_completed}/{daily_total} completed
📊 This Week: {weekly_completed}/{weekly_total} completed
📈 This Month: {monthly_completed}/{monthly_total} completed
        """
        
        self.stats_label.setText(stats_text)

class TaskPilotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.current_user = None
        
        

        self.login_successful = False
        self.setup_login()
        
        if self.login_successful:
            if self.login_successful:
             self.setup_ui()        # ✅ this creates tasks_layout
             QTimer.singleShot(0, self.load_tasks)  # ✅ this runs load_tasks AFTER UI is ready

            
            # Setup timer for auto-refresh
            self.timer = QTimer()
            self.timer.timeout.connect(self.refresh_tasks)
            self.timer.start(30000)  # Refresh every 30 seconds
        
    def setup_login(self):
        login_dialog = LoginDialog()
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            self.current_user = login_dialog.username
            self.login_successful = True
            return login_dialog.username
        else:
            sys.exit()



           
    def setup_ui(self):
    # Set window title with user name
       self.setWindowTitle(f"TaskPilot - Welcome {self.current_user}")
       self.setGeometry(100, 100, 1200, 800)

    # Apply basic background style
       self.setStyleSheet("""
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #f8f9fa, stop:1 #e9ecef);
        }
    """)

    # Setup main tab widget
       self.tabs = QTabWidget()
       self.setCentralWidget(self.tabs)

    # ✅ Create and add tasks tab (important: this defines self.tasks_layout)
       self.tasks_tab = self.create_tasks_tab()
       self.tabs.addTab(self.tasks_tab, "📋 Tasks")
 
    # ✅ Now safe to call refresh_tasks
       self.refresh_tasks()

    # Optionally add other tabs later (Reports, Settings, etc.)
    
    



    def add_task(self):
        dialog = AddTaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
         task_data = dialog.get_task_data()

        # Validate mandatory fields
        if not task_data["title"].strip():
            QMessageBox.warning(self, "Validation Error", "Task title is required!")
            return

        if not task_data["category"].strip():
            QMessageBox.warning(self, "Validation Error", "Category is required!")
            return

        if not task_data["priority"]:
            QMessageBox.warning(self, "Validation Error", "Priority is required!")
            return

        task = Task(**task_data)
        self.tasks.append(task)

        # ✅ Debug output
        print(f"[DEBUG] Current user: {self.current_user}")
        print(f"[DEBUG] Saving {len(self.tasks)} tasks for {self.current_user}")

        TaskManager.save_tasks(self.tasks, self.current_user)
        self.refresh_tasks()
        QMessageBox.information(self, "Success", "Task added successfully!")







        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                background: white;
            }
            QTabBar::tab {
                background: #e9ecef;
                padding: 12px 24px;
                margin: 2px;
                border-radius: 6px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
            }
        """)
        
        # Add tabs
        self.tasks_tab = self.create_tasks_tab()
        self.productivity_tab = ProductivityWidget()
        
        self.tab_widget.addTab(self.tasks_tab, "📋 Tasks")
        self.tab_widget.addTab(self.productivity_tab, "📈 Analytics")
        
        main_layout.addWidget(self.tab_widget)
        
        # Status bar
        self.statusBar().showMessage(f"Welcome {self.current_user} - TaskPilot Professional")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background: #495057;
                color: white;
                font-weight: bold;
            }
        """)
        
    def create_header(self):
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
                margin: 10px;
            }
        """)
        
        layout = QHBoxLayout(header)
        
        # Logo and title with user welcome
        title_label = QLabel(f"🚀 TaskPilot - Welcome, {self.current_user}!")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white; margin-left: 20px;")
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # Add task button
        add_btn = AnimatedButton("➕ Add New Task")
        add_btn.clicked.connect(self.add_task)
        layout.addWidget(add_btn)
        
        # Refresh button
        refresh_btn = AnimatedButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_tasks)
        layout.addWidget(refresh_btn)
        
        # Logout button
        logout_btn = AnimatedButton("🚪 Logout")
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #c82333);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c82333, stop:1 #bd2130);
            }
        """)
        layout.addWidget(logout_btn)
        
        return header
        
    def create_tasks_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Filter controls
        filter_widget = QWidget()
        filter_widget.setStyleSheet("""
            QWidget {
                background: rgba(255,255,255,0.9);
                border-radius: 10px;
                border: 1px solid #dee2e6;
                padding: 2px;
                margin: 5px;
            }
        """)
        filter_layout = QHBoxLayout(filter_widget)
        
        # Category filter
        cat_filter_lbl = QLabel("📂 Filter by Category:")
        cat_filter_lbl.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        cat_filter_lbl.setStyleSheet("""color: white; font-weight: bold; padding: 2px;
                                     background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                                        font-color: white;
                                     """)
        filter_layout.addWidget(cat_filter_lbl)
        
        self.category_filter = QComboBox()
        self.category_filter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.category_filter.setStyleSheet("""
            QComboBox {
                padding: 2px;
                border: 2px solid #dee2e6;
                border-radius: 6px;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                font-color: white;
                font-weight: bold;
                min-width: 150px;
            }
            QComboBox:focus {
                border-color: #667eea;
            }
        """)
        self.category_filter.addItem("All Categories")
      
        self.category_filter.currentTextChanged.connect(self.filter_tasks)
        filter_layout.addWidget(self.category_filter)
        self.category_filter.addItems(["Work", "Personal", "Health", "Shopping", "Education"])
        filter_layout.addSpacing(20)
        
        # Status filter
        status_filter_lbl = QLabel("📊 Filter by Status:")
        status_filter_lbl.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        status_filter_lbl.setStyleSheet("""color: white; font-weight: bold;
                                       background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                                        padding: 2px;
                                        font-color: white;
                                        """)
        filter_layout.addWidget(status_filter_lbl)
        
        self.status_filter = QComboBox()
        self.status_filter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.status_filter.setStyleSheet("""
            QComboBox {
                padding: 25px;
                border: 2px solid #dee2e6;
                border-radius: 6px;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                font-weight: bold;
                min-width: 150px;
                                         font-color: white;
            }
            QComboBox:focus {
                border-color: #667eea;
            }
        """)
        self.status_filter.addItems(["All Tasks", "Pending", "Completed"])
        self.status_filter.setCurrentText("All Tasks")
        
        self.status_filter.currentTextChanged.connect(self.filter_tasks)
        filter_layout.addWidget(self.status_filter)
        filter_layout.addSpacing(20)

    
        
        filter_layout.addStretch()
        
        layout.addWidget(filter_widget)

        # ➕ Add Task Button — next to filters
        add_task_btn = QPushButton("➕ Add Task")
        add_task_btn.setFixedHeight(80)
        add_task_btn.setStyleSheet("""
    QPushButton {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
        color: white;
        font-size: 15px;
        padding: 2px;
        border: none;
        border-radius: 4px;
                                   min-width: 120px;
        font-weight: bold;
                                   fontcolor: white;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")
        add_task_btn.clicked.connect(self.add_task)
        filter_layout.addWidget(add_task_btn)

        
        # Tasks scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
                font-color: #2c3e50;
            }
            QScrollBar:vertical {
                background: white;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: white;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: white;
            }
        """)
        
        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.addStretch()
        
        self.scroll_area.setWidget(self.tasks_container)
        layout.addWidget(self.scroll_area)

        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        


        

            # ⬇️ Filter Bar (your existing code)
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
    # ... add category and status filters ...
        layout.addWidget(filter_widget)

    # ⬇️ Task Cards
        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.addStretch()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.tasks_container)

        layout.addWidget(self.scroll_area)

        return widget


        
        
    

    


        
    def load_tasks(self):
        self.tasks = TaskManager.load_tasks(self.current_user)
        self.refresh_tasks()


    


    
    
    def refresh_tasks(self):
    # Clear existing task cards
     for i in reversed(range(self.tasks_layout.count() - 1)):  # -1 to keep the stretch
        child = self.tasks_layout.itemAt(i).widget()
        if child:
            child.setParent(None)

            if not self.tasks:
               label = QLabel("No tasks added yet. Click ➕ Add Task to get started!")
               label.setAlignment(Qt.AlignmentFlag.AlignCenter)
               label.setStyleSheet("font-size: 16px; color: black; padding: 20px;")
               self.tasks_layout.addWidget(label)
               return


    # Update category filter
     categories = set(task.category for task in self.tasks)
     current_category = self.category_filter.currentText()
     self.category_filter.clear()
     self.category_filter.addItem("All Categories")
     self.category_filter.addItems(sorted(categories))
     if current_category in [self.category_filter.itemText(i) for i in range(self.category_filter.count())]:
        self.category_filter.setCurrentText(current_category)

    

    
     
        
    def filter_tasks(self):
        # Clear existing task cards
        for i in reversed(range(self.tasks_layout.count() - 1)):
            child = self.tasks_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Apply filters
        category_filter = self.category_filter.currentText()
        status_filter = self.status_filter.currentText()
        
        filtered_tasks = self.tasks
        
        if category_filter != "All Categories":
            filtered_tasks = [t for t in filtered_tasks if t.category == category_filter]
            
        if status_filter == "Pending":
            filtered_tasks = [t for t in filtered_tasks if not t.completed]
        elif status_filter == "Completed":
            filtered_tasks = [t for t in filtered_tasks if t.completed]
        
        # Sort tasks by priority and due date
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        filtered_tasks.sort(key=lambda t: (
            t.completed,  # Completed tasks last
            priority_order.get(t.priority, 1),  # By priority
            t.due or "9999-12-31"  # By due date
        ))
        
        # Add task cards
        for task in filtered_tasks:
            card = TaskCard(task, self)
            self.tasks_layout.insertWidget(self.tasks_layout.count() - 1, card)
            
    def add_task(self):
        dialog = AddTaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            task_data = dialog.get_task_data()
            
            # Validate mandatory fields
            if not task_data["title"].strip():
                QMessageBox.warning(self, "Validation Error", "Task title is required!")
                return
                
            if not task_data["category"].strip():
                QMessageBox.warning(self, "Validation Error", "Category is required!")
                return
                
            if not task_data["priority"]:
                QMessageBox.warning(self, "Validation Error", "Priority is required!")
                return
            
            task = Task(**task_data)
            self.tasks.append(task)
            TaskManager.save_tasks(self.tasks, self.current_user)
            self.refresh_tasks()
            QMessageBox.information(self, "Success", "Task added successfully!")

                
    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            TaskManager.save_tasks(self.tasks, self.current_user)
            self.refresh_tasks()
    
    def logout(self):
        reply = QMessageBox.question(self, 'Logout', 
                                   f'Are you sure you want to logout, {self.current_user}?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            # Restart the application to show login screen
            QApplication.quit()
            QApplication.processEvents()
            app = QApplication(sys.argv)
            window = TaskPilotGUI()
            if window.login_successful:
                window.show()
                sys.exit(app.exec())




def save_tasks_to_file(task_list, file_path="tasks.json"):
    try:
        with open(file_path, "w") as f:
            json.dump(task_list, f, indent=4)
    except Exception as e:
        print("Error saving tasks:", e)


def load_tasks_from_file(file_path="tasks.json"):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading tasks:", e)
                # Return empty list if something fails
            return []
    return []




def main():
    app = QApplication(sys.argv)
    app.setApplicationName("TaskPilot Professional")
    
    # Initialize encryption
    initialize_encryption()
    
    # Create and show main window (with login)
    window = TaskPilotGUI()
    if window.login_successful:
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()