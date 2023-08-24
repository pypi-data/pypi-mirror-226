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
from collections import Counter, defaultdict
from ...utils import sent_incidence, incidence
import itertools

class Statistics(Category):
    lang = 'en'
    name_en = "General Statistics"

class SENT_ST_WRDSPERSENT(Metric):
    category = Statistics
    name_en = "Difference between the number of words and the number of sentences"

    def count(doc):
        stat = len([*doc]) - len([*doc.sents])
        if stat > 0:
            result = stat / len([*doc])
            return result, {}
        else:
            return 0.0, {}
        


"""
The algorithme of counting statistical metrics is the following:
1. Take the dependency tegs in every sentence 
2. Save them in separate sents
3. Compare each subsequent set to the previous one
4. Calculate the needed statictical feature between two sets and save it in the list
5. Sum up the values in the list and divide by the number of sentences in the doc
"""


class SENT_ST_DIFFERENCE(Metric):
    category = Statistics
    name_en = "Symmetric difference between nodes in sentences per doc"

    def count(doc):

        sets = [set([token.dep_ for token in sent]) for sent in doc.sents]
        stat = []
        if len(sets) > 1:
            for i in range(0, len(sets)-1, 1):
                difference = sets[i].symmetric_difference(sets[i+1])
                diffs = len(difference) / (len(sets[i])+len(sets[i+1]))
                stat.append(diffs)
            result = sent_incidence(doc, stat)
            debug = {'TOKENS': difference}
            return result, debug
        else:
            result = 0.0
            return result, {}

    

class SENT_ST_SYMMETRY(Metric):
    category = Statistics
    name_en = "Similarity between nodes in sentences per doc"

    def count(doc):

        sets = [set([token.dep_ for token in sent]) for sent in doc.sents]
        stat = []
        if len(sets) > 1:
            for i in range(0, len(sets)-1, 1):
                similarity = sets[i].intersection(sets[i+1])
                sim = len(similarity) / (len(sets[i])+len(sets[i+1]))
                stat.append(sim)
            result = sent_incidence(doc, stat)
            debug = {'TOKENS': similarity}
            return result, debug
        else:
            result = 0.0
            return result, {}
        

class ST_REPETITIONS_WORDS(Metric):
    category = Statistics
    name_en = "Repetitions of words in text"

    def count(doc):
        doc_list = [token.text for token in doc if token._.is_content_word]
        bow = Counter(doc_list)
        repetitions = [value for _, value in bow.items() if value > 1]
        if len(repetitions) > 0:
            result = sum(repetitions) / len(doc)
            debug = [key for key, value in bow.items() if value > 1]
            return result, debug
        else:
            result = 0.0
            return result, {}


class ST_REPETITIONS_SENT(Metric):
    category = Statistics
    name_en = "Repetitions of sentences in text"

    def count(doc):
        dict_sent = defaultdict(list)
        SENT_SET = set([*doc.sents])

        if len(SENT_SET) > 1:
            count = 1
            for sent in doc.sents:
                if sent in dict_sent.keys():
                    count += 1
                    dict_sent[sent] = count
                else:
                    dict_sent[sent] = count
        words = [value for _, value in dict_sent.items() if value > 1]
        result = incidence(doc, words)
        debug = [key for key, value in dict_sent.items() if value > 1]
        return result, debug


class SENT_D_VP(Metric):
    category = Statistics
    name_en = "Statistics between VPs"

    def count(doc):
        stat = []

        # Statistics VPs in the sentence
        for sent in doc.sents:
            tokens = [token.text for token in sent if not token._.verb_tense]
            incidence = len(tokens) / len(sent)
            if len([*doc.sents]) == 1:
                return incidence, tokens
            else:
                stat.append(incidence)
                continue

        # Statistics of VPs in the doc
        result = sent_incidence(doc, stat)
        # debug = {'TOKENS': tokens}
        return result, {}


class SENT_D_NP(Metric):
    category = Statistics
    name_en = "Statistics between NPs"

    def count(doc):
        stat = []

        # Statistics NPs in the sentence
        for sent in doc.sents:
            NPs = [*map(lambda x: x.text.split(), [*sent.noun_chunks])]
            n = list(itertools.chain(*NPs))
            tokens = [token.text for token in sent if token.text not in n]
            incidence = len(tokens) / len(sent)
            if len([*doc.sents]) == 1:
                return incidence, tokens
            else:
                stat.append(incidence)
                continue

        # Statistics of NPs in the doc
        result = sent_incidence(doc, stat)
        # debug = {'TOKENS': tokens}
        return result, {}


class SENT_D_PP(Metric):
    category = Statistics
    name_en = "Statistics between PPs"

    def count(doc):
        stat = []

        # Statistics PPs in the sentence
        for sent in doc.sents:
            PPs = [[*map(lambda x: x.text, [*token.subtree])] for token in sent if token.dep_ == 'prep']
            p = set(itertools.chain(*PPs))
            tokens = [token.text for token in sent if token.text not in p]
            incidence = len(tokens) / len(sent)
            if len([*doc.sents]) == 1:
                return incidence, tokens
            else:
                stat.append(incidence)
                continue

        # Statistics of PPs in the doc
        result = sent_incidence(doc, stat)
        # debug = {'TOKENS': tokens}
        return result, {}


class SENT_D_ADJP(Metric):
    category = Statistics
    name_en = "Statistics between ADJPs"

    def count(doc):
        stat = []

        # Statistics ADJPs in the sentence
        for sent in doc.sents:
            ADJPs = [[*map(lambda x: x.text, [*token.children])] for token in sent if token._.adjectives]
            a = list(itertools.chain(*ADJPs))
            tokens = [token.text for token in sent if token.text not in a]
            incidence = len(tokens) / len(sent)
            if len([*doc.sents]) == 1:
                return incidence, tokens
            else:
                stat.append(incidence)
                continue

        # Statistics of ADJPs in the doc
        result = sent_incidence(doc, stat)
        # debug = {'TOKENS': stat}
        return result, {}


class SENT_D_ADVP(Metric):
    category = Statistics
    name_en = "Statistics between ADVPs"

    def count(doc):
        stat = []

        # Statistics ADVPs in the sentence
        for sent in doc.sents:
            ADVPs = [[token.text, *map(lambda x: x.text, [*token.children])] for token in sent if token._.adverbs]
            a = list(itertools.chain(*ADVPs))
            tokens = [token.text for token in sent if token.text not in a]
            incidence = len(tokens) / len(sent)
            if len([*doc.sents]) == 1:
                return incidence, tokens
            else:
                stat.append(incidence)
                continue

        # Statistics of ADVPs in the doc
        result = sent_incidence(doc, stat)
        # debug = {'TOKENS': tokens}
        return result, {}

