![](https://img.shields.io/github/release/israel-dryer/ttkbootstrap.svg)
[![Downloads](https://pepy.tech/badge/ttkbootstrap)](https://pepy.tech/project/ttkbootstrap)
[![Downloads](https://pepy.tech/badge/ttkbootstrap/month)](https://pepy.tech/project/ttkbootstrap)
![](https://img.shields.io/github/issues/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/issues-closed/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/license/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/stars/israel-dryer/ttkbootstrap.svg)
![](https://img.shields.io/github/forks/israel-dryer/ttkbootstrap.svg)

# ttkbootstrap
日本語 | [English](README.md)

ttkbootstrapは、Bootstrapにインスパイアされたモダンでフラットなテーマを提供することで、tkinterを強化するPythonライブラリです。組み込みテーマ、事前定義されたウィジェットスタイルなどを使って、スタイリッシュなGUIアプリケーションを簡単に作成できます。

## ドキュメント
👀 [ドキュメントはこちら](https://ttkbootstrap.readthedocs.io/ja/latest/)

![](https://raw.githubusercontent.com/israel-dryer/ttkbootstrap/master/docs/assets/themes/themes.gif)

## 特徴
✔️ [**組み込みテーマ**](https://ttkbootstrap.readthedocs.io/ja/latest/themes/)  
ダークとライトのテーマを含む十数種類の厳選テーマ。

✔️ [**事前定義スタイル**](https://ttkbootstrap.readthedocs.io/ja/latest/styleguide/)  
**outline**や**round toggle**ボタンなど、美しいウィジェットスタイルが多数。

✔️ [**シンプルなキーワードAPI**](https://ttkbootstrap.readthedocs.io/ja/latest/gettingstarted/tutorial/#use-themed-widgets)  
従来の`primary.Striped.Horizontal.TProgressbar`のような複雑な指定ではなく、**primary**や**striped**といった簡単なキーワードで色やタイプを適用できます。Web開発でBootstrapを使ったことがある方なら、CSSクラスのようなこのアプローチに馴染みがあるでしょう。

✔️ [**新しいウィジェットが多数**](https://ttkbootstrap.readthedocs.io/ja/latest/api/widgets/dateentry/)  
**Meter**、**DateEntry**、**Floodgauge**など、美しく設計された新しいウィジェットを多数搭載。さらに、**dialogs**もテーマ対応で完全にカスタマイズ可能です。

✔️ [**テーマ作成機能を内蔵**](https://ttkbootstrap.readthedocs.io/ja/latest/themes/themecreator/)  
独自のテーマを作りたい？簡単です！ttkbootstrapにはテーマ作成ツールが組み込まれており、カスタムテーマの構築、読み込み、適用が容易にできます。

## インストール
ターミナル/コマンドプロンプトでpipを使ってttkbootstrapをインストールします。

```python
python -m pip install ttkbootstrap
```

## 簡単な使い方
複雑なttkスタイルクラスを使う代わりに、`bootstyle`パラメータでシンプルなキーワードを使用できます。

まず、IDEでファイルの先頭に以下を追加します：
```python
import ttkbootstrap as ttk
```

次に、`ttk.Window(...)`と`.mainloop()`でウィンドウを作成し、
ボタン（b1とb2）を追加して最初のウィンドウを作りましょう！
```python
root = ttk.Window(themename="superhero")

b1 = ttk.Button(root, text="Submit", bootstyle="success")
b1.pack(side=LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Submit", bootstyle="info-outline")
b2.pack(side=LEFT, padx=5, pady=10)

root.mainloop()
```
結果は次の通りです：

![コードの結果](beginningresult.png)

詳細な使い方は[**Getting Startedページ**](https://ttkbootstrap.readthedocs.io/ja/latest/gettingstarted/tutorial/)をご覧ください。
このページでは、ボタン作成、ウィジェット追加、スタイルの違いなどを説明しています。

新しいキーワードAPIは非常に柔軟です。以下の例はすべて同じ結果を生成します：
- `bootstyle="info-outline"`
- `bootstyle="info outline"`
- `bootstyle=("info", "outline")`
- `bootstyle=(INFO, OUTLINE)`

## アイコン
[ttkbootstrap-icons](https://github.com/israel-dryer/ttkbootstrap-icons)ライブラリを使って、アプリのボタンやラベルにBootstrapやLucideアイコンを追加できます。

## コントリビュート
貢献を歓迎します！ttkbootstrapに貢献したい場合は、ガイドラインをご確認ください。

## リンク
- **ドキュメント:** https://ttkbootstrap.readthedocs.io/ja/latest/
- **GitHub:** https://github.com/israel-dryer/ttkbootstrap

## サポート
このプロジェクトは、JetBrainsが提供する
<a href="https://www.jetbrains.com/pycharm/" target="_blank" rel="noopener">PyCharm IDE</a>のサポートを受けて開発されています。

<a href="https://www.jetbrains.com/" target="_blank" rel="noopener"> <picture> <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/f6d4e79d-97f4-4368-a944-affd423aa922"> <img width="250" alt="JetBrains logo" src="https://github.com/user-attachments/assets/1e42e5db-ffb5-4c8d-b238-3f5633fb7e6d"> </picture> </a>

<sub>© 2025 JetBrains s.r.o. JetBrainsおよびJetBrainsロゴはJetBrains s.r.o.の登録商標です。</sub>
