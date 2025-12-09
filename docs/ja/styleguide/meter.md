# メータ

このウィジェットスタイルは複数のコンポーネントで構成されています。インジケーターと
メインラベルはデフォルトで**プライマリ**、または[選択色](index.md#colors)です。
サブテキストが指定されている場合、ライトテーマでは**セカンダリ**、ダークテーマでは**ライト**となります。
ただし、これらの要素はすべて[利用可能な色](index.md#colors)で設定可能です。

![メーターカラー](../assets/widget-styles/meter.gif)

メーターウィジェットは高度にカスタマイズ可能で、
色やその他のウィジェット固有の設定を組み合わせることで多様な興味深いメーターを生成できます。

![メーター](../assets/widget-styles/meter.png)

```python
# デフォルトメータースタイル
Meter()

# 情報色メーター
Meter(bootstyle="info")

# 危険色サブテキスト
Meter(subtextstyle="danger")

# 成功色メーターと警告色サブテキスト
Meter(bootstyle="success", subtextstyle="warning")
```
