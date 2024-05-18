from datetime import datetime, timedelta


class Task:
    next_id = 1

    def __init__(
        self,
        title,
        description,
        deadline,
        est_comp_time,
        completed=False
            ):
        self.id = Task.next_id
        Task.next_id += 1
        self.title = title
        self.description = description
        self.deadline = deadline
        self.est_comp_time = est_comp_time
        self.completed = completed
        self.time_added = datetime.today()
        self.last_updated = self.time_added

    def __repr__(self):
        return (
            f"Task("
            f"title='{self.title}', "
            f"description='{self.description}', "
            f"deadline='{self.deadline}', "
            f"est_comp_time='{self.est_comp_time}', "
            f"completed={self.completed}, "
            f"time_added='{self.time_added}', "
            f"last_updated='{self.last_updated}')"
        )

    def update_task_details(self,
                            title=None,
                            description=None,
                            deadline=None,
                            est_comp_time=None,
                            completed=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if deadline is not None:
            self.deadline = deadline
        if est_comp_time is not None:
            self.est_comp_time = est_comp_time
        if completed is not None:
            self.completed = completed
        self.last_updated = datetime.today()

    def get_remaining_time(self):
        if self.deadline:
            remaining_time = self.deadline - datetime.today()
            return (remaining_time
                    if remaining_time.days >= 0 else timedelta(days=0))
        return None

    def get_task_info(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "est_comp_time": self.est_comp_time,
            "completed": self.completed,
            "time_added": self.time_added,
            "last_updated": self.last_updated
        }

    def __str__(self):
        return (
            f"Task ID {self.id}: {self.title} - "
            f"Status: {'Completed' if self.completed else 'Pending'}\n"
            f"  Description: {self.description}\n"
            f"  Deadline: {self.deadline}\n"
            f"  Estimated Completion Time: {self.est_comp_time} hours\n"
            f"  Time Added: {self.time_added}\n"
            f"  Last Updated: {self.last_updated}"
        )
