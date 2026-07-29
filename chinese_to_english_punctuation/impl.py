# -*- coding: utf-8 -*-

"""
把中文全角标点转换为英文半角标点, 并按中英混排的排版习惯补齐空格.
"""

import re
from dataclasses import dataclass

@dataclass
class PairMatch:
    """
    表示一对闭合标记的匹配信息

    :param marker: 标记符号，如 "**"、"()"、"[]" 等
    :param open_start: 开始标记的起始位置（索引）
    :param open_end: 开始标记的结束位置（索引，不包含）
    :param close_start: 结束标记的起始位置（索引）
    :param close_end: 结束标记的结束位置（索引，不包含）
    """

    marker: str
    open_start: int
    open_end: int
    close_start: int
    close_end: int


def find_pair_markers(line: str, marker: str) -> list[PairMatch]:
    """
    在字符串中查找成对的标记

    对于相同的开始和结束标记（如 **），会将找到的标记按顺序两两配对。
    例如：第1个和第2个配对，第3个和第4个配对，以此类推。

    :param line: 要搜索的字符串
    :param marker: 要匹配的标记，如 "**"

    :return: 匹配到的成对标记列表
    """
    matches = []
    positions = []

    # 找到所有标记的位置
    start = 0
    while True:
        pos = line.find(marker, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + len(marker)

    # 将位置两两配对（第1个和第2个，第3个和第4个，...）
    for i in range(0, len(positions) - 1, 2):
        open_pos = positions[i]
        close_pos = positions[i + 1]
        matches.append(
            PairMatch(
                marker=marker,
                open_start=open_pos,
                open_end=open_pos + len(marker),
                close_start=close_pos,
                close_end=close_pos + len(marker),
            )
        )

    return matches


def remove_spaces_around_paired_markers(line: str, matches: list[PairMatch]) -> str:
    """
    移除成对标记内侧的空格

    对于每一对标记：
    - 移除开始标记后面的空格（内侧）
    - 移除结束标记前面的空格（内侧）

    从后往前处理每一对标记，避免修改字符串后索引变化的问题。
    对于每一对，先处理结束标记前的空格，再处理开始标记后的空格。

    :param line: 要处理的字符串
    :param matches: 成对标记的匹配列表

    :return: 处理后的字符串
    """
    if not matches:
        return line

    # 按开始位置从后往前排序，确保修改不影响前面的索引
    sorted_matches = sorted(matches, key=lambda m: m.open_start, reverse=True)

    result = line
    for match in sorted_matches:
        # 先处理结束标记前面的空格
        space_count = 0
        pos = match.close_start
        while pos - space_count - 1 >= 0 and result[pos - space_count - 1] == " ":
            space_count += 1
        if space_count > 0:
            result = result[: pos - space_count] + result[pos:]

        # 再处理开始标记后面的空格
        # 注意：删除close前的空格不影响open_end的位置（因为在前面）
        space_count = 0
        pos = match.open_end
        while pos + space_count < len(result) and result[pos + space_count] == " ":
            space_count += 1
        if space_count > 0:
            result = result[:pos] + result[pos + space_count :]

    return result


def post_process_paired_markers(line: str) -> str:
    """
    后处理：移除成对标记内侧的多余空格

    目前支持的标记：
    - ** (Markdown粗体)

    这个函数会按顺序处理多个标记类型，每次处理完一个标记类型后，
    将修改后的字符串作为下一个标记类型的输入。

    :param line: 要处理的字符串

    :return: 处理后的字符串
    """
    # 可以扩展到其他标记，如 "()", "[]", "<>" 等
    markers_to_process = ["**"]

    for marker in markers_to_process:
        matches = find_pair_markers(line, marker)
        line = remove_spaces_around_paired_markers(line, matches)

    return line


def _process_last_special_char(line: str, tokens: list[str], char: str):
    try:
        if line.rstrip()[-1] == char:
            tokens.append("")
    except IndexError:
        pass


def handle_dou_hao(line: str) -> str:
    """
    中文逗号 ， → 英文逗号 ,
    并在逗号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("，") if token.strip()]
    _process_last_special_char(line, tokens, "，")
    return ", ".join(tokens).strip()


def handle_dun_hao(line: str) -> str:
    """
    中文顿号 、 → 英文逗号 ,
    并在逗号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("、") if token.strip()]
    _process_last_special_char(line, tokens, "、")
    return ", ".join(tokens).strip()


