# -*- coding: utf-8 -*-

"""
块级扫描: 逐行判断每一行属于「普通文本」、「代码类块」还是「原样保留」.

:func:`chinese_to_english_punctuation.impl.process` 是逐行处理的. 普通文本的
那套规则 (strip, 补空格, 压缩空格) 放到代码、Mermaid 图、HTML、表格里会把
格式搞乱, 所以先用这里的扫描器给每一行打上标签, 再按标签选择处理方式.

扫描器只识别常见的、合法的 Markdown / reStructuredText 结构, 不追求完整的
语法解析. 识别不了的东西一律当普通文本, 也就是保持旧行为.
"""

import enum
import re


class LineKind(enum.Enum):
    """
    一行文本的类别.

    - ``TEXT``: 普通文本, 走完整的转换规则.
    - ``CODE``: 代码类块 (代码, Mermaid, 数学公式, HTML, front matter 等).
      只做标点替换, 不动空白和格式.
    - ``VERBATIM``: 原样保留, 一个字符都不改. 用于依赖列宽对齐的表格.
    """

    TEXT = "text"
    CODE = "code"
    VERBATIM = "verbatim"


#: reStructuredText 中内容是代码 (或其他非正文) 的指令.
#: 这些指令的正文按 :attr:`LineKind.CODE` 处理.
RST_CODE_DIRECTIVES = {
    "code",
    "code-block",
    "sourcecode",
    "parsed-literal",
    "math",
    "raw",
    "mermaid",
    "graphviz",
    "graph",
    "digraph",
    "plantuml",
    "uml",
    "ipython",
    "jupyter-execute",
    "doctest",
    "testcode",
    "testoutput",
}

# Markdown fence 开头: 可选缩进 + 至少 3 个 ` 或 ~ + info string
_RE_FENCE_OPEN = re.compile(r"^\s*(?P<fence>`{3,}|~{3,})(?P<info>.*)$")

# reStructuredText 指令: 允许前面有列表标记 (用于 list-table 单元格里的指令),
# 例如 "   * - .. code-block:: python"
_RE_RST_DIRECTIVE = re.compile(
    r"^(?P<lead>\s*(?:(?:[-*+]|\d+\.|#\.)\s+)*)\.\.\s+(?P<name>[\w:.-]+?)::(?:\s|$)"
)

# reStructuredText 注释 / 指令 / 链接目标等以 ".. " 开头的显式标记
_RE_RST_EXPLICIT = re.compile(r"^\s*\.\.(?:\s|$)")

#: 会被识别为 Markdown HTML 块开头的标签名. 基于 CommonMark 的块级标签列表,
#: 再加上几个常单独成行的标签. 只认真实的标签名, 避免把 "<Python 教程> 是..."
#: 这种已经转换过的书名号误认成 HTML.
HTML_BLOCK_TAGS = {
    "address", "article", "aside", "audio", "base", "blockquote", "body",
    "br", "caption", "center", "col", "colgroup", "dd", "details", "dialog",
    "dir", "div", "dl", "dt", "fieldset", "figcaption", "figure", "footer",
    "form", "frame", "frameset", "h1", "h2", "h3", "h4", "h5", "h6", "head",
    "header", "hr", "html", "iframe", "img", "legend", "li", "link", "main",
    "menu", "menuitem", "nav", "noframes", "ol", "optgroup", "option", "p",
    "param", "picture", "pre", "script", "search", "section", "source",
    "span", "style", "summary", "svg", "table", "tbody", "td", "tfoot", "th",
    "thead", "title", "tr", "track", "ul", "video", "a", "b", "i", "sub",
    "sup", "kbd", "code", "em", "strong",
}  # fmt: skip

# Markdown HTML 块: 行首是一个 HTML 标签或注释
_RE_HTML_BLOCK = re.compile(
    r"^\s{0,3}<(?:!--|/?(?P<tag>[A-Za-z][A-Za-z0-9-]*)(?:[\s/>]|$))"
)

# reStructuredText grid table 的边框: +----+----+ 或 +====+====+
_RE_GRID_BORDER = re.compile(r"^\s*\+(?:[-=]+\+)+\s*$")

# reStructuredText simple table 的边框: 至少两列 "=====  ====="
_RE_SIMPLE_BORDER = re.compile(r"^\s*=+(?: +=+)+\s*$")


def _indent_width(line: str) -> int:
    """行首空白的宽度, tab 按 8 列展开."""
    expanded = line.expandtabs(8)
    return len(expanded) - len(expanded.lstrip())


def _is_blank(line: str) -> bool:
    return not line.strip()


