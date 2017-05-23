import re
import tkinter as tk
from tkinter import filedialog
from functools import partial

class Editor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.FONT_SIZE = 12
        self.WINDOW_TITLE = "Text Editor"

        self.AUTOCOMPLETE_WORDS = [
            "def", "import", "as", "if", "elif", "else", "while",
            "for", "try", "except", "print", "True", "False",
            "self", "None", "return", "with"
        ]
        self.KEYWORDS_1 = ["import", "as", "from", "def", "try", "except", "self"]
        self.KEYWORDS_FLOW = ["if", "else", "elif", "try", "except", "for", "in", "while", "return", "with"]
        self.KEYWORDS_FUNCTIONS = ["print", "list", "dict", "set", "int", "float", "str"]

        self.SPACES_REGEX = re.compile("^\s*")
        self.STRING_REGEX_SINGLE = re.compile("'[^'\r\n]*'")
        self.STRING_REGEX_DOUBLE = re.compile('"[^"\r\n]*"')
        self.NUMBER_REGEX = re.compile(r"\b(?=\(*)\d+\.?\d*(?=\)*\,*)\b")
        self.KEYWORDS_REGEX = re.compile("(?=\(*)(?<![a-z])(None|True|False)(?=\)*\,*)")
        self.SELF_REGEX = re.compile("(?=\(*)(?<![a-z])(self)(?=\)*\,*)")
        self.FUNCTIONS_REGEX = re.compile("(?=\(*)(?<![a-z])(print|list|dict|set|int|str)(?=\()")

        self.REGEX_TO_TAG = {
            self.STRING_REGEX_SINGLE : "string",
            self.STRING_REGEX_DOUBLE : "string",
            self.NUMBER_REGEX : "digit",
            self.KEYWORDS_REGEX : "keywordcaps",
            self.SELF_REGEX : "keyword1",
            self.FUNCTIONS_REGEX : "keywordfunc",
        }

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

        self.main_text.tag_config("keyword1", foreground="orange")
        self.main_text.tag_config("keywordcaps", foreground="navy")
        self.main_text.tag_config("keywordflow", foreground="purple")
        self.main_text.tag_config("keywordfunc", foreground="darkgrey")
        self.main_text.tag_config("decorator", foreground="khaki")
        self.main_text.tag_config("digit", foreground="red")
        self.main_text.tag_config("string", foreground="green")

        self.main_text.bind("<space>", self.destroy_autocomplete_menu)
        self.main_text.bind("<KeyRelease>", self.on_key_release)
        self.main_text.bind("<Tab>", self.insert_spaces)
        self.main_text.bind("<Escape>", self.destroy_autocomplete_menu)

        self.bind("<Control-s>", self.file_save)
        self.bind("<Control-o>", self.file_open)
        self.bind("<Control-n>", self.file_new)

    def file_new(self, event=None):
        file_name = filedialog.asksaveasfilename()
        if file_name:
            self.open_file = file_name
            self.main_text.delete(1.0, tk.END)
            self.title(" - ".join([self.WINDOW_TITLE, self.open_file]))

    def file_open(self, event=None):
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

        final_index = self.main_text.index(tk.END)
        final_line_number = int(final_index.split(".")[0])

        for line_number in range(final_line_number):
            line_to_tag = ".".join([str(line_number), "0"])
            self.tag_keywords(None, line_to_tag)


    def file_save(self, event=None):
        if not self.open_file:
            new_file_name = filedialog.asksaveasfilename()
            if new_file_name:
                self.open_file = new_file_name

        if self.open_file:
            new_contents = self.main_text.get(1.0, tk.END)
            with open(self.open_file, "w") as open_file:
                open_file.write(new_contents)

    def insert_spaces(self, event=None):
        self.main_text.insert(tk.INSERT, "    ")

        return "break"

    def get_menu_coordinates(self):
        bbox = self.main_text.bbox(tk.INSERT)
        menu_x = bbox[0] + self.winfo_x() + self.main_text.winfo_x()
        menu_y = bbox[1] + self.winfo_y() + self.main_text.winfo_y() + self.FONT_SIZE + 2

        return (menu_x, menu_y)

    def display_autocomplete_menu(self, event=None):
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
                self.complete_menu.bind("<Escape>", self.destroy_autocomplete_menu)
                self.main_text.bind("<Down>", self.focus_menu_item)

    def destroy_autocomplete_menu(self, event=None):
        try:
            self.complete_menu.destroy()
            self.main_text.unbind("<Down>")
            self.main_text.focus_force()
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

    def focus_menu_item(self, event=None):
        try:
            self.complete_menu.focus_force()
            self.complete_menu.entryconfig(0, state="active")
        except tk.TclError:
            pass

    def tag_keywords(self, event=None, current_index=None):
        if not current_index:
            current_index = self.main_text.index(tk.INSERT)
        line_number = current_index.split(".")[0]
        line_beginning = ".".join([line_number, "0"])
        line_text = self.main_text.get(line_beginning, line_beginning + " lineend")
        line_words = line_text.split()
        number_of_spaces = self.number_of_leading_spaces(line_text)
        y_position = number_of_spaces

        for tag in self.main_text.tag_names():
            self.main_text.tag_remove(tag, line_beginning, line_beginning + " lineend")

        self.add_regex_tags(line_number, line_text)

        for word in line_words:
            stripped_word = word.strip("():,")

            word_start = str(y_position)
            word_end = str(y_position + len(stripped_word))
            start_index = ".".join([line_number, word_start])
            end_index = ".".join([line_number, word_end])

            if stripped_word in self.KEYWORDS_1:
                self.main_text.tag_add("keyword1", start_index, end_index)
            elif stripped_word in self.KEYWORDS_FLOW:
                self.main_text.tag_add("keywordflow", start_index, end_index)
            elif stripped_word.startswith("@"):
                self.main_text.tag_add("decorator", start_index, end_index)

            y_position += len(word) + 1

    def number_of_leading_spaces(self, line):
        spaces = re.search(self.SPACES_REGEX, line)
        if spaces.group(0) is not None:
            number_of_spaces = len(spaces.group(0))
        else:
            number_of_spaces = 0

        return number_of_spaces

    def add_regex_tags(self, line_number, line_text):
        for regex, tag in self.REGEX_TO_TAG.items():
            for match in regex.finditer(line_text):
                start, end = match.span()
                start_index = ".".join([line_number, str(start)])
                end_index = ".".join([line_number, str(end)])
                self.main_text.tag_add(tag, start_index, end_index)

    def on_key_release(self, event=None):
        if not event.keysym in ("Up", "Down", "Left", "Right", "BackSpace", "Delete", "Escape"):
            self.display_autocomplete_menu()
        self.tag_keywords()

if __name__ == "__main__":
    editor = Editor()
    editor.mainloop()
