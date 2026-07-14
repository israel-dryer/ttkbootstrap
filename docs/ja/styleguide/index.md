# スタイルガイド

これは、ttkbootstrapのスタイルを適用するためのスタイルガイドです。すべてのttkbootstrapスタイルは、
**ttk**ウィジェットのコンストラクタに注入された**bootstyle**パラメータを使用して
適用されます。

ℹ️ [レガシーウィジェットのスタイリングについて詳しくはこちら](legacywidgets.md)。

## 色

以下のカラーオプションは、除外されている場合を除き、_すべての_ウィジェットで利用可能であり、
各ウィジェットで説明されているウィジェット固有のスタイルキーワードと併用できます。
デフォルトのスタイルにはキーワードは不要です。 

以下のキーワードの実際の色値は
[各テーマで定義されています](../themes/definitions.md)、ただし
以下の説明は、各色キーワードから一般的に期待される動作です。

| キーワード      | 説明                           | 例 |
| ---          | ---                                   | ---      |
| primary    | ほとんどのウィジェットのデフォルト色    | ![primary](../assets/colors/primary.png) |
| secondary  | 通常は_グレー_の色              | ![secondary](../assets/colors/secondary.png) |
| success    | 通常は_緑_色です                           | ![success](../assets/colors/success.png) |
| info       | 通常は_青_色です                           | ![info](../assets/colors/info.png) |
| 警告    | 通常は_オレンジ_色           | ![warning](../assets/colors/warning.png) |
| 危険     | 通常は_赤_色               | ![danger](../assets/colors/danger.png) |
| light      | 通常は _薄い灰色_ です        | ![light](../assets/colors/light.png) |
| dark       | 通常は _濃い灰色_ です         | ![dark](../assets/colors/dark.png) |


```python
# 情報用カラーボタンのスタイル
Button(bootstyle="info")

# 警告色のスケールスタイル
Scale(bootstyle="warning")

# 成功色のプログレスバー
Progressbar(bootstyle="success")
```
