---
name: pypi-chinese_to_english_punctuation
description: Converts Chinese full-width punctuation into English half-width punctuation and fixes the spacing between Chinese characters and adjacent English words or numbers, while preserving leading indentation so Markdown and reStructuredText code blocks stay intact. The single public function is process, which takes text and returns text. A command line tool named c2ep exposes the same behavior, with a text subcommand that reads from stdin or an argument and writes to stdout, and a file subcommand that rewrites a UTF-8 file in place. Use this when normalizing punctuation in mixed Chinese and English documents. Generated for chinese_to_english_punctuation version 0.1.1. Higher installed versions should generally be compatible, lower versions may still work but correctness is not guaranteed.
---

# chinese_to_english_punctuation

Normalizes the punctuation of documents whose narrative is Chinese but whose technical terms stay in English. Converts full-width marks (`，。：；？！（）“”、`) to their ASCII equivalents, inserts the single space that belongs between a Chinese character and an adjacent Latin word or number, and preserves leading indentation so code blocks and nested list continuations survive untouched.

## Import

```python
from chinese_to_english_punctuation.api import process
import chinese_to_english_punctuation.api as chinese_to_english_punctuation
```

## Public API

- `process` — Convert the Chinese full-width punctuation in a block of text to English half-width punctuation and fix the surrounding spacing.

## CLI

The command is typically `.venv/bin/c2ep`. Run `c2ep -h`, or `c2ep text -h` / `c2ep file -h`, for help. Full args live in `ref/cli.md`.

## More detail

For signatures and key examples see `ref/public-api.md`. For full CLI args see `ref/cli.md`.
