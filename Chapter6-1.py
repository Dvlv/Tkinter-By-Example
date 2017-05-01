import tkinter as tk

class Editor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.FONT_SIZE = 12
        self.FONT_OFFSET = self.FONT_SIZE / 1.5

        self.menubar = tk.Menu(self, bg="lightgrey", fg="black")

        self.file_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.file_menu.add_command(label="New", command=self.file_new, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.file_open, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.file_save, accelerator="Ctrl+S")

        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.configure(menu=self.menubar)

        self.main_text = tk.Text(self, bg="white", fg="black", font=("Ubuntu Mono", self.FONT_SIZE))

        self.main_text.pack()

        self.main_text.bind('<space>', self.display_menu)
        self.main_text.bind('<KeyRelease>', self.display_autofill_menu)

    def file_new(self):
        pass
    def file_open(self):
        pass
    def file_save(self):
        pass
    def display_menu(self, evt):
        self.complete_menu = tk.Menu(self, tearoff=0, bg="lightgrey", fg="black")
        self.complete_menu.add_command(label="test", command=self.file_new)
        coords = str(self.main_text.index(tk.INSERT)).split('.')
        x = int(coords[1])
        y = int(coords[0])
        offset_x = self.main_text.winfo_rootx()
        offset_y = self.main_text.winfo_rooty() + (self.FONT_SIZE * (y/1.5 + 1))
        x *= self.FONT_OFFSET
        y *= self.FONT_OFFSET
        x = int(x)
        y = int(y)
        offset_x = int(offset_x)
        offset_y = int(offset_y)
        self.complete_menu.post(offset_x + x, offset_y + y)
        self.main_text.bind('<Down>', self.focus_menu_item)

    def focus_menu_item(self, evt=None):
        self.complete_menu.focus_set()
        self.complete_menu.entryconfig("test", state="active")

editor = Editor()
editor.mainloop()
