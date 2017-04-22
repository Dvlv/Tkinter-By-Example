import tkinter as tk
from tkinter import font

class GameScreen():
    def __init__(self, master, image, roi, inventory_item=None, help_text=None):
        self.master = master
        self.roi = roi
        self.image = tk.PhotoImage(file=image)
        self.inventory_item = inventory_item
        self.help_text = help_text

    def on_click(self, event):
        if (self.roi[0] <= event.x <= self.roi[2]
            and self.roi[1] <= event.y <= self.roi[3]):

            if self.inventory_item:
                self.master.add_inventory_item(self.inventory_item)
            self.master.show_next_screen()


class Game(tk.Tk):
    def __init__(self):
        super().__init__()

        self.inventory_slots = []
        self.inventory_slots_in_use = []
        self.current_screen_number = 0
        self.success_font = font.Font(family="ubuntu", size=50, weight=font.BOLD)

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
        self.help_box.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.inventory_title = tk.Label(self.right_frame, text="Inventory:", background="grey", foreground="white")

        self.inventory_space = tk.Frame(self.right_frame, bg="blue", width=300, height=320)
        self.inventory_space.pack_propagate(0)

        self.inventory_space.pack(side=tk.BOTTOM)
        self.inventory_title.pack(side=tk.BOTTOM, fill=tk.X)

        self.inventory_slot_1 = tk.Button(self.inventory_space, image=self.question_mark_image, width=50, height=50)
        self.inventory_slot_2 = tk.Button(self.inventory_space, image=self.question_mark_image, width=50, height=50)
        self.inventory_slot_3 = tk.Button(self.inventory_space, image=self.question_mark_image, width=50, height=50)

        self.inventory_slot_1.pack(pady=(40,20), padx=20)
        self.inventory_slot_2.pack(pady=20, padx=20)
        self.inventory_slot_3.pack(pady=(20,0), padx=20)

        self.inventory_slots.append(self.inventory_slot_1)
        self.inventory_slots.append(self.inventory_slot_2)
        self.inventory_slots.append(self.inventory_slot_3)

        self.right_frame.pack(side=tk.RIGHT)
        self.screen.pack(side=tk.LEFT)

        self.screen.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        self.active_screen.on_click(event)

    def set_game_screens(self, game_screens):
        self.game_screens = game_screens

    def display_screen(self, game_screen_number):
        self.active_screen = self.game_screens[game_screen_number]
        self.screen.delete("all")
        self.screen.create_image((250,400), image=self.active_screen.image)
        self.help_var.set(self.active_screen.help_text)

    def show_next_screen(self):
        self.current_screen_number += 1;
        if self.current_screen_number < len(self.game_screens):
            self.display_screen(self.current_screen_number)
        else:
            self.screen.delete("all")
            self.screen.configure(bg="black")
            self.screen.create_text((250,300), text="You Win!", font=self.success_font, fill="white")

    def add_inventory_item(self, item_name):
        next_available_inventory_slot = len(self.inventory_slots_in_use)
        if next_available_inventory_slot < len(self.inventory_slots):
            next_slot = self.inventory_slots[next_available_inventory_slot]

            if item_name == "key":
                next_slot.configure(image=self.key_image)

            self.inventory_slots_in_use.append(item_name)

    def play(self):
        if not self.game_screens:
            print("No screens added!")
        else:
            self.display_screen(0)


game = Game()

scene1 = GameScreen(game, "assets/scene1.png", (378,135,427,217), "key", "You Need To Leave but the Door is Locked!")
scene2 = GameScreen(game, "assets/scene2.png", (117,54,329,412), None, "You Got the Key!")
scene3 = GameScreen(game, "assets/scene3.png", (117,54,329,412), None, "The Door is Open!")

all_screens = [scene1, scene2, scene3]

game.set_game_screens(all_screens)
game.play()
game.mainloop()
