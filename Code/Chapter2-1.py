#! /usr/bin/env python
"""*********************************************************************
In this chapter we'll be creating a basic to-do list. Here we'll learn
about the following:
    -- Allowing the user to enter text
    -- Binding functions to keypresses
    -- Dynamically generating widgets
    -- Scrolling an area
    -- Storing data (with sqlite)
*********************************************************************"""
try:
    import tkinter as tk
except ImportError:
    # Python 2
    import Tkinter as tk

class Todo(tk.Tk):
    """We start off by defining our Todo class and initialising
    it with an empty list of tasks."""
    def __init__(self, tasks=""):
        try:
            super(Todo, self).__init__()
        except TypeError:
            # Python 2
            tk.Tk.__init__(self)

        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks

        self.title("To-Do App v1")
        self.geometry("300x400")

        todo1 = tk.Label(self, text="--- Add Items Here ---", bg="lightgrey", fg="black", pady=10)

        self.tasks.append(todo1)

        for task in self.tasks:
            task.pack(side=tk.TOP, fill=tk.X)

        self.task_create = tk.Text(self, height=3, bg="white", fg="black")

        self.task_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.task_create.focus_set()

        self.bind("<Return>", self.add_task)

        self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

    def add_task(self, event=None):
        """
        When adding a new item, the first thing to do is get the text which the user entered
        into our Text widget.
        The arguments here tell the widget how much of the text to grab.
        """
        task_text = self.task_create.get(1.0, tk.END).strip()

        if task_text:
            new_task = tk.Label(self, text=task_text, pady=10)

            _, task_style_choice = divmod(len(self.tasks), 2)

            my_scheme_choice = self.colour_schemes[task_style_choice]

            new_task.configure(bg=my_scheme_choice["bg"])
            new_task.configure(fg=my_scheme_choice["fg"])

            new_task.pack(side=tk.TOP, fill=tk.X)

            self.tasks.append(new_task)

        self.task_create.delete(1.0, tk.END)

if __name__ == "__main__":
    TODO = Todo()
    TODO.mainloop()
