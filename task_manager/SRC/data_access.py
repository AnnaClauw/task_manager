import os
import json
from datetime import datetime
from task import Task  # Import the Task class


class TaskRepository:
    def __init__(self, user_file='users.json', task_file='tasks.json'):
        self.user_file = user_file
        self.task_file = task_file
        self.users = self.load_data(self.user_file)
        self.tasks = self.load_tasks(self.task_file)

    def load_data(self, file_name):
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                json.dump([], f)
        with open(file_name, 'r') as f:
            return json.load(f)

    def load_tasks(self, file_name):
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                json.dump([], f)
        with open(file_name, 'r') as f:
            tasks_data = json.load(f)
            tasks = []
            for task_data in tasks_data:
                task = Task(
                    title=task_data.get('title'),
                    description=task_data.get('description'),
                    deadline=task_data.get('deadline'),
                    est_comp_time=task_data.get('est_comp_time'),
                    completed=task_data.get('completed', False)
                )
                task.id = task_data.get('id', Task.next_id)
                Task.next_id = max(Task.next_id, task.id + 1)
                # Convert string dates back to datetime objects
                if 'time_added' in task_data:
                    task.time_added = datetime.fromisoformat(
                        task_data['time_added'])
                if 'last_updated' in task_data:
                    task.last_updated = datetime.fromisoformat(
                        task_data['last_updated'])
                tasks.append(task)
        return tasks

    def save_data(self, data, file_name):
        # Convert Task instances to dictionaries
        data = [task.__dict__ for task in data]
        # Convert datetime objects to ISO format strings
        for item in data:
            if 'time_added' in item and isinstance(
                    item['time_added'], datetime):
                item['time_added'] = item['time_added'].isoformat()
            if 'last_updated' in item and isinstance(
                    item['last_updated'], datetime):
                item['last_updated'] = item['last_updated'].isoformat()
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

    def get_all_users(self):
        return self.users

    def get_all_tasks(self):
        return self.tasks

    def add_user(self, user):
        self.users.append(user)
        self.save_data(self.users, self.user_file)

    def add_task(self, task):
        self.tasks.append(task)
        self.save_data(self.tasks, self.task_file)

    def get_task_by_id(self, task_id):
        """Get a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, updated_task):
        for idx, task in enumerate(self.tasks):
            if task.id == updated_task.id:
                self.tasks[idx] = updated_task
                self.save_data(self.tasks, self.task_file)
                return
        print(f"Task with ID {updated_task.id} not found.")
