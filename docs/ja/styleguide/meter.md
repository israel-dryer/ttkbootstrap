# メーター

このウィジェットスタイルは、一連のコンポーネントで構成されています。インジケーターと
メインラベルは、デフォルトで**プライマリ**、または[選択された色](index.md#colors)になります。
指定された場合、サブテキストはライトテーマでは**セカンダリ**、ダークテーマでは
**ライト**になります。ただし、これらの要素はすべて、
[利用可能な色](index.md#colors)を使用して設定可能です。

![メーターの色](../assets/widget-styles/meter.gif)

メーターウィジェットは高度にカスタマイズ可能であり、色やその他のウィジェット固有の設定を組み合わせることで、
多種多様な興味深いメーターを作成できます。

![meter](../assets/widget-styles/meter.png)

```python
# デフォルトのメータースタイル
Meter()

# 情報表示用のカラーメーター
Meter(bootstyle="info")

# 警告色のサブテキスト
Meter(subtextstyle="danger")

# 成功色のメーターと警告色のサブテキスト
Meter(bootstyle="success", subtextstyle="warning")
```
