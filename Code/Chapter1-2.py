#! /usr/bin/env python
"""****************************************************************************************
# Using Classes:
Whilst Tkinter code can be written using only functions, it's much better to use a class to
keep track of all individual widgets which may need to reference each other. Without doing
this, you need to rely on globalor nonlocal variables, which gets ugly as your app grows.
It also allows for much finer controls once yourapp gets more complex, allowing you to
override default behaviours of Tkinter's own objects.
****************************************************************************************"""
try:
    import tkinter as tk
except ImportError:
    # Python 2
    import Tkinter as tk

class TkGUI(tk.Tk):
    """We start off by defining our Todo class and initialising it
    with an empty list of task."""
    def __init__(self):
        try:
            super(TkGUI, self).__init__(self)
        except TypeError:
            # Python 2
            tk.Tk.__init__(self)

        self.label = tk.Label(self, text="Hello World", padx=5, pady=5)

        self.label.pack()

if __name__ == "__main__":
    ROOT = TkGUI()
    ROOT.mainloop()
