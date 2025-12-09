# DatePickerDialog

このウィジェットスタイルは、ボタンとラベルウィジェットの集合を包含します。
_ヘッダー_と_アクティブな日付_は、**プライマリ**カラー（デフォルト）または
[選択された色](index.md#colors)で表示されます。
_曜日ヘッダー_と_現在の日付_は、
`セカンダリ`カラーを使用します。

このウィジェットの使用方法の詳細については、
[APIドキュメント](../api/dialogs/datepickerdialog.md) を参照してください。

![date picker](../assets/widget-styles/date-picker-popup.gif)

```python
# デフォルトポップアップ
DatePickerDialog()

# 警告色ポップアップ
DatePickerDialog(bootstyle="warning")
```
