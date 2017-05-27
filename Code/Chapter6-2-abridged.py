import re
...

class Editor(tk.Tk):
    def __init__(self):
        ...

        self.AUTOCOMPLETE_WORDS = [
            "def", "import", "as", "if", "elif", "else", "while",
            "for", "try", "except", "print", "True", "False",
            "self", "None", "return", "with"
        ]
        self.KEYWORDS_1 = ["import", "as", "from", "def", "try", "except", "self"]
        self.KEYWORDS_FLOW = ["if", "else", "elif", "try", "except", "for", "in", "while", "return", "with"]

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

        ...

        self.main_text.tag_config("keyword1", foreground="orange")
        self.main_text.tag_config("keywordcaps", foreground="navy")
        self.main_text.tag_config("keywordflow", foreground="purple")
        self.main_text.tag_config("keywordfunc", foreground="darkgrey")
        self.main_text.tag_config("decorator", foreground="khaki")
        self.main_text.tag_config("digit", foreground="red")
        self.main_text.tag_config("string", foreground="green")

        ...
        self.main_text.bind("<KeyRelease>", self.on_key_release)
        self.main_text.bind("<Escape>", self.destroy_autocomplete_menu)
        ...

    def file_new(self, event=None):
        ...

    def file_open(self, event=None):
        ...

        final_index = self.main_text.index(tk.END)
        final_line_number = int(final_index.split(".")[0])

        for line_number in range(final_line_number):
            line_to_tag = ".".join([str(line_number), "0"])
            self.tag_keywords(None, line_to_tag)


    def file_save(self, event=None):
        ...

    def insert_spaces(self, event=None):
        ...

    def get_menu_coordinates(self):
        ...

    def display_autocomplete_menu(self, event=None):
        ...
        self.complete_menu.post(x, y)
        self.complete_menu.bind("<Escape>", self.destroy_autocomplete_menu)
        self.main_text.bind("<Down>", self.focus_menu_item)

    def destroy_autocomplete_menu(self, event=None):
        ...

    def insert_word(self, word, part, index):
        ...

    def adjust_floating_index(self, number):
        ...

    def focus_menu_item(self, event=None):
        ...

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
    ...
