# Public API reference

## `process`

```python
def process(text: str) -> str
```

Converts every line of `text` and returns the result. Accepts single-line or multi-line input; there is no state carried between calls.

Semantics worth knowing before you use it:

- **Line-oriented.** Implemented as `splitlines()` + `"\n".join()`. Two consequences the caller must handle: a **trailing newline is dropped**, and **CRLF is normalized to LF**. If you are rewriting a file, re-attach the trailing newline yourself, or use the `c2ep file` CLI, which already does.
- **Indentation is preserved verbatim.** Leading whitespace is split off before conversion and re-attached after, so fenced code blocks, `.. code-block` directives, and nested list continuations are not damaged.
- **Whitespace-only lines collapse to empty lines.** Trailing whitespace on a line is not preserved.
- **Idempotent.** Running it on already-converted text is a no-op, which makes it safe in a `--check`-style loop.
- **Not Markdown-aware.** It does not parse fences; content *inside* a code block is converted like any other line. Indentation survives, but a full-width comma in a Python string literal will still become an ASCII comma.

What it converts:

| Chinese | English | Notes |
|---|---|---|
| `，` `、` | `, ` | space after |
| `。` | `. ` | space after |
| `：` `；` | `: ` `; ` | space after |
| `？` `！` | `? ` `! ` | space after |
| `（）` | `()` | space *before* the opener, *after* the closer |
| `【】` `［］` | `[]` | same spacing rule |
| `《》` `〈〉` `＜＞` | `<>` | same spacing rule |
| `｛｝` | `{}` | full-width braces only |
| `“”` | `"` | same spacing rule |

Runs of two or three identical `。？！` are treated as a unit (`。。。` → `...`). Spaces are inserted between Chinese characters and adjacent Latin letters or digits, but not before closing punctuation or after opening brackets/quotes. Nested or adjacent paired marks do not get a space wedged between them (`【《书名》】` → `[<书名>]`). Spaces just inside paired Markdown `**bold**` markers are cleaned up last.

**Not** converted: single quotes `‘’` pass through unchanged, because `’` doubles as an apostrophe and telling the two apart needs context.

Note that `＜` `＞` are always treated as a bracket pair, never as full-width comparison operators — `a＜b` becomes `a <b`.

The paired marks are driven by the `BRACKET_PAIRS` table in `chinese_to_english_punctuation/impl.py`. That module and everything in it is **not** public — read the file if you need to know exactly how a given mark is treated.

## Key scenarios

Convert a chunk of text:

```python
from chinese_to_english_punctuation.api import process

process("这是Python代码，它使用Flask框架。")
# '这是 Python 代码, 它使用 Flask 框架.'

process("价格：100元；数量：5个。下一句")
# '价格: 100 元; 数量: 5 个. 下一句'
```

Convert a file safely, restoring the trailing newline that `process` drops:

```python
from pathlib import Path
from chinese_to_english_punctuation.api import process

path = Path("./README.md")
old = path.read_bytes().decode("utf-8")   # raises UnicodeDecodeError if not UTF-8
new = process(old)
if old.endswith("\n") and not new.endswith("\n"):
    new += "\n"
if new != old:
    path.write_bytes(new.encode("utf-8"))
```

Use it as a check in CI — exit non-zero when a document is not normalized:

```python
import sys
from pathlib import Path
from chinese_to_english_punctuation.api import process

bad = [p for p in Path("docs").rglob("*.md")
       if process(p.read_text(encoding="utf-8")).rstrip("\n")
       != p.read_text(encoding="utf-8").rstrip("\n")]
sys.exit(1 if bad else 0)
```
