import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from scrumProject import ScrumProject, load_project, save_project

class ScrumApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerenciador de Projetos Scrum")
        master.geometry("600x400")  # Tamanho da janela
        master.configure(bg="#f0f0f0")  # Cor de fundo

        self.projects = load_project('projects_data.json')
        self.selected_project = None

        # Frame para gerenciamento de projetos
        self.project_frame = tk.Frame(master, bg="#ffffff", padx=10, pady=10)
        self.project_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.project_listbox = tk.Listbox(self.project_frame)
        self.project_listbox.pack(fill=tk.BOTH, expand=True)

        self.load_projects()

        # Botões
        self.add_project_button = tk.Button(master, text="Adicionar Projeto", command=self.add_project, bg="#4CAF50", fg="white")
        self.add_project_button.pack(pady=5)

        self.select_project_button = tk.Button(master, text="Selecionar Projeto", command=self.select_project, bg="#2196F3", fg="white")
        self.select_project_button.pack(pady=5)

    def load_projects(self):
        self.project_listbox.delete(0, tk.END)  # Limpa a lista
        for project in self.projects:
            self.project_listbox.insert(tk.END, project['project_name'])

    def add_project(self):
        project_name = simpledialog.askstring("Nome do Projeto", "Digite o nome do projeto:")
        scrum_master = simpledialog.askstring("Scrum Master", "Digite o nome do Scrum Master:")
        if project_name and scrum_master:
            new_project = ScrumProject(project_name, scrum_master)
            self.projects.append(new_project.to_dict())
            save_project('projects_data.json', {"projects": self.projects})
            self.load_projects()
            messagebox.showinfo("Sucesso", f"Projeto '{project_name}' adicionado com sucesso!")

    def select_project(self):
        selected_index = self.project_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.selected_project = ScrumProject(**self.projects[index])
            self.show_project_info()
        else:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um projeto.")

    def show_project_info(self):
        project_info_window = tk.Toplevel(self.master)
        project_info_window.title(f"Informações do Projeto: {self.selected_project.project_name}")

        info_text = self.selected_project.show_scrum_info()
        backlog_text = self.selected_project.view_backlog()

        # Exibir informações do projeto
        tk.Label(project_info_window, text=info_text, justify=tk.LEFT).pack(pady=10)

        # Exibir backlog
        tk.Label(project_info_window, text=backlog_text, justify=tk.LEFT).pack(pady=10)

        # Botões para adicionar tarefa e iniciar sprint
        tk.Button(project_info_window, text="Adicionar Tarefa", command=self.add_task, bg="#4CAF50", fg="white").pack(pady=5)
        tk.Button(project_info_window, text="Iniciar Sprint", command=self.start_sprint, bg="#FFC107", fg="black").pack(pady=5)

    def add_task(self):
        if not self.selected_project:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um projeto.")
            return
        
        title = simpledialog.askstring("Título da Tarefa", "Digite o título da tarefa:")
        description = simpledialog.askstring("Descrição da Tarefa", "Digite a descrição da tarefa:")
        assigned_to = simpledialog.askstring("Responsável", "Digite o responsável pela tarefa:")
        if title and description and assigned_to:
            self.selected_project.add_task_to_backlog(title, description, assigned_to)
            messagebox.showinfo("Sucesso", f"Tarefa '{title}' adicionada com sucesso!")

    def start_sprint(self):
        if not self.selected_project:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione um projeto.")
            return
        
        result = self.selected_project.start_sprint()
        messagebox.showinfo("Iniciar Sprint", result)
