# mazegen

迷路を生成する Python パッケージです。

生成ロジックのみを提供し、設定ファイルの読み込み、ターミナル表示、
コマンドライン処理からは独立しています。そのため他の Python
プロジェクトからも利用できます。

---

## インストール

```bash
python3 -m pip install mazegen-1.0.0-py3-none-any.whl
```

---

## 基本的な使い方

```python
from mazegen import MazeGenerator

generator = MazeGenerator(20, 15)
maze = generator.generate()
```

`MazeGenerator` は迷路のサイズだけを保持します。生成のたびに変わる
値（seed、開始位置など）は `generate()` に渡します。

---

## API

### `MazeGenerator(width, height)`

| 引数 | 型 | 説明 |
| --- | --- | --- |
| `width` | `int` | 迷路の横幅（セル数） |
| `height` | `int` | 迷路の高さ（セル数） |

### `generate(seed=None, perfect=True, start=(0, 0), blocked=None) -> Maze`

| 引数 | 型 | 既定値 | 説明 |
| --- | --- | --- | --- |
| `seed` | `int \| None` | `None` | 乱数の種。同じ値を渡すと同じ迷路が再現される |
| `perfect` | `bool` | `True` | `True` なら閉路のない迷路、`False` ならループを含む迷路 |
| `start` | `tuple[int, int]` | `(0, 0)` | 生成を開始するセル |
| `blocked` | `set[tuple[int, int]] \| None` | `None` | 通路として使わないセルの集合 |

`start` が `blocked` に含まれている場合は `ValueError` を送出します。

### `get_shortest_path(maze, start, goal) -> str`

`start` から `goal` までの最短経路を、`N` / `E` / `S` / `W` の文字列で返します。

```python
from mazegen import get_shortest_path

solution = get_shortest_path(maze, (0, 0), (19, 14))
print(solution)   # 例: "EESSWNEE..."
```

`goal` に到達できない場合は `ValueError` を送出します。

### `to_hex(maze) -> str`

迷路を 16 進表記の文字列に変換します。詳細は後述します。

---

## 生成された構造へのアクセス

`generate()` は `Maze` を返します。

```python
@dataclass
class Maze:
    width: int
    height: int
    edges: set[frozenset[tuple[int, int]]]
```

### `edges` の読み方

`edges` は **通路の集合** です。壁の集合ではありません。

隣り合う 2 つのセルの座標を含む `frozenset` が `edges` にあれば、
その 2 セルの間は通行できます。なければ、そこには壁があります。

```python
if frozenset({(3, 5), (4, 5)}) in maze.edges:
    ...  # (3,5) と (4,5) は行き来できる
```

`frozenset` を使っているため向きはありません。`(3,5)` から見た東の通路と、
`(4,5)` から見た西の通路は、同じ 1 つの要素で表されます。
そのため、隣接するセルの壁が食い違うことは構造的に起こりません。

### 通行可能な隣を調べる例

```python
def neighbors(maze, cell):
    x, y = cell
    around = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
    return [
        n for n in around
        if 0 <= n[0] < maze.width and 0 <= n[1] < maze.height
        and frozenset((cell, n)) in maze.edges
    ]
```

---

## `blocked` の使い方

`blocked` に渡したセルは、生成の開始前に訪問済みとして扱われます。
そのため通路が一切つながらず、四方すべてが壁のセルになります。

これを利用すると、迷路の中に任意の図形を埋め込めます。

```python
blocked = {(4, 7), (5, 7), (6, 7)}
maze = generator.generate(seed=42, blocked=blocked)
```

`blocked` のセルは孤立するため、他のセルから到達できません。
盤面を分断しないよう、周囲に通路が回り込める余白を残してください。

なお、`blocked` のセルは `get_shortest_path()` の始点・終点には使えません。

---

## 16 進表記への変換

`to_hex()` は、1 セルにつき 1 桁の 16 進数を返します。行の区切りは `\n` です。

各桁は、そのセルの 4 方向の壁の有無をビットで表します。
**壁が閉じているとビットが 1**、開いていると 0 です。

| ビット | 値 | 方向 |
| --- | --- | --- |
| 0 | 1 | 北 |
| 1 | 2 | 東 |
| 2 | 4 | 南 |
| 3 | 8 | 西 |

例えば `3`（2 進で `0011`）は北と東が閉じ、南と西が開いている状態です。
`f` は四方すべてが閉じたセルで、`blocked` に渡したセルがこれにあたります。

`Maze` が保持する `edges` と、この 16 進表記は独立しています。
`Maze` をそのまま別のプログラムで扱うことも、`to_hex()` で変換して
ファイルに書き出すこともできます。

---

## 全体の例

```python
from mazegen import MazeGenerator, get_shortest_path, to_hex

generator = MazeGenerator(20, 15)
maze = generator.generate(seed=42, perfect=False)

print(to_hex(maze))
print(get_shortest_path(maze, (0, 0), (19, 14)))
```

---

## ライセンス

MIT License. 詳細はリポジトリの `LICENSE.md` を参照してください。