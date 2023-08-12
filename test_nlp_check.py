from unittest import TestCase
from nlp_check import *
from language_tool_python import LanguageTool


class Test(TestCase):
    def setUp(self) -> None:
        ...


    def test_is_plural_nltk(self):
        nltk.set_proxy('http://127.0.0.1:4780')
        nltk.download('wordnet')
        singular_word = "cut"
        plural_word = "cutes"

        if is_plural_nltk(plural_word, singular_word):
            print(f"'{plural_word}' is the plural form of '{singular_word}'.")
        else:
            print(f"'{plural_word}' is not the plural form of '{singular_word}'.")

    def test_is_spelling_pair_error(self):
        word1 = "the"
        word2 = "quickk"
        if is_spelling_pair_error(word1, word2):
            print(f"'{word1} {word2}' contains spelling errors.")
        else:
            print(f"'{word1} {word2}' is correctly spelled.")

    def test_check_spelling_pair_distance(self):
        word1 = "manipulation"
        word2 = "manuplayation"
        max_distance = 2
        if check_spelling_pair_distance(word1, word2, max_distance):
            print(f"{word1} 和 {word2} 是成对的拼写错误喵！")
        else:
            print(f"{word1} 和 {word2} 不是成对的拼写错误喵！")

    def test_check_spelling_pair_languagetool(self):
        # 创建 LanguageTool 对象
        tool = LanguageTool('en-US')

        # 例子：检查 "hello" 和 "helo" 是否成对的拼写错误
        input = "hello"
        gt = "hello"
        if check_spelling_pair_languagetool(tool, input, gt):
            print(f"{input} 和 {gt} 是成对的拼写错误喵！")
        else:
            print(f"{input} 和 {gt} 不是成对的拼写错误喵！")
