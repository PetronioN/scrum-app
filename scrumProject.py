from task import Task
from datetime import datetime, timedelta
import json

def load_project(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}

def save_project(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

class ScrumProject:
    def __init__(self, project_name, scrum_master):
        self.project_name = project_name
        self.scrum_master = scrum_master
        self.product_backlog = []
        self.sprint_planning_date = None
        self.daily_scrum_time = None
        self.sprint_duration = 0

    def add_task_to_backlog(self, title, description, assigned_to):
        task = Task(title, description, assigned_to)
        self.product_backlog.append(task)

    def set_sprint_planning(self, date):
        self.sprint_planning_date = datetime.strptime(date, "%Y-%m-%d")

    def set_daily_scrum(self, time):
        self.daily_scrum_time = datetime.strptime(time, "%H:%M").time()

    def set_sprint_duration(self, days):
        self.sprint_duration = days

    def view_backlog(self):
        backlog_info = "\nBacklog do Produto:\n"
        for i, task in enumerate(self.product_backlog, 1):
            backlog_info += f"{i}. {task}\n"
        return backlog_info

    def start_sprint(self):
        today = datetime.today()
        if not self.sprint_planning_date:
            return "Reunião de Planejamento da Sprint ainda não foi agendada."
        
        if today.date() < self.sprint_planning_date.date():
            return f"A Sprint não pode começar antes da Reunião de Planejamento em {self.sprint_planning_date.date()}"
        else:
            sprint_end_date = today + timedelta(days=self.sprint_duration)
            return f"Sprint iniciada! Ela terminará em {sprint_end_date.date()}."

    def show_scrum_info(self):
        info = f"\nProjeto: {self.project_name}\n"
        info += f"Scrum Master: {self.scrum_master}\n"
        info += f"Data da Reunião de Planejamento da Sprint: {self.sprint_planning_date.date() if self.sprint_planning_date else 'Não definida'}\n"
        info += f"Horário do Daily Scrum: {self.daily_scrum_time if self.daily_scrum_time else 'Não definido'}\n"
        return info

    def to_dict(self):
        return {
            "project_name": self.project_name,
            "scrum_master": self.scrum_master,
            "sprint_planning_date": self.sprint_planning_date.strftime("%Y-%m-%d") if self.sprint_planning_date else None,
            "daily_scrum_time": self.daily_scrum_time.strftime("%H:%M") if self.daily_scrum_time else None,
            "sprint_duration": self.sprint_duration,
            "product_backlog": [task.to_dict() for task in self.product_backlog]
        }