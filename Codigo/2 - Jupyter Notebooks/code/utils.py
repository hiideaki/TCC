
from unidecode import unidecode
from nltk.corpus import stopwords


CUSTOM_STOPWORDS = ['vai', 'ser', 'pra', 'ter']

def get_stopwords(langs=["portuguese"], use_custom=True):
    STOPWORDS = []
    for lang in langs:
        STOPWORDS.extend([unidecode(sw) for sw in stopwords.words(lang)])

    if use_custom:
        STOPWORDS.extend([unidecode(sw) for sw in CUSTOM_STOPWORDS])
    return set(STOPWORDS)

