from queue import Queue
from random import randint
from threading import Thread
from time import sleep
import tkinter as tk
import ttkbootstrap as ttk
from tkinter.messagebox import showinfo
from ttkbootstrap.style import utility


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        utility.enable_high_dpi_awareness(self)
        self.title('Long Running Operation - Determinate')
        self.style = ttk.Style('lumen')

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
            "approximately 1 to 15 seconds"
        ])
        lbl = ttk.Label(self, text=_text, justify=tk.LEFT)
        lbl.pack(fill=tk.X, pady=10)

        # start button
        self.btn = ttk.Button(self, text="START", command=self.start_task)
        self.btn.pack(pady=10)

        # determinate progress bar (for know number of steps)
        self.progressbar = ttk.Progressbar(
            master=self, 
            maximum=10, 
            bootstyle='info-striped'
        )
        self.progressbar.pack(fill=tk.X)

    def simulated_blocking_io_task(self, thread_num):
        """A simulated IO operation to run for a random time interval 
        between 1 and 15 seconds"""
        seconds_to_run = randint(1, 15)
        sleep(seconds_to_run)
        self.task_queue.task_done()
        print('Finished task on Thread:', thread_num)

    def start_task(self):
        """Start the progressbar and run the task in another thread"""
        self.btn.configure(state=tk.DISABLED)
        for i in range(1, 11):
            self.task_queue.put(
                Thread(
                    target=self.simulated_blocking_io_task, 
                    args=[i], daemon=True
                ).start())
        self.listen_for_complete_task()

    def listen_for_complete_task(self):
        """Check to see if task is complete; if so, stop the 
        progressbar and show and alert
        """
        if self.task_queue.unfinished_tasks == 0:
            self.progressbar.configure(value=10)
            showinfo(title='alert', message="process complete")
            self.btn.configure(state=tk.NORMAL)
            return
        tasks_completed = self.progressbar.cget('maximum') - self.task_queue.unfinished_tasks
        self.progressbar.configure(value=tasks_completed)
        self.after(500, self.listen_for_complete_task)


if __name__ == '__main__':
    Application().mainloop()