def _scan_indented_body(lines: list[str], start: int, base: int) -> int:
    """
    从 ``start`` 开始, 找到缩进大于 ``base`` 的连续行 (中间可以有空行).

    :return: 块结束的位置 (不包含). 末尾的空行不算在块内.
    """
    end = start
    i = start
    while i < len(lines):
        line = lines[i]
        if _is_blank(line):
            i += 1
            continue
        if _indent_width(line) <= base:
            break
        i += 1
        end = i
    return end


def classify_lines(lines: list[str]) -> list[LineKind]:
    """
    给每一行打上 :class:`LineKind` 标签.

    识别的结构:

    - Markdown fenced code block (````` ``` ````` 和 ``~~~``), 按 fence 字符和长度
      配对, 所以 4 个反引号可以包住 3 个反引号的嵌套代码块.
    - Markdown ``$$`` 数学块, HTML 块, 文件开头的 YAML front matter.
    - reStructuredText 的代码类指令 (见 :data:`RST_CODE_DIRECTIVES`),
      包括写在列表 / list-table 单元格里的指令.
    - reStructuredText 以 ``::`` 结尾的段落引出的 literal block.
    - reStructuredText 的 grid table 和 simple table (原样保留).

    :param lines: 不含换行符的行列表

    :return: 与 ``lines`` 一一对应的标签列表
    """
    n = len(lines)
    kinds = [LineKind.TEXT] * n

    def mark(start: int, end: int, kind: LineKind):
        for j in range(start, end):
            kinds[j] = kind

    i = 0

    # YAML front matter: 只认文件第一行的 "---"
    if n and lines[0].strip() == "---":
        for j in range(1, n):
            if lines[j].strip() in ("---", "..."):
                mark(0, j + 1, LineKind.CODE)
                i = j + 1
                break

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # --- Markdown fenced code block
        m = _RE_FENCE_OPEN.match(line)
        if m and not (m.group("fence")[0] == "`" and "`" in m.group("info")):
            fence = m.group("fence")
            close = re.compile(
                r"^\s*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$"
            )
            j = i + 1
            while j < n and not close.match(lines[j]):
                j += 1
            # 没有闭合的 fence 一直延续到文件末尾, 与 CommonMark 一致
            end = min(j + 1, n)
            mark(i, end, LineKind.CODE)
            i = end
            continue

        # --- Markdown $$ 数学块
        if stripped == "$$":
            j = i + 1
            while j < n and lines[j].strip() != "$$":
                j += 1
            end = min(j + 1, n)
            mark(i, end, LineKind.CODE)
            i = end
            continue

        # --- reStructuredText 代码类指令
        m = _RE_RST_DIRECTIVE.match(line)
        if m:
            if m.group("name").lower() in RST_CODE_DIRECTIVES:
                base = len(m.group("lead").expandtabs(8))
                end = _scan_indented_body(lines, i + 1, base)
                # 指令行本身按普通文本处理 (例如 ":caption:" 所在的标题),
                # 只有正文是代码.
                mark(i + 1, end, LineKind.CODE)
                i = end
                continue
            i += 1
            continue

        # --- reStructuredText grid table
        if _RE_GRID_BORDER.match(line):
            j = i + 1
            while j < n and lines[j].lstrip()[:1] in ("+", "|"):
                j += 1
            mark(i, j, LineKind.VERBATIM)
            i = j
            continue

        # --- reStructuredText simple table
        # 底边框后面一定是空行或文件结尾; 中间的分隔线后面一定还有内容行.
        if _RE_SIMPLE_BORDER.match(line):
            j = i + 1
            while j < n:
                if _RE_SIMPLE_BORDER.match(lines[j]) and (
                    j + 1 >= n or _is_blank(lines[j + 1])
                ):
                    break
                j += 1
            end = min(j + 1, n)
            mark(i, end, LineKind.VERBATIM)
            i = end
            continue

        # --- Markdown HTML 块, 到空行为止
        m = _RE_HTML_BLOCK.match(line)
        if m and (m.group("tag") is None or m.group("tag").lower() in HTML_BLOCK_TAGS):
            j = i
            while j < n and not _is_blank(lines[j]):
                j += 1
            mark(i, j, LineKind.CODE)
            i = j
            continue

        # --- reStructuredText literal block: 以 "::" 结尾的段落
        if (
            stripped.endswith("::")
            and not _RE_RST_EXPLICIT.match(line)
            and i + 1 < n
            and _is_blank(lines[i + 1])
        ):
            base = _indent_width(line)
            end = _scan_indented_body(lines, i + 1, base)
            if end > i + 1:
                mark(i + 1, end, LineKind.CODE)
                i = end
                continue

        i += 1

    return kinds
