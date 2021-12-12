import textwrap
from time import sleep
from queue import Queue
from random import randint
from threading import Thread
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


class LongRunning(ttk.Frame):

    threadqueue = Queue()

    def __init__(self, master):
        super().__init__(master, padding=5, bootstyle=INFO)
        self.pack(fill=BOTH, expand=YES)
        self.message = ttk.StringVar(value='')
        self.create_elements()

    def create_elements(self):
        """Create the layout elements."""
        container = ttk.Frame(self, padding=10)
        container.pack(fill=BOTH, expand=YES)
        
        _text = ("Click the START button to begin a long-running task " + 
                 "that will last approximately 1 to 15 seconds.")
        wrapped = '\n'.join(textwrap.wrap(_text, width=35))
        lbl = ttk.Label(container, text=wrapped, justify=LEFT)
        lbl.pack(fill=X, pady=10, expand=YES)

        self.start_btn = ttk.Button(
            master=container, 
            text='START',
            command=self.start_task
        )
        self.start_btn.pack(fill=X, pady=10)
        self.progressbar = ttk.Progressbar(
            master=container, 
            maximum=10, 
            bootstyle=(STRIPED, SUCCESS)
        )
        self.progressbar.pack(fill=X, expand=YES)
        msg_lbl = ttk.Label(container, textvariable=self.message, anchor=CENTER)
        msg_lbl.pack(fill=X, pady=10)

    def start_task(self):
        """Start the progressbar and run the task in another thread"""
        self.start_btn.configure(state=DISABLED)
        for i in range(1, 11):
            thread = Thread(
                target=self.simulate_io_task, 
                args=[i], 
                daemon=True
            )
            LongRunning.threadqueue.put(thread.start())
        self.listen_for_complete_task()

    def listen_for_complete_task(self):
        """Check to see if task is complete; if so, stop the 
        progressbar and show and alert
        """
        if LongRunning.threadqueue.unfinished_tasks == 0:
            self.progressbar.configure(value=10)
            Messagebox.ok(title='alert', message="process complete")
            self.start_btn.configure(state=NORMAL)
            self.message.set('')
            return
        max_value = self.progressbar.cget('maximum')
        tasks_completed = max_value - LongRunning.threadqueue.unfinished_tasks
        self.progressbar.configure(value=tasks_completed)
        self.after(500, self.listen_for_complete_task)

    def simulate_io_task(self, threadnum):
        """Simulate an IO operation to run for a random interval 
        between 1 and 15 seconds.
        """
        seconds_to_run = randint(1, 15)
        sleep(seconds_to_run)
        LongRunning.threadqueue.task_done()
        self.message.set(f'Finished task on Thread: {threadnum}')


if __name__ == '__main__':

    app = ttk.Window(title="task", themename="lumen")
    LongRunning(app)
    app.mainloop()
