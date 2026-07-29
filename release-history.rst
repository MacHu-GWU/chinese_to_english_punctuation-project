.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

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


0.1.1 (1970-01-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release
