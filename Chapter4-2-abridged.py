import tkinter as tk
from tkinter import font
from functools import partial

class GameScreen():
    def __init__(self, master, image, roi, inventory_item=None, help_text=None, required_item=None):
        ...
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
        ...
        self.cannot_use_font = font.Font(family="ubuntu", size=28, weight=font.BOLD)
        self.item_in_use = ""
        self.has_won = False

        ...

        self.help_history_var_1 = tk.StringVar(self.right_frame)
        self.help_history_var_2 = tk.StringVar(self.right_frame)
        self.help_history_var_3 = tk.StringVar(self.right_frame)

        self.help_history_vars = [self.help_history_var_1, self.help_history_var_2, self.help_history_var_3]

        self.help_history_box_1 = tk.Label(self.right_frame, textvar=self.help_history_var_1, bg="black", fg="white", padx=10, pady=10)
        self.help_history_box_2 = tk.Label(self.right_frame, textvar=self.help_history_var_2, bg="black", fg="white", padx=10, pady=10)
        self.help_history_box_3 = tk.Label(self.right_frame, textvar=self.help_history_var_3, bg="black", fg="white", padx=10, pady=10)

        self.help_history_box_1.pack(side=tk.TOP, fill=tk.X, padx=10)
        self.help_history_box_2.pack(side=tk.TOP, fill=tk.X, padx=10)
        self.help_history_box_3.pack(side=tk.TOP, fill=tk.X, padx=10)

        ...

        self.inventory_row_1 = tk.Frame(self.inventory_space, pady=10)
        self.inventory_row_2 = tk.Frame(self.inventory_space, pady=10)
        self.inventory_row_3 = tk.Frame(self.inventory_space, pady=10)

        self.inventory_slot_1 = tk.Button(self.inventory_row_1,
                                          image=self.question_mark_image,
                                          width=50, height=50,
                                          bg="black",
                                          command=lambda: self.use_item(0))

        self.inventory_slot_2 = tk.Button(self.inventory_row_2,
                                          image=self.question_mark_image,
                                          width=50, height=50,
                                          bg="black",
                                          command=lambda: self.use_item(1))

        self.inventory_slot_3 = tk.Button(self.inventory_row_3,
                                          image=self.question_mark_image,
                                          width=50, height=50,
                                          bg="black",
                                          command=lambda: self.use_item(2))

        self.item_name_1 = tk.StringVar(self.inventory_row_1)
        self.item_name_2 = tk.StringVar(self.inventory_row_2)
        self.item_name_3 = tk.StringVar(self.inventory_row_3)

        self.item_label_vars = [self.item_name_1, self.item_name_2, self.item_name_3]

        self.item_label_1 = tk.Label(self.inventory_row_1, textvar=self.item_name_1, anchor="w")
        self.item_label_2 = tk.Label(self.inventory_row_2, textvar=self.item_name_2, anchor="w")
        self.item_label_3 = tk.Label(self.inventory_row_3, textvar=self.item_name_3, anchor="w")

        self.inventory_row_1.pack(fill=tk.X, expand=1)
        self.inventory_row_2.pack(fill=tk.X, expand=1)
        self.inventory_row_3.pack(fill=tk.X, expand=1)

        self.inventory_slot_1.pack(side=tk.LEFT, padx=(100,20))
        self.item_label_1.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.inventory_slot_2.pack(side=tk.LEFT, padx=(100,20))
        self.item_label_2.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.inventory_slot_3.pack(side=tk.LEFT, padx=(100,20))
        self.item_label_3.pack(side=tk.LEFT, fill=tk.X, expand=1)

        ...

    def handle_click(self, event):
        ...

    def set_game_screens(self, game_screens):
        ...

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
                self.screen.configure(cursor="box_spiral")

                for button in self.inventory_slots:
                    button.configure(state="normal")
                    button.configure(bg="black")

                self.inventory_slots[item_number].configure(bg="white")
                self.inventory_slots[item_number].configure(command=self.clear_used_item)

    def clear_used_item(self):
        self.item_in_use = ""
        for index, button in enumerate(self.inventory_slots):
            button.configure(state="normal")
            button.configure(bg="black")

            use_cmd = partial(self.use_item, item_number=index)
            button.configure(command=use_cmd)

    def show_cannot_use_message(self):
        text_id = self.screen.create_text((250,25), text="You cannot use that there!", font=self.cannot_use_font, fill="white")
        self.after(2000, lambda: self.screen.delete(text_id))

    def play(self):
        ...


if __name__ == "__main__":
    ...
