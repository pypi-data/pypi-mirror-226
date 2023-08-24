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
import itertools
from ...utils import incidence, ratio, start_end_quote


class Syntactic(Category):
    lang = 'en'
    name_en = "Syntactic"


class SY_QUESTION(Metric):
    category = Syntactic
    name_en = "Number of words in interrogative sentences"

    def count(doc):
        sentences = [sent.text.split() for sent in doc.sents if sent[-1].text == '?']
        flatten = list(itertools.chain.from_iterable(sentences))
        result = incidence(doc, flatten)
        return result, {}


class SY_NARRATIVE(Metric):
    category = Syntactic
    name_en = "Number of words in narrative sentences"

    def count(doc):
        sents = [sent.text.split() for sent in doc.sents if sent[-1].text == "."]
        flatten = list(itertools.chain.from_iterable(sents))
        result = incidence(doc, flatten)
        return result, {}
    


class SY_NEGATIVE_QUESTIONS(Metric):
    category = Syntactic
    name_en = "Words in negative questions"

    def count(doc):
        general_question = []
        for sent in doc.sents:
                if any(token for token in sent if token.dep_ == "neg"):
                    broad_case = [sent.text for token in sent if token.is_sent_start and token.head == token and token.pos_ == "AUX"]
                    case_one = list(itertools.chain(*broad_case))
                    general_question.append(case_one)
                    
                    root = [sent.text for token in sent if token.head == token and any(child for child in token.lefts if child.dep_ == "aux"\
                                                                                    and child.is_sent_start) and sent not in case_one]
                    case_two = list(itertools.chain(*root))
                    general_question.append(case_two)
                    
                    middle = [sent.text for token in sent if token.head == token and any(child for child in token.lefts if child.dep_ == "aux") and\
                                any(c for c in token.lefts if c.is_punct) and sent[-1].text == "?"]
                    case_tree = list(itertools.chain(*middle))
                    general_question.append(case_tree)

        flatten = list(itertools.chain(*general_question))
        result = incidence(doc, flatten)
        debug = {'TOKENS': flatten}
        return result, debug


class SY_SPECIAL_QUESTIONS(Metric):
    category = Syntactic
    name_en = "Words in special questions"

    def count(doc):
        QUESTION_WORDS = ["what", "which", "who", "whom", "whose", "where", "when", "why", "how"]
        root = [[sent.text for token in sent if token.head == token and any(child for child in token.lefts if child.text.lower() in QUESTION_WORDS)] for sent in doc.sents]
        nested = list(itertools.chain(*root))
        flattend = list(itertools.chain(*nested))
        result = incidence(doc, flattend)
        debug = {'TOKENS': flattend}
        return result, debug


class SY_TAG_QUESTIONS(Metric):
    category = Syntactic
    name_en = "Words in tag questions"

    def count(doc):
        QUESTION_WORDS = ["what", "which", "who", "whom", "whose", "where", "when", "why", "how"]
        tag_question = [[sent.text for token in sent if token.dep_ == "ROOT" and any(token for token in token.rights if token.dep_ == "nsubj" or token.dep_ == "snubjpass")\
                     and any(token for token in token.lefts if token.text.lower() not in QUESTION_WORDS)] for sent in doc.sents]
        nested = list(itertools.chain(*tag_question))
        flatten = list(itertools.chain(*nested))
        result = incidence(doc, flatten)
        debug = {'TOKENS': flatten}
        return result, debug
    

class SY_GENERAL_QUESTIONS(Metric):
    category = Syntactic
    name_en = "Words in general questions"

    def count(doc):
        general_question = []

        for sent in doc.sents:
              if any(token for token in sent if token.dep_ == "neg"):
                     continue 
              else:
                  broad_case = [sent.text for token in sent if token.is_sent_start and token.head == token and token.pos_ == "AUX"]
                  case_one = list(itertools.chain(*broad_case))
                  general_question.append(case_one)
                  
                  root = [sent.text for token in sent if token.head == token and any(child for child in token.lefts if child.dep_ == "aux"\
                                                                                    and child.is_sent_start) and sent not in case_one]
                  case_two = list(itertools.chain(*root))
                  general_question.append(case_two)
                  
                  middle = [sent.text for token in sent if token.head == token and any(child for child in token.lefts if child.dep_ == "aux") and\
                              any(c for c in token.lefts if c.is_punct) and sent[-1].text == "?"]
                  case_tree = list(itertools.chain(*middle))
                  general_question.append(case_tree)

        flatten = list(itertools.chain(*general_question))
        result = incidence(doc, flatten)
        debug = {'TOKENS': flatten}
        return result, debug
    

