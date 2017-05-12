import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as msg
from functools import partial

class FindPopup(tk.Toplevel):
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.title("Find in file")
        self.center_window()

        self.transient(master)

        self.matches_are_highlighted = False

        self.main_frame = tk.Frame(self, bg="lightgrey")
        self.button_frame = tk.Frame(self.main_frame, bg="lightgrey")

        self.find_label = tk.Label(self.main_frame, text="Find: ", bg="lightgrey", fg="black")
        self.find_entry = tk.Entry(self.main_frame, bg="white", fg="black")
        self.find_button = tk.Button(self.button_frame, text="Find All", bg="lightgrey", fg="black", command=self.find)
        self.next_button = tk.Button(self.button_frame, text="Next", bg="lightgrey", fg="black", command=self.jump_to_next_match)
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", bg="lightgrey", fg="black", command=self.cancel)

        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.find_button.pack(side=tk.LEFT, pady=(0,10), padx=(20,25))
        self.next_button.pack(side=tk.LEFT, pady=(0,10), padx=(20,25))
        self.cancel_button.pack(side=tk.LEFT, pady=(0,10), padx=(20,0))
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.find_label.pack(side=tk.LEFT, fill=tk.X, padx=(20,0))
        self.find_entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=(0,20))

        self.find_entry.focus_force()
        self.find_entry.bind("<Return>", self.jump_to_next_match)
        self.bind("<Escape>", self.cancel)

        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def find(self, evt=None):
        text_to_find = self.find_entry.get()
        if text_to_find:
            self.master.highlight_matches(text_to_find)
            self.matches_are_highlighted = True

    def jump_to_next_match(self, evt=None):
        text_to_find = self.find_entry.get()
        if text_to_find:
            if not self.matches_are_highlighted:
                self.master.highlight_matches(text_to_find)
                self.matches_are_highlighted = True
            self.master.next_match()

    def cancel(self, evt=None):
        self.master.remove_all_find_tags()
        self.destroy()

    def center_window(self):
        master_pos_x = self.master.winfo_x()
        master_pos_y = self.master.winfo_y()

        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

        my_width = 300
        my_height = 100

        pos_x = (master_pos_x + (master_width // 2)) - (my_width // 2)
        pos_y = (master_pos_y + (master_height // 2)) - (my_height // 2)

        geometry = "{}x{}+{}+{}".format(my_width, my_height, pos_x, pos_y)
        self.geometry(geometry)



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
        self.NUMBER_REGEX = re.compile("(?=\(*)(?<![a-z])\d+\.?\d*(?=\)*\,*)")
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

        self.edit_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.edit_menu.add_command(label="Cut", command=self.edit_cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Paste", command=self.edit_paste, accelerator="Ctrl+V")
        self.edit_menu.add_command(label="Undo", command=self.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.edit_redo, accelerator="Ctrl+Y")

        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)

        self.configure(menu=self.menubar)

        self.line_numbers = tk.Text(self, bg="lightgrey", fg="black", width=6)
        self.line_numbers.insert(1.0, "1 \n")
        self.line_numbers.configure(state="disabled")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.main_text = tk.Text(self, bg="white", fg="black", font=("Ubuntu Mono", self.FONT_SIZE))
        self.scrollbar = tk.Scrollbar(self.main_text, orient="vertical", command=self.scroll_text_and_line_numbers)
        self.main_text.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_text.pack(expand=1, fill=tk.BOTH)

        self.main_text.tag_config("keyword1", foreground="orange")
        self.main_text.tag_config("keywordcaps", foreground="navy")
        self.main_text.tag_config("keywordflow", foreground="purple")
        self.main_text.tag_config("keywordfunc", foreground="darkgrey")
        self.main_text.tag_config("decorator", foreground="khaki")
        self.main_text.tag_config("digit", foreground="red")
        self.main_text.tag_config("string", foreground="green")
        self.main_text.tag_config("findmatch", background="yellow")
        self.main_text.tag_config("findmatchactive", background="cyan")

        self.main_text.bind("<space>", self.destroy_autocomplete_menu)
        self.main_text.bind("<KeyRelease>", self.on_key_release)
        self.main_text.bind("<Tab>", self.insert_spaces)

        self.main_text.bind("<Control-y>", self.edit_redo)

        self.bind("<Control-s>", self.file_save)
        self.bind("<Control-o>", self.file_open)
        self.bind("<Control-n>", self.file_new)

        self.bind("<Control-a>", self.select_all)
        self.bind("<Control-f>", self.show_find_window)

        self.main_text.bind('<MouseWheel>', self.scroll_text_and_line_numbers)
        self.main_text.bind('<Button-4>', self.scroll_text_and_line_numbers)
        self.main_text.bind('<Button-5>', self.scroll_text_and_line_numbers)

        self.line_numbers.bind('<MouseWheel>', self.skip_event)
        self.line_numbers.bind('<Button-4>', self.skip_event)
        self.line_numbers.bind('<Button-5>', self.skip_event)

    def skip_event(self, evt=None):
        return "break"

    def scroll_text_and_line_numbers(self, *args):
        try: # from scrollbar
            self.main_text.yview_moveto(args[1])
            self.line_numbers.yview_moveto(args[1])
        except IndexError:
            #from mouse MouseWheel
            event = args[0]
            if event.delta:
                move = -1*(event.delta/120)
            else:
                if event.num == 5:
                    move = 1
                else:
                    move = -1

            self.main_text.yview_scroll(move, 'units')
            self.line_numbers.yview_scroll(move, 'units')

        return "break"

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

        final_index = self.main_text.index(tk.END)
        final_line_number = int(final_index.split(".")[0])

        for line_number in range(final_line_number):
            line_to_tag = ".".join([str(line_number), "0"])
            self.tag_keywords(None, line_to_tag)

        self.update_line_numbers()


    def file_save(self, evt=None):
        if not self.open_file:
            new_file_name = filedialog.asksaveasfilename()
            if new_file_name:
                self.open_file = new_file_name

        if self.open_file:
            new_contents = self.main_text.get(1.0, tk.END)
            with open(self.open_file, "w") as open_file:
                open_file.write(new_contents)

    def select_all(self, evt=None):
        self.main_text.tag_add("sel", 1.0, tk.END)

        return "break"

    def edit_cut(self, evt=None):
        self.main_text.event_generate("<<Cut>>")

        return "break"

    def edit_paste(self, evt=None):
        self.main_text.event_generate("<<Paste>>")
        self.on_key_release()

        return "break"

    def edit_undo(self, evt=None):
        self.main_text.event_generate("<<Undo>>")

        return "break"

    def edit_redo(self, evt=None):
        self.main_text.event_generate("<<Redo>>")

        return "break"

    def insert_spaces(self, evt=None):
        self.main_text.insert(tk.INSERT, "    ")

        return "break"

    def get_menu_coordinates(self):
        bbox = self.main_text.dlineinfo(tk.INSERT)
        menu_x = bbox[2] + self.winfo_x() + self.main_text.winfo_x()
        menu_y = bbox[1] + self.winfo_y() + self.main_text.winfo_y() + self.FONT_SIZE + 2

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

    def tag_keywords(self, evt=None, current_index=None):
        if not current_index:
            current_index = self.main_text.index(tk.INSERT)
        line_number = current_index.split(".")[0]
        line_beginning = ".".join([line_number, "0"])
        line_text = self.main_text.get(line_beginning, line_beginning + ' lineend')
        line_words = line_text.split()
        number_of_spaces = self.number_of_leading_spaces(line_text)
        y_position = number_of_spaces

        for tag in self.main_text.tag_names():
            if tag != "sel":
                self.main_text.tag_remove(tag, line_beginning, line_beginning + ' lineend')

        self.add_regex_tags(line_number, line_text)

        for word in line_words:
            stripped_word = word.strip('():,')

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

    def on_key_release(self, evt=None):
        self.display_autocomplete_menu()
        self.tag_keywords()
        self.update_line_numbers()

    def update_line_numbers(self):
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete(1.0, tk.END)
        number_of_lines = self.main_text.index(tk.END).split(".")[0]
        line_number_string = "\n".join(str(no+1) for no in range(int(number_of_lines)))
        self.line_numbers.insert(1.0, line_number_string)
        self.line_numbers.configure(state="disabled")

    def show_find_window(self, evt=None):
        FindPopup(self)

    def highlight_matches(self, text_to_find):
        self.main_text.tag_remove("findmatch", 1.0, tk.END)
        self.match_coordinates = []
        self.current_match = -1

        find_regex = re.compile(text_to_find)
        search_text_lines = self.main_text.get(1.0, tk.END).split("\n")

        for line_number, line in enumerate(search_text_lines):
            line_number += 1
            for match in find_regex.finditer(line):
                start, end = match.span()
                start_index = ".".join([str(line_number), str(start)])
                end_index = ".".join([str(line_number), str(end)])
                self.main_text.tag_add("findmatch", start_index, end_index)
                self.match_coordinates.append((start_index, end_index))

    def next_match(self, evt=None):
        try:
            current_target, current_target_end = self.match_coordinates[self.current_match]
            self.main_text.tag_remove("sel", current_target, current_target_end)
            self.main_text.tag_add("findmatch", current_target, current_target_end)
        except IndexError:
            pass

        self.current_match = self.current_match + 1
        next_target, target_end = self.match_coordinates[self.current_match]
        self.main_text.mark_set(tk.INSERT, next_target)
        self.main_text.tag_remove("findmatch", next_target, target_end)
        self.main_text.tag_add("sel", next_target, target_end)
        self.main_text.see(next_target)

    def remove_all_find_tags(self):
        self.main_text.tag_remove("findmatch", 1.0, tk.END)


if __name__ == "__main__":
    editor = Editor()
    editor.mainloop()
