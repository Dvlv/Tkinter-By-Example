...
import tkinter.messagebox as msg

class FindPopup(tk.Toplevel):
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.title("Find in file")
        self.center_window()

        self.transient(master)

        self.matches_are_highlighted = True

        self.main_frame = tk.Frame(self, bg="lightgrey")
        self.button_frame = tk.Frame(self.main_frame, bg="lightgrey")

        self.find_label = tk.Label(self.main_frame, text="Find: ", bg="lightgrey", fg="black")
        self.find_entry = tk.Entry(self.main_frame, bg="white", fg="black")
        self.find_button = tk.Button(self.button_frame, text="Find All", bg="lightgrey", fg="black", command=self.find)
        self.next_button = tk.Button(self.button_frame, text="Next", bg="lightgrey", fg="black", command=self.jump_to_next_match)
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", bg="lightgrey", fg="black", command=self.cancel)

        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.find_button.pack(side=tk.LEFT, pady=(0,10), padx=(20,20))
        self.next_button.pack(side=tk.LEFT, pady=(0,10), padx=(15,20))
        self.cancel_button.pack(side=tk.LEFT, pady=(0,10), padx=(15,0))
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.find_label.pack(side=tk.LEFT, fill=tk.X, padx=(20,0))
        self.find_entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=(0,20))

        self.find_entry.focus_force()
        self.find_entry.bind("<Return>", self.jump_to_next_match)
        self.find_entry.bind("<KeyRelease>", self.matches_are_not_highlighted)
        self.bind("<Escape>", self.cancel)

        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def find(self, event=None):
        text_to_find = self.find_entry.get()
        if text_to_find and not self.matches_are_highlighted:
            self.master.remove_all_find_tags()
            self.master.highlight_matches(text_to_find)
            self.matches_are_highlighted = True

    def jump_to_next_match(self, event=None):
        text_to_find = self.find_entry.get()
        if text_to_find:
            if not self.matches_are_highlighted:
                self.find()
            self.master.next_match()

    def cancel(self, event=None):
        self.master.remove_all_find_tags()
        self.destroy()

    def matches_are_not_highlighted(self, event):
        key_pressed = event.keysym
        if not key_pressed == "Return":
            self.matches_are_highlighted = False

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
        ...
        self.edit_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.edit_menu.add_command(label="Cut", command=self.edit_cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Paste", command=self.edit_paste, accelerator="Ctrl+V")
        self.edit_menu.add_command(label="Undo", command=self.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.edit_redo, accelerator="Ctrl+Y")

        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)

        ...

        self.line_numbers = tk.Text(self, bg="lightgrey", fg="black", width=6)
        self.line_numbers.insert(1.0, "1 \n")
        self.line_numbers.configure(state="disabled")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        ...

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.scroll_text_and_line_numbers)
        self.main_text.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_text.pack(expand=1, fill=tk.BOTH)

        ...
        self.main_text.tag_config("findmatch", background="yellow")

        ...

        self.main_text.bind("<Control-y>", self.edit_redo)

        ...

        self.bind("<Control-a>", self.select_all)
        self.bind("<Control-f>", self.show_find_window)

        self.main_text.bind("<MouseWheel>", self.scroll_text_and_line_numbers)
        self.main_text.bind("<Button-4>", self.scroll_text_and_line_numbers)
        self.main_text.bind("<Button-5>", self.scroll_text_and_line_numbers)

        self.line_numbers.bind("<MouseWheel>", self.skip_event)
        self.line_numbers.bind("<Button-4>", self.skip_event)
        self.line_numbers.bind("<Button-5>", self.skip_event)

    def skip_event(self, event=None):
        return "break"

    def scroll_text_and_line_numbers(self, *args):
        try:
            # from scrollbar
            self.main_text.yview_moveto(args[1])
            self.line_numbers.yview_moveto(args[1])
        except IndexError:
            #from MouseWheel
            event = args[0]
            if event.delta:
                move = -1*(event.delta/120)
            else:
                if event.num == 5:
                    move = 1
                else:
                    move = -1

            self.main_text.yview_scroll(int(move), "units")
            self.line_numbers.yview_scroll(int(move), "units")

        return "break"

    def file_new(self, event=None):
        ...

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

        self.tag_all_lines()


    def file_save(self, event=None):
        ...

    def select_all(self, event=None):
        self.main_text.tag_add("sel", 1.0, tk.END)

        return "break"

    def edit_cut(self, event=None):
        self.main_text.event_generate("<<Cut>>")

        return "break"

    def edit_paste(self, event=None):
        self.main_text.event_generate("<<Paste>>")
        self.on_key_release()
        self.tag_all_lines()

        return "break"

    def edit_undo(self, event=None):
        self.main_text.event_generate("<<Undo>>")

        return "break"

    def edit_redo(self, event=None):
        self.main_text.event_generate("<<Redo>>")

        return "break"

    def insert_spaces(self, event=None):
        ...

    def get_menu_coordinates(self):
        ...

    def display_autocomplete_menu(self, event=None):
        ...

    def destroy_autocomplete_menu(self, event=None):
        ...

    def insert_word(self, word, part, index):
        ...

    def adjust_floating_index(self, number):
        ...

    def focus_menu_item(self, event=None):
        ...

    def tag_keywords(self, event=None, current_index=None):
        ...

    def number_of_leading_spaces(self, line):
        ...

    def add_regex_tags(self, line_number, line_text):
        ...

    def on_key_release(self, event=None):
        ...
        self.update_line_numbers()

    def tag_all_lines(self):
        final_index = self.main_text.index(tk.END)
        final_line_number = int(final_index.split(".")[0])

        for line_number in range(final_line_number):
            line_to_tag = ".".join([str(line_number), "0"])
            self.tag_keywords(None, line_to_tag)

        self.update_line_numbers()

    def update_line_numbers(self):
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete(1.0, tk.END)
        number_of_lines = self.main_text.index(tk.END).split(".")[0]
        line_number_string = "\n".join(str(no+1) for no in range(int(number_of_lines)))
        self.line_numbers.insert(1.0, line_number_string)
        self.line_numbers.configure(state="disabled")

    def show_find_window(self, event=None):
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

    def next_match(self, event=None):
        try:
            current_target, current_target_end = self.match_coordinates[self.current_match]
            self.main_text.tag_remove("sel", current_target, current_target_end)
            self.main_text.tag_add("findmatch", current_target, current_target_end)
        except IndexError:
            pass

        try:
            self.current_match = self.current_match + 1
            next_target, target_end = self.match_coordinates[self.current_match]
        except IndexError:
            if len(self.match_coordinates) == 0:
                msg.showinfo("No Matches", "No Matches Found")
            else:
                if msg.askyesno("Wrap Search?", "Reached end of file. Continue from the top?"):
                    self.current_match = -1
                    self.next_match()
        else:
            self.main_text.mark_set(tk.INSERT, next_target)
            self.main_text.tag_remove("findmatch", next_target, target_end)
            self.main_text.tag_add("sel", next_target, target_end)
            self.main_text.see(next_target)

    def remove_all_find_tags(self):
        self.main_text.tag_remove("findmatch", 1.0, tk.END)
        self.main_text.tag_remove("sel", 1.0, tk.END)


if __name__ == "__main__":
    editor = Editor()
    editor.mainloop()
