.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Recognize code-like blocks and convert them in a format-preserving mode that
  only swaps the marks and never touches whitespace: Markdown fenced code
  (fence length aware, so a four-backtick fence can wrap a three-backtick one), Mermaid
  diagrams, ``$$`` math, HTML blocks, YAML front matter, reStructuredText
  code-like directives (also inside ``list-table`` cells) and ``::`` literal
  blocks. Mermaid nodes such as ``B{配置存在？}`` and edges such as ``|是|`` no
  longer get stray spaces inserted.
- reStructuredText grid tables and simple tables are left exactly as they are,
  so their column alignment survives.
- Inline code spans (single or double backticks) are converted in the
  same format-preserving mode and spaced like an English word, and ``**``
  inside a code span is no longer paired with a ``**`` outside it. Markdown
  link targets ``[text](url)`` and bare URLs are left untouched.

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


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
