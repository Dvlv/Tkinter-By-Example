import tkinter as tk
from tkinter import filedialog
from functools import partial

class Editor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.FONT_SIZE = 12
        self.FONT_OFFSET = self.FONT_SIZE / 1.5
        self.AUTOCOMPLETE_WORDS = ['def', 'if', 'while', 'for', 'print', 'True', 'False']
        self.WINDOW_TITLE = 'Text Editor'

        self.open_file = ''
        self.insert_point_store = ''

        self.title(self.WINDOW_TITLE)
        self.geometry('800x600')

        self.menubar = tk.Menu(self, bg="lightgrey", fg="black")

        self.file_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.file_menu.add_command(label="New", command=self.file_new, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.file_open, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.file_save, accelerator="Ctrl+S")

        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.configure(menu=self.menubar)

        self.main_text = tk.Text(self, bg="white", fg="black", font=("Ubuntu Mono", self.FONT_SIZE))

        self.main_text.pack(expand=1, fill=tk.BOTH)

        self.main_text.bind('<space>', self.destroy_autofill_menu)
        self.main_text.bind('<KeyRelease>', self.display_autofill_menu)

        self.bind('<Control-s>', self.file_save)
        self.bind('<Control-o>', self.file_open)
        self.bind('<Control-n>', self.file_new)

    def file_new(self, evt=None):
        self.open_file = filedialog.asksaveasfilename()
        self.main_text.delete(1.0, tk.END)
        self.title(' - '.join([self.WINDOW_TITLE, self.open_file]))

    def file_open(self, evt=None):
        file_to_open = filedialog.askopenfilename()

        if file_to_open:
            self.open_file = file_to_open

            with open(file_to_open, 'r') as file_contents:
                file_lines = file_contents.readlines()
                self.main_text.delete(1.0, tk.END)
                if len(file_lines) > 0:
                    for index, line in enumerate(file_lines):
                        index = float(index) + 1.0
                        self.main_text.insert(index, line)

        self.title(' - '.join([self.WINDOW_TITLE, self.open_file]))

    def file_save(self, evt=None):
        if not self.open_file:
            self.open_file = filedialog.asksaveasfilename()
        new_contents = self.main_text.get(1.0, tk.END)
        with open(self.open_file, 'w') as open_file:
            open_file.write(new_contents)

    def display_menu(self, evt=None, words=None, currently_typed_word=None, current_index=None):
        self.destroy_autofill_menu()
        if words and currently_typed_word:
            self.complete_menu = tk.Menu(self, tearoff=0, bg="lightgrey", fg="black")
            for word in words:
                insert_word_callback = partial(self.insert_word, word=word, part=currently_typed_word, index=current_index)
                self.complete_menu.add_command(label=word, command=insert_word_callback)

        coords = str(self.main_text.index(tk.INSERT)).split('.')

        x = int(coords[1])
        y = int(coords[0])

        offset_x = self.main_text.winfo_rootx()
        offset_x = int(offset_x)

        offset_y = self.main_text.winfo_rooty() + (self.FONT_SIZE * (y/1.5 + 1))
        offset_y = int(offset_y)

        x *= self.FONT_OFFSET
        x = int(x)

        y *= self.FONT_OFFSET
        y = int(y)

        self.complete_menu.post(offset_x + x, offset_y + y)

        self.main_text.bind('<Down>', self.focus_menu_item)

    def display_autofill_menu(self, evt=None):
        current_index = self.main_text.index(tk.INSERT)
        start = self.adjust_floating_index(current_index)
        suggestions = []

        try:
            currently_typed_word = self.main_text.get(start + ' wordstart', tk.INSERT)
        except tk.TclError:
            currently_typed_word = ''

        currently_typed_word = str(currently_typed_word).strip()
        print(currently_typed_word)

        if currently_typed_word:
            self.destroy_autofill_menu()

            for word in self.AUTOCOMPLETE_WORDS:
                if word.startswith(currently_typed_word) and not currently_typed_word == word:
                    suggestions.append(word)

            if len(suggestions) > 0:
                self.display_menu(None, suggestions, currently_typed_word, current_index)

    def destroy_autofill_menu(self, evt=None):
        try:
            self.complete_menu.destroy()
        except AttributeError:
            pass

    def insert_word(self, word, part, index):
        amount_typed = len(part)
        remaining_word = word[amount_typed:]
        remaining_word_offset = ' +' + str(len(remaining_word)) + 'c'
        self.main_text.insert(index, remaining_word)
        self.main_text.mark_set(tk.INSERT, index + remaining_word_offset)
        self.complete_menu.destroy()
        self.main_text.focus_force()

    def adjust_floating_index(self, number):
        num_decimal_places = len(number.split(".")[1])
        number_float = float(number)
        if num_decimal_places > 1:
            number_string = '{:.2f}'
            number_float -= 0.01
        else:
            number_string = '{:.1f}'
            number_float -= 0.1
        number_to_return = number_string.format(number_float)

        return number_to_return

    def focus_menu_item(self, evt=None):
        try:
            self.complete_menu.focus_force()
            self.complete_menu.entryconfig(0, state="active")
        except tk.TclError:
            pass


editor = Editor()
editor.mainloop()
