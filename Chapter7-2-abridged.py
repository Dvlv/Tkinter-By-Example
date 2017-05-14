import sqlite3
import os
import functools
from tkinter import ttk

class CountingThread(threading.Thread):
    ...


class LogWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__()

        self.title("Log")
        self.geometry("600x300")

        self.notebook = ttk.Notebook(self)

        dates_sql = "SELECT DISTINCT date FROM pymodoros ORDER BY date DESC"
        dates = self.master.runQuery(dates_sql, None, True)

        for index, date in enumerate(dates):
            dates[index] = date[0].split()[0]

        dates = sorted(list(set(dates)))[::-1]

        for date in dates:
            tab = tk.Frame(self.notebook)

            columns = ("name", "finished", "time")

            tree = ttk.Treeview(tab, columns=columns, show="headings")

            tree.heading("name", text="Name")
            tree.heading("finished", text="Full 25 Minutes")
            tree.heading("time", text="Time")

            tree.column("name", anchor="center")
            tree.column("finished", anchor="center")
            tree.column("time", anchor="center")

            tasks_sql = "SELECT * FROM pymodoros WHERE date LIKE ?"
            date_like = date + "%"
            data = (date_like,)

            tasks = self.master.runQuery(tasks_sql, data, True)

            for task_name, task_finished, task_date in tasks:
                task_finished_text = "Yes" if task_finished else "No"
                task_time = task_date.split()[1]
                task_time_pieces = task_time.split(":")
                task_time_pretty = "{}:{}".format(task_time_pieces[0], task_time_pieces[1])
                tree.insert('', tk.END, values=(task_name, task_finished_text, task_time_pretty))

            tree.pack(fill=tk.BOTH, expand=1)

            self.notebook.add(tab, text=date)

        self.notebook.pack(fill=tk.BOTH, expand=1)


class Timer(tk.Tk):
    def __init__(self):
        ...

        self.menubar = tk.Menu(self, bg="lightgrey", fg="black")

        self.log_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.log_menu.add_command(label="View Log", command=self.show_log_window, accelerator="Ctrl+L")

        self.menubar.add_cascade(label="Log", menu=self.log_menu)
        self.configure(menu=self.menubar)

        ...

        self.bind("<Control-l>", self.show_log_window)

        ...

    def setup_worker(self):
        ...

    def start(self):
        if not self.task_name_entry.get():
            msg.showerror("No Task", "Please enter a task name")
            return

        ...
        self.task_finished_early = False
        ...

    def pause(self):
        ...

    def finish_early(self):
        self.start_button.configure(text="Start", command=self.start)
        self.task_finished_early = True
        self.worker.end_now = True

    def finish(self):
        ...
        if not self.task_finished_early:
            self.mark_finished_task()
        del self.worker
        msg.showinfo("Pomodoro Finished!", "Task completed, take a break!")

    def update_time_remaining(self, time_string):
        ...

    def add_new_task(self):
        task_name = self.task_name_entry.get()
        self.task_started_time = datetime.datetime.now()
        add_task_sql = "INSERT INTO pymodoros VALUES (?, 0, ?)"
        self.runQuery(add_task_sql, (task_name, self.task_started_time))

    def mark_finished_task(self):
        task_name = self.task_name_entry.get()
        add_task_sql = "UPDATE pymodoros SET finished = ? WHERE task = ? and date = ?"
        self.runQuery(add_task_sql, ("1", task_name, self.task_started_time))

    def show_log_window(self, evt=None):
        LogWindow(self)

    def safe_destroy(self):
        ...

    @staticmethod
    def runQuery(sql, data=None, receive=False):
        conn = sqlite3.connect('pymodoro.db')
        cursor = conn.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        if receive:
            return cursor.fetchall()
        else:
            conn.commit()

        conn.close()

    @staticmethod
    def firstTimeDB():
        create_tables = 'CREATE TABLE pymodoros (task text, finished integer, date text)'
        Timer.runQuery(create_tables)


if __name__ == "__main__":
    timer = Timer()

    if not os.path.isfile('pymodoro.db'):
        timer.firstTimeDB()

    timer.mainloop()