class SY_EXCLAMATION(Metric):
    category = Syntactic
    name_en = "Number of words in exclamatory sentences"

    def count(doc):
        sent = [sent.text.split() for sent in doc.sents for token in sent if token.text == "!"]
        flatten = list(itertools.chain.from_iterable(sent))
        result = incidence(doc, flatten)
        return result, {}


class SY_IMPERATIVE(Metric):
    category = Syntactic
    name_en = "Words in imperative sentences"

    def count(doc):

        sentence_tokens = [[token.text for token in sent if token.is_alpha] for sent in doc.sents if
                           "VerbForm=Inf" in sent[0].morph and sent[0].tag_ == "VB"]
        flatten = list(itertools.chain.from_iterable(sentence_tokens))
        result = incidence(doc, flatten)
        debug = {'TOKENS': sentence_tokens}
        return result, debug


class SY_SUBORD_SENT(Metric):
    category = Syntactic
    name_en = "Words in subordinate sentences"

    def count(doc):
        subord_sentences = [sent.text for sent in doc.sents if any(token.pos_ == "SCONJ" or token.tag_ == "WDT" for token in sent)]
        join_sents = [*itertools.chain(*subord_sentences)]
        result = incidence(doc, join_sents)
        debug = {'TOKENS': join_sents}
        return result, debug


class SY_SUBORD_SENT_PUNCT(Metric):
    category = Syntactic
    name_en = "Punctuation in subordinate sentences"

    def count(doc):
        sub_sent_punct = [sent for sent in doc.sents if any(token.pos_ == "SCONJ" for token in sent)]
        join_sents = itertools.chain(*sub_sent_punct)
        sent_tok = [tkn.text for tkn in join_sents if tkn.pos_ in "PUNCT"]
        result = incidence(doc, sent_tok)
        debug = {'TOKENS': sent_tok}
        return result, debug


class SY_COORD_SENT(Metric):
    category = Syntactic
    name_en = "Words in coordinate sentences"

    def count(doc):
        coord_sentences = [sent.text for sent in doc.sents if any("ConjType=Cmp" in token.morph for token in sent)]
        join_sents = [*itertools.chain(*coord_sentences)]
        result = incidence(doc, join_sents)
        debug = {'TOKENS': join_sents}
        return result, debug


class SY_COORD_SENT_PUNCT(Metric):
    category = Syntactic
    name_en = "Punctuation in coordinate sentences"

    def count(doc):
        coord_sent_punct = [sent for sent in doc.sents if any(token.pos_ == "CCONJ" for token in sent)]
        join_sents = itertools.chain(*coord_sent_punct)
        sent_tok = [tkn.text for tkn in join_sents if tkn.pos_ in "PUNCT"]
        result = incidence(doc, sent_tok)
        debug = {'TOKENS': sent_tok}
        return result, debug


class SY_SIMPLE_SENT(Metric):
    category = Syntactic
    name_en = "Tokens in simple sentences"

    def count(doc):
        simple_sent = [sent.text.split() for sent in doc.sents if
                       any("ConjType=Cmp" not in token.morph or token.pos_ != "SCONJ" for token in sent)]
        join_sent = [*itertools.chain(*simple_sent)]
        result = incidence(doc, join_sent)
        debug = {'TOKENS': join_sent}
        return result, debug


class SY_DIRECT_SPEECH(Metric):
    category = Syntactic
    name_en = "Words in direct speech"

    def count(doc):
        start, end = start_end_quote(doc)
        if start != None and end != None:
            span = doc[start:end]
            span_words = [token for token in span]
            result = incidence(doc, span_words)
            debug = {'TOKENS': span_words}
            return result, debug
        else:
            result = ratio(len(doc), 0)
            return result, {}


