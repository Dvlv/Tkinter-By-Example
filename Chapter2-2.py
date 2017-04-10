import tkinter as tk
import tkinter.messagebox as msg

class Todo(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks

        self.items_canvas = tk.Canvas(self)

        self.items_frame = tk.Frame(self.items_canvas)
        self.text_frame = tk.Frame(self)

        self.scrollbar = tk.Scrollbar(self.items_canvas, orient='vertical', command=self.items_canvas.yview)

        self.items_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.title("To-Do App v1")
        self.geometry("300x400")

        self.task_create = tk.Text(self.text_frame, height=3, bg="white", fg="black")

        self.items_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_frame = self.items_canvas.create_window((0, 0), window=self.items_frame, anchor="n")

        self.task_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.task_create.focus_set()

        self.todo1 = tk.Label(self.items_frame, text="--- Add Items Here ---", bg="lightgrey", fg="black", pady=10)
        self.todo1.bind("<Button-1>", self.remove_item)

        self.tasks.append(self.todo1)

        for task in self.tasks:
            task.pack(side=tk.TOP, fill=tk.X)

        self.bind("<Return>", self.add_item)
        self.bind('<Configure>', self.on_frame_configure)
        self.bind_all('<MouseWheel>', self.mouse_scroll)
        self.bind_all('<Button-4>', self.mouse_scroll)
        self.bind_all('<Button-5>', self.mouse_scroll)
        self.items_canvas.bind('<Configure>', self.task_width)

        self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

    def add_item(self, evt):
        item_text = self.task_create.get(1.0,tk.END).strip()

        if len(item_text) > 0:
            new_item = tk.Label(self.items_frame, text=item_text, pady=10)

            _, item_style_choice = divmod(len(self.tasks), 2)

            my_scheme_choice = self.colour_schemes[item_style_choice]

            new_item.configure(bg=my_scheme_choice["bg"])
            new_item.configure(fg=my_scheme_choice["fg"])
            new_item.bind("<Button-1>", self.remove_item)

            new_item.pack(side=tk.TOP, fill=tk.X)

            self.tasks.append(new_item)

        self.task_create.delete(1.0, tk.END)

    def remove_item(self, evt):
        item = evt.widget
        if msg.askyesno('Really Delete?', 'Delete ' + item.cget('text') + '?'):
            self.tasks.remove(evt.widget)
            evt.widget.destroy()

    def on_frame_configure(self, event):
        self.items_canvas.configure(scrollregion=self.items_canvas.bbox("all"))

    def task_width(self, event):
        canvas_width = event.width
        self.items_canvas.itemconfig(self.canvas_frame, width = canvas_width)

    def mouse_scroll(self, event):
        if event.delta:
            self.items_canvas.yview_scroll(-1*(event.delta/120), 'units')
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            self.items_canvas.yview_scroll(move, 'units')

if __name__ == "__main__":
    todo = Todo()
    todo.mainloop()
