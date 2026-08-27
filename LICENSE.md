## コードの再利用性

このプロジェクトでは、迷路生成に関する主要な処理を `mazegen` パッケージとして
独立させています。

`mazegen` は `a_maze_ing.py` の対話処理、設定ファイルの読み込み、
ターミナル表示などから分離されているため、他のPythonプロジェクトでも
迷路生成機能を再利用できます。

### 再利用可能な主な機能

- `MazeGenerator`
  - 指定された幅・高さの迷路を生成します。
  - seedを指定することで、同じ条件の迷路を再現できます。
  - `perfect=True / False` に応じた迷路生成に対応します。

- `Maze`
  - 生成された迷路構造を表す型です。

- `get_shortest_path`
  - 生成された迷路から、ENTRYからEXITまでの最短経路を取得します。

- `to_hex`
  - 生成された迷路構造を、課題指定の16進数形式へ変換します。

---

### パッケージのビルドとインストール

`mazegen` はPythonパッケージとしてビルドし、別のPython環境に
インストールして利用できます。

#### 1. パッケージのビルド

リポジトリのルートディレクトリで以下を実行します。

```bash
python3 -m build
```

Makefileを使用する場合は以下でもビルドできます。

```bash
make build
```

ビルドに成功すると、`dist/` に以下のような配布ファイルが生成されます。

```text
dist/
├── mazegen-1.0.0-py3-none-any.whl
└── mazegen-1.0.0.tar.gz
```

#### 2. パッケージのインストール

wheelを使用する場合：

```bash
python3 -m pip install dist/mazegen-1.0.0-py3-none-any.whl
```

別のディレクトリやプロジェクトからインストールする場合は、
wheelファイルへのパスを指定します。

```bash
python3 -m pip install /path/to/mazegen-1.0.0-py3-none-any.whl
```

`.tar.gz` を使用する場合も同様にインストールできます。

```bash
python3 -m pip install /path/to/mazegen-1.0.0.tar.gz
```

インストール後は、A-Maze-ingのディレクトリ外からでも
`mazegen` をimportして使用できます。

---

### 基本的な使用例

まず `MazeGenerator` のインスタンスを作成します。

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
)
```

次に `generate()` を使用して迷路を生成します。

```python
maze = generator.generate(
    seed=42,
    perfect=True,
    start=(0, 0),
    blocked=set(),
)
```

`generate()` の戻り値として、生成された迷路構造を取得できます。

---

### カスタムパラメータの指定

迷路のサイズは `MazeGenerator` のインスタンスを作成するときに指定します。

```python
generator = MazeGenerator(
    width=30,
    height=20,
)
```

迷路を生成するときには、`generate()` にseedやPerfect Mazeの設定などを
指定できます。

```python
maze = generator.generate(
    seed=123,
    perfect=False,
    start=(0, 0),
    blocked=set(),
)
```

主なパラメータは以下の通りです。

| パラメータ | 説明 |
| --- | --- |
| `width` | 迷路の横幅 |
| `height` | 迷路の高さ |
| `seed` | 迷路生成に使用する乱数seed |
| `perfect` | `True` ならPerfect Maze、`False` ならループを持つ迷路を生成 |
| `start` | 迷路生成を開始するセルの座標 |
| `blocked` | 迷路生成時に使用しないセルの集合 |

同じseedと同じ条件を指定することで、同じ迷路を再現できます。

---

### 生成された迷路構造へのアクセス

生成された迷路は `generate()` の戻り値として取得できます。

```python
maze = generator.generate(
    seed=42,
    perfect=True,
    start=(0, 0),
    blocked=set(),
)
```

この `maze` が生成された迷路構造です。

迷路生成部分は出力ファイルの形式から独立しているため、
取得した `maze` を別のゲーム、可視化プログラム、経路探索などで
利用することもできます。

---

### 解へのアクセス

`get_shortest_path()` を使用すると、生成された迷路のENTRYからEXITまでの
最短経路を取得できます。

```python
from mazegen import get_shortest_path

solution = get_shortest_path(
    maze,
    (0, 0),
    (19, 14),
)

print(solution)
```

第2引数にENTRY、第3引数にEXITの座標を指定します。

取得したsolutionは、以下の文字を使用した文字列として表現されます。

```text
N = North
E = East
S = South
W = West
```

例えば、

```text
EESSWN
```

のような形式で経路を取得できます。

---

### 16進数表現への変換

必要に応じて、`to_hex()` を使用して迷路構造を課題指定の
16進数形式へ変換できます。

```python
from mazegen import to_hex

hex_text = to_hex(maze)

print(hex_text)
```

`MazeGenerator` が内部で扱う迷路構造と、
出力ファイルで使用する16進数形式は分離されています。

そのため、内部の迷路構造をそのまま別のプログラムで利用することも、
`to_hex()` を使用して出力形式へ変換することもできます。

---

### 完全な使用例

以下は、迷路の生成から最短経路の取得、16進数への変換までを行う例です。

```python
from mazegen import MazeGenerator, get_shortest_path, to_hex


generator = MazeGenerator(
    width=20,
    height=15,
)

maze = generator.generate(
    seed=42,
    perfect=True,
    start=(0, 0),
    blocked=set(),
)

solution = get_shortest_path(
    maze,
    (0, 0),
    (19, 14),
)

hex_text = to_hex(maze)

print(hex_text)
print(f"Solution: {solution}")
```

このように `mazegen` を利用することで、A-Maze-ing本体とは独立して、
迷路生成、迷路構造へのアクセス、最短経路探索、16進数への変換を
別のPythonプロジェクトから利用できます。

---


## ライセンス

本プロジェクトの再利用可能な `mazegen` パッケージは、
MIT Licenseの下で公開しています。

このライセンスにより、著作権表示およびライセンス表示を保持することを
条件として、コードの使用、複製、変更、再配布、商用利用が認められます。

このライセンスを選択した理由は、`MazeGenerator` を本プロジェクトだけでなく、
将来のPythonプロジェクトでも容易に再利用できるようにするためです。