def handle_ju_hao(line: str) -> str:
    """
    中文句号 。 → 英文句号 .
    并在句号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("。") if token.strip()]
    _process_last_special_char(line, tokens, "。")
    return ". ".join(tokens).strip()


def handle_mao_hao(line: str) -> str:
    """
    中文冒号 ： → 英文冒号 :
    并在冒号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("：") if token.strip()]
    _process_last_special_char(line, tokens, "：")
    return ": ".join(tokens).strip()


def handle_fen_hao(line: str) -> str:
    """
    中文分号 ； → 英文分号 ;
    并在分号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("；") if token.strip()]
    _process_last_special_char(line, tokens, "；")
    return "; ".join(tokens).strip()


def handle_wen_hao(line: str) -> str:
    """
    中文问号 ？ → 英文问号 ?
    并在问号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("？") if token.strip()]
    _process_last_special_char(line, tokens, "？")
    return "? ".join(tokens).strip()


def handle_exclamation(line: str) -> str:
    """
    中文感叹号 ！ → 英文感叹号 !
    并在感叹号后添加一个空格
    """
    tokens = [token.strip() for token in line.split("！") if token.strip()]
    _process_last_special_char(line, tokens, "！")
    return "! ".join(tokens).strip()


@dataclass(frozen=True)
class BracketPair:
    """
    一对成对出现的中文标点, 以及它们对应的英文形式

    :param open_cn: 中文左标记, 如 "（"
    :param open_en: 对应的英文左标记, 如 "("
    :param close_cn: 中文右标记, 如 "）"
    :param close_en: 对应的英文右标记, 如 ")"
    """

    open_cn: str
    open_en: str
    close_cn: str
    close_en: str


#: 所有成对标点的映射表. 新增一种括号只要在这里加一行.
#: 顺序会影响相邻标记的处理结果, 引号放在最后, 与括号类保持先后关系.
BRACKET_PAIRS = [
    BracketPair("（", "(", "）", ")"),
    BracketPair("【", "[", "】", "]"),
    BracketPair("［", "[", "］", "]"),
    BracketPair("《", "<", "》", ">"),
    BracketPair("〈", "<", "〉", ">"),
    BracketPair("＜", "<", "＞", ">"),
    BracketPair("｛", "{", "｝", "}"),
    BracketPair("“", '"', "”", '"'),
]

#: 右标记后面紧跟这些字符时, 不再补空格.
#: 除了英文标点, 还包括中文的右标记 —— 它们在后续的 pair 中才会被转换成英文,
#: 但此刻已经能确定「右边是一个收口符号」, 不该在中间插空格.
NO_SPACE_BEFORE = ",.:;?!)]}>" + "）】］》〉＞｝”"

#: 左标记前面紧挨着这些字符时, 不再补空格. 理由同 :data:`NO_SPACE_BEFORE`.
NO_SPACE_AFTER = "([{<" + "（【［《〈＜｛“"


def handle_open_bracket(line: str, open_cn: str, open_en: str) -> str:
    """
    中文左标记 → 英文左标记, 并在左标记前添加一个空格

    如果左标记本身就在行首, 或者紧挨着另一个左标记 (例如 "【（" ), 就不补空格.

    :param line: 要处理的字符串
    :param open_cn: 中文左标记, 如 "（"
    :param open_en: 对应的英文左标记, 如 "("

    :return: 处理后的字符串

    .. note::

        不能过滤掉 split 产生的空 token. 空 token 携带了「这里是行首」这样的
        结构信息, 过滤掉会导致 join 少一个分隔符, 左标记直接消失.
        例如 "（内容）" split 后是 ["", "内容）"], 过滤后只剩一个 token,
        join 不产生任何分隔符, 左括号就丢了.
    """
    tokens = [token.strip() for token in line.split(open_cn)]
    result = tokens[0]
    for token in tokens[1:]:
        if result and result[-1] not in NO_SPACE_AFTER:
            result += " "
        result += open_en + token
    return result.strip()


