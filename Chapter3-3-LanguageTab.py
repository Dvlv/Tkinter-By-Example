class LanguageTab(tk.Frame):
    def __init__(self, master, lang_name, lang_code):
        super().__init__(master)

        self.lang_name = lang_name
        self.lang_code = lang_code

        self.translation_var = tk.StringVar(self)
        self.translation_var.set("")

        self.translated_label = tk.Label(self, textvar=self.translation_var, bg="lightgrey", fg="black")

        self.copy_button = tk.Button(self, text="Copy to Clipboard", command=self.copy_to_clipboard)

        self.copy_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.translated_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def copy_to_clipboard(self):
        root = self.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append(self.translation_var.get())
        msg.showinfo("Copied Successfully", "Text copied to clipboard")
