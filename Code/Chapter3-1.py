#! /usr/bin/env python
"""*********************************************************************
In this chapter we'll be creating a tool which will translate english 
text into multiple other languages using the Google Translate API. 
Here we'll learn about the following:
-- Creating a tabbed interface
-- Creating a Menu
-- Creating a pop-up window
-- Accessing the Clipboard
-- Calling APIs with requests 
*********************************************************************"""
try:
    import tkinter as tk
    from tkinter import *
    import tkinter.messagebox as msg
    from tkinter.ttk import Notebook
except ImportError:
    # Python 2
    import Tkinter as tk
    from Tkinter import *
    import tkMessageBox as msg
    from ttk import Notebook

import requests

class TranslateBook(tk.Tk):
    def __init__(self):
        try:
            super(TranslateBook, self).__init__()
        except TypeError:
            # Python 2
            tk.Tk.__init__(self)
            
        self.title("Translation Book v1")
        self.geometry("500x300")

        self.notebook = Notebook(self)

        english_tab = tk.Frame(self.notebook)
        italian_tab = tk.Frame(self.notebook)

        self.translate_button = tk.Button(english_tab, text="Translate", command=self.translate)
        self.translate_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.english_entry = tk.Text(english_tab, bg="white", fg="black")
        self.english_entry.pack(side=tk.TOP, expand=1)

        self.italian_copy_button = tk.Button(italian_tab, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.italian_copy_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.italian_translation = tk.StringVar(italian_tab)
        self.italian_translation.set("")

        self.italian_label = tk.Label(italian_tab, textvar=self.italian_translation, bg="lightgrey", fg="black")
        self.italian_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.notebook.add(english_tab, text="English")
        self.notebook.add(italian_tab, text="Italian")

        self.notebook.pack(fill=tk.BOTH, expand=1)

    def translate(self, target_language="it", text=None):
        if not text:
            text = self.english_entry.get(1.0, tk.END)

        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}".format("en", target_language, text)

        try:
            r = requests.get(url)
            r.raise_for_status()
            translation = r.json()[0][0][0]
            self.italian_translation.set(translation)
            msg.showinfo("Translation Successful", "Text successfully translated")
        except Exception as e:
            msg.showerror("Translation Failed", str(e))

    def copy_to_clipboard(self, text=None):
        if not text:
            text = self.italian_translation.get()

        self.clipboard_clear()
        self.clipboard_append(text)
        msg.showinfo("Copied Successfully", "Text copied to clipboard")


if __name__ == "__main__":
    translatebook = TranslateBook()
    translatebook.mainloop()
