
.. .. image:: https://readthedocs.org/projects/chinese-to-english-punctuation/badge/?version=latest
    :target: https://chinese-to-english-punctuation.readthedocs.io/en/latest/
    :alt: Documentation Status

.. .. image:: https://github.com/MacHu-GWU/chinese_to_english_punctuation-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/chinese_to_english_punctuation-project/actions?query=workflow:CI

.. .. image:: https://codecov.io/gh/MacHu-GWU/chinese_to_english_punctuation-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/chinese_to_english_punctuation-project

.. image:: https://img.shields.io/pypi/v/chinese-to-english-punctuation.svg
    :target: https://pypi.python.org/pypi/chinese-to-english-punctuation

.. image:: https://img.shields.io/pypi/l/chinese-to-english-punctuation.svg
    :target: https://pypi.python.org/pypi/chinese-to-english-punctuation

.. image:: https://img.shields.io/pypi/pyversions/chinese-to-english-punctuation.svg
    :target: https://pypi.python.org/pypi/chinese-to-english-punctuation

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/chinese_to_english_punctuation-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/chinese_to_english_punctuation-project

------

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://chinese-to-english-punctuation.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/chinese_to_english_punctuation-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/chinese_to_english_punctuation-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/chinese_to_english_punctuation-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/chinese-to-english-punctuation#files


Welcome to ``chinese_to_english_punctuation`` Documentation
==============================================================================
.. .. image:: https://chinese-to-english-punctuation.readthedocs.io/en/latest/_static/chinese_to_english_punctuation-logo.png
    :target: https://chinese-to-english-punctuation.readthedocs.io/en/latest/

``chinese_to_english_punctuation`` rewrites Chinese full-width punctuation into
its English half-width equivalent, and fixes the spacing around it. Documents
written by Chinese speakers about technical topics almost always end up mixing
the two: the narrative uses ，。：；？！（）“” while the technical terms stay in
English. That mix reads poorly in Markdown and reStructuredText, and it breaks
tooling that expects ASCII punctuation. This library converts ``，`` to ``,``,
``。`` to ``.``, ``（）`` to ``()`` and so on, inserts the single space that
belongs between a Chinese character and an adjacent Latin word or number, and
leaves everything else alone.

The conversion is line-oriented and deliberately conservative about structure.
Leading indentation is preserved verbatim, so fenced code blocks, ``.. code-block``
directives and nested list continuations survive untouched. Runs of two or three
identical marks (``。。。``, ``？？？``, ``！！！``) are treated as a single unit
rather than being split apart. Spaces that would otherwise be introduced just
inside paired Markdown markers such as ``**bold**`` are cleaned up afterwards.

The public Python API is a single function, ``process``, which takes text and
returns text. The same behavior is available from the command line through
``c2ep``, which offers ``c2ep text`` for reading from ``--text`` or stdin and
writing to stdout, and ``c2ep file`` for rewriting a UTF-8 file in place. Files
that are not valid UTF-8 are rejected rather than guessed at, and ``--dry_run``
reports what would change without touching anything.

Usage:

.. code-block:: python

    from chinese_to_english_punctuation.api import process

    process("这是Python代码，它使用Flask框架。")
    # '这是 Python 代码, 它使用 Flask 框架.'

.. code-block:: console

    $ c2ep text --text "这是Python代码，它使用Flask框架。"
    这是 Python 代码, 它使用 Flask 框架.

    $ c2ep file --path ./README.md --dry_run
    ./README.md: 12 line(s) would change (dry run, nothing written)

    $ c2ep file --path ./README.md
    ./README.md: 12 line(s) changed


.. _install:

Install
------------------------------------------------------------------------------

``chinese_to_english_punctuation`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install chinese-to-english-punctuation

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade chinese-to-english-punctuation
