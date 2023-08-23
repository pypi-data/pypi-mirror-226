from rebyu.pipeline.base import BaseStep, BasePipeline
from rebyu.pipeline.step import (
    RebyuStep,
    PREP_CAST_NAN,
    PREP_CAST_CASE,
    PREP_TRIM_TEXT,
    PREP_REMOVE_PATTERNS,
    PREP_REMOVE_NUMBERS,
    PREP_REMOVE_PUNCTUATIONS,
    PREP_REMOVE_WHITESPACES,
    PREP_REMOVE_SPECIFICS,
    PREP_REMOVE_EMOJIS,
    PREP_REMOVE_STOPWORDS,
    PREP_REPLACE_WORD,
    PREP_CENSOR_USERNAME,
    PREP_CENSOR_URLS,
    PREP_EXPAND_CONTRACTIONS,
    PREP_SENTENCE_LENGTH,
    PREP_WORD_COUNT,
    COMPOSE_COUNTER_VOCAB,
    COMPOSE_COUNTER_CHARVOCAB,
    COMPOSE_SET_CHARVOCAB,

    # TextBlob
    PREP_TEXTBLOB,
    PREP_TEXTBLOB_TOKENIZE,
    PREP_TEXTBLOB_SENTENCES,
    ANALYZE_TEXTBLOB_POLARITY,

    # NLTK
    PREP_NLTK_TOKENIZE,
    COMPOSE_NLTK_VOCAB,
    COMPOSE_NLTK_POS_TAG,
    COMPOSE_NLTK_NER,
    ANALYZE_VADER_POLARITY,

    # Transformers
    PREP_TRANSFORMERS_TOKENIZE,
    ANALYZE_TRANSFORMERS_MODEL,
    ANALYZE_TRANSFORMERS_PIPELINE,

    ANALYZE_CARDIFFNLP_SENTIMENT,
    ANALYZE_CARDIFFNLP_EMOTION,
    ANALYZE_FINITEAUTOMATA_SENTIMENT,
    ANALYZE_FINITEAUTOMATA_EMOTION
)
from rebyu.pipeline.pipeline import RebyuPipeline

BLANK_PIPELINE = RebyuPipeline(
    pid='blank-pipeline',
    steps=[]
)

TEST_PIPELINE = RebyuPipeline(
    pid='test-pipeline',
    steps=[
        PREP_CAST_NAN,
        PREP_CAST_CASE,
        PREP_EXPAND_CONTRACTIONS,
        PREP_REMOVE_NUMBERS,
        PREP_REMOVE_PUNCTUATIONS,
        PREP_REMOVE_WHITESPACES,
        PREP_NLTK_TOKENIZE,
        COMPOSE_COUNTER_VOCAB,
        COMPOSE_SET_CHARVOCAB
    ]
)

TEXTBLOB_PIPELINE = RebyuPipeline(
    pid='textblob-pipeline',
    steps=[
        PREP_CAST_NAN,
        PREP_REMOVE_PUNCTUATIONS,
        PREP_SENTENCE_LENGTH,
        PREP_TEXTBLOB,
        PREP_TEXTBLOB_TOKENIZE,
        PREP_WORD_COUNT,
        COMPOSE_COUNTER_VOCAB,
        COMPOSE_COUNTER_CHARVOCAB,
        ANALYZE_TEXTBLOB_POLARITY
    ]
)
"""TextBlob-based Pipeline for Composition Extraction and Sentiment Analysis\n

1. PREP_CASE_NAN - Casting Non-Str to Empty String\n
2. PREP_REMOVE_PUNCTUATIONS - Remove Punctuations
3. PREP_SENTENCE_LENGTH - Get the Length of Text
4. PREP_TEXTBLOB - Transform to TextBlob Object
5. PREP_TEXTBLOB_TOKENIZE - Tokenize using TextBlob.tokens
6. PREP_WORD_COUNT - Get the Total Word Count
7. COMPOSE_COUNTER_VOCAB - Create a Counter Vocabulary
8. COMPOSE_COUNTER_CHARVOCAB - Create a Counter Character Vocabulary
9. ANALYZE_TEXTBLOB_POLARITY - Get the Polarity of the Text
"""

NLTK_PIPELINE = RebyuPipeline(
    pid='nltk-pipeline',
    steps=[
        PREP_CAST_NAN,
        PREP_REMOVE_PUNCTUATIONS,
        PREP_SENTENCE_LENGTH,
        PREP_NLTK_TOKENIZE,
        PREP_WORD_COUNT,
        COMPOSE_NLTK_VOCAB,
        COMPOSE_COUNTER_CHARVOCAB,
        COMPOSE_NLTK_POS_TAG,
        COMPOSE_NLTK_NER,
        ANALYZE_VADER_POLARITY
    ]
)
"""NLTK-based Pipeline for Composition Extraction and Sentiment Analysis\n

1. PREP_CASE_NAN - Casting Non-Str to Empty String\n
2. PREP_REMOVE_PUNCTUATIONS - Remove Punctuations
3. PREP_SENTENCE_LENGTH - Get the Length of Text
4. PREP_NLTK_TOKENIZE - Tokenize using NLTK
5. PREP_WORD_COUNT - Get the Total Word Count
6. COMPOSE_NLTK_VOCAB - Create an NLTK Vocabulary
7. COMPOSE_COUNTER_CHARVOCAB - Create a Counter Character Vocabulary
8. COMPOSE_NLTK_POS_TAG - Extract Part-of-Speech Tags
9. COMPOSE_NLTK_NER - Extract Named-Entities
10. ANALYZE_VADER_POLARITY - Get the Polarity of the Text
"""

CARDIFFNLP_PIPELINE = RebyuPipeline(
    pid='cardiff-nlp',
    steps=[
        PREP_CAST_NAN,
        PREP_TRIM_TEXT,
        PREP_CENSOR_USERNAME,
        PREP_CENSOR_URLS,
        PREP_REMOVE_EMOJIS,
        ANALYZE_CARDIFFNLP_SENTIMENT,
        ANALYZE_CARDIFFNLP_EMOTION
    ]
)

FINITEAUTOMATA_PIPELINE = RebyuPipeline(
    pid='finiteautomata',
    steps=[
        PREP_CAST_NAN,
        PREP_TRIM_TEXT,
        PREP_CENSOR_USERNAME,
        PREP_CENSOR_URLS,
        ANALYZE_FINITEAUTOMATA_SENTIMENT,
        ANALYZE_FINITEAUTOMATA_EMOTION
    ]
)