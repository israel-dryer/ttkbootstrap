# Magic Mouse
このアプリケーションは、多数のオプションと
いくつかのラベルフレームを備えた複雑なデザインを実演しています。画像を使用するすべてのボタンには、
**リンク**ボタンスタイルが適用されています。

![ファイル検索画像の例](../assets/gallery/magic_mouse.png)

## スタイルの概要
使用されているテーマは**lumen**です。

| 項目              | クラス        | ブートスタイル  |
| ---               | ---          | ---        |
| 画像ボタン        | `Button`     | link       |
| ライセンス番号    | `Label`      | primary    |

## サンプルコード
repl.itで[このコードを実行](https://replit.com/@israel-dryer/magic-mouse#main.py)

```python
from pathlib import Path
from tkinter import PhotoImage
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


PATH = Path(__file__).parent / 'assets'


class MouseUtilities(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)
        
        self.images = [
            PhotoImage(
                name='reset', 
                file=PATH / 'magic_mouse/icons8_reset_24px.png'),
            PhotoImage(
                name='reset-small', 
                file=PATH / 'magic_mouse/icons8_reset_16px.png'),
            PhotoImage(
                name='submit', 
                file=PATH / 'magic_mouse/icons8_submit_progress_24px.png'),
            PhotoImage(
                name='question', 
                file=PATH / 'magic_mouse/icons8_question_mark_16px.png'),
            PhotoImage(
                name='direction', 
                file=PATH / 'magic_mouse/icons8_move_16px.png'),
            PhotoImage(
                name='bluetooth', 
                file=PATH / 'magic_mouse/icons8_bluetooth_2_16px.png'),
            PhotoImage(
                name='buy', 
                file=PATH / 'magic_mouse/icons8_buy_26px_2.png'),
            PhotoImage(
                name='mouse', 
                file=PATH / 'magic_mouse/magic_mouse.png')
        ]

        for i in range(3):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=1)

        # 列 1
        col1 = ttk.Frame(self, padding=10)
        col1.grid(row=0, column=0, sticky=NSEW)

        # デバイス情報
        dev_info = ttk.Labelframe(col1, text='Device Info', padding=10)
        dev_info.pack(side=TOP, fill=BOTH, expand=YES)

        # ヘッダー
        dev_info_header = ttk.Frame(dev_info, padding=5)
        dev_info_header.pack(fill=X)

        btn = ttk.Button(
            master=dev_info_header,
            image='reset',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=LEFT)

        lbl = ttk.Label(dev_info_header, text='Model 2009, 2xAA Batteries')
        lbl.pack(side=LEFT, fill=X, padx=15)

        btn = ttk.Button(
            master=dev_info_header,
            image='submit',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=LEFT)

        # 画像
        ttk.Label(dev_info, image='mouse').pack(fill=X)

        # プログレスバー
        pb = ttk.Progressbar(dev_info, value=66)
        pb.pack(fill=X, pady=5, padx=5)
        ttk.Label(pb, text='66%', bootstyle=(PRIMARY, INVERSE)).pack()

        # 進行状況メッセージ
        self.setvar('progress', 'バッテリーが放電中です。')
        lbl = ttk.Label(
            master=dev_info,
            textvariable='progress',
            font='Helvetica 8',
            anchor=CENTER
        )
        lbl.pack(fill=X)

        # ライセンス情報
        lic_info = ttk.Labelframe(col1, text='ライセンス情報', padding=20)
        lic_info.pack(side=TOP, fill=BOTH, expand=YES, pady=(10, 0))
        lic_info.rowconfigure(0, weight=1)
        lic_info.columnconfigure(0, weight=2)

        lic_title = ttk.Label(
            master=lic_info,
            text='試用版、残り28日',
            anchor=CENTER
        )
        lic_title.pack(fill=X, pady=(0, 20))

        lbl = ttk.Label(
            master=lic_info,
            text='マウスのシリアル番号:',
            anchor=CENTER,
            font='Helvetica 8'
        )
        lbl.pack(fill=X)
        self.setvar('license', 'dtMM2-XYZGHIJKLMN3')

        lic_num = ttk.Label(
            master=lic_info,
            textvariable='license',
            bootstyle=PRIMARY,
            anchor=CENTER
        )
        lic_num.pack(fill=X, pady=(0, 20))

        buy_now = ttk.Button(
            master=lic_info,
            image='buy',
            text='Buy now',
            compound=BOTTOM,
            command=self.callback
        )
        buy_now.pack(padx=10, fill=X)

        # 2列目
        col2 = ttk.Frame(self, padding=10)
        col2.grid(row=0, column=1, sticky=NSEW)

        # スクロール
        scrolling = ttk.Labelframe(col2, text='Scrolling', padding=(15, 10))
        scrolling.pack(side=TOP, fill=BOTH, expand=YES)

        op1 = ttk.Checkbutton(scrolling, text='スクロール', variable='op1')
        op1.pack(fill=X, padding=5)

        # 水平スクロールなし
        op2 = ttk.Checkbutton(
            master=scrolling,
            text='水平スクロールなし',
            variable='op2'
        )
        op2.pack(fill=X, padx=(20, 0), pady=5)

        btn = ttk.Button(
            master=op2,
            image='question',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=RIGHT)

        # 反転
        op3 = ttk.Checkbutton(
            master=scrolling,
            text='スクロール方向を垂直方向に反転',
            variable='op3'
        )
        op3.pack(fill=X, padx=(20, 0), pady=5)

        btn = ttk.Button(
            master=op3,
            image='direction',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=RIGHT)

        # 垂直または水平方向のみスクロール
        op4 = ttk.Checkbutton(
            master=scrolling,
            text='垂直または水平方向のみスクロール',
            state=DISABLED
        )
        op4.configure(variable='op4')
        op4.pack(fill=X, padx=(20, 0), pady=5)

        # スムーズスクロール
        op5 = ttk.Checkbutton(
            master=scrolling,
            text='スムーズスクロール',
            variable='op5'
        )
        op5.pack(fill=X, padx=(20, 0), pady=5)

        btn = ttk.Button(
            master=op5,
            image='bluetooth',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=RIGHT)

        # スクロール速度
        scroll_speed_frame = ttk.Frame(scrolling)
        scroll_speed_frame.pack(fill=X, padx=(20, 0), pady=5)

        lbl = ttk.Label(scroll_speed_frame, text='Speed:')
        lbl.pack(side=LEFT)

        scale = ttk.Scale(scroll_speed_frame, value=35, from_=1, to=100)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

        scroll_speed_btn = ttk.Button(
            master=scroll_speed_frame,
            image='reset-small',
            bootstyle=LINK,
            command=self.callback
        )
        scroll_speed_btn.pack(side=LEFT)

        # スクロール方向
        scroll_sense_frame = ttk.Frame(scrolling)
        scroll_sense_frame.pack(fill=X, padx=(20, 0), pady=(5, 0))

        ttk.Label(scroll_sense_frame, text='Sense:').pack(side=LEFT)

        scale = ttk.Scale(scroll_sense_frame, value=50, from_=1, to=100)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

        scroll_sense_btn = ttk.Button(
            master=scroll_sense_frame,
            image='reset-small',
            bootstyle=LINK,
            command=self.callback
        )
        scroll_sense_btn.pack(side=LEFT)

        # 1本指のジェスチャー
        finger_gest = ttk.Labelframe(
            master=col2,
            text='1本指のジェスチャー',
            padding=(15, 10)
        )
        finger_gest.pack(
            side=TOP,
            fill=BOTH,
            expand=YES,
            pady=(10, 0)
        )
        op6 = ttk.Checkbutton(
            master=finger_gest,
            text='高速左右スワイプ',
            variable='op6'
        )
        op6.pack(fill=X, pady=5)

        cb = ttk.Checkbutton(
            master=finger_gest,
            text='スワイプ方向を切り替える',
            variable='op7'
        )
        cb.pack(fill=X, padx=(20, 0), pady=5)

        # ジェスチャーの方向
        gest_sense_frame = ttk.Frame(finger_gest)
        gest_sense_frame.pack(fill=X, padx=(20, 0), pady=(5, 0))

        ttk.Label(gest_sense_frame, text='Sense:').pack(side=LEFT)

        scale = ttk.Scale(gest_sense_frame, value=50, from_=1, to=100)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

        btn = ttk.Button(
            master=gest_sense_frame,
            image='reset-small',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=LEFT)

        # ミドルクリック
        middle_click = ttk.Labelframe(
            master=col2,
            text='Middle Click',
            padding=(15, 10)
        )
        middle_click.pack(
            side=TOP,
            fill=BOTH,
            expand=YES,
            pady=(10, 0)
        )
        cbo = ttk.Combobox(
            master=middle_click,
            values=['2本指（任意）', 'その他1本指', 'その他2本指']
        )
        cbo.current(0)
        cbo.pack(fill=X)

        # 3列目
        col3 = ttk.Frame(self, padding=10)
        col3.grid(row=0, column=2, sticky=NSEW)

        # 2本指のジェスチャー
        two_finger_gest = ttk.Labelframe(
            master=col3,
            text='2本指のジェスチャー',
            padding=10
        )
        two_finger_gest.pack(side=TOP, fill=BOTH)

        op7 = ttk.Checkbutton(
            master=two_finger_gest,
            text='高速左右スワイプ',
            variable='op7'
        )
        op7.pack(fill=X, padding=5)

        op8 = ttk.Checkbutton(
            master=two_finger_gest,
            text='スワイプ方向の切り替え',
            variable='op8'
        )
        op8.pack(fill=X, padx=(20, 0), pady=5)

        # ジェスチャーの方向
        gest_sense_frame = ttk.Frame(two_finger_gest)
        gest_sense_frame.pack(fill=X, padx=(20, 0), pady=(5, 0))

        ttk.Label(gest_sense_frame, text='Sense:').pack(side=LEFT)

        scale = ttk.Scale(gest_sense_frame, value=50, from_=1, to=100)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

        btn = ttk.Button(
            master=gest_sense_frame,
            image='reset-small',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=LEFT)

        # 高速な2本指スワイプ（下方向）
        lbl = ttk.Label(
            master=two_finger_gest,
            text='高速な2本指スワイプ（上/下方向）時:'
        )
        lbl.pack(fill=X, pady=(10, 5))

        op9 = ttk.Checkbutton(
            master=two_finger_gest,
            text='スワイプ方向を切り替える',
            variable='op9'
        )
        op9.pack(fill=X, padx=(20, 0), pady=5)

        op10 = ttk.Checkbutton(
            master=two_finger_gest,
            text='スワイプ方向を入れ替える',
            variable='op10'
        )
        op10.pack(fill=X, padx=(20, 0), pady=5)

        two_finger_cbo = ttk.Combobox(
            master=two_finger_gest,
            values=['タスクビューの切り替え | 通常 | デスクトップビュー']
        )
        two_finger_cbo.current(0)
        two_finger_cbo.pack(fill=X, padx=(20, 0), pady=5)

        # 2本指ジェスチャー
        two_finger_sense_frame = ttk.Frame(two_finger_gest)
        two_finger_sense_frame.pack(fill=X, padx=(20, 0), pady=(5, 0))

        ttk.Label(two_finger_sense_frame, text='Sense:').pack(side=LEFT)

        scale = ttk.Scale(two_finger_sense_frame, value=50, from_=1, to=100)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

        two_finger_sense_btn = ttk.Button(
            master=two_finger_sense_frame,
            image='reset-small',
            bootstyle=LINK
        )
        two_finger_sense_btn.configure(command=self.callback)
        two_finger_sense_btn.pack(side=LEFT)

        # マウスオプション
        mouse_options = ttk.Labelframe(
            master=col3,
            text='2 Finger Gestures',
            padding=(15, 10)
        )
        mouse_options.pack(
            side=TOP,
            fill=BOTH,
            expand=YES,
            pady=(10, 0)
        )

        op11 = ttk.Checkbutton(
            master=mouse_options,
            text='マウスが離された場合の入力を無視する',
            variable='op11'
        )
        op11.pack(fill=X, pady=5)

        op12 = ttk.Checkbutton(
            master=mouse_options,
            text='マウスが離された場合の入力を無視する',
            variable='op12'
        )
        op12.pack(fill=X, pady=5)

        op13 = ttk.Checkbutton(
            master=mouse_options,
            text='マウスが離された場合、入力を無視する',
            variable='op13'
        )
        op13.pack(fill=X, pady=5)

        # 基本速度
        base_speed_sense_frame = ttk.Frame(mouse_options)
        base_speed_sense_frame.pack(fill=X, padx=(20, 0), pady=(5, 0))

        lbl = ttk.Label(base_speed_sense_frame, text='基本速度:')
        lbl.pack(side=LEFT)

        scale = ttk.Scale(base_speed_sense_frame, value=50, from_=1, to=100)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

        base_speed_sense_btn = ttk.Button(
            master=base_speed_sense_frame,
            image='reset-small',
            bootstyle=LINK
        )
        base_speed_sense_btn.configure(command=self.callback)
        base_speed_sense_btn.pack(side=LEFT)

        # すべてのチェックボタンをオンにする
        for i in range(1, 14):
            self.setvar(f'op{i}', 1)

        # 選択ボタンをオフにする
        for j in [2, 9, 12, 13]:
            self.setvar(f'op{j}', 0)

    def callback(self):
        """デモ用コールバック"""
        Messagebox.ok(
            title='Button callback', 
            message="ボタンを押しました。"
        )


if __name__ == '__main__':

    app = ttk.Window("Magic Mouse", "yeti")
    MouseUtilities(app)
    app.mainloop()
```
