# スタイルガイド

これは ttkbootstrap スタイルを適用するためのスタイルガイドです。すべての ttkbootstrap スタイルは、
**ttk** ウィジェットコンストラクタに注入された **bootstyle** パラメータを使用して適用されます。

ℹ️ [レガシーウィジェットのスタイリングについて詳しく知る](legacywidgets.md)。

## 色

以下のカラーオプションは、除外されている場合を除き、_すべての_ウィジェットで使用可能です。
各ウィジェットごとに説明されているウィジェット固有のスタイルキーワードと併用できます。
デフォルトスタイルにはキーワードは不要です。 

下記キーワードの実際の色値は
[各テーマで定義されています](../themes/definitions.md)。
ただし下記説明は各色キーワードの典型的な挙動を示します。

| キーワード      | 説明                           | 例 |
| ---          | ---                                   | ---      |
| primary    | ほとんどのウィジェットのデフォルト色    | ![primary](../assets/colors/primary.png) |
| secondary  | 通常は_灰色_のカラー              | ![secondary](../assets/colors/secondary.png) |
| success    | 通常は_緑色_             | ![success](../assets/colors/success.png) |
| info       | 通常は_青色_              | ![info](../assets/colors/info.png) |
| warning    | 通常は_オレンジ色_           | ![warning](../assets/colors/warning.png) |
| danger    | 通常は_赤色_               | ![danger](../assets/colors/danger.png) |
| light      | 通常は_ライトグレー_色         | ![light](../assets/colors/light.png) |
| dark       | 通常は_ダークグレー_色         | ![dark](../assets/colors/dark.png) |


```python
# 情報色のボタンスタイル
Button(bootstyle="info")

# 警告色のスケールスタイル
Scale(bootstyle="warning")

# 成功色のプログレスバー
Progressbar(bootstyle="success")
```
