.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.3 (2026-11-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Code-like blocks are now recognized and converted in a format-preserving
  mode: only the marks are swapped (plus one space after a comma, period and
  the like when it runs straight into text), and whitespace, alignment and
  syntax are otherwise left alone. This covers Markdown fenced code (fence length aware, so a
  four-backtick fence can wrap a three-backtick one, and fences indented inside
  list items), Mermaid diagrams, ``$$`` math, HTML blocks, YAML front matter,
  reStructuredText code-like directives such as ``code-block``, ``math``,
  ``raw`` and ``mermaid`` (also when nested inside ``list-table`` cells or
  other directives), and ``::`` literal blocks.
- reStructuredText grid tables and simple tables are left exactly as they are,
  so their column alignment survives.
- Inline code spans (single or double backticks) are converted in the same
  format-preserving mode and spaced like an English word. reStructuredText
  roles such as ``:func:`` and link references ending in ``_`` stay attached.
- New ``skip_code`` option, ``process(text, skip_code=True)`` and
  ``c2ep text|file --skip_code``, leaves code blocks and inline code completely
  untouched.

**Bugfixes**

- Mermaid diagrams no longer get broken by stray spaces: ``B{配置存在？}`` was
  converted to ``B{配置存在? }``, ``|是|`` to ``| 是|`` and ``E>结束。]`` to
  ``E> 结束. ]``.
- Runs of spaces inside code blocks (aligned assignments and comments) are no
  longer collapsed into one.
- ``**`` inside an inline code span is no longer paired with a ``**`` outside
  it, which used to delete spaces in the wrong places.
- Markdown link targets ``[text](url)`` and bare URLs are left untouched. A URL
  containing an emoji, such as a shields.io badge, no longer gets a space
  inserted into it.


0.1.2 (2026-07-29)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add six more paired marks to the conversion table: ``【】`` and ``［］`` to
  ``[]``, ``《》`` and ``〈〉`` and ``＜＞`` to ``<>``, and the full-width curly
  braces ``｛｝`` to ``{}``.
- Nested and adjacent paired marks no longer get a stray space inserted between
  them, so ``【《书名》】`` now converts to ``[<书名>]``.

**Minor Improvements**

- The bracket and quote handlers are now driven by a single ``BRACKET_PAIRS``
  table instead of one hand-written function per mark. Adding a new pair is one
  line. These are internal helpers; the public API is unchanged.

**Bugfixes**

- Two consecutive closing marks (``（（a））``) no longer produce a stray space
  before the last one. Was ``((a) )``, now ``((a))``.
- ``<`` is now treated as an opening mark by the Chinese/English spacing pass,
  so ``《中文》`` converts to ``<中文>`` rather than ``< 中文>``.
- ``c2ep file`` no longer reports ``0 line(s) changed`` for a file it did in
  fact rewrite. The line counter runs on ``splitlines()`` output and cannot see
  line terminators, so a CRLF file whose text is already correct counted zero
  changed lines. That case now reports ``line endings normalized``.


0.1.1 (1970-01-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release
