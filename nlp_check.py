import nltk
from nltk.stem import WordNetLemmatizer
from language_tool_python import LanguageTool
import spacy


def is_plural_nltk(Lemmatizer,  singular, word,):
    lemmatizer = Lemmatizer
    plural_lemma = lemmatizer.lemmatize(word, "n")
    return plural_lemma == singular


def check_spelling_pair_languagetool(tool: LanguageTool, input, gt):
    # 检查每个单词的拼写和语法错误
    errors = tool.check(input)
    if len(errors) == 0:
        return False
    return gt in errors[0].replacements
