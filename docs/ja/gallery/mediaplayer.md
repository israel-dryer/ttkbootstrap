# メディアプレーヤー
この例では、メディアプレーヤーのGUIを作成する方法を示します。ボタンは
単純なUnicode文字で構成されています。 

![ファイル検索画像の例](../assets/gallery/media_player.png)

## スタイルの概要
この例で使用されているテーマは **yeti** です。

| 項目                  | クラス     | ブートスタイル |
| ---                   | ---       | --- |
| ヘッダー                | `Label`   | light-inverse |
| メディアコントロール        | `Button`  | primary |
| ファイルオープン             | `Button`  | secondary |
| 経過時間スライダー   | `Scale`   | secondary |


## サンプルコード
repl.itでこのコードを実行する[(https://replit.com/@israel-dryer/media-player#main.py)](https://replit.com/@israel-dryer/media-player#main.py)

```python
from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.icons import Emoji


class MediaPlayer(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)
        self.hdr_var = ttk.StringVar()
        self.elapsed_var = ttk.DoubleVar(value=0)
        self.remain_var = ttk.DoubleVar(value=190)
        
        self.create_header()
        self.create_media_window()
        self.create_progress_meter()
        self.create_buttonbox()
    
    def create_header(self):
        """ユーザーメッセージを表示するためのアプリケーションヘッダー"""
        self.hdr_var.set("ファイルをオープンして再生を開始してください")
        lbl = ttk.Label(
            master=self, 
            textvariable=self.hdr_var, 
            bootstyle=(LIGHT, INVERSE),
            padding=10
        )
        lbl.pack(fill=X, expand=YES)

    def create_media_window(self):
        """メディアを格納するフレームを作成する"""
        img_path = Path(__file__).parent / 'assets/mp_background.png'
        self.demo_media = ttk.PhotoImage(file=img_path)
        self.media = ttk.Label(self, image=self.demo_media)
        self.media.pack(fill=BOTH, expand=YES)

    def create_progress_meter(self):
        """ラベル付きの進行状況メーターを含むフレームを作成する"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, padding=10)
        
        self.elapse = ttk.Label(container, text='00:00')
        self.elapse.pack(side=LEFT, padx=10)

        self.scale = ttk.Scale(
            master=container, 
            command=self.on_progress, 
            bootstyle=SECONDARY
        )
        self.scale.pack(side=LEFT, fill=X, expand=YES)

        self.remain = ttk.Label(container, text='03:10')
        self.remain.pack(side=LEFT, fill=X, padx=10)

    def create_buttonbox(self):
        """メディアコントロール付きのボタンボックスを作成する"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES)
        ttk.Style().configure('TButton', font="-size 14")

        rev_btn = ttk.Button(
            master=container,
            text=Emoji.get('black left-pointing double triangle with vertical bar'),
            padding=10,
        )
        rev_btn.pack(side=LEFT, fill=X, expand=YES)

        play_btn = ttk.Button(
            master=container,
            text=Emoji.get('black right-pointing triangle'),
            padding=10,
        )
        play_btn.pack(side=LEFT, fill=X, expand=YES)

        fwd_btn = ttk.Button(
            master=container,
            text=Emoji.get('black right-pointing double triangle with vertical bar'),
            padding=10,
        )
        fwd_btn.pack(side=LEFT, fill=X, expand=YES)

        pause_btn = ttk.Button(
            master=container,
            text=Emoji.get('double vertical bar'),
            padding=10,
        )
        pause_btn.pack(side=LEFT, fill=X, expand=YES)        

        stop_btn = ttk.Button(
            master=container,
            text=Emoji.get('黒い四角（停止）'),
            padding=10,
        )
        stop_btn.pack(side=LEFT, fill=X, expand=YES)          

        stop_btn = ttk.Button(
            master=container,
            text=Emoji.get('フォルダを開く'),
            bootstyle=SECONDARY,
            padding=10
        )
        stop_btn.pack(side=LEFT, fill=X, expand=YES)             


    def on_progress(self, val: float):
        """スケールが更新された際に、進行状況ラベルを更新します。"""
        elapsed = self.elapsed_var.get()
        remaining = self.remain_var.get()
        total = int(elapsed + remaining)
        
        elapse = int(float(val) * total)
        elapse_min = elapse // 60
        elapse_sec = elapse % 60
        
        remain_tot = total - elapse
        remain_min = remain_tot // 60
        remain_sec = remain_tot % 60

        self.elapsed_var.set(elapse)
        self.remain_var.set(remain_tot)

        self.elapse.configure(text=f'{elapse_min:02d}:{elapse_sec:02d}')
        self.remain.configure(text=f'{remain_min:02d}:{remain_sec:02d}')
        

if __name__ == '__main__':

    app = ttk.Window("Media Player", "yeti")
    mp = MediaPlayer(app)
    mp.scale.set(0.35)  # デフォルト値を設定
    app.mainloop()
```
