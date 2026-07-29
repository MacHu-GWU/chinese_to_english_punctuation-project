# -*- coding: utf-8 -*-

from chinese_to_english_punctuation import api


def test():
    _ = api
    _ = api.process


if __name__ == "__main__":
    from chinese_to_english_punctuation.tests import run_cov_test

    run_cov_test(
        __file__,
        "chinese_to_english_punctuation.api",
        preview=False,
    )
