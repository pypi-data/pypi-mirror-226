from spacy.matcher import Matcher

from ...structures import Metric, Category
from ...utils import ratio


class Deskryptywne(Category):
  lang='pl'
  name_en='Descriptive'
  name_local='Deskryptywne'


class DESC_ADJ(Metric):
    category = Deskryptywne
    name_en = "Adjectival description of properties"
    name_local = "Opis właściwości przymiotnikowy"

    def count(doc):   
        nlp = DESC_ADJ.get_nlp() 
        matcher = Matcher(nlp.vocab)
        pattern = [{"POS": "ADJ", "IS_DIGIT": False}, {"POS":"CCONJ", "OP": "?"}, {"IS_PUNCT": True, "OP": "?"}, {"POS": "ADJ"}]
        pattern = [{"POS": "ADJ", "IS_DIGIT": False}, {"ORTH": {"IN": ['-',',',';','/']}, "OP":"?"}, {"POS":"CCONJ"},{"ORTH": {"IN": ['-',',',';','/']}, "OP":"?"},{"POS": "ADJ"}]
        matcher.add("nazwa", [pattern])
        matches = matcher(doc)
        tri_grams = [doc[start:end].text for _, start, end in matches]

        results = set([token.lemma_.lower() for token in doc if token.is_punct == False])
        debug = {'FOUND': results}
        return ratio(len(results), len(doc)), debug


class DESC_ADV(Metric):
    category = Deskryptywne
    name_en = "Adverbial description of properties"
    name_local = "Opis właściwości przysłówkowy"

    def count(doc):
        nlp = DESC_ADV.get_nlp()
        matcher = Matcher(nlp.vocab)
        pattern = [{"POS": "ADV", "IS_DIGIT": False}, {"POS":"CCONJ", "OP": "?"}, {"IS_PUNCT": True, "OP": "?"}, {"POS": "ADV"}]
        pattern = [{"POS": "ADV", "IS_DIGIT": False}, {"ORTH": {"IN": ['-',',',';','/']}, "OP":"?"}, {"POS":"CCONJ"},{"ORTH": {"IN": ['-',',',';','/']}, "OP":"?"},{"POS": "ADV"}]
        matcher.add("nazwa", [pattern])
        matches = matcher(doc)
        tri_grams = [doc[start:end].text for _, start, end in matches]
        
        results = set([token.lemma_.lower() for token in doc if token.is_punct == False])
        debug = {'FOUND': results}
        return ratio(len(results), len(doc)), debug


class DESC_NVA(Metric):
    category = Deskryptywne
    name_en = "Pattern 'sth is/works somehow'(N/PRON-V-ADJ/ADV)"
    name_local = "Schemat 'Coś jest jakieś/działa jakoś' (N/PRON-V-ADJ/ADV)"

    def count(doc):
        nlp = DESC_NVA.get_nlp()
        matcher = Matcher(nlp.vocab)
        pattern = [{"POS": {"IN": ["NOUN", "PRON", "PROPN"]}}, {"POS": {"IN": ["VERB", "AUX"]}, "ORTH": {"NOT_IN": ['to']}},{"POS": {"IN": ["ADJ", "ADV"]}}]
        matcher.add("nazwa", [pattern])
        matches = matcher(doc)
        tri_grams = [doc[start:end].text for _, start, end in matches]
        tri_gram_count = len(tri_grams)*3
        debug = {'FOUND': tri_grams}
        return ratio(tri_gram_count, len(doc)), debug


class DESC_NVN(Metric):
    category = Deskryptywne
    name_en = "Pattern 'sb did sth' (N-V-ADJ*-N)"
    name_local = "Schemat 'ktoś zrobił coś' (N-V-ADJ*-N)"

    def count(doc):
        nlp = DESC_NVN.get_nlp()
        matcher = Matcher(nlp.vocab)
        pattern = [{"POS": {"IN": ["NOUN", "PRON", "PROPN"]}}, {"MORPH": {"INTERSECTS": ["Tense=Past"]}},{"POS": {"IN": ["ADJ", "ADV", "PRON"]}, "OP": "?"}, {"POS": "NOUN"}]
        matcher.add("nazwa", [pattern])
        matches = matcher(doc)
        tri_grams = [doc[start:end].text for _, start, end in matches]
        tri_gram_count = len(tri_grams)*3
        debug = {'FOUND': tri_grams}
        return ratio(tri_gram_count, len(doc)), debug