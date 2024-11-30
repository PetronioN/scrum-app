class Task:
    def __init__(self, title, description, assigned_to, status="To Do"):
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.status = status

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "assigned_to": self.assigned_to,
            "status": self.status
        }

    def __str__(self):
        return f"[{self.status}] Tarefa: {self.title}, Responsável: {self.assigned_to}"
