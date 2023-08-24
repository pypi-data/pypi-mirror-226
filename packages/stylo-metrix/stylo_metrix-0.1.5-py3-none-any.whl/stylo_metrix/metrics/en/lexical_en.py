# Copyright (C) 2022  NASK PIB
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from ...structures import Metric, Category
from ...utils import incidence, log_incidence, clean_text
import math 
import regex as re


class Lexical(Category):
    lang = 'en'
    name_en = "Lexical"

class L_TYPE_TOKEN_RATIO_LEMMAS(Metric):
    category = Lexical
    name_en = "Type-token ratio for words lemmas"

    def count(doc):
        types = set(token.lemma_ for token in doc if token.is_alpha)
        result = incidence(doc, types)
        debug = {'TOKENS': types}
        return result, debug



class HERDAN_TTR(Metric):
    category = Lexical
    name_en = "Herdan's TTR"

    def count(doc):
        '''
        Function to calculate Herdan's TTR 
        param: doc - spacy doc object
        return: float - Herdan's TTR score
        '''
        # get types and tokens
        line = clean_text(doc.text)
        types = set(line.split())
        tokens = line.split()

        # calculate Herdan's TTR
        return log_incidence(len(types), len(tokens)), {}


class MASS_TTR(Metric):
    category = Lexical
    name_en = "Mass TTR"

    def count(doc):
        '''
        Function to calculate Mass TTR 
        param: doc - spacy doc object
        return: float - Mass TTR score

        The TTR score that displays most stability with respect to the text length.
        '''
        # get types and tokens
        line = clean_text(doc.text)
        types = set(line.split())
        tokens = line.split()
        try:
            if len(tokens) > 0 and len(types) > 0:
                return (math.log(len(tokens)) - math.log(len(types))) / math.log2(len(tokens)), {}
        except ZeroDivisionError:
            return 0.0, {}
        

class L_REF(Metric):
    category = Lexical
    name_en = "References"

    def count(doc):
        search = [token.text for token in doc if token.text.startswith('@')]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug


class L_HASHTAG(Metric):
    category = Lexical
    name_en = "Hashtags"

    def count(doc):
        search = re.findall(r'#\w+', doc.text)
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug
    

