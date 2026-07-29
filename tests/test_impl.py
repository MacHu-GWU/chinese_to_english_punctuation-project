# -*- coding: utf-8 -*-

from chinese_to_english_punctuation.impl import process

# Test cases as list of tuples (input, expected_output)
TEST_CASES = [
    # --- handle_dou_hao
    (
        "你好，世界",
        "你好, 世界",
    ),
    (
        "第一，第二，第三",
        "第一, 第二, 第三",
    ),
    (
        "末尾逗号，下一句",
        "末尾逗号, 下一句",
    ),
    # --- handle_dun_hao
    (
        "苹果、香蕉、橙子",
        "苹果, 香蕉, 橙子",
    ),
    (
        "一、二、三",
        "一, 二, 三",
    ),
    (
        "末尾顿号、下一句",
        "末尾顿号, 下一句",
    ),
    # --- handle_ju_hao
    (
        "这是一句话。下一句",
        "这是一句话. 下一句",
    ),
    (
        "第一句。第二句。下一句",
        "第一句. 第二句. 下一句",
    ),
    (
        "多个句号。。。下一句",
        "多个句号... 下一句",
    ),
    # --- handle_mao_hao
    (
        "标题：内容",
        "标题: 内容",
    ),
    (
        "时间：下午三点",
        "时间: 下午三点",
    ),
    (
        "末尾冒号：下一句",
        "末尾冒号: 下一句",
    ),
    # --- handle_fen_hao
    (
        "第一部分；第二部分",
        "第一部分; 第二部分",
    ),
    (
        "A组；B组；C组",
        "A 组; B 组; C 组",
    ),
    (
        "末尾分号；下一句",
        "末尾分号; 下一句",
    ),
    # --- handle_wen_hao
    (
        "你好吗？下一句",
        "你好吗? 下一句",
    ),
    (
        "什么？为什么？下一句",
        "什么? 为什么? 下一句",
    ),
    (
        "连续问号？？？下一句",
        "连续问号??? 下一句",
    ),
    # --- handle_exclamation
    (
        "太好了！下一句",
        "太好了! 下一句",
    ),
    (
        "哇！真的！下一句",
        "哇! 真的! 下一句",
    ),
    (
        "连续感叹！！！下一句",
        "连续感叹!!! 下一句",
    ),
    # --- handle_zuo_kuo_hao
    (
        "这是（括号内容）",
        "这是 (括号内容)",
    ),
    ("（开头括号）内容", "(开头括号) 内容"),
    ("多个（第一个）和（第二个）", "多个 (第一个) 和 (第二个)"),
    # --- handle_you_kuo_hao
    ("（内容）结束", "(内容) 结束"),
    ("（内容），后面是逗号", "(内容), 后面是逗号"),
    ("（内容）。后面是句号", "(内容). 后面是句号"),
    ("（内容）", "(内容)"),
    ("（a）（b）", "(a) (b)"),
    ("末尾括号（）下一句", "末尾括号 () 下一句"),
    # --- 方括号 【】 -> []
    ("这是【方括号内容】", "这是 [方括号内容]"),
    ("【开头方括号】内容", "[开头方括号] 内容"),
    ("【内容】，后面是逗号", "[内容], 后面是逗号"),
    ("【内容】。后面是句号", "[内容]. 后面是句号"),
    ("【内容】", "[内容]"),
    ("【a】【b】", "[a] [b]"),
    ("参考【Python文档】的说明", "参考 [Python 文档] 的说明"),
    # --- 书名号 《》 -> <>
    ("请阅读《Python教程》", "请阅读 <Python 教程>"),
    ("《书名》是一本好书", "<书名> 是一本好书"),
    ("《书名》。", "<书名>."),
    ("《中文》", "<中文>"),
    ("《》", "<>"),
    # --- 全角方括号 ［］ -> []
    ("这是［全角方括号］", "这是 [全角方括号]"),
    ("［开头］内容", "[开头] 内容"),
    ("参考［1］，见下文", "参考 [1], 见下文"),
    ("［a］［b］", "[a] [b]"),
    # --- 单书名号 〈〉 -> <>
    ("这是〈单书名号〉", "这是 <单书名号>"),
    ("〈开头〉内容", "<开头> 内容"),
    ("〈内容〉。", "<内容>."),
    # --- 全角尖括号 ＜＞ -> <>
    ("这是＜全角尖括号＞", "这是 <全角尖括号>"),
    ("＜开头＞内容", "<开头> 内容"),
    # --- 全角花括号 ｛｝ -> {}
    ("参数｛a｝", "参数 {a}"),
    ("｛开头花括号｝内容", "{开头花括号} 内容"),
    ("｛内容｝，后面是逗号", "{内容}, 后面是逗号"),
    # --- 嵌套 / 相邻的成对标点, 中间不应该插空格
    ("【《书名》】", "[<书名>]"),
    ("【（a）】", "[(a)]"),
    ("（（a））", "((a))"),
    ("《（a）》", "<(a)>"),
    ("《〈嵌套〉》", "<<嵌套>>"),
    ("［【a】］", "[[a]]"),
    ("＜〈a〉＞", "<<a>>"),
    # --- handle_zuo_shuang_yin_hao
    (
        '他说 "你好"',
        '他说 "你好"',
    ),
    (
        '"引用内容"',
        '"引用内容"',
    ),
    (
        '多个 "第一个" 和 "第二个" ',
        '多个 "第一个" 和 "第二个"',
    ),
    # --- handle_you_shuang_yin_hao
    (
        '"内容" 结束',
        '"内容" 结束',
    ),
    (
        '"内容"，后面是逗号',
        '"内容", 后面是逗号',
    ),
    (
        '"内容"。后面是句号',
        '"内容". 后面是句号',
    ),
    (
        '"末尾引号" 下一句',
        '"末尾引号" 下一句',
    ),
    # --- 全角引号 “ ” (不能在行首/行尾丢失)
    ("“开头引号”内容", '"开头引号" 内容'),
    ("“引用内容”", '"引用内容"'),
    ("“内容”结束", '"内容" 结束'),
    ("“内容”，后面是逗号", '"内容", 后面是逗号'),
    ("他说：“你好”。", '他说: "你好".'),
    ("“a”“b”", '"a" "b"'),
    # --- handle_space_between_chinese_and_english
    ("中文Eng中文", "中文 Eng 中文"),
    (
        "这是Python代码，它使用Flask框架。",
        "这是 Python 代码, 它使用 Flask 框架.",
    ),
    ("中文Hello World中文", "中文 Hello World 中文"),
    ("Python是一种编程语言", "Python 是一种编程语言"),
    ("价格是100元", "价格是 100 元"),
    ("Python3是最新版本", "Python3 是最新版本"),
    ("使用Python3和Flask2框架", "使用 Python3 和 Flask2 框架"),
    ("版本3.11已发布", "版本 3.11 已发布"),
    # --- complex cases combining multiple handlers
    (
        '"Python"是一种编程语言，它很流行。下一句',
        '"Python" 是一种编程语言, 它很流行. 下一句',
    ),
    (
        "这是第一个、第二个、第三个（注意括号）！下一句",
        "这是第一个, 第二个, 第三个 (注意括号)! 下一句",
    ),
    ("价格：100元；数量：5个。下一句", "价格: 100 元; 数量: 5 个. 下一句"),
    ("**参考资料：**", "**参考资料:**"),
    (
        '从"A"到"B"只需1天。',
        '从 "A" 到 "B" 只需 1 天.',
    ),
    (
        "注意：**这很着急，也很重要。**",
        "注意: **这很着急, 也很重要.**",
    ),
    (
        "**模型（Model）**：选择一个",
        "**模型 (Model)**: 选择一个",
    ),
    # --- 缩进保留 (indentation preservation)
    (
        "    缩进的一行，不能被吞掉。",
        "    缩进的一行, 不能被吞掉.",
    ),
    (
        "\t制表符缩进，也不能被吞掉。",
        "\t制表符缩进, 也不能被吞掉.",
    ),
    # markdown code block, 缩进有语义, 必须原样保留
    (
        "\n".join(
            [
                "```python",
                "def add_two(a, b):",
                '    """',
                "    一些中文的标点符号，比如逗号。",
                "",
                "    :param a: 第一个数",
                '    """',
                "    return a + b",
                "```",
            ]
        ),
        "\n".join(
            [
                "```python",
                "def add_two(a, b):",
                '    """',
                "    一些中文的标点符号, 比如逗号.",
                "",
                "    :param a: 第一个数",
                '    """',
                "    return a + b",
                "```",
            ]
        ),
    ),
    # reStructuredText code block, 缩进有语义, 必须原样保留
    (
        "\n".join(
            [
                ".. code-block:: python",
                "",
                "    def add_two(a, b):",
                "        # 一些中文的标点符号，比如逗号。",
                "        return a + b",
            ]
        ),
        "\n".join(
            [
                ".. code-block:: python",
                "",
                "    def add_two(a, b):",
                "        # 一些中文的标点符号, 比如逗号.",
                "        return a + b",
            ]
        ),
    ),
    # 纯空白行 -> 空行
    (
        "第一行\n    \n第二行",
        "第一行\n\n第二行",
    ),
]


def test_process():
    """Test all punctuation and spacing conversions"""
    for i, (text_in, expected) in enumerate(TEST_CASES):
        text_out = process(text_in)
        assert text_out == expected, (
            f"Test case {i + 1} failed\n"
            f"Input:    {text_in!r}\n"
            f"Output:   {text_out!r}\n"
            f"Expected: {expected!r}"
        )


def test_process_is_idempotent():
    """Running process() on already-converted text must be a no-op."""
    for i, (text_in, expected) in enumerate(TEST_CASES):
        once = process(text_in)
        twice = process(once)
        assert twice == once, (
            f"Test case {i + 1} is not idempotent\n"
            f"Input:  {text_in!r}\n"
            f"Once:   {once!r}\n"
            f"Twice:  {twice!r}"
        )


if __name__ == "__main__":
    from chinese_to_english_punctuation.tests import run_cov_test

    run_cov_test(
        __file__,
        "chinese_to_english_punctuation.impl",
        preview=False,
    )
