class TranslateBook(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Translation Book v3")
        self.geometry("500x300")

        self.menu = tk.Menu(self, bg="lightgrey", fg="black")

        self.languages_menu = tk.Menu(self.menu, tearoff=0, bg="lightgrey", fg="black")
        self.languages_menu.add_command(label="Add New", command=self.show_new_language_popup)
        self.languages_menu.add_command(label="Portuguese", command=lambda: self.add_new_tab(LanguageTab(self, "Portuguese", "pt")))

        self.menu.add_cascade(label="Languages", menu=self.languages_menu)

        self.config(menu=self.menu)

        self.notebook = Notebook(self)

        self.language_tabs = []

        english_tab = tk.Frame(self.notebook)

        self.translate_button = tk.Button(english_tab, text="Translate", command=self.translate)
        self.translate_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.english_entry = tk.Text(english_tab, bg="white", fg="black")
        self.english_entry.pack(side=tk.TOP, expand=1)

        self.notebook.add(english_tab, text="English")

        self.notebook.pack(fill=tk.BOTH, expand=1)

    def translate(self, text=None):
        if len(self.language_tabs) < 1:
            msg.showerror("No Languages", "No languages added. Please add some from the menu")
            return

        if not text:
            text = self.english_entry.get(1.0, tk.END).strip()

        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}"

        try:
            for language in self.language_tabs:
                full_url = url.format("en", language.lang_code, text)
                r = requests.get(full_url)
                r.raise_for_status()
                translation = r.json()[0][0][0]
                language.translation_var.set(translation)
        except Exception as e:
            msg.showerror("Translation Failed", str(e))
        else:
            msg.showinfo("Translations Successful", "Text successfully translated")

    def add_new_tab(self, tab):
        self.language_tabs.append(tab)
        self.notebook.add(tab, text=tab.lang_name)

        try:
            self.languages_menu.entryconfig(tab.lang_name, state="disabled")
        except:
            # language isn't in menu.
            pass

    def show_new_language_popup(self):
        NewLanguageForm(self)

