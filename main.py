from task_manager import add_task, list_tasks, complete_task, delete_task
from reports import show_productivity_report
from alarm_system import alarm_system
from encryption import initialize_encryption
import threading


def show_menu():
    while True:
        print("Welcome to 📋 TaskPilot")
        print("1. Your All Tasks")
        print("2. + New Task")
        print("3. Mark Task as done")
        print("4. Delete Task")
        print("5. Category view")
        print("6. Productivity Report")
        print("7. Exit")

        choice = input("👉 Choose: ").strip()

        if choice == '1':
            list_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            complete_task()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            cat = input("Enter category: ")
            list_tasks(filter_category=cat)
        elif choice == '6':
            p = input("Type (daily/weekly): ").strip().lower()
            show_productivity_report(period=p)
        elif choice == '7':
            print("👋 Thankyou for using TaskPilot.")
            break
        else:
            print("❗ Invalid option. Try again.")


if __name__ == "__main__":
    initialize_encryption()
    threading.Thread(target=alarm_system, daemon=True).start()
    show_menu()
