# TTKクリエイター

ttkbootstrapにはTTK Creatorが同梱されており、作成したテーマを編集、保存、エクスポート、インポートできます。

プログラムを実行するには、**ttkbootstrap**をインストールした後、コンソールで次のコマンドを入力します：

```shell
python -m ttkcreator
```

![creator](../assets/ttkcreator/creator.png)

## 新しいテーマを作成
テーマを変更するためのすべてのコントロールは、左側のコントロールフレームにあります。

1. **name**エントリでテーマ名を入力
2. **ベーステーマ**を選択します。これにより初期カラーが設定されます
3. 各カラーキーワードに対して次のいずれかの方法で色を選択します：
   * 🎨ボタンをクリックしてカラーダイアログから選択
   * または、16進数または有効なカラー名を入力
4. **Save**ボタンをクリック

テーマは `ttkbootstrap.themes.user.py` ファイルに保存されます。

!!! tip "テーマをリセット"
カラー選択をリセットしたい場合は、トップメニューの**Reset**オプションをクリックして、
すべてのカラーを**ベーステーマ**カラーに戻します。

## TTK Creatorテーマをインポート
以下の形式のユーザーテーマファイルがある場合、ttkbootstrapにインポートできます。

1. トップメニューの**Import**ボタンをクリック
2. インポートするテーマファイルを選択し、**Ok**をクリック

!!! warning
ユーザーテーマファイルをインポートすると、既存のユーザー定義テーマが上書きされます。
保持したい場合は、事前に**Export**してください。

`user.py`ファイルにはユーザー定義テーマの辞書が含まれています。
インポートするファイルは以下のパターンに一致する必要があります。

```python
USER_THEMES = {
    "supercosmo": {
        "type": "light",
        "colors": {
            "primary": "#2780e3",
            "secondary": "#7E8081",
            "success": "#3fb618",
            "info": "#9954bb",
            "warning": "#ff7518",
            "danger": "#ff0039",
            "light":"#F8F9FA",
            "dark": "#373A3C",
            "bg": "#ffffff",
            "fg": "#373a3c",
            "selectbg": "#7e8081",
            "selectfg": "#ffffff",
            "border": "#ced4da",
            "inputfg": "#373a3c",
            "inputbg": "#fdfdfe"
        }
    }
}
```

## JSONからユーザーテーマをインポート
`Style.load_user_themes`メソッドを使用してテーマをインポートできます。
この方法でインポートされたテーマは、実行時にのみプロジェクトに影響し、
前の例のようにttkbootstrapのソースファイルを変更しません。
これは、テーマをJSON形式で保存している場合や、特定のプロジェクトでのみテーマを利用したい場合に便利です。

JSONファイルの形式は次の例と一致する必要があります：

```json
{
  "themes": [
    {
      "midnight": {
        "type": "dark",
        "colors": {
          "primary": "#0a21f5",
            "secondary": "#555555",
            "success": "#77b300",
            "info": "#c6c6c6",
            "warning": "#ff8800",
            "danger": "#cc0000",
            "light": "#adafae",
            "dark": "#000000",
            "bg": "#000000",
            "fg": "#ffffff",
            "selectbg": "#454545",
            "selectfg": "#ffffff",
            "border": "#060606",
            "inputfg": "#ffffff",
            "inputbg": "#191919",
            "active": "#282828"
        }
      }
    },
    {
      "nightout": {
        "type": "dark",
        "colors": {
          "primary": "#164fe2",
            "secondary": "#555555",
            "success": "#77b300",
            "info": "#c0c0c0",
            "warning": "#ff8800",
            "danger": "#cc0000",
            "light": "#ADAFAE",
            "dark": "#222222",
            "bg": "#000000",
            "fg": "#ffffff",
            "selectbg": "#454545",
            "selectfg": "#ffffff",
            "border": "#060606",
            "inputfg": "#ffffff",
            "inputbg": "#191919",
            "active": "#282828"
        }
      }
    }
  ]
}
```

## TTK Creatorテーマをエクスポート
ユーザー定義テーマは、上記の形式でエクスポートできます。

1. トップメニューの**Export**ボタンをクリック
2. エクスポート先の場所を選択
3. 有効なファイル名を選択します（拡張子はデフォルトで`.py`）
4. **Ok**をクリックして設定を保存
