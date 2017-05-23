import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msg
import configparser as cp
import ntpath

class CentralForm(tk.Toplevel):
    def __init__(self, master, my_height=80):
        super().__init__()
        self.master = master

        master_pos_x = self.master.winfo_x()
        master_pos_y = self.master.winfo_y()

        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

        my_width = 300

        pos_x = (master_pos_x + (master_width // 2)) - (my_width // 2)
        pos_y = (master_pos_y + (master_height // 2)) - (my_height // 2)

        geometry = "{}x{}+{}+{}".format(my_width, my_height, pos_x, pos_y)
        self.geometry(geometry)


class AddSectionForm(CentralForm):
    def __init__(self, master):
        super().__init__(master)

        self.title("Add New Section")

        self.main_frame = tk.Frame(self, bg="lightgrey")
        self.name_label = tk.Label(self.main_frame, text="Section Name", bg="lightgrey", fg="black")
        self.name_entry = tk.Entry(self.main_frame, bg="white", fg="black")
        self.submit_button = tk.Button(self.main_frame, text="Create", command=self.create_section)

        self.main_frame.pack(expand=1, fill=tk.BOTH)
        self.name_label.pack(side=tk.TOP, fill=tk.X)
        self.name_entry.pack(side=tk.TOP, fill=tk.X, padx=10)
        self.submit_button.pack(side=tk.TOP, fill=tk.X, pady=(10,0), padx=10)

    def create_section(self):
        section_name = self.name_entry.get()
        if section_name:
            self.master.add_section(section_name)
            self.destroy()
            msg.showinfo("Section Added", "Section " + section_name + " successfully added")
        else:
            msg.showerror("No Name", "Please enter a section name", parent=self)


class AddItemForm(CentralForm):
    def __init__(self,  master):

        my_height = 120

        super().__init__(master, my_height)

        self.title("Add New Item")

        self.main_frame = tk.Frame(self, bg="lightgrey")
        self.name_label = tk.Label(self.main_frame, text="Item Name", bg="lightgrey", fg="black")
        self.name_entry = tk.Entry(self.main_frame, bg="white", fg="black")
        self.value_label = tk.Label(self.main_frame, text="Item Value", bg="lightgrey", fg="black")
        self.value_entry = tk.Entry(self.main_frame, bg="white", fg="black")
        self.submit_button = tk.Button(self.main_frame, text="Create", command=self.create_item)

        self.main_frame.pack(fill=tk.BOTH, expand=1)
        self.name_label.pack(side=tk.TOP, fill=tk.X)
        self.name_entry.pack(side=tk.TOP, fill=tk.X, padx=10)
        self.value_label.pack(side=tk.TOP, fill=tk.X)
        self.value_entry.pack(side=tk.TOP, fill=tk.X, padx=10)
        self.submit_button.pack(side=tk.TOP, fill=tk.X, pady=(10,0), padx=10)

    def create_item(self):
        item_name = self.name_entry.get()
        item_value = self.value_entry.get()
        if item_name and item_value:
            self.master.add_item(item_name, item_value)
            self.destroy()
            msg.showinfo("Item Added", item_name + " successfully added")
        else:
            msg.showerror("Missing Info", "Please enter a name and value", parent=self)


class IniEditor(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Config File Editor")
        self.geometry("600x600")

        self.active_ini = ""
        self.active_ini_filename = ""
        self.ini_elements = {}

        self.menubar = tk.Menu(self, bg="lightgrey", fg="black")

        self.file_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.file_menu.add_command(label="New", command=self.file_new, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.file_open, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.file_save, accelerator="Ctrl+S")

        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.config(menu=self.menubar)

        self.left_frame = tk.Frame(self, width=200, bg="grey")
        self.left_frame.pack_propagate(0)

        self.right_frame = tk.Frame(self, width=400, bg="lightgrey")
        self.right_frame.pack_propagate(0)

        self.file_name_var = tk.StringVar(self)
        self.file_name_label = tk.Label(self, textvar=self.file_name_var, fg="black", bg="white", font=(None, 12))
        self.file_name_label.pack(side=tk.TOP, expand=1, fill=tk.X, anchor="n")

        self.section_select = tk.Listbox(self.left_frame, selectmode=tk.SINGLE)
        self.section_select.configure(exportselection=False)
        self.section_select.pack(expand=1)
        self.section_select.bind("<<ListboxSelect>>", self.display_section_contents)

        self.section_add_button = tk.Button(self.left_frame, text="Add Section", command=self.add_section_form)
        self.section_add_button.pack(pady=(0,20))

        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.right_frame.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

        self.right_frame.bind("<Configure>", self.frame_height)

        self.bind("<Control-n>", self.file_new)
        self.bind("<Control-o>", self.file_open)
        self.bind("<Control-s>", self.file_save)

    def add_section_form(self):
        if not self.active_ini:
            msg.showerror("No File Open", "Please open an ini file first")
            return

        AddSectionForm(self)

    def add_section(self, section_name):
        self.active_ini[section_name] = {}
        self.populate_section_select_box()

    def frame_height(self, event=None):
        new_height = self.winfo_height()
        self.right_frame.configure(height=new_height)

    def file_new(self, event=None):
        ini_file = filedialog.asksaveasfilename(filetypes=[("Configuration file", "*.ini")])

        while ini_file and not ini_file.endswith(".ini"):
            msg.showerror("Wrong Filetype", "Filename must end in .ini")
            ini_file = filedialog.askopenfilename()

        if ini_file:
            self.parse_ini_file(ini_file)

    def file_open(self, event=None):
        ini_file = filedialog.askopenfilename(filetypes=[("Configuration file", "*.ini")])

        while ini_file and not ini_file.endswith(".ini"):
            msg.showerror("Wrong Filetype", "Please select an ini file")
            ini_file = filedialog.askopenfilename()

        if ini_file:
            self.parse_ini_file(ini_file)

    def file_save(self, event=None):
        if not self.active_ini:
            msg.showerror("No File Open", "Please open an ini file first")
            return

        for section in self.active_ini:
            for key in self.active_ini[section]:
                try:
                    self.active_ini[section][key] = self.ini_elements[section][key].get()
                except KeyError:
                    # wasn't changed, no need to save it
                    pass

        with open(self.active_ini_filename, "w") as ini_file:
            self.active_ini.write(ini_file)

        msg.showinfo("Saved", "File Saved Successfully")

    def add_item_form(self):
        AddItemForm(self)

    def add_item(self, item_name, item_value):
        chosen_section = self.section_select.get(self.section_select.curselection())
        self.active_ini[chosen_section][item_name] = item_value
        self.display_section_contents()

    def parse_ini_file(self, ini_file):
        self.active_ini = cp.ConfigParser()
        self.active_ini.read(ini_file)
        self.active_ini_filename = ini_file
        self.populate_section_select_box()

        file_name = ": ".join([ntpath.basename(ini_file), ini_file])
        self.file_name_var.set(file_name)

        self.clear_right_frame()

    def clear_right_frame(self):
        for child in self.right_frame.winfo_children():
            child.destroy()

    def populate_section_select_box(self):
        self.section_select.delete(0, tk.END)

        for index, section in enumerate(self.active_ini.sections()):
            self.section_select.insert(index, section)
            self.ini_elements[section] = {}
        if "DEFAULT" in self.active_ini:
            self.section_select.insert(len(self.active_ini.sections()) + 1, "DEFAULT")
            self.ini_elements["DEFAULT"] = {}

    def display_section_contents(self, event=None):
        if not self.active_ini:
            msg.showerror("No File Open", "Please open an ini file first")
            return

        chosen_section = self.section_select.get(self.section_select.curselection())

        for child in self.right_frame.winfo_children():
            child.pack_forget()

        for key in sorted(self.active_ini[chosen_section]):
            new_label = tk.Label(self.right_frame, text=key, font=(None, 12), bg="black", fg="white")
            new_label.pack(fill=tk.X, side=tk.TOP, pady=(10,0))

            try:
                section_elements = self.ini_elements[chosen_section]
            except KeyError:
                section_elements = {}

            try:
                ini_element = section_elements[key]
            except KeyError:
                value = self.active_ini[chosen_section][key]

                if value.isnumeric():
                    spinbox_default = tk.IntVar(self.right_frame)
                    spinbox_default.set(int(value))
                    ini_element = tk.Spinbox(self.right_frame, from_=0, to=99999, textvariable=spinbox_default, bg="white", fg="black", justify="center")
                else:
                    ini_element = tk.Entry(self.right_frame, bg="white", fg="black", justify="center")
                    ini_element.insert(0, value)

                self.ini_elements[chosen_section][key] = ini_element

            ini_element.pack(fill=tk.X, side=tk.TOP, pady=(0,10))

        save_button = tk.Button(self.right_frame, text="Save Changes", command=self.file_save)
        save_button.pack(side=tk.BOTTOM, pady=(0,20))

        add_button = tk.Button(self.right_frame, text="Add Item", command=self.add_item_form)
        add_button.pack(side=tk.BOTTOM, pady=(0,20))


if __name__ == "__main__":
    ini_editor = IniEditor()
    ini_editor.mainloop()
