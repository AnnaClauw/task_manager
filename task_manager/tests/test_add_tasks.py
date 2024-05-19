import sys
import os
import unittest
from datetime import datetime, timedelta
from SRC.business_logic import TaskService
from SRC.data_access import TaskRepository

# Ensure the SRC directory is in the Python path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../SRC')))


class TestAddTasks(unittest.TestCase):

    def setUp(self):
        # Setup code to initialize TaskService instance before each test
        self.task_service = TaskService()
        self.task_service.task_repo = TaskRepository(test_mode=True)

    def tearDown(self):
        test_tasks_file = 'task_manager/test_tasks.json'
        if os.path.exists(test_tasks_file):
            with open(test_tasks_file, 'w') as f:
                f.write("[]\n")
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
            'title': 'Task 1',
            'description': 'This is the first task',
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


if __name__ == '__main__':
    unittest.main()
