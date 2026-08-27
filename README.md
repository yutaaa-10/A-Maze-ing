*This project has been created as part of the 42 curriculum by dkon, yukurosa.*


# A-Maze-ing


## 概要 (Description)

A-Maze-ingは、Pythonで迷路を生成するプログラムです。

このプロジェクトの目的は、迷路生成を通してアルゴリズム、ランダム性、
グラフ理論、経路探索、データ表現などの概念を学ぶことです。

プログラムは設定ファイルから迷路の情報を読み込み、その設定に基づいて
迷路を生成します。また、入口から出口までの最短経路を求め、
迷路の壁を16進数で表現した出力ファイルを生成します。

さらに、迷路生成部分は他のPythonプロジェクトでも再利用できるように、
`mazegen` というPythonパッケージとして提供しています。

---



## 手順 (Instructions)

### 開発ツールのインストール

`flake8` と `mypy` をインストールします。

```bash
make install
```

### プログラムの実行

デフォルトの `config.txt` を使用する場合：

```bash
make run
```

内部では次のコマンドが実行されます。

```bash
python3 a_maze_ing.py config.txt
```

別の設定ファイルを使用する場合：

```bash
make run CONFIG=example.txt
```

### デバッグ

Pythonの `pdb` を使用して実行します。

```bash
make debug
```

### パッケージのビルド

`mazegen` パッケージをビルドします。

```bash
make build
```

内部では、

```bash
python3 -m build
```

が実行され、`.whl` / `.tar.gz` が生成されます。

### キャッシュの削除

```bash
make clean
```

`__pycache__`、`.mypy_cache`、`.pytest_cache` を削除します。

### Lint

```bash
make lint
```

`flake8` と `mypy` を実行してコードを検査します。

より厳格なmypyチェックを行う場合：

```bash
make lint-strict
```


## 追加セクション (Additional sections)


###  設定ファイルの完全な構造と形式

迷路のサイズ、入口・出口、出力ファイル、Perfect は、config.txtから指定します。

リポジトリには、プログラムをすぐに実行できるデフォルトの
`config.txt` が含まれています。

#### 基本形式

設定ファイルは、1行につき1つの設定を以下の形式で記述します。

```text
KEY=VALUE
```

`#` から始まる行はコメントとして扱われ、プログラムから無視されます。

例：
```text
# Maze configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

#### ファイル構造

| キー | 形式 | 説明 | 例 |
| --- | --- | --- | --- |
| `WIDTH` | 整数 | 迷路の横幅（セル数） | `WIDTH=20` |
| `HEIGHT` | 整数 | 迷路の高さ（セル数） | `HEIGHT=15` |
| `ENTRY` | `x,y` | 迷路の入口となるセルの座標 | `ENTRY=0,0` |
| `EXIT` | `x,y` | 迷路の出口となるセルの座標 | `EXIT=19,14` |
| `OUTPUT_FILE` | 文字列 | 生成した迷路を書き込むファイル名 | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` / `False` | Perfect Mazeを生成するかを指定 | `PERFECT=True` |


### 選択した迷路生成アルゴリズム



### この迷路生成アルゴリズムを選択した理由


### コードのどの部分が再利用可能で、どのように再利用できるのか。

#### コードの再利用性

このプロジェクトでは、迷路生成ロジックを `mazegen` パッケージ内の
`MazeGenerator` クラスとして独立させています。

`MazeGenerator` は `a_maze_ing.py` の実行処理や表示処理から分離されているため、
他のPythonプロジェクトでも迷路生成機能だけを再利用できます。

パッケージは `.whl` または `.tar.gz` としてビルドでき、例えばwheelの場合は
以下のようにインストールできます。

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

インストール後は、別のPythonプロジェクトから次のように利用できます。

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    seed=42,
)
```

`width`、`height`、`seed` などのパラメータを変更することで、
用途に応じた異なる迷路を生成できます。

また、`MazeGenerator` から生成された迷路の構造にアクセスできるため、
ゲーム、迷路の可視化、経路探索など、別のアプリケーションでも迷路生成機能を
利用できます。



### チームとプロジェクト管理

#### 各チームメンバーの役割
・dkon：
```text
主に、迷路アルゴリズムの実装を担当。他にも、config.txtの作成やエラー処理も対応。
```

・yukurosa:
```text
主に、視覚表示や、メインファイルを作成。他にも、Makefileやtomlファイルも作成
```


#### 当初の計画と、それがどのように変化したか


#### 上手くいった点と改善すべき点
・上手く行った点:
```text

```

・改善すべき点:
```text

```

#### 特定のツールの使用状況
```text
主に、githubを使ってお互いの実装を共有し、離れているときはDiscordでコミュニケーションを取りました。
```

