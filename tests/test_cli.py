# -*- coding: utf-8 -*-

import io
import sys

import pytest

from chinese_to_english_punctuation.cli import main


class TestText:
    def test_with_text_arg(self, capsys):
        assert main(["text", "--text", "你好，世界"]) == 0
        assert capsys.readouterr().out == "你好, 世界\n"

    def test_read_from_stdin(self, capsys, monkeypatch):
        monkeypatch.setattr(sys, "stdin", io.StringIO("这是Python代码，很流行。\n"))
        assert main(["text"]) == 0
        assert capsys.readouterr().out == "这是 Python 代码, 很流行.\n"

    def test_multi_line(self, capsys):
        assert main(["text", "--text", "第一行，\n第二行。"]) == 0
        assert capsys.readouterr().out == "第一行,\n第二行.\n"


class TestFile:
    def test_rewrite_in_place(self, tmp_path, capsys):
        p = tmp_path / "a.md"
        p.write_text("你好，世界。\n价格是100元\n", encoding="utf-8")
        assert main(["file", "--path", str(p)]) == 0
        assert p.read_text(encoding="utf-8") == "你好, 世界.\n价格是 100 元\n"
        assert "2 line(s) changed" in capsys.readouterr().out

    def test_trailing_newline_preserved(self, tmp_path):
        p = tmp_path / "a.md"
        p.write_text("你好，世界。\n", encoding="utf-8")
        assert main(["file", "--path", str(p)]) == 0
        assert p.read_text(encoding="utf-8").endswith("\n")

    def test_no_trailing_newline_not_added(self, tmp_path):
        p = tmp_path / "a.md"
        p.write_text("你好，世界。", encoding="utf-8")
        assert main(["file", "--path", str(p)]) == 0
        assert p.read_text(encoding="utf-8") == "你好, 世界."

    def test_bom_preserved(self, tmp_path):
        p = tmp_path / "a.md"
        p.write_bytes("﻿你好，世界。\n".encode("utf-8"))
        assert main(["file", "--path", str(p)]) == 0
        assert p.read_bytes() == "﻿你好, 世界.\n".encode("utf-8")

    def test_no_change_is_not_rewritten(self, tmp_path, capsys):
        p = tmp_path / "a.md"
        p.write_text("hello, world.\n", encoding="utf-8")
        mtime_before = p.stat().st_mtime_ns
        assert main(["file", "--path", str(p)]) == 0
        assert "no change" in capsys.readouterr().out
        assert p.stat().st_mtime_ns == mtime_before

    def test_dry_run_does_not_write(self, tmp_path, capsys):
        p = tmp_path / "a.md"
        p.write_text("你好，世界。\n", encoding="utf-8")
        assert main(["file", "--path", str(p), "--dry_run"]) == 0
        assert p.read_text(encoding="utf-8") == "你好，世界。\n"
        assert "would change" in capsys.readouterr().out

    def test_not_found(self, tmp_path, capsys):
        p = tmp_path / "does-not-exist.md"
        assert main(["file", "--path", str(p)]) == 1
        assert "not found" in capsys.readouterr().err

    def test_not_a_file(self, tmp_path, capsys):
        assert main(["file", "--path", str(tmp_path)]) == 1
        assert "is not a file" in capsys.readouterr().err

    def test_not_utf8(self, tmp_path, capsys):
        p = tmp_path / "a.md"
        p.write_bytes("你好，世界。".encode("gbk"))
        assert main(["file", "--path", str(p)]) == 1
        assert "not valid UTF-8" in capsys.readouterr().err

    def test_crlf_normalized_to_lf(self, tmp_path):
        p = tmp_path / "a.md"
        p.write_bytes("你好，世界。\r\n第二行。\r\n".encode("utf-8"))
        assert main(["file", "--path", str(p)]) == 0
        assert p.read_bytes() == "你好, 世界.\n第二行.\n".encode("utf-8")


class TestUsageErrors:
    def test_no_subcommand(self):
        with pytest.raises(SystemExit) as e:
            main([])
        assert e.value.code == 2

    def test_file_without_path(self):
        with pytest.raises(SystemExit) as e:
            main(["file"])
        assert e.value.code == 2


if __name__ == "__main__":
    from chinese_to_english_punctuation.tests import run_cov_test

    run_cov_test(
        __file__,
        "chinese_to_english_punctuation.cli",
        preview=False,
    )
