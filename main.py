import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk

def load_projects(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            projects = []
            for project_data in data.get("projects", []):
                project = ScrumProject(
                    project_data['project_name'],
                    project_data['scrum_master'],
                    project_data['sprint_planning_date'],
                    project_data['daily_scrum_time'],
                    project_data['sprint_duration']
                )
                project.product_backlog = [Task(**task) for task in project_data.get('product_backlog', [])]
                project.sprint_tasks = []
                projects.append(project)
            return projects
    except FileNotFoundError:
        return []

def save_projects(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

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

class ScrumProject:
    def __init__(self, project_name, scrum_master, sprint_planning_date=None, daily_scrum_time=None, sprint_duration=0):
        self.project_name = project_name
        self.scrum_master = scrum_master
        self.product_backlog = []
        self.sprint_planning_date = datetime.strptime(sprint_planning_date, "%Y-%m-%d") if sprint_planning_date else None
        self.daily_scrum_time = datetime.strptime(daily_scrum_time, "%H:%M").time() if daily_scrum_time else None
        self.sprint_duration = sprint_duration
        self.sprint_tasks = []

    def set_sprint_info(self, planning_date, daily_time, duration):
        self.sprint_planning_date = planning_date
        self.daily_scrum_time = daily_time
        self.sprint_duration = duration
        return f"Informações da Sprint definidas: Data de Planejamento - {planning_date}, Hora da Daily Scrum - {daily_time}, Duração - {duration} dias."

    def add_task_to_backlog(self, title, description, assigned_to):
        task = Task(title, description, assigned_to)
        self.product_backlog.append(task)

    def start_sprint(self):
        today = datetime.today()
        if not self.sprint_planning_date:
            return "Reunião de Planejamento da Sprint ainda não foi agendada."

        if today.date() < self.sprint_planning_date.date():
            return f"A Sprint não pode começar antes da Reunião de Planejamento em {self.sprint_planning_date.date()}."
        else:
            print("product_backlog", self.product_backlog)
            self.sprint_tasks = self.product_backlog.copy()
            self.product_backlog.clear()
            return f"Sprint iniciada! Ela terminará em {today + timedelta(days=self.sprint_duration)}."

    def view_backlog(self):
        if not self.product_backlog:
            return "Não há tarefas no backlog."

        backlog_info = "\nBacklog do Produto:\n"
        for i, task in enumerate(self.product_backlog, 1):
            backlog_info += f"{i}. {task}\n"
        return backlog_info

    def view_sprint_tasks(self):
        if not self.sprint_tasks:
            return "Não há tarefas na Sprint."

        sprint_info = "\nTarefas da Sprint:\n"
        for i, task in enumerate(self.sprint_tasks, 1):
            sprint_info += f"{i}. {task}\n"
        return sprint_info

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
            "product_backlog": [task.to_dict() for task in self.product_backlog],
            "sprint_tasks": [task.to_dict() for task in self.sprint_tasks]
        }

class ScrumApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciador de Projetos Scrum")
        master.geometry("600x400")
        master.configure(bg="#f0f0f0")

        self.projects = load_projects('projects_data.json')
        self.selected_project = None

        self.project_frame = tk.Frame(master, bg="#ffffff", padx=10, pady=10)
        self.project_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.project_listbox = tk.Listbox(self.project_frame)
        self.project_listbox.pack(fill=tk.BOTH, expand=True)

        self.load_projects()

        button_frame = tk.Frame(master)
        button_frame.pack(pady=5)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.add_project_button = ctk.CTkButton(button_frame, text="Adicionar Projeto", command=self.add_project, fg_color="#4CAF50", hover_color="#45a049")
        self.add_project_button.pack(side="left", padx=5)

        self.select_project_button = ctk.CTkButton(button_frame, text="Selecionar Projeto", command=self.select_project, fg_color="#2196F3", hover_color="#1e88e5")
        self.select_project_button.pack(side="left", padx=5)

    def load_projects(self):
        for widget in self.project_frame.winfo_children():
            widget.destroy()

        for project in self.projects:
            card = ctk.CTkFrame(self.project_frame, fg_color="#333", corner_radius=10)
            card.pack(padx=10, pady=5, fill="x", expand=True)

            project_name_label = ctk.CTkLabel(card, text=project.project_name, font=("Helvetica", 16, "bold"))
            project_name_label.pack(anchor="w", pady=10, padx=10)

            scrum_master_label = ctk.CTkLabel(card, text=f"Scrum Master: {project.scrum_master}", text_color="#666666")
            scrum_master_label.pack(anchor="w", padx=10)

            select_button = ctk.CTkButton(card, text="Selecionar", command=lambda p=project: self.select_project(p), fg_color="#2196F3", hover_color="#1976D2", text_color="white")
            select_button.pack(pady=5)

    def create_project_card(self, project):
        card_frame = ctk.CTkFrame(self.project_frame, fg_color="#f9f9f9", corner_radius=8)
        card_frame.pack(fill="x", padx=5, pady=5)

        project_name_label = ctk.CTkLabel(card_frame, text=project.project_name, font=("Arial", 14, "bold"))
        project_name_label.pack(anchor="w", pady=2)

        scrum_master_label = ctk.CTkLabel(card_frame, text=f"Scrum Master: {project.scrum_master}")
        scrum_master_label.pack(anchor="w")

        select_button = ctk.CTkButton(card_frame, text="Selecionar", command=lambda: self.select_specific_project(project), fg_color="#2196F3", hover_color="#1976D2", text_color="white")
        select_button.pack(pady=5)

    def select_specific_project(self, project):
        self.selected_project = project

        project_info_window = ctk.CTkToplevel(self.master)
        project_info_window.title("Informações do Projeto")
        project_info_window.geometry("400x300")

        info_label = ctk.CTkLabel(project_info_window, text=self.selected_project.show_scrum_info(), fg_color="#f0f0f0", corner_radius=5)
        info_label.pack(pady=10)

        ctk.CTkButton(project_info_window, text="Adicionar Tarefa", command=self.add_task, fg_color="#4CAF50", hover_color="#45A049", text_color="white").pack(pady=5)

        ctk.CTkButton(project_info_window, text="Iniciar Sprint", command=self.start_sprint, fg_color="#2196F3", hover_color="#1976D2", text_color="white").pack(pady=5)

        ctk.CTkButton(project_info_window, text="Visualizar Tarefas da Sprint", command=self.show_sprint_tasks, fg_color="#2196F3", hover_color="#1976D2", text_color="white").pack(pady=5)

        ctk.CTkButton(project_info_window, text="Visualizar Backlog", command=self.show_backlog, fg_color="#2196F3", hover_color="#1976D2", text_color="white").pack(pady=5)

        ctk.CTkButton(project_info_window, text="Definir Informações da Sprint", command=self.set_sprint_info, fg_color="#FF9800", hover_color="#E68A00", text_color="white").pack(pady=5)

    def add_project(self):
        project_name = simpledialog.askstring("Nome do Projeto", "Digite o nome do projeto:")
        scrum_master = simpledialog.askstring("Scrum Master", "Digite o nome do Scrum Master:")
        if project_name and scrum_master:
            new_project = ScrumProject(project_name, scrum_master)
            self.projects.append(new_project)
            save_projects('projects_data.json', {"projects": [project.to_dict() for project in self.projects]})
            self.load_projects()
            messagebox.showinfo("Sucesso", "Projeto adicionado com sucesso!")
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos.")

    def select_project(self, project):
        self.selected_project = project

        project_info_window = tk.Toplevel(self.master)
        project_info_window.title("Informações do Projeto")
        project_info_window.geometry("400x300")

        info_label = tk.Label(project_info_window, text=self.selected_project.show_scrum_info(), bg="#f0f0f0")
        info_label.pack(pady=10)

        tk.Button(project_info_window, text="Adicionar Tarefa", command=self.add_task, bg="#4CAF50", fg="white").pack(pady=5)
        tk.Button(project_info_window, text="Iniciar Sprint", command=self.start_sprint, bg="#2196F3", fg="white").pack(pady=5)
        tk.Button(project_info_window, text="Visualizar Tarefas da Sprint", command=self.show_sprint_tasks, bg="#2196F3", fg="white").pack(pady=5)
        tk.Button(project_info_window, text="Visualizar Backlog", command=self.show_backlog, bg="#2196F3", fg="white").pack(pady=5)
        tk.Button(project_info_window, text="Definir Informações da Sprint", command=self.set_sprint_info, bg="#FF9800", fg="white").pack(pady=5)

    def show_backlog(self):
        if not self.selected_project:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um projeto.")
            return

        backlog_info = self.selected_project.view_backlog()
        messagebox.showinfo("Tarefas do Backlog", backlog_info)

    def add_task(self):
        if not self.selected_project:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um projeto.")
            return

        title = simpledialog.askstring("Título da Tarefa", "Digite o título da tarefa:")
        description = simpledialog.askstring("Descrição da Tarefa", "Digite a descrição da tarefa:")
        assigned_to = simpledialog.askstring("Responsável", "Digite o nome do responsável:")

        if title and description and assigned_to:
            self.selected_project.add_task_to_backlog(title, description, assigned_to)
            save_projects('projects_data.json', {"projects": [project.to_dict() for project in self.projects]})
            messagebox.showinfo("Sucesso", "Tarefa adicionada ao backlog com sucesso!")
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos.")

    def start_sprint(self):
        if not self.selected_project:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um projeto.")
            return

        result = self.selected_project.start_sprint()
        save_projects('projects_data.json', {"projects": [project.to_dict() for project in self.projects]})
        messagebox.showinfo("Iniciar Sprint", result)

    def show_sprint_tasks(self):
        if not self.selected_project:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um projeto.")
            return

        sprint_tasks_info = self.selected_project.view_sprint_tasks()
        messagebox.showinfo("Tarefas da Sprint", sprint_tasks_info)

    def set_sprint_info(self):
        if not self.selected_project:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um projeto.")
            return

        sprint_info_window = tk.Toplevel(self.master)
        sprint_info_window.title("Definir Informações da Sprint")

        tk.Label(sprint_info_window, text="Data da Reunião de Planejamento (YYYY-MM-DD):").pack(pady=5)
        planning_date_entry = tk.Entry(sprint_info_window)
        planning_date_entry.pack(pady=5)

        tk.Label(sprint_info_window, text="Horário da Daily Scrum (HH:MM):").pack(pady=5)
        daily_time_entry = tk.Entry(sprint_info_window)
        daily_time_entry.pack(pady=5)

        tk.Label(sprint_info_window, text="Duração da Sprint (em dias):").pack(pady=5)
        duration_entry = tk.Entry(sprint_info_window)
        duration_entry.pack(pady=5)

        def submit_sprint_info():
            planning_date = planning_date_entry.get()
            daily_time = daily_time_entry.get()
            duration = duration_entry.get()

            try:
                planning_date = datetime.strptime(planning_date, "%Y-%m-%d")
                if daily_time:
                    daily_time = datetime.strptime(daily_time, "%H:%M").time()
                else:
                    daily_time = None

                duration = int(duration) if duration else 0

                message = self.selected_project.set_sprint_info(planning_date, daily_time, duration)
                messagebox.showinfo("Sucesso", message)
                sprint_info_window.destroy()
            except ValueError as e:
                messagebox.showerror("Erro", f"Entrada inválida: {e}")

        tk.Button(sprint_info_window, text="Definir", command=submit_sprint_info, bg="#4CAF50", fg="white").pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScrumApp(root)
    root.mainloop()
