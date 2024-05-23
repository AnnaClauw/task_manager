from datetime import datetime
from task import Task
from data_access import TaskRepository


class TaskService:
    def __init__(self):
        self.task_repo = TaskRepository()

    def add_task(self, title, description, deadline, est_comp_time):
        if not title:
            raise ValueError("Task title is required")
        if len(title) > 255:
            raise ValueError("Task title cannot exceed 255 characters")
        if deadline < datetime.now():
            raise ValueError("Deadline cannot be in the past")

        task = Task(title, description, deadline, est_comp_time)
        self.task_repo.add_task(task)

    def update_task(self, task_id, **kwargs):
        task = self.task_repo.get_task_by_id(task_id)
        if task:
            # Handle the 'completed' status separately if provided
            if 'completed' in kwargs:
                task.completed = kwargs['completed']
            for key, value in kwargs.items():
                if key != 'completed' and value:
                    setattr(task, key, value)
            task.last_updated = datetime.today()
            self.task_repo.update_task(task)
        else:
            print(f"Task with ID {task_id} not found.")

    def get_all_tasks(self):
        """Retrieve all tasks."""
        return self.task_repo.get_all_tasks()

    def sort_tasks_by_deadline(self):
        """Sort tasks by deadline and print them."""
        tasks = self.task_repo.get_all_tasks()
        sorted_tasks = sorted(tasks, key=lambda x: x.deadline)
        for task in sorted_tasks:
            print(task)
        return sorted_tasks

    def sort_tasks_by_est_comp_time(self):
        """Sort tasks by estimated completion time and print them."""
        tasks = self.task_repo.get_all_tasks()
        sorted_tasks = sorted(tasks, key=lambda x: x.est_comp_time)
        for task in sorted_tasks:
            print(task)
        return sorted_tasks

    def sort_tasks_by_time_added(self):
        """Sort tasks by time added and print them."""
        tasks = self.task_repo.get_all_tasks()
        sorted_tasks = sorted(tasks, key=lambda x: x.time_added)
        for task in sorted_tasks:
            print(task)
        return sorted_tasks
