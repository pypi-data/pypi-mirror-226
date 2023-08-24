from spacy.matcher import Matcher

from ...structures import Metric, Category
from ...utils import ratio

class Interpunkcja(Category):
    lang='pl'
    name_en='Punctuation'
    name_local='Interpunkcja'

class PUNCT_TOTAL(Metric):
    category = Interpunkcja
    name_en = "Punctuation"
    name_local = "Interpunkcja"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'PUNCT']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class PUNCT_BI_NOUN(Metric):
    category = Interpunkcja
    name_en = "Punctuation following a noun"
    name_local = "Interpunkcja po rzeczowniku"

    def count(doc):
        nlp = PUNCT_BI_NOUN.get_nlp()
        matcher = Matcher(nlp.vocab)
        pattern = [{"POS": "NOUN"},  {"POS": "PUNCT"}]
        matcher.add("nazwa", [pattern])
        matches = matcher(doc)
        bi_grams = [doc[start:end].text for _, start, end in matches]
        bi_gram_count = len(bi_grams)*2
        debug = {'FOUND': bi_grams}
        return ratio(bi_gram_count, len(doc)), debug
		
class PUNCT_BI_VERB(Metric):
    category = Interpunkcja
    name_en = "Punctuation following a verb"
    name_local = "Interpunkcja po czasowniku"

    def count(doc):
        nlp = PUNCT_BI_VERB.get_nlp()
        matcher = Matcher(nlp.vocab)
        patterns = [
            [{"POS": {"IN": ["VERB", "AUX"]}}, {"IS_PUNCT": True}],
            [{"POS": {"IN": ["VERB", "AUX"]}}, {"LOWER": "się", "POS": "PRON"}, {"IS_PUNCT": True}]]
        matcher.add("punct_bi_verb3", patterns)
        matches = matcher(doc)
        bi_grams = [doc[start:end].text for _, start, end in matches]
        bi_gram_count = len(bi_grams) * 2
        debug = {"FOUND": bi_grams}
        return ratio(bi_gram_count, len(doc)), debug