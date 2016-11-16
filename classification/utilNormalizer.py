# -*- coding: utf-8 -*-
import re
import unicodedata
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer


class Normalizer:
    """ Normalize Text """
    def __init__(self, row):
        self.row = row

    list_stop_word_french=['alors','au','aucuns','aussi','autre','avant','avec','avoir','bon','car','ce','cela','ces','ceux','chaque',
                           'ci','comme','comment','dans','des','du','dedans','dehors','depuis','devrait','doit','donc','dos','début',
                           'elle','elles','en','encore','essai','est','et','eu','fait','faites','fois','font','hors','ici','il','ils',
                           'je','juste','la','le','les','leur','là','ma','maintenant','mais','mes','mine','moins','mon','mot','même',
                           'ni','nommés','notre','nous','ou','où','par','parce','pas','peut','peu','plupart','pour','pourquoi','quand',
                           'que','quel','quelle','quelles','quels','qui','sa','sans','ses','seulement','si','sien','son','sont','sous',
                           'soyez','sujet','sur','ta','tandis','tellement','tels','tes','ton','tous','tout','trop','très','tu','voient',
                           'vont','votre','vous','vu','ça','étaient','état','étions','été','être', 'a']

    # Suppress number
    reg_numb = re.compile('[^\D]')
    # Suppress punctuation
    reg_ponct = re.compile('[^a-z 0-9ÀÁÂÃÄÅàáâãäåÒÓÔÕÖØòóôõöøÈÉÊËèéêëÇçÌÍÎÏìíîïÙÚÛÜùúûüÿÑñ²°Ø×ßŠ”�œ…]')
    # Suppress apostrophe
    reg_apos = re.compile('(l\')')

    # Suppress stop words
    french_stopwords_ini = stopwords.words('french')
    french_stopwords_ini.extend(list_stop_word_french)
    french_stopwords = set(french_stopwords_ini)

    # Stemming of words
    stemmer = FrenchStemmer()

    def to_lower(self, row):
        """ to lower case """
        return row.lower()
        # print 'low_case : ', str1

    def suppress_number(self):
        """ Suppress number """
        return reg_numb.sub('', str1)
        # print 'only_letters : ', str1

    # Suppress apostrophe
    str1 = reg_apos.sub('', str1)
    # print 'no apostrophe : ', str1

    # Suppress punctuation
    str1 = reg_ponct.sub('', str1)
    # print 'no_ponctuation : ', str1

    # Suppress stop words
    str1 = [token for token in str1.split(' ') if token.lower() not in french_stopwords]
    # print 'no_stop_words : ', str1

    # Suppress accent
    str1 = [word.encode('ascii', 'ignore') for word in str1]
    # str1 = [unicodedata.normalize('NFD', unicode(word, 'utf-8')).encode('ascii', 'ignore') for word in str1]
    # print 'no_accent : ', str1

    # Stemming of words
    str1 = [stemmer.stem(word) for word in str1]
    # print 'stemming : ', str1

    # Merging words
    # print 'merge_list : ', ' '.join(str1)
    return ' '.join(str1)
