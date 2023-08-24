from spacy.matcher import DependencyMatcher

from ...structures import Metric, Category
from ...utils import ratio

class Syntaktyka(Category):
    lang='pl'
    name_en='Syntactic'
    name_local='Syntaktyka'


class SY_CCONJ(Metric):
    category = Syntaktyka
    name_en = "Coordinating conjunctions"
    name_local = "Spojniki wspolrzedne"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'CCONJ']
        result = len(debug)
        return ratio(result, len(doc)), debug

		
class SY_SCONJ(Metric):
    category = Syntaktyka
    name_en = "Subordinating conjunctions"
    name_local = "Spojniki podrzedne"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'SCONJ']
        result = len(debug)
        return ratio(result, len(doc)), debug


class SY_FMWE(Metric):
    category = Syntaktyka
    name_en = "Flat multiwords expressions"
    name_pl = "Zwiazki wielowyrazowe"
 
    def count(doc):
        flat = [[token.head, token] for token in doc if "flat" in token.dep_]
        debug = [token for i in flat for token in i]
        result = len(debug)
        return ratio(result, len(doc)), debug


class SY_APPM(Metric):
    category = Syntaktyka
    name_en = "Appositional modifiers"
    name_pl = "Modyfikatory w apozycji"
 
    def count(doc):
        flat = [[token.head, token] for token in doc if "appos" in token.dep_]
        debug = [token for i in flat for token in i]
        result = len(debug)
        return ratio(result, len(doc)), debug


class SY_S_DE(Metric):
    category = Syntaktyka
    name_en = "Words in declarative sentences"
    name_local = "Wyrazy w zdaniach oznajmujących"

    def count(doc):
        decl = set([sent for sent in doc.sents for token in sent if token.text in [".", "..."]])
        debug = [token for i in decl for token in i]
        result = len(debug)
        return ratio(result, len(doc)), debug


class SY_S_EX(Metric):
    category = Syntaktyka
    name_en = "Words in exclamatory sentences"
    name_local = "Wyrazy w zdaniach wykrzyknikowych"

    def count(doc):
        exl = set([sent for sent in doc.sents for token in sent if token.text == "!"])
        debug = [token for i in exl for token in i]
        result = len(debug)
        return ratio(result, len(doc)), debug


class SY_S_IN(Metric):
    category = Syntaktyka
    name_en = "Words in interrogative sentences"
    name_local = "Wyrazy w zdaniach pytajacych"

    def count(doc):
        quest = set([sent for sent in doc.sents for token in sent if token.text == "?"])
        debug = [token for i in quest for token in i]
        result = len(debug)
        return ratio(result, len(doc)), debug


class SY_S_NEG(Metric):
    category = Syntaktyka
    name_en = "Words in negative sentences"
    name_local = "Wyrazy w zdaniach przeczacych"

    def count(doc):
        neg = set([sent for sent in doc.sents for token in sent if "Polarity=Neg" in token.morph])
        debug = [token for i in neg for token in i]
        result = len(debug)
        return ratio(result, len(doc)), debug


class SY_S_NOM(Metric):
    category = Syntaktyka
    name_en = "Words in nominal sentences"
    name_local = "Rownowazniki zdan"

    def count(doc):
        nom = set([sent for sent in doc.sents if all(
        token.pos_ == 'AUX' and 'VerbType=Quasi' in token.morph for token in sent if token.pos_ == 'AUX')
        and not any(token for token in sent if token.pos_ in ['VERB', 'AUX']
        and token.pos_ != 'AUX')])
        debug = [token for i in nom for token in i]
        result = len(debug)
        return ratio(result, len(doc)), debug


class SY_S_INF(Metric):
    category = Syntaktyka
    name_en = "Words in infinitive-only sentences without finite verbs"
    name_local = "Słowa w zdaniach z bezokolicznikami bez czasowników osobowych"
	
    def count(doc):
        inf = set([sent for sent in doc.sents if not any(token for token in sent if "VerbForm=Fin" in token.morph)
                and any(token for token in sent if "VerbForm=Inf" in token.morph)])
        debug = [token for i in inf for token in i]
        result = len(debug)
        return ratio(result, len(doc)), debug


class SY_NPRED(Metric):
    category = Syntaktyka
    name_en = "Nominal predicates"
    name_local = "Orzeczenia imienne"
    
    def count(doc):
        nominal_predicates = []
        
        for sent in doc.sents:  
            for token in sent:
                if token.dep_ == 'cop':  
                    subject = token.head
                    predicate = token
                    
                    if subject.pos_ in ['NOUN','ADJ', 'PRON']:
                        nominal_predicates.append((subject.text, predicate.text))
        
        result = len(nominal_predicates)
        normalized_value = result / len(doc)
        return normalized_value, nominal_predicates


class SY_INV_OBJ(Metric):
    category = Syntaktyka
    name_en = "OVS word order"
    name_local = "Inwersja zdania, rozpoczęcie od dopełnienia"

    def count(doc):    
        nlp = SY_INV_OBJ.get_nlp()
        results = []
        counter = 0
        matcher = DependencyMatcher(nlp.vocab)        
        pattern = [# anchor token: root
            {   "RIGHT_ID" : "verb",
                "RIGHT_ATTRS": {"DEP": {"IN" : ["ROOT", 'xcomp']}}},
           
           # root >-- left child
           
            {   "LEFT_ID": "verb",  
                "REL_OP": ">--",
                "RIGHT_ID": "left child",
                "RIGHT_ATTRS": {"MORPH": {"INTERSECTS": ["Case=Gen", "Case=Dat", "Case=Acc", "Case=Ins", "Case=Loc"]}}
                  }
           ]
                
        matcher.add("LEFT_CHILD", [pattern])
        matches = matcher(doc)

        for i in range(len(matches)):
            match_id, token_ids = matches[i]
            match = []
            for l in doc[token_ids[1]].lefts:
              match.append(l)
            for n in range((token_ids[0]+1)-token_ids[1]):
              match.append(doc[token_ids[1]+n])
            results.append(match)
        
        counter = sum([len(listElem) for listElem in results])
        
        debug = {'FOUND': results}
        return ratio(counter, len(doc)), debug


class SY_INV_EPI(Metric):
    category = Syntaktyka
    name_en = "Inverted epithet"
    name_local = "Inwersja epitetu"

    def count(doc):    
        
        results = [token.text for token in doc if token.pos_ == "ADJ" and token.head.pos_ == "NOUN" and token in token.head.rights]
        debug = {'FOUND': results}
        return ratio(len(results), len(doc)), debug