class L_RT(Metric):
    category = Lexical
    name_en = "Retweets"

    def count(doc):
        search = [token.text for token in doc if token.text == "RT" or token.text == "rt"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug
    

class L_LINKS(Metric):
    category = Lexical
    name_en = "Links"

    def count(doc):
        expr = r"\w+\.\w+.com\/.*"
        search = re.findall(r'https?://[^\s\n\r]+', doc.text) + re.findall(expr, doc.text)
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug
    

class L_CONT_A(Metric):
    category = Lexical
    name_en = "Content words"

    def count(doc):
        search = [token.text for token in doc if token._.is_content_word]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug


class L_FUNC_A(Metric):
    category = Lexical
    name_en = "Function words"

    def count(doc):
        search = [token.text for token in doc if token._.is_function_word]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug

class L_CONT_T(Metric):
    category = Lexical
    name_en = "Content words types"

    def count(doc):
        search = set(token.text for token in doc if token._.is_content_word)
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug


class L_FUNC_T(Metric):
    category = Lexical
    name_en = "Function words types"

    def count(doc):
        search = set(token.text for token in doc if token._.is_function_word)
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug


class L_SYL_G2(Metric):
    category = Lexical
    name_en = "Words formed of more than 2 syllables"

    def count(doc):
        lengths = [token._.syllables_count for token in doc if token._.syllables_count is not None]
        selected = [length for length in lengths if length > 2]
        result = incidence(doc, selected)
        debug = {'TOKENS': selected}
        return result, debug


"""NOUNS"""

class L_PLURAL_NOUNS(Metric):
    category = Lexical
    name_en = "Nouns in plural"

    def count(doc):
        nouns_plural = [token for token in doc if token.pos_ == "NOUN" and "Number=Plur" in token.morph]
        result = incidence(doc, nouns_plural)
        debug = {'TOKENS': nouns_plural}
        return result, debug


class L_SINGULAR_NOUNS(Metric):
    category = Lexical
    name_en = "Nouns in singular"

    def count(doc):
        nouns_sing = [token for token in doc if token.pos_ == "NOUN" and "Number=Sing" in token.morph]
        result = incidence(doc, nouns_sing)
        debug = {'TOKENS': nouns_sing}
        return result, debug


class L_PROPER_NAME(Metric):
    category = Lexical
    name_en = "Proper names"

    def count(doc):
        ents = [token for token in doc if token.pos_ == "PROPN"]
        result = incidence(doc, ents)
        debug = {'TOKENS': ents}
        return result, debug


class L_PERSONAL_NAME(Metric):
    category = Lexical
    name_en = "Personal names"

    def count(doc):
        ents = [list(ent) for ent in doc.ents if ent.label_ == 'PERSON']
        sum_ents = sum(ents, [])
        result = incidence(doc, sum_ents)
        debug = {'TOKENS': sum_ents}
        return result, debug


class L_NOUN_PHRASES(Metric):
    category = Lexical
    name_en = "Incidence of noun phrases"

    def count(doc):
        phrases = [noun_phrase for noun_phrase in doc.noun_chunks]
        np_ph = [noun for phrase in phrases for noun in phrase]
        result = incidence(doc, np_ph)
        debug = {'TOKENS': np_ph}
        return result, debug


"""PUNCTUATION"""


class L_PUNCT(Metric):
    category = Lexical
    name_en = "Punctuation"

    def count(doc):
        ents = [token for token in doc if token.pos_ == "PUNCT"]
        result = incidence(doc, ents)
        debug = {'TOKENS': ents}
        return result, debug


class L_PUNCT_DOT(Metric):
    category = Lexical
    name_en = "Punctuation - dots"

    def count(doc):
        ents = [token for token in doc if token.text == "."]
        result = incidence(doc, ents)
        debug = {'TOKENS': ents}
        return result, debug


class L_PUNCT_COM(Metric):
    category = Lexical
    name_en = "Punctuation - comma"

    def count(doc):
        ents = [token for token in doc if token.text == ","]
        result = incidence(doc, ents)
        debug = {'TOKENS': ents}
        return result, debug


class L_PUNCT_SEMC(Metric):
    category = Lexical
    name_en = "Punctuation - semicolon"

    def count(doc):
        ents = [token for token in doc if token.text == ";"]
        result = incidence(doc, ents)
        debug = {'TOKENS': ents}
        return result, debug


class L_PUNCT_COL(Metric):
    category = Lexical
    name_en = "Punctuation - colon"

    def count(doc):
        ents = [token for token in doc if token.text == ":"]
        result = incidence(doc, ents)
        debug = {'TOKENS': ents}
        return result, debug


class L_PUNCT_DASH(Metric):
    category = Lexical
    name_en = "Punctuation - dashes"

    def count(doc):
        ents = [token for token in doc if token.text == "—"]
        result = incidence(doc, ents)
        debug = {'TOKENS': ents}
        return result, debug


"""
POSSESSIVE NOUNS WITH 'S
"""

class L_POSSESSIVES(Metric):
    category = Lexical
    name_en = "Nouns in possessive case"
    
    def count(doc):
        pers_pron = [token for token in doc if token.pos_ == "PART" and token.dep_ == "case"]
        result = incidence(doc, pers_pron)
        debug = {'TOKENS': pers_pron}
        return result, debug


"""
ADJECTIVES & ADVERBS DEGREES OF COMPARISON
"""

class L_ADJ_POSITIVE(Metric):
    category = Lexical
    name_en = "Adjectives in positive degree"

    def count(doc):
        search = [token for token in doc if token._.adjectives == "positive_adjective"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug


class L_ADJ_COMPARATIVE(Metric):
    category = Lexical
    name_en = "Adjectives in comparative degree"

    def count(doc):
        search = [token for token in doc if token._.adjectives == "comparative_adjective"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug


class L_ADJ_SUPERLATIVE(Metric):
    category = Lexical
    name_en = "Adjectives in superlative degree"

    def count(doc):
        search = [token for token in doc if token._.adjectives == "superlative_adjective"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug


class L_ADV_POSITIVE(Metric):
    category = Lexical
    name_en = "Adverbs in positive degree"

    def count(doc):
        search = [token for token in doc if token._.adverbs == "positive_adverb"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug


class L_ADV_COMPARATIVE(Metric):
    category = Lexical
    name_en = "Adverbs in comparative degree"

    def count(doc):
        search = [token for token in doc if token._.adverbs == "comparative_adverb"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug


class L_ADV_SUPERLATIVE(Metric):
    category = Lexical
    name_en = "Adverbs in superlative degree"

    def count(doc):
        search = [token for token in doc if token._.adverbs == "superlative_adverb"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug

"""
Lexical
"""
class PS_CONTRADICTION(Metric):
    category = Lexical
    name_en = "Opposition, limitation, contradiction"

    def count(doc):
        search = [token.text for token in doc if token._.linking_words == "contradiction"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug

class PS_AGREEMENT(Metric):
    category = Lexical
    name_en = "Agreement, similarity"

    def count(doc):
        search = [token.text for token in doc if token._.linking_words == "agreement"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug

class PS_EXAMPLES(Metric):
    category = Lexical
    name_en = "Examples, emphasis"

    def count(doc):
        search = [token.text for token in doc if token._.linking_words == "examples"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug

class PS_CONSEQUENCE(Metric):
    category = Lexical
    name_en = "Consequence, result"

    def count(doc):
        search = [token.text for token in doc if token._.linking_words == "consequence"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug

class PS_CAUSE(Metric):
    category = Lexical
    name_en = "Cause, purpose"

    def count(doc):
        search = [token.text for token in doc if token._.linking_words == "cause"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug

class PS_LOCATION(Metric):
    category = Lexical
    name_en = "Location, space"

    def count(doc):
        search = [token.text for token in doc if token._.linking_words == "space"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug
    
class PS_TIME(Metric):
    category = Lexical
    name_en = "Time"

    def count(doc):
        search = [token.text for token in doc if token._.linking_words == "time"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug

class PS_CONDITION(Metric):
    category = Lexical
    name_en = "Condition, hypothesis"

    def count(doc):
        search = [token.text for token in doc if token._.linking_words == "condition"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug

class PS_MANNER(Metric):
    category = Lexical
    name_en = "Manner"

    def count(doc):
        search = [token.text for token in doc if token._.linking_words == "manner"]
        result = incidence(doc, search)
        debug = {'TOKENS': search}
        return result, debug