def handle_close_bracket(line: str, close_cn: str, close_en: str) -> str:
    """
    中文右标记 → 英文右标记, 并在右标记后添加一个空格

    如果右标记后面紧跟着 :data:`NO_SPACE_BEFORE` 里的字符, 就不补空格.

    :param line: 要处理的字符串
    :param close_cn: 中文右标记, 如 "）"
    :param close_en: 对应的英文右标记, 如 ")"

    :return: 处理后的字符串

    .. note::

        同 :func:`handle_open_bracket`, 不过滤空 token.
        行尾的右标记会产生一个末尾空 token, 循环自然会为它补上 ") ",
        因此不需要单独判断「行尾是不是右标记」, 多出的尾部空格由 strip() 清理.
    """
    tokens = [token.strip() for token in line.split(close_cn)]
    new_tokens = list()
    for ith, token in enumerate(tokens):
        new_tokens.append(token)
        if ith + 1 >= len(tokens):
            break
        next_token = tokens[ith + 1]
        if next_token:
            no_space = next_token[0] in NO_SPACE_BEFORE
        else:
            # 空的 next_token 只有两种来源: 紧跟着又一个相同的右标记
            # (例如 "））"), 或者这里已经是行尾. 两种情况都不补空格 ——
            # 行尾多出来的空格反正也会被 strip() 清掉.
            no_space = True
        new_tokens.append(close_en if no_space else close_en + " ")
    return "".join(new_tokens).strip()


def handle_all_brackets(line: str) -> str:
    """
    按 :data:`BRACKET_PAIRS` 依次处理所有成对标点

    :param line: 要处理的字符串

    :return: 处理后的字符串
    """
    for pair in BRACKET_PAIRS:
        line = handle_open_bracket(line, pair.open_cn, pair.open_en)
        line = handle_close_bracket(line, pair.close_cn, pair.close_en)
    return line


def handle_consecutive_punctuation(line: str) -> str:
    """
    处理连续的2-3个相同的中文标点符号

    连续的中文标点应该被视为一个整体，直接转换为对应数量的英文标点，不在中间添加空格。
    例如：
    - 。。。 → ...
    - ？？？ → ???
    - ！！！ → !!!

    :param line: 要处理的字符串
    :return: 处理后的字符串
    """
    # 定义中文标点到英文标点的映射
    punctuation_map = {
        "。": ".",
        "？": "?",
        "！": "!",
    }

    # 处理每种标点的连续情况（2-3个）
    for chinese_punct, english_punct in punctuation_map.items():
        # 匹配2-3个连续的相同标点
        pattern = f"{re.escape(chinese_punct)}{{2,3}}"

        def replace_func(match, english_punct=english_punct):
            # 将连续的中文标点替换为相同数量的英文标点
            count = len(match.group())
            return english_punct * count

        line = re.sub(pattern, replace_func, line)

    return line


def handle_space_between_chinese_and_english(line: str) -> str:
    """
    Add space between Chinese and English characters/numbers/punctuation.
    Goes through character by character and maintains two consecutive characters.
    If one is an ASCII character (a-z, A-Z, 0-9, or certain ASCII punctuation) and the other is non-ASCII, add space between them.

    Special rules:
    - Closing punctuation (,.!?;:)) should NOT have space before them
    - Opening punctuation (([{"') should NOT have space after them
    - Closing quotes (determined by context) can have space after them
    """
    if not line:
        return line

    result = []
    prev_char = None

    # Punctuation that should stay close to preceding text (no space before)
    closing_punctuation = ",.!?;:)]}>"
    # Punctuation that should stay close to following text (no space after)
    # This includes opening brackets and left quotes
    opening_punctuation = "([{<\""

    # Track whether we're inside quotes (simple toggle)
    inside_quotes = False

    for current_char in line:
        # Check if we need to add space between prev_char and current_char
        if prev_char is not None:
            # Check character types
            prev_is_english = prev_char.isalpha() and ord(prev_char) < 128
            current_is_english = current_char.isalpha() and ord(current_char) < 128
            prev_is_number = prev_char.isdigit()
            current_is_number = current_char.isdigit()
            prev_is_non_ascii = ord(prev_char) >= 128
            current_is_non_ascii = ord(current_char) >= 128
            # Check for ASCII punctuation (excluding space and common separators)
            prev_is_ascii_punct = (
                ord(prev_char) < 128
                and not prev_char.isalnum()
                and prev_char not in " \t\n"
            )
            current_is_closing_punct = current_char in closing_punctuation

            # Special handling for quotes: check if previous quote is a closing quote
            # A quote is closing if it comes after alphanumeric characters or non-ASCII chars
            prev_is_closing_quote = (
                prev_char == '"'
                and len(result) >= 2
                and (result[-2].isalnum() or ord(result[-2]) >= 128)
            )

            # Check if current char is a quote and determine if it's opening or closing
            # Use quote state tracking: if we're not inside quotes, it's opening; otherwise closing
            if current_char == '"':
                current_is_opening_quote = not inside_quotes
                current_is_closing_quote_char = inside_quotes
            else:
                current_is_opening_quote = False
                current_is_closing_quote_char = False

            # Opening punctuation, but exclude closing quotes
            # Note: quotes in opening_punctuation are treated as opening ONLY when followed by content
            prev_is_opening_punct = (
                prev_char in opening_punctuation and not prev_is_closing_quote
            )

            # Add space in the following cases:
            should_add_space = False

            # 1. Between English letter and non-ASCII character, example: "Eng中文"
            if prev_is_english and current_is_non_ascii:
                should_add_space = True
            # 2. Between non-ASCII character and English letter, example: "中文Eng"
            # BUT NOT after opening punctuation/quotes
            elif (
                prev_is_non_ascii and current_is_english and not prev_is_opening_punct
            ):
                should_add_space = True
            # 3. Between number and non-ASCII character, example: "100中文"
            elif prev_is_number and current_is_non_ascii:
                should_add_space = True
            # 4. Between non-ASCII character and number, example: "中文100"
            # BUT NOT after opening punctuation/quotes
            elif prev_is_non_ascii and current_is_number and not prev_is_opening_punct:
                should_add_space = True
            # 5. Between ASCII punctuation and non-ASCII character
            # BUT NOT after opening punctuation like ( or opening quotes
            elif (
                prev_is_ascii_punct
                and current_is_non_ascii
                and not prev_is_opening_punct
            ):
                should_add_space = True
            # 6. Between non-ASCII character and ASCII letter
            # Example: '中文A' should add space
            # BUT NOT before opening quotes
            elif (
                prev_is_non_ascii
                and prev_char not in " "
                and current_char.isalpha()
                and ord(current_char) < 128
                and not current_is_opening_quote
            ):
                should_add_space = True
            # 7. Between non-ASCII character and opening quote, example: '从"' -> '从 "'
            elif prev_is_non_ascii and current_is_opening_quote:
                should_add_space = True

            # Actually add the space if conditions met
            # Don't add before closing punctuation or closing quotes
            if (
                should_add_space
                and not current_is_closing_punct
                and not current_is_closing_quote_char
            ):
                result.append(" ")

        result.append(current_char)
        prev_char = current_char

        # Update quote state
        if current_char == '"':
            inside_quotes = not inside_quotes

    return "".join(result)


