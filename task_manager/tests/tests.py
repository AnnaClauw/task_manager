import unittest
from business_logic import TaskService, Task


class TestTaskService(unittest.TestCase):
    def test_add_task(self):
        """Test the add_task method of TaskService."""
        # Arrange
        task_service = TaskService()
        initial_task_count = len(task_service.get_all_tasks()) # Get initial task count
        new_task = Task(title="New Task", description="Description of the new task")
        # Act
        task_service.add_task(new_task)
        # Assert
        updated_task_count = len(task_service.get_all_tasks()) # Get updated task count
        self.assertEqual(updated_task_count, initial_task_count + 1) #Check if the task count increased by 1
        self.assertIn(new_task, task_service.get_all_tasks()) # Check if the new task is in the list of tasks

if __name__ == "__main__":
    unittest.main()