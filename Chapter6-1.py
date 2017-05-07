import tkinter as tk
from tkinter import filedialog
from functools import partial

class Editor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.FONT_SIZE = 12
        self.AUTOCOMPLETE_WORDS = ["def", "import", "if", "else", "while", "for","try:", "except:", "print(", "True", "False"]
        self.WINDOW_TITLE = "Text Editor"

        self.open_file = ""

        self.title(self.WINDOW_TITLE)
        self.geometry("800x600")

        self.menubar = tk.Menu(self, bg="lightgrey", fg="black")

        self.file_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.file_menu.add_command(label="New", command=self.file_new, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.file_open, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.file_save, accelerator="Ctrl+S")

        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.configure(menu=self.menubar)

        self.main_text = tk.Text(self, bg="white", fg="black", font=("Ubuntu Mono", self.FONT_SIZE))

        self.main_text.pack(expand=1, fill=tk.BOTH)

        self.main_text.bind("<space>", self.destroy_autocomplete_menu)
        self.main_text.bind("<KeyRelease>", self.display_autocomplete_menu)
        self.main_text.bind("<Tab>", self.insert_spaces)

        self.bind("<Control-s>", self.file_save)
        self.bind("<Control-o>", self.file_open)
        self.bind("<Control-n>", self.file_new)

    def file_new(self, evt=None):
        file_name = filedialog.asksaveasfilename()
        if file_name:
            self.open_file = file_name
            self.main_text.delete(1.0, tk.END)
            self.title(" - ".join([self.WINDOW_TITLE, self.open_file]))

    def file_open(self, evt=None):
        file_to_open = filedialog.askopenfilename()

        if file_to_open:
            self.open_file = file_to_open
            self.main_text.delete(1.0, tk.END)

            with open(file_to_open, "r") as file_contents:
                file_lines = file_contents.readlines()
                if len(file_lines) > 0:
                    for index, line in enumerate(file_lines):
                        index = float(index) + 1.0
                        self.main_text.insert(index, line)

        self.title(" - ".join([self.WINDOW_TITLE, self.open_file]))

    def file_save(self, evt=None):
        if not self.open_file:
            new_file_name = filedialog.asksaveasfilename()
            if new_file_name:
                self.open_file = new_file_name

        if self.open_file:
            new_contents = self.main_text.get(1.0, tk.END)
            with open(self.open_file, "w") as open_file:
                open_file.write(new_contents)

    def insert_spaces(self, evt=None):
        self.main_text.insert(tk.INSERT, "    ")

        return "break"

    def get_menu_coordinates(self):
        bbox = self.main_text.dlineinfo(tk.INSERT)
        menu_x = bbox[2] + self.winfo_x()
        menu_y = bbox[1] + self.winfo_y() + self.FONT_SIZE + 2

        return (menu_x, menu_y)

    def display_autocomplete_menu(self, evt=None):
        current_index = self.main_text.index(tk.INSERT)
        start = self.adjust_floating_index(current_index)

        try:
            currently_typed_word = self.main_text.get(start + " wordstart", tk.INSERT)
        except tk.TclError:
            currently_typed_word = ""

        currently_typed_word = str(currently_typed_word).strip()

        if currently_typed_word:
            self.destroy_autocomplete_menu()

            suggestions = []
            for word in self.AUTOCOMPLETE_WORDS:
                if word.startswith(currently_typed_word) and not currently_typed_word == word:
                    suggestions.append(word)

            if len(suggestions) > 0:
                x, y = self.get_menu_coordinates()
                self.complete_menu = tk.Menu(self, tearoff=0, bg="lightgrey", fg="black")

                for word in suggestions:
                    insert_word_callback = partial(self.insert_word, word=word, part=currently_typed_word, index=current_index)
                    self.complete_menu.add_command(label=word, command=insert_word_callback)

                self.complete_menu.post(x, y)
                self.main_text.bind("<Down>", self.focus_menu_item)

    def destroy_autocomplete_menu(self, evt=None):
        try:
            self.complete_menu.destroy()
            self.main_text.unbind("<Down>")
        except AttributeError:
            pass

    def insert_word(self, word, part, index):
        amount_typed = len(part)
        remaining_word = word[amount_typed:]
        remaining_word_offset = " +" + str(len(remaining_word)) + "c"
        self.main_text.insert(index, remaining_word)
        self.main_text.mark_set(tk.INSERT, index + remaining_word_offset)
        self.destroy_autocomplete_menu()
        self.main_text.focus_force()

    def adjust_floating_index(self, number):
        indices = number.split(".")
        x_index = indices[0]
        y_index = indices[1]
        y_as_number = int(y_index)
        y_previous = y_as_number - 1

        return ".".join([x_index, str(y_previous)])

    def focus_menu_item(self, evt=None):
        try:
            self.complete_menu.focus_force()
            self.complete_menu.entryconfig(0, state="active")
        except tk.TclError:
            pass

if __name__ == "__main__":
    editor = Editor()
    editor.mainloop()
