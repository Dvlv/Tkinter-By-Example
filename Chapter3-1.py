import tkinter as tk
from tkinter.ttk import Notebook as nbk
import requests

class TranslateBook(tk.Tk):
    def __init__():
        super().__init__()

    def translate(self, target_language, text):
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}".format('en',target_language, text)
        r = requests.get(url2)
        r.raise_for_status()
        return r.json()
