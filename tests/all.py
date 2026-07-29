# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from chinese_to_english_punctuation.tests import run_cov_test

    run_cov_test(
        __file__,
        "chinese_to_english_punctuation",
        is_folder=True,
        preview=False,
    )
