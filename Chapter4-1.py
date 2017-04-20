import tkinter as tk
from tkinter import ttk

class Game(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Point and Click")
        self.geometry("800x640")
        self.minsize(width=800, height=640)
        self.maxsize(width=800, height=640)

        self.key_image = tk.PhotoImage(file='assets/key.png')
        self.question_mark_image = tk.PhotoImage(file='assets/questionmark.png')

        self.screen = tk.Canvas(self, bg="white", width=500, height=800)
        self.right_frame = tk.Frame(self, background="red", width=300, height=800)
        self.right_frame.pack_propagate(0)

        self.help_var = tk.StringVar(self.right_frame)
        self.help_var.set("Try Clicking Something")
        self.help_box = tk.Label(self.right_frame, textvar=self.help_var, background="black", foreground="white", padx=10, pady=20)

        self.inventory_title = tk.Label(self.right_frame, text="Inventory:", background="grey", foreground="white")

        self.inventory_space = tk.Frame(self.right_frame, bg="blue", width=300, height=320)
        self.inventory_space.pack_propagate(0)

        self.inventory_slot_1 = tk.Button(self.inventory_space, image=self.question_mark_image, width=50, height=50)
        self.inventory_slot_2 = tk.Button(self.inventory_space, image=self.question_mark_image, width=50, height=50)
        self.inventory_slot_3 = tk.Button(self.inventory_space, image=self.question_mark_image, width=50, height=50)

        self.help_box.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.inventory_slot_1.pack(pady=(40,20), padx=20)
        self.inventory_slot_2.pack(pady=20, padx=20)
        self.inventory_slot_3.pack(pady=(20,0), padx=20)

        self.inventory_space.pack(side=tk.BOTTOM)

        self.inventory_title.pack(side=tk.BOTTOM, fill=tk.X)

        self.right_frame.pack(side=tk.RIGHT)
        self.screen.pack(side=tk.LEFT)

game = Game()
game.mainloop()
