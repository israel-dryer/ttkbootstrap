import tkinter as tk
from queue import Queue
from random import randint
from threading import Thread
from time import sleep
from tkinter import ttk
from tkinter.messagebox import showinfo
from ttkbootstrap import Style


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Long Running Operation - Indeterminate')
        self.style = Style('lumen')

        # set the main background color to primary, then add 10px 
        # padding to create a thick border effect
        self.configure(background=self.style.colors.primary)
        self.lr = LongRunning(self)
        self.lr.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)


class LongRunning(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=20)
        self.task_queue = Queue()

        # instructions
        _text = '\n'.join([
            "Click the START button to begin a",
            "long-running task that will last",
            "approximately 5 to 15 seconds"
        ])
        lbl = ttk.Label(self, text=_text, justify=tk.LEFT)
        lbl.pack(fill=tk.X, pady=10)

        # start button
        self.btn = ttk.Button(self, text="START", command=self.start_task)
        self.btn.pack(pady=10)

        # indeterminate progressbar
        self.progressbar = ttk.Progressbar(
            master=self, 
            mode='indeterminate', 
            bootstyle='info'
        )
        self.progressbar.pack(fill=tk.X)

    def simulated_blocking_io_task(self):
        """A simulated IO operation to run for a random time interval 
        between 5 and 10 seconds
        """
        seconds_to_run = randint(5, 10)
        sleep(seconds_to_run)
        self.task_queue.task_done()

    def start_task(self):
        """Start the progressbar and run the task in another thread"""
        self.progressbar.start(10)
        self.task_queue.put(
            Thread(
                target=self.simulated_blocking_io_task, 
                daemon=True
            ).start()
        )
        self.btn.configure(state=tk.DISABLED)
        self.listen_for_complete_task()

    def listen_for_complete_task(self):
        """Check to see if task is complete; if so, stop the 
        progressbar and show and alert
        """
        if self.task_queue.unfinished_tasks == 0:
            self.progressbar.stop()
            showinfo(title='alert', message="process complete")
            self.btn.configure(state=tk.NORMAL)
            return
        self.after(500, self.listen_for_complete_task)


if __name__ == '__main__':
    Application().mainloop()
