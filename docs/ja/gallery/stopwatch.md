# ストップウォッチ
このストップウォッチアプリには、標準的な開始、停止、リセットの
機能があります。**開始**ボタンと
**一時停止**ボタンには、ボタンの状態に応じて異なるスタイルが適用されます。 

![ファイル検索画像の例](../assets/gallery/timer_widget_started.png)  

![ファイル検索画像例](../assets/gallery/timer_widget_paused.png)  

## スタイル概要
適用されているテーマは **cosmo** です。

| 項目      | クラス     | ブートスタイル |
| ---       | ---       | --- |
| 開始     | `Button`  | info |
| 一時停止 | `Button`  | info-outline |
| リセット | `Button`  | success |
| 終了     | `Button`  | danger |

## サンプルコード
repl.itでこのコードを実行する[(https://replit.com/@israel-dryer/stopwatch#main.py)](https://replit.com/@israel-dryer/stopwatch#main.py)

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
        """ストップウォッチの数字表示を作成する"""
        lbl = ttk.Label(
            master=self,
            font="-size 32",
            anchor=CENTER,
            textvariable=self.stopwatch_text,
        )
        lbl.pack(side=TOP, fill=X, padx=60, pady=20)

    def create_stopwatch_controls(self):
        """ボタン付きのコントロールフレームを作成する"""
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
                text="リセット",
                width=10,
                bootstyle=SUCCESS,
                command=self.on_reset,
            )
        )
        self.buttons.append(
            ttk.Button(
                master=container,
                text="終了",
                width=10,
                bootstyle=DANGER,
                command=self.on_quit,
            )
        )
        for button in self.buttons:
            button.pack(side=LEFT, fill=X, expand=YES, pady=10, padx=5)

    def on_toggle(self):
        """開始ボタンと一時停止ボタンを切り替えます。"""
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
        """アプリケーションを終了します。"""
        self.quit()

    def on_reset(self):
        """ストップウォッチの表示をリセットします。"""
        self.elapsed.set(0)
        self.stopwatch_text.set("00:00:00")

    def start(self):
        """ストップウォッチを開始し、表示を更新する。"""
        self.afterid.set(self.after(1, self.increment))

    def pause(self):
        """ストップウォッチを一時停止する"""
        self.after_cancel(self.afterid.get())

    def increment(self):
        """ストップウォッチの値をインクリメントする。このメソッドは、
        停止または一時停止されるまで、1秒ごとに自身をスケジュールし続ける。"""
        current = self.elapsed.get() + 1
        self.elapsed.set(current)
        formatted = "{:02d}:{:02d}:{:02d}".format(
            (current // 100) // 60, (current // 100) % 60, (current % 100)
        )
        self.stopwatch_text.set(formatted)
        self.afterid.set(self.after(100, self.increment))


if __name__ == "__main__":

    app = ttk.Window(
        title="ストップウォッチ", 
        themename="cosmo", 
        resizable=(False, False)
    )
    Stopwatch(app)
    app.mainloop()
```
