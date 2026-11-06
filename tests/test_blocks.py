# -*- coding: utf-8 -*-

from chinese_to_english_punctuation.blocks import LineKind, classify_lines

T = LineKind.TEXT
C = LineKind.CODE
V = LineKind.VERBATIM


def _kinds(text: str) -> list[LineKind]:
    return classify_lines(text.split("\n"))


def test_markdown_fence():
    assert _kinds("前\n```python\nx，y\n```\n后") == [T, C, C, C, T]
    assert _kinds("~~~\nx\n~~~\n后") == [C, C, C, T]
    # 4 个反引号包住 3 个反引号, 内层的 ``` 不会提前结束代码块
    assert _kinds("````md\n```py\nx\n```\n````\n后") == [C, C, C, C, C, T]
    # ``` 和 ~~~ 不能互相闭合
    assert _kinds("```\n~~~\n```\n后") == [C, C, C, T]
    # 没有闭合的 fence 一直延续到文件末尾
    assert _kinds("```\nx\ny") == [C, C, C]
    # 列表里缩进的 fence
    assert _kinds("- 项\n\n  ```js\n  x\n  ```\n- 项") == [T, T, C, C, C, T]
    # 行内的 ``` 不是 fence
    assert _kinds("```a``` 后面") == [T]


def test_markdown_math_html_front_matter():
    assert _kinds("$$\n\\text{a，b}\n$$\n后") == [C, C, C, T]
    assert _kinds("<div>\n  <p>段落</p>\n</div>\n\n后") == [C, C, C, T, T]
    assert _kinds("<!-- 注释 -->\n\n后") == [C, T, T]
    # 已经转换过的书名号不是 HTML
    assert _kinds("<Python 教程> 是一本书") == [T]
    assert _kinds("---\ntitle: 标题\n---\n正文") == [C, C, C, T]
    # 不在第一行的 --- 是分隔线, 不是 front matter
    assert _kinds("正文\n---\n正文") == [T, T, T]


def test_rst_code_directive():
    text = "\n".join(
        [
            ".. code-block:: python",
            "   :caption: 标题",
            "",
            "   x = 1",
            "",
            "正文",
        ]
    )
    assert _kinds(text) == [T, C, C, C, T, T]
    # 非代码指令的正文仍然是普通文本
    assert _kinds(".. note::\n\n   提示\n\n正文") == [T, T, T, T, T]
    # 嵌套在 note 里的代码块
    text = ".. note::\n\n   提示\n\n   .. code-block::\n\n      x\n\n   提示"
    assert _kinds(text) == [T, T, T, T, T, C, C, T, T]


def test_rst_code_directive_in_list_table():
    text = "\n".join(
        [
            ".. list-table::",
            "",
            "   * - 名称",
            "     - .. code-block:: python",
            "",
            "          x = 1",
            "   * - 下一行",
        ]
    )
    assert _kinds(text) == [T, T, T, T, C, C, T]


def test_rst_literal_block():
    assert _kinds("示例::\n\n    x = 1\n\n正文") == [T, C, C, T, T]
    # :: 后面不是缩进的内容, 就不是 literal block
    assert _kinds("示例::\n\n正文") == [T, T, T]
    # .. 开头的指令以 :: 结尾, 但不是 literal block
    assert _kinds(".. note::\n\n   提示") == [T, T, T]


def test_rst_tables():
    grid = "+----+----+\n| a  | b  |\n+====+====+\n| c  | d  |\n+----+----+\n\n后"
    assert _kinds(grid) == [V, V, V, V, V, T, T]
    simple = "===  ===\na    b\n===  ===\nc    d\n===  ===\n\n后"
    assert _kinds(simple) == [V, V, V, V, V, T, T]
    # 只有一列的 ==== 是标题下划线, 不是表格
    assert _kinds("标题\n====\n\n正文") == [T, T, T, T]


if __name__ == "__main__":
    from chinese_to_english_punctuation.tests import run_cov_test

    run_cov_test(
        __file__,
        "chinese_to_english_punctuation.blocks",
        preview=False,
    )
