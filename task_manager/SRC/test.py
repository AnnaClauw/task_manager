# import sys
import os
import unittest
from datetime import datetime, timedelta
from business_logic import TaskService
from data_access import TaskRepository

# Ensure the SRC directory is in the Python path
# sys.path.insert(0, os.path.abspath(
# os.path.join(os.path.dirname(__file__), '../SRC')))


class TestAddTasks(unittest.TestCase):

    def setUp(self):
        # Setup code to initialize TaskService instance before each test
        self.task_service = TaskService()
        self.task_service.task_repo = TaskRepository()

    def tearDown(self):
        tasks_file = 'tasks.json'
        if os.path.exists(tasks_file):
            with open(tasks_file, 'w') as f:
                f.write("[]\n")
            print("Deleted tasks")
        super().tearDown()

    def test_add_single_task(self):
        # Test Case 1: Add a single task
        title = 'Task 1'
        description = 'This is the first task'
        deadline = datetime.now() + timedelta(days=2)
        est_comp_time = 2  # in hours

        self.task_service.add_task(title, description, deadline, est_comp_time)
        tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, title)
        self.assertEqual(tasks[0].description, description)
        super().tearDown()

    def test_add_multiple_tasks(self):
        # Test Case 2: Add multiple tasks
        task1_details = {
            'title': 'Task A',
            'description': 'This is the first task of test 2',
            'deadline': datetime.now() + timedelta(days=2),
            'est_comp_time': 2
        }
        task2_details = {
            'title': 'Task 2',
            'description': 'This is the second task',
            'deadline': datetime.now() + timedelta(days=3),
            'est_comp_time': 3
        }

        self.task_service.add_task(**task1_details)
        self.task_service.add_task(**task2_details)
        tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, task1_details['title'])
        self.assertEqual(tasks[1].title, task2_details['title'])
        super().tearDown()

    def test_add_task_with_past_deadline(self):
        # Test Case 3: Add task with a past deadline
        title = 'Task with past deadline'
        description = 'This task has a deadline in the past'
        deadline = datetime.now() - timedelta(days=1)
        est_comp_time = 2

        with self.assertRaises(ValueError):
            self.task_service.add_task(title,
                                       description,
                                       deadline,
                                       est_comp_time)
        super().tearDown()

    def test_add_task_with_long_title(self):
        # Test Case 4: Add task with a very long title
        title = 'A' * 256  # Assuming title length limit is 255 characters
        description = 'This task has a very long title'
        deadline = datetime.now() + timedelta(days=2)
        est_comp_time = 2

        with self.assertRaises(ValueError):
            self.task_service.add_task(title,
                                       description,
                                       deadline,
                                       est_comp_time)
        super().tearDown()


class TestUpdateTasks(unittest.TestCase):

    def setUp(self):
        # Setup code to initialize TaskService instance before each test
        self.task_service = TaskService()
        self.task_service.task_repo = TaskRepository()
        # Add a task to be updated later
        title = 'Initial Task'
        description = 'This is the initial task'
        deadline = datetime.now() + timedelta(days=2)
        est_comp_time = 2
        self.task_service.add_task(title, description, deadline, est_comp_time)
        self.initial_task = self.task_service.task_repo.get_all_tasks()[0]

    def tearDown(self):
        tasks_file = 'tasks.json'
        if os.path.exists(tasks_file):
            with open(tasks_file, 'w') as f:
                f.write("[]\n")
            print("Deleted tasks")
        super().tearDown()

    def test_update_existing_task(self):
        # Test Case 1: Update an existing task
        task_id = self.initial_task.id
        updates = {
            'title': 'Updated Task',
            'description': 'This is the updated task',
            'deadline': datetime.now() + timedelta(days=5),
            'est_comp_time': 3,  # in hours
            'completed': True
        }

        self.task_service.update_task(task_id, **updates)
        updated_task = self.task_service.task_repo.get_task_by_id(task_id)

        self.assertEqual(updated_task.title, updates['title'])
        self.assertEqual(updated_task.description, updates['description'])
        self.assertEqual(updated_task.deadline, updates['deadline'])
        self.assertEqual(updated_task.est_comp_time, updates['est_comp_time'])
        self.assertTrue(updated_task.completed)

    def test_update_nonexistent_task(self):
        # Test Case 2: Try to update a nonexistent task
        nonexistent_task_id = 999
        updates = {
            'title': 'Nonexistent Task',
            'description': 'This task does not exist',
            'deadline': datetime.now() + timedelta(days=5),
            'est_comp_time': 3
        }

        self.task_service.update_task(nonexistent_task_id, **updates)
        updated_task = self.task_service.task_repo.get_task_by_id(
            nonexistent_task_id)
        self.assertIsNone(updated_task)


if __name__ == '__main__':
    unittest.main()
