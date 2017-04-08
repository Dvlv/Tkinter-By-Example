import tkinter as tk

class Todo(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks

        self.title("To-Do App v1")
        self.geometry("300x400")

        self.todo1 = tk.Label(self, text="--- Add Items Here ---", bg="lightgrey", fg="black", pady=10)

        self.tasks.append(self.todo1)

        for task in self.tasks:
            task.pack(side=tk.TOP, fill=tk.X)

        self.task_create = tk.Text(self, height=3, bg="white", fg="black")

        self.task_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.task_create.focus_set()

        self.bind("<Return>", self.add_item)

        self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

    def add_item(self, evt):
        item_text = self.task_create.get(1.0,tk.END).strip()

        if len(item_text) > 0:
            new_item = tk.Label(self, text=item_text, pady=10)

            _, item_style_choice = divmod(len(self.tasks), 2)

            my_scheme_choice = self.colour_schemes[item_style_choice]

            new_item.configure(bg=my_scheme_choice["bg"])
            new_item.configure(fg=my_scheme_choice["fg"])

            new_item.pack(side=tk.TOP, fill=tk.X)

            self.tasks.append(new_item)

        self.task_create.delete(1.0, tk.END)

if __name__ == "__main__":
    todo = Todo()
    todo.mainloop()