def split_indent(line: str) -> tuple[str, str]:
    """
    将一行拆分为「行首缩进」和「剩余内容」两部分

    各个 handler 内部会对 token 做 strip(), 会把行首缩进一起吞掉.
    对于 Markdown / reStructuredText 的代码块 (以及列表的续行) 来说,
    缩进是有语义的, 不能被破坏. 所以在处理前先把缩进摘出来, 处理完再拼回去.

    :param line: 要拆分的字符串

    :return: (缩进, 去掉行首空白后的内容) 元组

    .. code-block:: python

        >>> split_indent("    hello")
        ('    ', 'hello')
        >>> split_indent("\\thello")
        ('\\t', 'hello')
    """
    content = line.lstrip()
    indent = line[: len(line) - len(content)]
    return indent, content


def handle_everything(line: str) -> str:
    """
    对单独一行文本按顺序应用所有的 handler.

    :param line: 要处理的一行文本 (不含换行符)

    :return: 处理后的一行文本
    """
    # 先把行首缩进摘出来, 避免后续 handler 的 strip() 把它吞掉
    indent, line = split_indent(line)
    # 空行 (或纯空白行) 直接返回空字符串, 不保留无意义的尾部空白
    if not line:
        return ""
    # First, handle consecutive punctuation (2-3 of the same type)
    # This must be done before individual punctuation handling
    line = handle_consecutive_punctuation(line)
    # Then handle individual punctuation marks
    line = handle_dou_hao(line)
    line = handle_dun_hao(line)
    line = handle_ju_hao(line)
    line = handle_mao_hao(line)
    line = handle_fen_hao(line)
    line = handle_wen_hao(line)
    line = handle_exclamation(line)
    # Then the paired marks: brackets and quotes
    line = handle_all_brackets(line)
    # Add spaces between Chinese and English after all punctuation conversions
    line = handle_space_between_chinese_and_english(line)
    # Post-process to remove spaces inside paired markers
    line = post_process_paired_markers(line)
    # 最后把行首缩进拼回去
    return indent + line


def process(text: str) -> str:
    """
    把一段文本中的中文全角标点转换为英文半角标点, 并补齐中英文之间的空格.

    :param text: 要处理的文本, 可以是多行

    :return: 处理后的文本. 注意行尾换行符不会被保留, 换行符统一为 ``\\n``.
    """
    lines = text.splitlines()
    new_lines = [handle_everything(line) for line in lines]
    return "\n".join(new_lines)
