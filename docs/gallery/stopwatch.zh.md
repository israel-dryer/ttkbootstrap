# 秒表
此秒表应用程序具有标准的启动、停止和重置功能。 **Start** 和 **Pause** 按钮会根据按钮的状态应用不同的样式。

![文件搜索图像示例](../assets/gallery/timer_widget_started.png)

![文件搜索图像示例](../assets/gallery/timer_widget_paused.png)

## 风格总结
应用的主题是**cosmo**。

| 项目      | 类     | 配色样式 |
| ---       | ---       | --- |
| 开始     | `Button`  | info |
| 暂停     | `Button`  | info-outline |
| 重置     | `Button`  | success |
| 退出      | `Button`  | danger |

## 示例代码
[在 repl.it 上实时运行此代码](https://replit.com/@israel-dryer/stopwatch#main.py)

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class Stopwatch(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)
        self.running = ttk.BooleanVar(value=False)
        self.afterid = ttk.StringVar()
        self.elapsed = ttk.IntVar()
        self.stopwatch_text = ttk.StringVar(value="00:00:00")

        self.create_stopwatch_label()
        self.create_stopwatch_controls()

    def create_stopwatch_label(self):
        """Create the stopwatch number display"""
        lbl = ttk.Label(
            master=self,
            font="-size 32",
            anchor=CENTER,
            textvariable=self.stopwatch_text,
        )
        lbl.pack(side=TOP, fill=X, padx=60, pady=20)

    def create_stopwatch_controls(self):
        """Create the control frame with buttons"""
        container = ttk.Frame(self, padding=10)
        container.pack(fill=X)
        self.buttons = []
        self.buttons.append(
            ttk.Button(
                master=container,
                text="Start",
                width=10,
                bootstyle=INFO,
                command=self.on_toggle,
            )
        )
        self.buttons.append(
            ttk.Button(
                master=container,
                text="Reset",
                width=10,
                bootstyle=SUCCESS,
                command=self.on_reset,
            )
        )
        self.buttons.append(
            ttk.Button(
                master=container,
                text="Quit",
                width=10,
                bootstyle=DANGER,
                command=self.on_quit,
            )
        )
        for button in self.buttons:
            button.pack(side=LEFT, fill=X, expand=YES, pady=10, padx=5)

    def on_toggle(self):
        """Toggle the start and pause button."""
        button = self.buttons[0]
        if self.running.get():
            self.pause()
            self.running.set(False)
            button.configure(bootstyle=INFO, text="Start")
        else:
            self.start()
            self.running.set(True)
            button.configure(bootstyle=(INFO, OUTLINE), text="Pause")

    def on_quit(self):
        """Quit the application."""
        self.quit()

    def on_reset(self):
        """Reset the stopwatch number display."""
        self.elapsed.set(0)
        self.stopwatch_text.set("00:00:00")

    def start(self):
        """Start the stopwatch and update the display."""
        self.afterid.set(self.after(1, self.increment))

    def pause(self):
        """Pause the stopwatch"""
        self.after_cancel(self.afterid.get())

    def increment(self):
        """Increment the stopwatch value. This method continues to
        schedule itself every 1 second until stopped or paused."""
        current = self.elapsed.get() + 1
        self.elapsed.set(current)
        formatted = "{:02d}:{:02d}:{:02d}".format(
            (current // 100) // 60, (current // 100) % 60, (current % 100)
        )
        self.stopwatch_text.set(formatted)
        self.afterid.set(self.after(100, self.increment))


if __name__ == "__main__":

    app = ttk.Window(
        title="Stopwatch", 
        themename="cosmo", 
        resizable=(False, False)
    )
    Stopwatch(app)
    app.mainloop()
```