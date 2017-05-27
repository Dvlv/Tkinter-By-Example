...

class CountingThread(threading.Thread):
    ...


class LogWindow(tk.Toplevel):
    def __init__(self, master):
        ...
        self.tab_trees = {}

        style = ttk.Style()
        style.configure("Treeview", font=(None,12))
        style.configure("Treeview.Heading", font=(None, 14))

        dates = self.master.get_unique_dates()

        for index, date in enumerate(dates):
            dates[index] = date[0].split()[0]

        dates = sorted(set(dates), reverse=True)

        for date in dates:
            ...

            tree.pack(fill=tk.BOTH, expand=1)
            tree.bind("<Double-Button-1>", self.confirm_delete)
            self.tab_trees[date] = tree

            self.notebook.add(tab, text=date)

        self.notebook.pack(fill=tk.BOTH, expand=1)

    def confirm_delete(self, event=None):
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        tree = self.tab_trees[current_tab]
        selected_item_id = tree.selection()
        selected_item = tree.item(selected_item_id)

        if msg.askyesno("Delete Item?", "Delete " + selected_item["values"][0] + "?", parent=self):
            task_name = selected_item["values"][0]
            task_time = selected_item["values"][2]
            task_date = " ".join([current_tab, task_time])
            self.master.delete_task(task_name, task_date)
            tree.delete(selected_item_id)

class Timer(tk.Tk):
    def __init__(self):
        ...

        style = ttk.Style()
        style.configure("TLabel", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
        style.configure("B.TLabel", font=(None, 40))
        style.configure("B.TButton", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
        style.configure("TEntry", foregound="black", background="white")

        ...

        self.task_name_label = ttk.Label(self.main_frame, text="Task Name:")
        self.task_name_entry = ttk.Entry(self.main_frame, font=(None, 16))
        self.start_button = ttk.Button(self.main_frame, text="Start", command=self.start, style="B.TButton")
        self.time_remaining_var = tk.StringVar(self.main_frame)
        self.time_remaining_var.set("25:00")
        self.time_remaining_label = ttk.Label(self.main_frame, textvar=self.time_remaining_var, style="B.TLabel")
        self.pause_button = ttk.Button(self.main_frame, text="Pause", command=self.pause, state="disabled", style="B.TButton")

        ...

        self.task_name_entry.focus_set()

    def setup_worker(self):
        ...

    def start(self):
        if not self.task_name_entry.get():
            ...

        if self.task_is_duplicate():
            msg.showerror("Task Duplicate", "Please enter a different task name")
            return

        ...

    def pause(self):
        ...

    def finish_early(self):
        ...

    def finish(self):
       ...

    def update_time_remaining(self, time_string):
        ...

    def add_new_task(self):
        ...

    def mark_finished_task(self):
        ...

    def show_log_window(self, event=None):
        ...

    def safe_destroy(self):
        ...

    def get_unique_dates(self):
        dates_sql = "SELECT DISTINCT date FROM pymodoros ORDER BY date DESC"
        dates = self.runQuery(dates_sql, None, True)

        return dates

    def get_tasks_by_date(self, date):
        tasks_sql = "SELECT * FROM pymodoros WHERE date LIKE ?"
        date_like = date + "%"
        data = (date_like,)

        tasks = self.runQuery(tasks_sql, data, True)

        return tasks

    def delete_task(self, task_name, task_date):
        delete_task_sql = "DELETE FROM pymodoros WHERE task = ? AND date LIKE ?"
        task_date_like = task_date + "%"
        data = (task_name, task_date_like)
        self.runQuery(delete_task_sql, data)

    def task_is_duplicate(self):
        task_name = self.task_name_entry.get()
        today = datetime.datetime.now().date()
        task_exists_sql = "SELECT task FROM pymodoros WHERE task = ? AND date LIKE ?"
        today_like = str(today) + "%"
        data = (task_name, today_like)
        tasks = self.runQuery(task_exists_sql, data, True)

        return len(tasks)

    @staticmethod
    def runQuery(sql, data=None, receive=False):
        ...

    @staticmethod
    def firstTimeDB():
        ...


if __name__ == "__main__":
    ...