class SY_INVERSE_PATTERNS(Metric):
    category = Syntactic
    name_en = "Incidents of inverse patterns"

    def count(doc):

        # if token is npadvmod and goes before the ROOT verb
        pattern_1 = [token.text for sent in doc.sents for token in sent if token.dep_ == "npadvmod" and token.i < token.head.i]
        # if token is dep and goes before the ROOT verb
        pattern_2 = [token.text for sent in doc.sents for token in sent if token.dep_ == "dep" and token.i < token.head.i]
        # if token is dobj and goes before the ROOT verb
        pattern_3 = [token.text for sent in doc.sents for token in sent if token.dep_ == "dobj" and token.i < token.head.i]
        # if token determines a relative clause and goes before the ROOT
        pattern_4 = [token.text for sent in doc.sents for token in sent if token.dep_ == "relcl" and token.i < token.head.i]
        # if token is the ROOT in the Past Tense and the token is sentence start
        pattern_5 = [token.text for sent in doc.sents for token in sent if token.dep_ == "ROOT" and "Tense=Past" in token.morph and token.is_sent_start]

        patterns = pattern_1 + pattern_2 + pattern_3 + pattern_4 + pattern_5
        result = incidence(doc, patterns)
        debug = {'TOKENS': patterns}
        return result, debug


class FOS_SIMILE(Metric):
    category = Syntactic
    name_en = "Simile"

    def count(doc):
        head_pos = ["AUX", "VERB"]
        prep_tokens = [token for token in doc if token.pos_ == 'ADP' and token.text == 'like' and token.head.pos_ in head_pos]
        check = [[child for child in token.children if child.dep_ == "pobj" or child.dep_ == "pcomp"] for token in prep_tokens]
        as_as = [token for token in doc if token.text == 'as' and token.dep_ == "prep" and token.head.pos_ in ["ADJ", "NOUN"]]
        tokens = list(itertools.chain(*check)) + as_as
        result = incidence(doc, tokens)
        debug = {'TOKENS': tokens}
        return result, debug


class FOS_FRONTING(Metric):
    category = Syntactic
    name_en = "Fronting"

    def count(doc):

        search = []
        heads = ["nsubj", "aux", "ROOT", "nsubjpass", "auxpass"]
        tags = ["prep", "pobj", "amod", "dobj"]

        for sent in doc.sents:
            tokens = []
            for token in sent:
                if token.dep_ not in heads:
                    tokens.append(token.dep_)
                else:
                    break
            search.append(sent.text if any(tag in tokens for tag in tags) else [])
        toks = list(itertools.chain(*search))
        result = incidence(doc, toks)
        debug = {'TOKENS': search}
        return result, debug


class PS_SYNTACTIC_IRRITATION(Metric):
    category = Syntactic
    name_en = "Incidents of continuous tenses as irritation markers"

    def count(doc):
        words = ["constantly", "continuously", "always", "all the time", "every time"]
        sents = []
        
        search = [sents.append(sent.text) for sent in doc.sents if any(token for token in sent if token._.verb_tense == "present_cont" or token._.verb_tense == "past_cont" or token._.verb_tense == "present_perfect_cont" or token._.verb_tense == "past_perfect_cont")
                  and any(token for token in sent if token.text in words)]
        result = incidence(doc, sents)
        debug = {'TOKENS': sents}
        return result, debug


class SY_INTENSIFIER(Metric):
    category = Syntactic
    name_en = "Intensifiers"

    def count(doc):
        INT = ["do", "does", "did"]
        sents = []
        for sent in doc.sents:
            for token in sent:
                if token.head == token and any(child for child in token.children if child.dep_ == "aux" and child.is_sent_start == False and child.text in INT) and not any(child for child in token.subtree if child.dep_ == "neg") and not any(child for child in sent if child.is_sent_end and child.text == "?"):
                    sents.append(list(itertools.chain(sent.text)))
        flatten = list(itertools.chain(*sents))
        result = incidence(doc, flatten)
        debug = {'TOKENS': flatten}
        return result, debug