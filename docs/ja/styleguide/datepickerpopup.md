# DatePickerDialog

このウィジェットスタイルは、ボタンおよびラベルウィジェットのコレクションで構成されています。
_ヘッダー_と_アクティブな日付_は、**プライマリ**カラー（デフォルト）または
[選択された色](index.md#colors)で表示されます。_曜日ヘッダー_と_現在の日付_は、
`セカンダリ`カラーを使用します。

このウィジェットの使用方法に関する詳細は、[APIドキュメント](../api/dialogs/datepickerdialog.md)をご確認ください。

![日付ピッカー](../assets/widget-styles/date-picker-popup.gif)

```python
# デフォルトのポップアップ
DatePickerDialog()

# 警告色のポップアップ
DatePickerDialog(bootstyle="warning")
```
