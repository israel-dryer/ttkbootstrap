# ファイルバックアップユーティリティ
この例では、さまざまなスタイルを使用して、
ファイルバックアップユーティリティアプリケーションのUIを構築する方法を示します。カスタムクラス `CollapsingFrame` には、
左側の情報パネルと右下の出力領域が含まれています。これらには、
ヘッダーの右側にインジケーターボタンがあり、
マウスクリック操作で `Frame` を折りたたんだり展開したりできます。 

![ファイル検索画像の例](../assets/gallery/back_me_up.png)

## スタイルの概要
この例で使用されているテーマは **litera** です。

| 項目                              | クラス             | Bootstyle |
| ---                               | ---               | ---|
| 上部ボタンバー                    | `Button`          | primary |
| 折りたたみ可能なフレーム                | `CollapsingFrame` | secondary |
| セパレータ                        | `Separator`       | secondary |
| プログレスバー                      | `Progressbar`     | success |
| プロパティ、停止、バックアップに追加  | `Button`          | link |
| ファイルを開く                        | `Button`          | secondary-link |

## サンプルコード
[このコードをrepl.itで実行](https://replit.com/@israel-dryer/file-backup-utility#main.py)

```python
from datetime import datetime
from random import choices
import ttkbootstrap as ttk
from ttkbootstrap.style import Bootstyle
from tkinter.filedialog import askdirectory
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
from pathlib import Path


PATH = Path(__file__).parent / 'assets'


class BackMeUp(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        image_files = {
            'properties-dark': 'icons8_settings_24px.png',
            'properties-light': 'icons8_settings_24px_2.png',
            'add-to-backup-dark': 'icons8_add_folder_24px.png',
            'add-to-backup-light': 'icons8_add_book_24px.png',
            'stop-backup-dark': 'icons8_cancel_24px.png',
            'stop-backup-light': 'icons8_cancel_24px_1.png',
            'play': 'icons8_play_24px_1.png',
            'refresh': 'icons8_refresh_24px_1.png',
            'stop-dark': 'icons8_stop_24px.png',
            'stop-light': 'icons8_stop_24px_1.png',
            'opened-folder': 'icons8_opened_folder_24px.png',
            'logo': 'backup.png'
        }

        self.photoimages = []
        imgpath = Path(__file__).parent / 'assets'
        for key, val in image_files.items():
            _path = imgpath / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

        # ボタンバー
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=X, pady=1, side=TOP)

        ## 新規バックアップ
        _func = lambda: Messagebox.ok(message='新規バックアップを追加中')
        btn = ttk.Button(
            master=buttonbar, text='新しいバックアップセット',
            image='add-to-backup-light', 
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        ## バックアップ
        _func = lambda: Messagebox.ok(message='バックアップ中...')
        btn = ttk.Button(
            master=buttonbar, 
            text='バックアップ', 
            image='play', 
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## 更新
        _func = lambda: Messagebox.ok(message='更新中...')
        btn = ttk.Button(
            master=buttonbar, 
            text='更新', 
            image='refresh',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## 停止
        _func = lambda: Messagebox.ok(message='バックアップを停止します。')
        btn = ttk.Button(
            master=buttonbar, 
            text='停止', 
            image='stop-light',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## 設定
        _func = lambda: Messagebox.ok(message='設定を変更しています')
        btn = ttk.Button(
            master=buttonbar, 
            text='設定', 
            image='properties-light',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        # 左パネル
        left_panel = ttk.Frame(self, style='bg.TFrame')
        left_panel.pack(side=LEFT, fill=Y)

        ## バックアップ概要 (折りたたみ可能)
        bus_cf = CollapsingFrame(left_panel)
        bus_cf.pack(fill=X, pady=1)

        ## コンテナ
        bus_frm = ttk.Frame(bus_cf, padding=5)
        bus_frm.columnconfigure(1, weight=1)
        bus_cf.add(
            child=bus_frm, 
            title='バックアップ概要', 
            bootstyle=SECONDARY)

        ## 宛先
        lbl = ttk.Label(bus_frm, text='宛先:')
        lbl.grid(row=0, column=0, sticky=W, pady=2)
        lbl = ttk.Label(bus_frm, textvariable='destination')
        lbl.grid(row=0, column=1, sticky=EW, padx=5, pady=2)
        self.setvar('destination', 'd:/test/')

        ## 最終実行
        lbl = ttk.Label(bus_frm, text='最終実行:')
        lbl.grid(row=1, column=0, sticky=W, pady=2)
        lbl = ttk.Label(bus_frm, textvariable='lastrun')
        lbl.grid(row=1, column=1, sticky=EW, padx=5, pady=2)
        self.setvar('lastrun', '2021年6月14日 19:34:43')

        ## ファイルが同一
        lbl = ttk.Label(bus_frm, text='ファイルが同一:')
        lbl.grid(row=2, column=0, sticky=W, pady=2)
        lbl = ttk.Label(bus_frm, textvariable='filesidentical')
        lbl.grid(row=2, column=1, sticky=EW, padx=5, pady=2)
        self.setvar('filesidentical', '15%')

        ## セクションセパレータ
        sep = ttk.Separator(bus_frm, bootstyle=SECONDARY)
        sep.grid(row=3, column=0, columnspan=2, pady=10, sticky=EW)

        ## プロパティボタン
        _func = lambda: Messagebox.ok(message='プロパティを変更しています')
        bus_prop_btn = ttk.Button(
            master=bus_frm, 
            text='プロパティ', 
            image='properties-dark', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        bus_prop_btn.grid(row=4, column=0, columnspan=2, sticky=W)

        ## バックアップに追加ボタン
        _func = lambda: Messagebox.ok(message='バックアップに追加中')
        add_btn = ttk.Button(
            master=bus_frm, 
            text='バックアップに追加', 
            image='add-to-backup-dark', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        add_btn.grid(row=5, column=0, columnspan=2, sticky=W)

        # バックアップステータス (折りたたみ可能)
        status_cf = CollapsingFrame(left_panel)
        status_cf.pack(fill=BOTH, padding=1)

        ## コンテナ
        status_frm = ttk.Frame(status_cf, padding=10)
        status_frm.columnconfigure(1, weight=1)
        status_cf.add(
            child=status_frm, 
            title='バックアップステータス', 
            bootstyle=SECONDARY
        )
        ## 進行状況メッセージ
        lbl = ttk.Label(
            master=status_frm, 
            textvariable='prog-message', 
            font='Helvetica 10 bold'
        )
        lbl.grid(row=0, column=0, columnspan=2, sticky=W)
        self.setvar('prog-message', 'バックアップ中...')

        ## 進行状況バー
        pb = ttk.Progressbar(
            master=status_frm, 
            variable='prog-value', 
            bootstyle=SUCCESS
        )
        pb.grid(row=1, column=0, columnspan=2, sticky=EW, pady=(10, 5))
        self.setvar('prog-value', 71)

        ## 開始時刻
        lbl = ttk.Label(status_frm, textvariable='prog-time-started')
        lbl.grid(row=2, column=0, columnspan=2, sticky=EW, pady=2)
        self.setvar('prog-time-started', '開始日時: 2021年6月14日 19:34:56')

        ## 経過時間
        lbl = ttk.Label(status_frm, textvariable='prog-time-elapsed')
        lbl.grid(row=3, column=0, columnspan=2, sticky=EW, pady=2)
        self.setvar('prog-time-elapsed', '経過時間: 1 秒')

        ## 残り時間
        lbl = ttk.Label(status_frm, textvariable='prog-time-left')
        lbl.grid(row=4, column=0, columnspan=2, sticky=EW, pady=2)
        self.setvar('prog-time-left', '残り: 0 秒')

        ## セクション区切り
        sep = ttk.Separator(status_frm, bootstyle=SECONDARY)
        sep.grid(row=5, column=0, columnspan=2, pady=10, sticky=EW)

        ## 停止ボタン
        _func = lambda: Messagebox.ok(message='バックアップを停止します')
        btn = ttk.Button(
            master=status_frm, 
            text='停止', 
            image='stop-backup-dark', 
            compound=LEFT, 
            command=_func, 
            bootstyle=LINK
        )
        btn.grid(row=6, column=0, columnspan=2, sticky=W)

        ## セクションセパレータ
        sep = ttk.Separator(status_frm, bootstyle=SECONDARY)
        sep.grid(row=7, column=0, columnspan=2, pady=10, sticky=EW)

        # 現在のファイルメッセージ
        lbl = ttk.Label(status_frm, textvariable='current-file-msg')
        lbl.grid(row=8, column=0, columnspan=2, pady=2, sticky=EW)
        self.setvar('current-file-msg', 'アップロード中: d:/test/settings.txt')

        # ロゴ
        lbl = ttk.Label(left_panel, image='logo', style='bg.TLabel')
        lbl.pack(side='bottom')

        # 右パネル
        right_panel = ttk.Frame(self, padding=(2, 1))
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        ## ファイル入力
        browse_frm = ttk.Frame(right_panel)
        browse_frm.pack(side=TOP, fill=X, padx=2, pady=1)
        
        file_entry = ttk.Entry(browse_frm, textvariable='folder-path')
        file_entry.pack(side=LEFT, fill=X, expand=YES)
        
        btn = ttk.Button(
            master=browse_frm, 
            image='opened-folder', 
            bootstyle=(LINK, SECONDARY),
            command=self.get_directory
        )
        btn.pack(side=RIGHT)

        ## ツリービュー
        tv = ttk.Treeview(right_panel, show='headings', height=5)
        tv.configure(columns=(
            'name', 'state', 'last-modified', 
            'last-run-time', 'size'
        ))
        tv.column('name', width=150, stretch=True)
        
        for col in ['last-modified', 'last-run-time', 'size']:
            tv.column(col, stretch=False)
        
        for col in tv['columns']:
            tv.heading(col, text=col.title(), anchor=W)
        
        tv.pack(fill=X, pady=1)

        ## スクロールテキスト出力
        scroll_cf = CollapsingFrame(right_panel)
        scroll_cf.pack(fill=BOTH, expand=YES)
        
        output_container = ttk.Frame(scroll_cf, padding=1)
        _value = 'Log: バックアップ中... [ファイルのアップロード中: D:/sample_file_35.txt]'
        self.setvar('scroll-message', _value)
        st = ScrolledText(output_container)
        st.pack(fill=BOTH, expand=YES)
        scroll_cf.add(output_container, textvariable='scroll-message')

        # サンプルデータを初期化

        ## サンプルディレクトリの開始
        file_entry.insert(END, 'D:/text/myfiles/top-secret/samples/')

        ## ツリービューとバックアップログ
        for x in range(20, 35):
            result = choices(['Backup Up', 'Missed in Destination'])[0]
            st.insert(END, f'19:34:{x}\t\t Uploading: D:/file_{x}.txt\n')
            st.insert(END, f'19:34:{x}\t\t {result} をアップロード中\n')
            timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            tv.insert('', END, x, 
                      values=(f'sample_file_{x}.txt', 
                              result, timestamp, timestamp, 
                              f'{int(x // 3)} MB')
            )
        tv.selection_set(20)

    def get_directory(self):
        """ディレクトリを取得するためのダイアログを開き、変数を更新する"""
        self.update_idletasks()
        d = askdirectory()
        if d:
            self.setvar('folder-path', d)


class CollapsingFrame(ttk.Frame):
    """クリックで展開・折り畳みができるフレームウィジェットです。"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        # ウィジェットの画像
        self.images = [
            ttk.PhotoImage(file=PATH/'icons8_double_up_24px.png'),
            ttk.PhotoImage(file=PATH/'icons8_double_right_24px.png')
        ]

    def add(self, child, title="", bootstyle=PRIMARY, **kwargs):
        """折りたたみ可能なフレームに子要素を追加する

        パラメータ:

            child (Frame):
                ウィジェットに追加する子フレーム。

            title (str):
                折りたたみ可能なセクションのヘッダーに表示されるタイトル。

            bootstyle (str):
                折りたたみセクションのヘッダーに適用するスタイル。

            **kwargs (Dict):
                その他のオプションのキーワード引数。
        """
        if child.winfo_class() != 'TFrame':
            return
        
        style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = ttk.Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # ヘッダーのタイトル
        header = ttk.Label(
            master=frm,
            text=title,
            bootstyle=(style_color, INVERSE)
        )
        if kwargs.get('textvariable'):
            header.configure(textvariable=kwargs.get('textvariable'))
        header.pack(side=LEFT, fill=BOTH, padx=10)

        # ヘッダーのトグルボタン
        def _func(c=child): return self._toggle_open_close(c)
        btn = ttk.Button(
            master=frm,
            image=self.images[0],
            bootstyle=style_color,
            command=_func
        )
        btn.pack(side=RIGHT)

        # トグル操作が可能になるよう、トグルボタンを子ウィンドウに割り当てる
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)

        # 行の割り当てをインクリメント
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """セクションを開閉し、トグルボタンの
        画像をそれに応じて変更します。

        パラメータ:
            
            child (Frame):
                グリッドマネージャーに追加または削除する子要素。
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image=self.images[1])
        else:
            child.grid()
            child.btn.configure(image=self.images[0])


if __name__ == '__main__':
    
    app = ttk.Window("Back Me Up")
    BackMeUp(app)
    app.mainloop()
```
