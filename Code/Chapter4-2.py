#! /usr/bin/env python
"""*********************************************************************
In this chapter we'll be creating one of those point-and-click puzzle 
games. Here we'll learn about the following:
-- Handling images
-- Drawing on and updating a Can
*********************************************************************"""
try:
    import tkinter as tk
    from tkinter import font
    PhotoImage = tk.PhotoImage
except ImportError:
    # Python 2
    import Tkinter as tk
    import tkFont as font
    from PIL import Image, ImageTk 
    PhotoImage = ImageTk.PhotoImage

from functools import partial

class GameScreen():
    def __init__(self, master, image, roi, inventory_item=None, help_text=None, required_item=None):
        self.master = master
        self.roi = roi
        self.image = PhotoImage(file=image)
        self.inventory_item = inventory_item
        self.help_text = help_text
        self.required_item = required_item

    def on_click(self, event, item_in_use):
        if self.master.has_won:
            return

        if item_in_use and not self.required_item:
            self.master.show_cannot_use_message()
        elif (self.roi[0] <= event.x <= self.roi[2]
            and self.roi[1] <= event.y <= self.roi[3]):

            if self.inventory_item:
                self.master.add_inventory_item(self.inventory_item)

            if self.required_item:
                if item_in_use == self.required_item:
                    self.master.show_next_screen()
            else:
                self.master.show_next_screen()
        else:
            if item_in_use:
                self.master.show_cannot_use_message()


