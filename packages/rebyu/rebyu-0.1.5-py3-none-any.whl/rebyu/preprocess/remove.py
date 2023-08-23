import re
import string
from typing import List, Any, AnyStr

import nltk
from nltk.corpus import stopwords

from rebyu.util.dependency import nltk_dependency_mgt

NUMBERS_REGEX = r'\d+'
URLS_REGEX = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,' \
             r'})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,' \
             r'})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,' \
             r'}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})? '

EMOJI_REGEX = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U0000FE00-\U0000FE0F"  # Variation Selectors
                           u"\U00002702-\U000027B0"  # Dingbats
                           "]+", flags=re.UNICODE)


def remove_patterns(text: Any, pattern: AnyStr):
    """ Remove patterns (regex) from a text

    :param text: Any string object
    :param pattern: Any string object
    :return: text
    """
    if type(text) is str:
        return re.sub(pattern, '', text)
    return text


def remove_numbers(text: Any, pattern: AnyStr = NUMBERS_REGEX):
    """ Remove numerical data from text (using a regex pattern)

    :param text: Any string object
    :param pattern: Any string object
    :return: text
    """
    return remove_patterns(text, pattern)


def remove_urls(text: Any, pattern: AnyStr = URLS_REGEX):
    """ Remove urls from text (using a regex pattern)

    :param text: Any string object
    :param pattern: Any string object
    :return: text
    """
    return remove_patterns(text, pattern)


def remove_emojis(text: Any, pattern: AnyStr = EMOJI_REGEX):
    """ Remove emojis from text
    (Emoticons, Symbols & Pictograms, Transport & Map Symbols, Alchemical Symbols,
    Geometric Shape Extended, Supplemental Arrows-C, Supplemental Symbols & Pictographs,
    Chess Symbols, Symbols and Pictographs Extended-A, Dingbats, and Enclosed Alphanumerics & Ideographic)

    :param text: Any string object
    :param pattern: Any string object
    :return: text
    """
    return remove_patterns(text, pattern)


def remove_punctuations(text: Any):
    """ Remove punctuations from text (from string.punctuation)

    :param text: Any string object
    :return: text
    """
    if type(text) is str:
        return text.translate(str.maketrans('', '', string.punctuation))
    return text


def remove_whitespaces(text: Any):
    """ Strip any whitespaces from text

    :param text: Any string object
    :return: text
    """
    if type(text) is str:
        return text.strip()
    return text


def remove_specifics(text: Any, sub: Any):
    """ Remove specific substring from text

    :param text: Any string object
    :param sub: Any string object
    :return: text
    """
    if type(text) is str and type(sub) is str:
        return text.replace(sub, '')
    return text


def trim_text(text: Any, length: int = 500, pos: AnyStr = 'LEFT'):
    """ Trim the Text by Length

    :param text: Any string object
    :param length: Max. String length
    :param pos: Trim Position (LEFT or RIGHT)
    :return: text
    """
    if pos == 'LEFT':
        return text[:length]
    return text[length:]


# -- NLTK -- #

def remove_stopwords(text: Any, extra: List[Any] = None, language: str = 'english'):
    """ Remove stopwords from text (using NLTK Stopwords)

    :param text: Any string object
    :param extra: List of Any string objects
    :param language: The language of the text
    :return: text
    """

    nltk_dependency_mgt(required=['punkt', 'stopwords'])

    stop_words = set(stopwords.words(language) + (extra or []))
    tokens = nltk.word_tokenize(text)
    filtered_tokens = filter(lambda x: x.lower() not in stop_words, tokens)

    if type(text) is str:
        return ' '.join(filtered_tokens)
    return filtered_tokens
