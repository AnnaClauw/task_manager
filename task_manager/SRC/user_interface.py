from business_logic import TaskService
from user import User


existing_users = []


def authenticate_user():
    while True:
        username = input("Enter your username: ")
        if any(user.name == username for user in existing_users):
            print("Authentication successful!")
            return username
        else:
            print("Invalid username.")
            choice = input("Would you like to register? (yes/no): ")
            if choice.lower() == "yes":
                return None


def register_user():
    """Register a new user."""
    while True:
        username = input("Enter a username to register: ")
        if any(user.name == username for user in existing_users):
            print("Username already exists. Choose a different username.")
        else:
            existing_users.append(User.create_user(username))
            print("User registration successful!")
            return username


def start_application():
    task_service = TaskService()
    while True:
        print("Task Management Application")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Update Task")
        print("4. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_tasks(task_service)
        elif choice == "2":
            add_task(task_service)
        elif choice == "3":
            update_task(task_service)
        elif choice == "4":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again")


def view_tasks(task_service):
    print("View Tasks")
    print("1. View tasks by estimated completion time")
    print("2. View tasks by deadline")
    print("3. View tasks by adding date")
    choice = input("Enter your choice: ")
    if choice == "1":
        tasks = task_service.sort_tasks_by_est_comp_time()
    elif choice == "2":
        tasks = task_service.sort_tasks_by_deadline()
    elif choice == "3":
        tasks = task_service.sort_tasks_by_time_added()
    else:
        print("Invalid choice. Returning to main menu.")
        return

    print("Tasks:")
    for task in tasks:
        print(f"- {task}")


def add_task(task_service):
    print("Add Task")
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    deadline = input("Enter task deadline (YYYY-MM-DD): ")
    est_comp_time = input(
        "Enter estimated completion time (in hours): ")
    task_service.add_task(title,
                          description,
                          deadline,
                          est_comp_time)
    print("Task added successfully!")


def update_task(task_service):
    print("Update Task")
    task_id = int(input("Enter task ID to update: "))
    # Get new task details
    title = input("Enter new task title"
                  "(leave blank to keep current): ").strip()
    description = input("Enter new task description "
                        "(leave blank to keep current): ").strip()
    deadline = input("Enter new task deadline (YYYY-MM-DD)"
                     "(leave blank to keep current): ").strip()
    est_comp_time = input("Enter new estimated completion time (in hours)"
                          "(leave blank to keep current): ").strip()
    # Ask user if they want to mark the task as completed
    completed_input = input("Mark task as completed? (yes/no, "
                            "leave blank to keep current): ").strip().lower()
    completed = None
    if completed_input == 'yes':
        completed = True
    elif completed_input == 'no':
        completed = False

    # Create a dictionary to hold updated values, excluding empty entries
    update_kwargs = {}
    if title:
        update_kwargs['title'] = title
    if description:
        update_kwargs['description'] = description
    if deadline:
        update_kwargs['deadline'] = deadline
    if est_comp_time:
        update_kwargs['est_comp_time'] = est_comp_time
    if completed is not None:
        update_kwargs['completed'] = completed
    # Update task with provided details
    task_service.update_task(task_id, **update_kwargs)
    print("Task updated successfully!")


if __name__ == "__main__":
    start_application()