class Game(tk.Tk):
    def __init__(self):
        try:
            super(Game, self).__init__()
        except TypeError:
            # Python 2
            tk.Tk.__init__(self)

        self.inventory_slots = []
        self.inventory_slots_in_use = []
        self.current_screen_number = 0
        self.success_font = font.Font(family="ubuntu", size=50, weight=font.BOLD)
        self.cannot_use_font = font.Font(family="ubuntu", size=28, weight=font.BOLD)
        self.item_in_use = ""
        self.has_won = False

        self.title("Point and Click")
        self.geometry("800x640")
        self.resizable(False, False)

        self.key_image = PhotoImage(file="../assets/key.png")
        self.question_mark_image = PhotoImage(file="../assets/questionmark.png")

        self.screen = tk.Canvas(self, bg="white", width=500, height=800)
        self.right_frame = tk.Frame(self, width=300, height=800)
        self.right_frame.pack_propagate(0)

        self.help_var = tk.StringVar(self.right_frame)
        self.help_var.set("")

        self.help_box = tk.Label(self.right_frame, textvar=self.help_var, bg="black", fg="white", padx=10, pady=20)
        self.help_box.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.help_history_var_1 = tk.StringVar(self.right_frame)
        self.help_history_var_2 = tk.StringVar(self.right_frame)
        self.help_history_var_3 = tk.StringVar(self.right_frame)

        help_history_box_1 = tk.Label(self.right_frame, textvar=self.help_history_var_1, bg="black", fg="white", padx=10, pady=10)
        help_history_box_2 = tk.Label(self.right_frame, textvar=self.help_history_var_2, bg="black", fg="white", padx=10, pady=10)
        help_history_box_3 = tk.Label(self.right_frame, textvar=self.help_history_var_3, bg="black", fg="white", padx=10, pady=10)

        help_history_box_1.pack(side=tk.TOP, fill=tk.X, padx=10)
        help_history_box_2.pack(side=tk.TOP, fill=tk.X, padx=10)
        help_history_box_3.pack(side=tk.TOP, fill=tk.X, padx=10)

        inventory_title = tk.Label(self.right_frame, text="Inventory:", background="grey", foreground="white")

        inventory_space = tk.Frame(self.right_frame, width=300, height=320)
        inventory_space.pack_propagate(0)

        inventory_space.pack(side=tk.BOTTOM)
        inventory_title.pack(side=tk.BOTTOM, fill=tk.X)

        inventory_row_1 = tk.Frame(inventory_space, pady=10)
        inventory_row_2 = tk.Frame(inventory_space, pady=10)
        inventory_row_3 = tk.Frame(inventory_space, pady=10)

        inventory_slot_1 = tk.Button(inventory_row_1,
                                     image=self.question_mark_image,
                                     width=50, height=50,
                                     bg="black",
                                     command=lambda: self.use_item(0))

        inventory_slot_2 = tk.Button(inventory_row_2,
                                     image=self.question_mark_image,
                                     width=50, height=50,
                                     bg="black",
                                     command=lambda: self.use_item(1))

        inventory_slot_3 = tk.Button(inventory_row_3,
                                     image=self.question_mark_image,
                                     width=50, height=50,
                                     bg="black",
                                     command=lambda: self.use_item(2))

        item_name_1 = tk.StringVar(inventory_row_1)
        item_name_2 = tk.StringVar(inventory_row_2)
        item_name_3 = tk.StringVar(inventory_row_3)

        self.item_label_vars = [item_name_1, item_name_2, item_name_3]

        item_label_1 = tk.Label(inventory_row_1, textvar=item_name_1, anchor="w")
        item_label_2 = tk.Label(inventory_row_2, textvar=item_name_2, anchor="w")
        item_label_3 = tk.Label(inventory_row_3, textvar=item_name_3, anchor="w")

        inventory_row_1.pack(fill=tk.X, expand=1)
        inventory_row_2.pack(fill=tk.X, expand=1)
        inventory_row_3.pack(fill=tk.X, expand=1)

        inventory_slot_1.pack(side=tk.LEFT, padx=(100,20))
        item_label_1.pack(side=tk.LEFT, fill=tk.X, expand=1)
        inventory_slot_2.pack(side=tk.LEFT, padx=(100,20))
        item_label_2.pack(side=tk.LEFT, fill=tk.X, expand=1)
        inventory_slot_3.pack(side=tk.LEFT, padx=(100,20))
        item_label_3.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.inventory_slots.append(inventory_slot_1)
        self.inventory_slots.append(inventory_slot_2)
        self.inventory_slots.append(inventory_slot_3)

        self.right_frame.pack(side=tk.RIGHT)
        self.screen.pack(side=tk.LEFT)

        self.screen.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        self.active_screen.on_click(event, self.item_in_use)

    def set_game_screens(self, game_screens):
        self.game_screens = game_screens

    def display_screen(self, game_screen_number):
        self.active_screen = self.game_screens[game_screen_number]
        self.screen.delete("all")
        self.screen.create_image((250,400), image=self.active_screen.image)
        self.show_help_text(self.active_screen.help_text)

    def show_next_screen(self):
        self.current_screen_number += 1;
        if self.current_screen_number < len(self.game_screens):
            self.display_screen(self.current_screen_number)
            self.clear_used_item()
        else:
            self.screen.delete("all")
            self.screen.configure(bg="black")
            self.screen.create_text((250,300), text="You Win!", font=self.success_font, fill="white")
            self.has_won = True

    def show_help_text(self, text):
        self.help_history_var_3.set(self.help_history_var_2.get())
        self.help_history_var_2.set(self.help_history_var_1.get())
        self.help_history_var_1.set(self.help_var.get())
        self.help_var.set(text)

    def add_inventory_item(self, item_name):
        next_available_inventory_slot = len(self.inventory_slots_in_use)
        if next_available_inventory_slot < len(self.inventory_slots):
            next_slot = self.inventory_slots[next_available_inventory_slot]
            next_label_var = self.item_label_vars[next_available_inventory_slot]

            if item_name == "key":
                next_slot.configure(image=self.key_image)

            next_label_var.set(item_name.title())
            self.inventory_slots_in_use.append(item_name)

    def use_item(self, item_number):
        if item_number < len(self.inventory_slots_in_use):
            item_name = self.inventory_slots_in_use[item_number]
            if item_name:
                self.item_in_use = item_name

                for button in self.inventory_slots:
                    button.configure(bg="black")

                self.inventory_slots[item_number].configure(bg="white")
                self.inventory_slots[item_number].configure(command=self.clear_used_item)

    def clear_used_item(self):
        self.item_in_use = ""
        for index, button in enumerate(self.inventory_slots):
            button.configure(bg="black")

            use_cmd = partial(self.use_item, item_number=index)
            button.configure(command=use_cmd)

    def show_cannot_use_message(self):
        text_id = self.screen.create_text((250,25), text="You cannot use that there!", font=self.cannot_use_font, fill="white")
        self.after(2000, lambda: self.screen.delete(text_id))

    def play(self):
        if not self.game_screens:
            print("No screens added!")
        else:
            self.display_screen(0)


if __name__ == "__main__":
    game = Game()

    scene1 = GameScreen(game, "../assets/scene1.png", (378,135,427,217), "key", "You Need To Leave but the Door is Locked!")
    scene2 = GameScreen(game, "../assets/scene2.png", (117,54,329,412), None, "You Got the Key!", "key")
    scene3 = GameScreen(game, "../assets/scene3.png", (117,54,329,412), None, "The Door is Open!")

    all_screens = [scene1, scene2, scene3]

    game.set_game_screens(all_screens)
    game.play()
    game.mainloop()
