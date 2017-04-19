import tkinter as tk
from tkinter import ttk

class Game(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Point and Click")
        self.geometry("800x640")

        self.screen = tk.Canvas(self, bg="white", width=500, height=800)
        self.right_frame = tk.Frame(self, background="red", width=300, height=800)
        self.right_frame.pack_propagate(0)

        self.help_var = tk.StringVar(self.right_frame)
        self.help_var.set("Try Clicking Something")
        self.help_box = tk.Label(self.right_frame, textvar=self.help_var, background="black", foreground="white", padx=10, pady=20)

        self.inventory_title = tk.Label(self.right_frame, text="Inventory:")

        self.inventory_space = tk.Frame(self.right_frame, bg="blue", width=300, height=320)
        self.inventory_space.pack_propagate(0)

        self.inventory_slot_1 = ttk.Button(self.inventory_space)
        self.inventory_slot_2 = ttk.Button(self.inventory_space)
        self.inventory_slot_3 = ttk.Button(self.inventory_space)

        # key image
        #self.key_image = tk.PhotoImage('assets/key.png')

        # question mark image
        #self.question_mark_image = tk.PhotoImage('assets/questionmark.png')
        self.help_box.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        #self.inventory_title.pack()

        #self.inventory_slot_1.pack(side=tk.LEFT, padx=(50,25))
        #self.inventory_slot_2.pack(side=tk.LEFT, padx=25)
        #self.inventory_slot_3.pack(side=tk.LEFT, padx=25)

        self.inventory_space.pack(side=tk.BOTTOM)

        self.right_frame.pack(side=tk.RIGHT)
        self.screen.pack(side=tk.LEFT)

game = Game()
game.mainloop()
