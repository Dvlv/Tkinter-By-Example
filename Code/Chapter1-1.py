#! /usr/bin/env python
"""*********************************************************************
As is tradition with all programming books, we'll start with the classic
Hello World example to introduce afew things.
This will pop up a small window with "Hello World" written inside.
*********************************************************************"""
try:
    import Tkinter as tk
except ImportError:
    # Python 3
    import tkinter as tk
ROOT = tk.Tk()

LABEL = tk.Label(ROOT, text="Hello World", padx=10, pady=10)
LABEL.pack()

ROOT.mainloop()
