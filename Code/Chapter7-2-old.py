import threading
import time
import datetime
import sqlite3
import os
import functools
import tkinter as tk
from tkinter import messagebox as msg

class CountingThread(threading.Thread):
    def __init__(self, master, start_time, end_time):
        super().__init__()
        self.master = master
        self.start_time = start_time
        self.end_time = end_time

        self.end_now = False
        self.paused = False
        self.force_quit = False

    def run(self):
        while True:
            if not self.paused and not self.end_now and not self.force_quit:
                self.main_loop()
                time.sleep(0.1)
                if datetime.datetime.now() >= self.end_time:
                    if not self.force_quit:
                        self.master.finish()
                        break
            elif self.end_now:
                self.master.finish()
                break
            elif self.force_quit:
                del self.master.worker
                return
            else:
                continue
        return

    def main_loop(self):
        now = datetime.datetime.now()
        if now < self.end_time:
            time.sleep(0.1)
            time_difference = self.end_time - now
            hours, remainder = divmod(time_difference.seconds, 3600)
            mins, secs = divmod(remainder, 60)
            time_string = "{:02d}:{:02d}".format(mins, secs)
            if not self.force_quit:
                self.master.update_time_remaining(time_string)


class Timer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro Timer")
        self.geometry("500x300")
        self.resizable(False, False)

        self.standard_font = (None, 16)

        self.menubar = tk.Menu(self, bg="lightgrey", fg="black")

        self.log_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.log_menu.add_command(label="View Log", command=self.show_log_window, accelerator="Ctrl+L")

        self.menubar.add_cascade(label="Log", menu=self.log_menu)
        self.configure(menu=self.menubar)

        self.main_frame = tk.Frame(self, width=500, height=300, bg="lightgrey")

        self.task_name_label = tk.Label(self.main_frame, text="Task Name:", bg="lightgrey", fg="black", font=self.standard_font)
        self.task_name_entry = tk.Entry(self.main_frame, bg="white", fg="black", font=self.standard_font)
        self.start_button = tk.Button(self.main_frame, text="Start", bg="lightgrey", fg="black", command=self.start, font=self.standard_font)
        self.time_remaining_var = tk.StringVar(self.main_frame)
        self.time_remaining_var.set("25:00")
        self.time_remaining_label = tk.Label(self.main_frame, textvar=self.time_remaining_var, bg="lightgrey", fg="black", font=(None, 40))
        self.pause_button = tk.Button(self.main_frame, text="Pause", bg="lightgrey", fg="black", command=self.pause, font=self.standard_font, state="disabled")

        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.task_name_label.pack(fill=tk.X, pady=15)
        self.task_name_entry.pack(fill=tk.X, padx=50, pady=(0,20))
        self.start_button.pack(fill=tk.X, padx=50)
        self.time_remaining_label.pack(fill=tk.X ,pady=15)
        self.pause_button.pack(fill=tk.X, padx=50)

        self.bind("<Control-l>", self.show_log_window)

        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)

    def setup_worker(self):
        now = datetime.datetime.now()
        #in_25_mins = now + datetime.timedelta(minutes=25)
        in_25_mins = now + datetime.timedelta(seconds=8)
        worker = CountingThread(self, now, in_25_mins)
        self.worker = worker
        self.start_time = now

    def start(self):
        if not hasattr(self, "worker"):
            self.setup_worker()

        if self.start_button.cget("text") == "Finish":
            self.start_button.configure(text="Restart")
            self.worker.end_now = True

        elif self.start_button.cget("text") == "Restart":
            self.setup_worker()
            self.restart()

        else:
            self.task_name_entry.configure(state="disabled")
            self.start_button.configure(text="Finish")
            self.time_remaining_var.set("25:00")
            self.pause_button.configure(state="normal")
            self.add_task_to_db()
            self.worker.start()


    def pause(self):
        self.worker.paused = not self.worker.paused
        if self.worker.paused:
            self.pause_button.configure(text="Resume")
            self.worker.start_time = datetime.datetime.now()
        else:
            self.pause_button.configure(text="Pause")
            end_timedelta = datetime.datetime.now() - self.worker.start_time
            self.worker.end_time = self.worker.end_time + datetime.timedelta(seconds=end_timedelta.seconds)

    def show_log_window(self):
        pass

    def add_task_to_db(self):
        pass

    def mark_task_as_completed(self):
        pass

    def update_time_remaining(self, time_string):
        self.time_remaining_var.set(time_string)

    def restart(self):
        self.task_name_entry.configure(state="disabled")
        self.start_button.configure(text="Finish")
        self.time_remaining_var.set("25:00")
        self.add_task_to_db()
        self.worker.start()

    def finish(self):
        self.mark_task_as_completed()
        self.task_name_entry.configure(state="normal")
        self.time_remaining_var.set("25:00")
        self.pause_button.configure(state="disabled")
        msg.showinfo("Pomodoro Finished!", "Task completed, take a break!")

    def safe_destroy(self):
        if hasattr(self, "worker"):
            self.worker.force_quit = True
            self.after(100, self.safe_destroy)
        else:
            self.destroy()


if __name__ == "__main__":
    timer = Timer()
    timer.mainloop()
