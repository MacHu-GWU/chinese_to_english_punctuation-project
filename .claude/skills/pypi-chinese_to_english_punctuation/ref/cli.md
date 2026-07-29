# CLI reference — `c2ep`

Entry point: `c2ep = "chinese_to_english_punctuation.cli:main"`. In a project venv the executable is `.venv/bin/c2ep`; without installing, `python -m chinese_to_english_punctuation.cli` is equivalent.

```
c2ep [-h] {text,file} ...
```

A subcommand is **required**. Exit codes: `0` success, `1` runtime failure, `2` usage error (argparse).

The two subcommands are deliberately separate because one is read-only and the other overwrites files on disk.

---

## `c2ep text`

Convert text and print the result to stdout. Read-only — never touches the filesystem.

```
c2ep text [-h] [--text TEXT]
```

| Flag | Type | Default | Description |
|---|---|---|---|
| `--text` | str | `None` | The text to convert. When omitted, the input is read from **stdin**, so the command works as a pipe filter. |

Output always ends with a single newline (it is written with `print`). Multi-line input is fine.

```console
$ c2ep text --text "这是Python代码，它使用Flask框架。"
这是 Python 代码, 它使用 Flask 框架.

$ cat README.md | c2ep text > README.normalized.md
```

---

## `c2ep file`

Convert a UTF-8 encoded text file **in place**.

```
c2ep file [-h] --path PATH [--dry_run]
```

| Flag | Type | Default | Description |
|---|---|---|---|
| `--path` | Path | *required* | Path to the file to convert in place. |
| `--dry_run` | flag | `False` | Report how many lines would change, without writing anything. |

Behavior:

- The file is read as bytes and strictly decoded as UTF-8. Anything else — GBK, GB18030, Big5, binary — is **rejected** with an error on stderr and exit code `1`, rather than guessed at.
- A leading byte order mark is split off before conversion and re-attached after, so the file's encoding form is unchanged.
- A trailing newline is preserved if the original had one; none is added if it did not.
- Line endings are **normalized to LF** — a CRLF file is rewritten with LF.
- If the conversion produces identical content, the file is **not** rewritten at all (mtime is untouched) and the command prints `no change`.

Output on stdout is one line: `<path>: no change`, `<path>: N line(s) changed`, or `<path>: N line(s) would change (dry run, nothing written)`.

Error cases, all exit `1` with a message on stderr: path not found, path is not a file, path is not valid UTF-8.

```console
$ c2ep file --path ./README.md --dry_run
./README.md: 12 line(s) would change (dry run, nothing written)

$ c2ep file --path ./README.md
./README.md: 12 line(s) changed

$ c2ep file --path ./README.md
./README.md: no change
```

Batch a directory with the shell, since there is no recursive subcommand yet:

```console
$ find docs -name '*.md' -exec c2ep file --path {} \;
```
