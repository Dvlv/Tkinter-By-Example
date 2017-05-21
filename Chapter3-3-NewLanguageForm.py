class NewLanguageForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__()

        self.master = master

        self.title("Add new Language")
        self.geometry("300x150")

        self.name_label = tk.Label(self, text="Language Name")
        self.name_entry = tk.Entry(self, bg="white", fg="black")
        self.code_label = tk.Label(self, text="Language Code")
        self.code_entry = tk.Entry(self, bg="white", fg="black")
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)

        self.name_label.pack(fill=tk.BOTH, expand=1)
        self.name_entry.pack(fill=tk.BOTH, expand=1)
        self.code_label.pack(fill=tk.BOTH, expand=1)
        self.code_entry.pack(fill=tk.BOTH, expand=1)
        self.submit_button.pack(fill=tk.X)

    def submit(self):
        lang_name = self.name_entry.get()
        lang_code = self.code_entry.get()

        if lang_name and lang_code:
            new_tab = LanguageTab(self.master, lang_name, lang_code)
            self.master.languages_menu.add_command(label=lang_name, command=lambda: self.master.add_new_tab(new_tab))
            msg.showinfo("Language Option Added", "Language option " + lang_name + " added to menu")
            self.destroy()
        else:
            msg.showerror("Missing Information", "Please add both a name and code")
