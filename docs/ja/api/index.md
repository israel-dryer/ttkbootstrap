# APIドキュメント

ttkbootstrap は tkinter のラッパーです。
このライブラリで特に定義されていないウィジェットや関数は、[その他のリファレンス](#other-references) で確認できます。

## 🌈 [colorutils モジュール](colorutils.md)
このモジュールには、色を操作するための様々なヘルパーメソッドが含まれています。

## 💬 dialogs モジュール
このモジュールには、エンドユーザー向けのカスタムダイアログを作成するために使用できる
様々なベースダイアログ基底クラス（「Dialog」で終わる）が含まれています。これらの基底クラスは、
`Messagebox` および `Querybox` コンテナクラス内の事前定義された静的ヘルパーメソッドの基盤として機能し、
多くの事前定義されたメッセージおよびクエリダイアログ設定を含んでいます。

❯ [ColorChooserDialog](dialogs/colorchooser.md)  
❯ [ColorDropperDialog](dialogs/colordropper.md)  
❯ [Dialog](dialogs/dialog.md)  
❯ [FontDialog](dialogs/fontdialog.md)  
❯ [MessageBox](dialogs/messagebox.md)  
❯ [MessageDialog](dialogs/messagedialog.md)  
❯ [QueryBox](dialogs/querybox.md)  
❯ [QueryDialog](dialogs/querydialog.md)  

## 😉 アイコンモジュール
このモジュールには、アプリケーション向けの絵文字や画像アイコンを提供するクラスが含まれています。
テキスト内では `Emoji` として、`PhotoImage` クラス内では `Icon` として使用できます。

❯ [Emoji](icons/emoji.md)  
❯ [Icon](icons/icon.md)  

## 🈚 ローカライゼーションモジュール
GUIウィジェット内のテキストをローカライズするためのメソッドとクラスが含まれます。
テキスト翻訳に使用するmsgファイルへの追加には[皆様のご協力が必要です](https://github.com/israel-dryer/ttkbootstrap/blob/master/src/ttkbootstrap/localization/msgs/README.md)！

## 📜 scrolled モジュール
このモジュールには、`ScrolledText` や `ScrolledFrame` などの様々なスクロール可能なウィジェットが含まれています。

❯ [ScrolledFrame](scrolled/scrolledframe.md)  
❯ [ScrolledText](scrolled/scrolledtext.md)  

## 🎨 スタイルモジュール
このモジュールには、ttkbootstrapのテーマとスタイルエンジンを構成するクラスが含まれています。
ttkbootstrapの使用方法によっては、これらのクラスを直接使用する必要が全くない場合もありますが、
逆に必要になる場合もあるため、ドキュメントは参考情報として用意されています。  

❯ [スタイル](style/style.md)  
❯ [カラー](style/colors.md)  
❯ [テーマ定義](style/themedefinition.md)  
❯ [StyleBuilderTk](style/stylebuildertk.md)  
❯ [StyleBuilderTTK](style/stylebuilderttk.md)  
❯ [Bootstyle](style/bootstyle.md)  

## 🪟 [tableview モジュール](tableview/tableview.md)
❯ [Tableview](tableview/tableview.md)  
❯ [TableColumn](tableview/tablecolumn.md)  
❯ [TableRow](tableview/tablerow.md)

## 🛎️ [toast モジュール](toast.md)
このモジュールには `ToastNotification` クラスが含まれており、
一時的なアラートやメッセージ用の半透明ポップアップウィンドウを提供します。

## 📝 [ツールチップモジュール](tooltip.md)
このモジュールには同名のクラスが含まれており、
ウィジェット上にマウスがホバーしている間テキストを表示し、
マウスが離れると閉じる半透明のツールチップポップアップウィンドウを提供します。

## ☑️ widgets モジュール
このモジュールには、以下にリンクされているカスタム ttkbootstrap ウィジェットが含まれています。  

❯ [DateEntry](widgets/dateentry.md)  
❯ [Floodgauge](widgets/floodgauge.md)  
❯ [Meter](widgets/meter.md)  

## 🗔 ウィンドウモジュール
このモジュールには、`tkinter.Tk` と [Style](style/style.md) クラスをラップする同名のクラスが含まれており、
アプリケーションの初期起動時により便利な API を提供します。これは `Toplevel` クラスにも適用されます。  

❯ [Window](window/window.md)  
❯ [Toplevel](window/toplevel.md)   


## ⚙️ [ユーティリティモジュール](utility.md)
このモジュールには、エンドユーザーにとって有用な場合もそうでない場合もある様々なユーティリティ関数が含まれています。
詳細を読むにはヘッダーをクリックしてください。

## ❓その他の参照資料
このAPIリファレンスは、**tkinter**から継承されたクラス、メソッド、関数は含みません。
tkinterの使用方法の詳細については、以下のリソースを参照してください：

❯ [docs.python.org](https://docs.python.org/3/library/tkinter.html)  
❯ [tkdocs](https://tkdocs.com/)  
❯ [pythontutorial.net](https://www.pythontutorial.net/tkinter/)  
❯ [anzeljg](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/)  
❯ [tcl/tk](https://www.tcl.tk/man/tcl8.6/TkCmd/contents.html)  
