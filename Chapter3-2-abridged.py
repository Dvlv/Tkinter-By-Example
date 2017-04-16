...

class TranslateBook(tk.Tk):
    def __init__(self):

        ...

        self.menu = tk.Menu(self, bg="lightgrey", fg="black")

        self.languages_menu = tk.Menu(self.menu, tearoff=0, bg="lightgrey", fg="black")
        self.languages_menu.add_command(label="Portuguese", command=self.add_portuguese_tab)

        self.menu.add_cascade(label="Languages", menu=self.languages_menu)

        self.config(menu=self.menu)

        ...

        self.italian_translation = tk.StringVar(italian_tab)
        self.italian_translation.set("")

        self.translate_button = tk.Button(english_tab, text="Translate", command=lambda langs=["it"], elems=[self.italian_translation]: self.translate(langs, None, elems))

        ...

    def translate(self, target_languages=None, text=None, elements=None):
        if not text:
            text = self.english_entry.get(1.0, tk.END).strip()
        if not elements:
            elements = [self.italian_translation]
        if not target_languages:
            target_languages = ["it"]

        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}"

        try:
            for code, element in zip(target_languages, elements):
                full_url = url.format("en", code, text)
                r = requests.get(full_url)
                r.raise_for_status()
                translation = r.json()[0][0][0]
                element.set(translation)
        except Exception as e:
            msg.showerror("Translation Failed", str(e))
        else:
            msg.showinfo("Translations Successful", "Text successfully translated")

    def copy_to_clipboard(self, text=None):
        ...

    def add_portuguese_tab(self):
        portuguese_tab = tk.Frame(self.notebook)
        self.portuguese_translation = tk.StringVar(portuguese_tab)
        self.portuguese_translation.set("")

        self.portuguese_copy_button = tk.Button(portuguese_tab, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(self.portuguese_translation.get()))
        self.portuguese_copy_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.portuguese_label = tk.Label(portuguese_tab, textvar=self.portuguese_translation, bg="lightgrey", fg="black")
        self.portuguese_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.notebook.add(portuguese_tab, text="Portuguese")

        self.languages_menu.entryconfig("Portuguese", state="disabled")

        self.translate_button.config(command=lambda langs=["it","pt"], elems=[self.italian_translation, self.portuguese_translation]: self.translate(langs, None, elems))


if __name__ == "__main__":
    translatebook = TranslateBook()
    translatebook.mainloop()
