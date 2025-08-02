import os
import tkinter as tk
from tkinter import ttk, messagebox
import json

class ModernTodo:
    def __init__(self, master):
        self.master = master
        self.master.title("Modern To-Do list")
        self.master.geometry("400x500")
        self.master.configure(bg="black")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", padding=10, font=('Italic', 10))
        style.configure("TEntry", padding=10, font=('Italic', 10))
        style.configure("Treeview", font=('Italic', 10), rowheight=25)
        style.configure("Treeview.Heading", font=('Italic', 11, 'bold'))

        self.frame = ttk.Frame(self.master, padding='10')
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(self.frame, textvariable=self.task_var, width=30)
        self.task_entry.grid(row=0, column=0, padx=5, pady=10, sticky='ew')

        self.add_button = ttk.Button(self.frame, text="Add Task", command=self.add_tasks)
        self.add_button.grid(row=0, column=1, padx=5, pady=10)

        self.task_tree = ttk.Treeview(self.frame, columns=("Task",), show="headings", height=15)
        self.task_tree.heading("Task", text="Tasks")
        self.task_tree.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="nse")

        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        self.delete_button = ttk.Button(self.frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=5, pady=10, sticky='ew')

        self.save_button = ttk.Button(self.frame, text="Save Tasks", command=self.save_task)
        self.save_button.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.load_tasks()

    # These methods should be outside __init__
    def add_tasks(self):
        task = self.task_var.get()
        if task:
            self.task_tree.insert("", tk.END, values=(task,))
            self.task_var.set("")
        else:
            messagebox.showwarning("Warning", "Please enter the task.")

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            self.task_tree.delete(selected_item)
        else:
            messagebox.showwarning("Warning", "Please select the task to delete")

    def save_task(self):
        tasks = [self.task_tree.item(child)['values'][0] for child in self.task_tree.get_children()]
        with open("tasks.json", "w") as f:
            json.dump(tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
            for task in tasks:
                self.task_tree.insert('', tk.END, values=(task,))
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTodo(root)
    root.mainloop()
