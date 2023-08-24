from spacy.matcher import Matcher

from ...structures import Metric, Category
from ...utils import ratio

class Odmiana(Category):
    lang='pl'
    name_en='Inflection'
    name_local='Odmiana'

class IN_ADJ_POS(Metric):
    category = Odmiana
    name_en = "Adjectives in positive degree"
    name_local = "Przymiotniki w stopniu rownym"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'ADJ' and token.is_digit == False and token.is_punct == False
                and str(token.morph.get('Degree'))=='[\'Pos\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_ADJ_COM(Metric):
    category = Odmiana
    name_en = "Adjectives in comparative degree"
    name_local = "Przymiotniki w stopniu wyzszym"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'ADJ' and token.is_digit == False and token.is_punct == False
                and str(token.morph.get('Degree'))=='[\'Cmp\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_ADJ_SUP(Metric):
    category = Odmiana
    name_en = "Adjectives in superlative degree"
    name_local = "Przymiotniki w stopniu najwyzszym"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'ADJ' and token.is_digit == False and token.is_punct == False
                and str(token.morph.get('Degree'))=='[\'Sup\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_ADV_POS(Metric):
    category = Odmiana
    name_en = "Adverbs in positive degree"
    name_local = "Przyslowki w stopniu rownym"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'ADV'
                and str(token.morph.get('Degree'))=='[\'Pos\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_ADV_COM(Metric):
    category = Odmiana
    name_en = "Adverbs in comparative degree"
    name_local = "Przyslowki w stopniu wyzszym"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'ADV'
                and str(token.morph.get('Degree'))=='[\'Cmp\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_ADV_SUP(Metric):
    category = Odmiana
    name_en = "Adverbs in superlative degree"
    name_local = "Przyslowki w stopniu najwyzszym"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'ADV'
                and str(token.morph.get('Degree'))=='[\'Sup\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_1M(Metric):
    category = Odmiana
    name_en = "Nouns in nominative case"
    name_local = "Rzeczowniki w mianowniku"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'NOUN'
                and str(token.morph.get('Case'))=='[\'Nom\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_2D(Metric):
    category = Odmiana
    name_en = "Nouns in genitive case"
    name_local = "Rzeczowniki w dopelniaczu"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'NOUN'
                and str(token.morph.get('Case'))=='[\'Gen\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_3C(Metric):
    category = Odmiana
    name_en = "Nouns in dative case"
    name_local = "Rzeczowniki w celowniku"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'NOUN'
                and str(token.morph.get('Case'))=='[\'Dat\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_4B(Metric):
    category = Odmiana
    name_en = "Nouns in accusative case"
    name_local = "Rzeczowniki w bierniku"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'NOUN'
                and str(token.morph.get('Case'))=='[\'Acc\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_5N(Metric):
    category = Odmiana
    name_en = "Nouns in instrumental case"
    name_local = "Rzeczowniki w narzędniku"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'NOUN'
                and str(token.morph.get('Case'))=='[\'Ins\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_6Msc(Metric):
    category = Odmiana
    name_en = "Nouns in locative case"
    name_local = "Rzeczowniki w miejscowniku"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'NOUN'
                and str(token.morph.get('Case'))=='[\'Loc\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_7W(Metric):
    category = Odmiana
    name_en = "Nouns in vocative case"
    name_local = "Rzeczowniki w wołaczu"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'NOUN'
                and str(token.morph.get('Case'))=='[\'Voc\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_SG(Metric):
    category = Odmiana
    name_en = "Singular nouns"
    name_local = "Rzeczowniki w liczbie pojedynczej"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['NOUN', 'PERSN']
        and str(token.morph.get('Number'))=='[\'Sing\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_PL(Metric):
    category = Odmiana
    name_en = "Plural nouns"
    name_local = "Rzeczowniki w liczbie mnogiej"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['NOUN', 'PERSN']
        and str(token.morph.get('Number'))=='[\'Plur\']']
        result = len(debug)
        return ratio(result, len(doc)), debug

class IN_N_MS(Metric):
    category = Odmiana
    name_en = "Singular masculine nouns"
    name_local = "Rzeczowniki w liczbie pojedynczej w rodzaju męskim"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['NOUN', 'PERSN']
        and str(token.morph.get('Gender'))=='[\'Masc\']'
        and str(token.morph.get('Number'))=='[\'Sing\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_MP(Metric):
    category = Odmiana
    name_en = "Nouns in masculine personal gender (plural)"
    name_local = "Rzeczowniki w liczbie mnogiej w rodzaju męskoosobowym"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['NOUN', 'PERSN']
        and str(token.morph.get('Animacy'))=='[\'Hum\']'      
        and str(token.morph.get('Gender'))=='[\'Masc\']'
        and str(token.morph.get('Number'))=='[\'Plur\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_FS(Metric):
    category = Odmiana
    name_en = "Singular feminine nouns"
    name_local = "Rzeczowniki w liczbie pojedynczej w rodzaju żeńskim"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['NOUN', 'PERSN']
        and str(token.morph.get('Gender'))=='[\'Fem\']'
        and str(token.morph.get('Number'))=='[\'Sing\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_NMP(Metric):
    category = Odmiana
    name_en = "Nouns in non-masculine personal gender (plural)"
    name_local = "Rzeczowniki w liczbie mnogiej w rodzaju niemęskoosobowym"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['NOUN', 'PERSN']
             and str(token.morph.get('Number')) == "['Plur']"
             and (str(token.morph.get('Gender')) == "['Masc']"
             and str(token.morph.get('Animacy')) != "['Hum']"
                  or str(token.morph.get('Gender')) != "['Masc']")]
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_N_NS(Metric):
    category = Odmiana
    name_en = "Singular neutral nouns"
    name_local = "Rzeczowniki w liczbie pojedynczej w rodzaju nijakim"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['NOUN', 'PERSN']
        and str(token.morph.get('Gender'))=='[\'Neut\']'
        and str(token.morph.get('Number'))=='[\'Sing\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_PRO_1M(Metric):
    category = Odmiana
    name_en = "Pronouns in nominative case"
    name_local = "Zaimki w mianowniku"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Case'))=='[\'Nom\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_PRO_2D(Metric):
    category = Odmiana
    name_en = "Pronouns in genitive case"
    name_local = "Zaimki w dopełniaczu"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Case'))=='[\'Gen\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_PRO_3C(Metric):
    category = Odmiana
    name_en = "Pronouns in dative case"
    name_local = "Zaimki w celowniku"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Case'))=='[\'Dat\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_PRO_4B(Metric):
    category = Odmiana
    name_en = "Pronouns in accusative case"
    name_local = "Zaimki w bierniku"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Case'))=='[\'Acc\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_PRO_5N(Metric):
    category = Odmiana
    name_en = "Pronouns in instrumental case"
    name_local = "Zaimki w narzędniku"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Case'))=='[\'Ins\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_PRO_6Msc(Metric):
    category = Odmiana
    name_en = "Pronouns in locative case"
    name_local = "Zaimki w miejscowniku"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Case'))=='[\'Loc\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_PRO_7W(Metric):
    category = Odmiana
    name_en = "Pronouns in vocative case"
    name_local = "Zaimki w wołaczu"
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Case'))=='[\'Voc\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_PRO_1S(Metric):
    category = Odmiana
    name_en = "First person singular pronouns"
    name_local = "Zaimki w 1 os. l. poj."
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Number'))=='[\'Sing\']'
                and str(token.morph.get('Person'))=='[\'1\']']
        result = len(debug)
        return ratio(result, len(doc)), debug

class IN_PRO_2S(Metric):
    category = Odmiana
    name_en = "Second person singular pronouns"
    name_local = "Zaimki w 2 os. l. poj."
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Number'))=='[\'Sing\']'
                and str(token.morph.get('Person'))=='[\'2\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
	
class IN_PRO_3S(Metric):
    category = Odmiana
    name_en = "Third person singular pronouns"
    name_local = "Zaimki w 3 os. l. poj."
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Number'))=='[\'Sing\']'
                and str(token.morph.get('Person'))=='[\'3\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_PRO_1P(Metric):
    category = Odmiana
    name_en = "First person plural pronouns"
    name_local = "Zaimki w 1 os. l. mn."
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Number'))=='[\'Plur\']'
                and str(token.morph.get('Person'))=='[\'1\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
				
class IN_PRO_2P(Metric):
    category = Odmiana
    name_en = "Second person plural pronouns"
    name_local = "Zaimki w 2 os. l. mn."
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Number'))=='[\'Plur\']'
                and str(token.morph.get('Person'))=='[\'2\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_PRO_3P(Metric):
    category = Odmiana
    name_en = "Third person plural pronouns"
    name_local = "Zaimki w 3 os. l. mn."
   
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['PRON', 'DET', 'ADV'] 
                and token.morph.get('PronType') 
                and str(token.morph.get('Number'))=='[\'Plur\']'
                and str(token.morph.get('Person'))=='[\'3\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_1S(Metric):
    category = Odmiana
    name_en = "Verbs in 1 person singular"
    name_local = "Czasowniki w pierwszej osobie liczby pojedynczej"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'VERB'
        and str(token.morph.get('Number'))=='[\'Sing\']'
        and str(token.morph.get('Person'))=='[\'1\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_2S(Metric):
    category = Odmiana
    name_en = "Verbs in 2 person singular"
    name_local = "Czasowniki w drugiej osobie liczby pojedynczej"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['VERB', 'AUX']
        and str(token.morph.get('Number'))=='[\'Sing\']'
        and str(token.morph.get('Person'))=='[\'2\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_3S(Metric):
    category = Odmiana
    name_en = "Verbs in 3 person singular"
    name_local = "Czasowniki w trzeciej osobie liczby pojedynczej"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'VERB'
        and str(token.morph.get('Number'))=='[\'Sing\']'
        and str(token.morph.get('Person'))=='[\'3\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_1P(Metric):
    category = Odmiana
    name_en = "Verbs in 3 person plural"
    name_local = "Czasowniki w pierwszej osobie liczby mnogiej"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['VERB', 'AUX']
        and str(token.morph.get('Number'))=='[\'Plur\']'
        and str(token.morph.get('Person'))=='[\'1\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_2P(Metric):
    category = Odmiana
    name_en = "Verbs in 2 person plural"
    name_local = "Czasowniki w drugiej osobie liczby mnogiej"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['VERB', 'AUX']
        and str(token.morph.get('Number'))=='[\'Plur\']'
        and str(token.morph.get('Person'))=='[\'2\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_3P(Metric):
    category = Odmiana
    name_en = "Verbs in 3 person plural"
    name_local = "Czasowniki w trzeciej osobie liczby mnogiej"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['VERB', 'AUX']
        and str(token.morph.get('Number'))=='[\'Plur\']'
        and str(token.morph.get('Person'))=='[\'3\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
    
class IN_V_QUASI(Metric):
    category = Odmiana
    name_en = "Quasi-verbs"
    name_local = "Quasi-czasowniki"
   
    def count(doc):
        
        debug = [token.text for token in doc if str(token.morph.get('VerbType'))=='[\'Quasi\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
    
class IN_V_MOD(Metric):
    category = Odmiana
    name_en = "Modal verbs ('should')"
    name_local = "Czasowniki modalne ('winien/powinien')"
   
    def count(doc):
        
        debug = [token.text for token in doc if str(token.morph.get('VerbType'))=='[\'Mod\']']         
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_PACT(Metric):
    category = Odmiana
    name_en = "Active adjectival participles"
    name_local = "Imieslowy przymiotnikowe czynne"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'ADJ'
        and str(token.morph.get('VerbForm'))=='[\'Part\']'
        and str(token.morph.get('Voice'))=='[\'Act\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_PPAS(Metric):
    category = Odmiana
    name_en = "Passive adjectival participles"
    name_local = "Imieslowy przymiotnikowe bierne"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'ADJ'
        and str(token.morph.get('VerbForm'))=='[\'Part\']'
        and str(token.morph.get('Voice'))=='[\'Pass\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_PPAS_PERF(Metric):
    category = Odmiana
    name_en = "Passive adjectival participles in perfective aspect"
    name_local = "Imieslowy przymiotnikowe bierne w aspekcie dokonanym"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'ADJ'
        and str(token.morph.get('VerbForm'))=='[\'Part\']'
        and str(token.morph.get('Voice'))=='[\'Pass\']'
        and str(token.morph.get('Aspect'))=='[\'Perf\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_PPAS_IMPERF(Metric):
    category = Odmiana
    name_en = "Passive adjectival participles in imperfective aspect"
    name_local = "Imieslowy przymiotnikowe bierne w aspekcie niedokonanym"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'ADJ'
        and str(token.morph.get('VerbForm'))=='[\'Part\']'
        and str(token.morph.get('Voice'))=='[\'Pass\']'
        and str(token.morph.get('Aspect'))=='[\'Imp\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_PCON(Metric):
    category = Odmiana
    name_en = "Present adverbial participles"
    name_local = "Imieslowy przyslowkowe wspolczesne"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'VERB'
        and str(token.morph.get('VerbForm'))=='[\'Conv\']'
        and str(token.morph.get('Aspect'))=='[\'Imp\']'
        and str(token.morph.get('Tense'))=='[\'Pres\']'] 
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_PANT(Metric):
    category = Odmiana
    name_en = "Perfect adverbial participles"
    name_local = "Imieslowy przyslowkowe uprzednie"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'VERB'
        and str(token.morph.get('VerbForm'))=='[\'Conv\']'
        and str(token.morph.get('Aspect'))=='[\'Perf\']'
        and str(token.morph.get('Tense'))=='[\'Past\']']       
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_PERF(Metric):
    category = Odmiana
    name_en = "Verbs in perfect aspect"
    name_local = "Czasowniki w aspekcie dokonanym"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'VERB'
        and str(token.morph.get('VerbForm'))!='[\'Conv\']'
        and str(token.morph.get('Aspect'))=='[\'Perf\']']    
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_IMPERF(Metric):
    category = Odmiana
    name_en = "Verbs in imperfect aspect"
    name_local = "Czasowniki w aspekcie niedokonanym"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'VERB'
        and str(token.morph.get('VerbForm'))!='[\'Conv\']'
        and str(token.morph.get('Aspect'))=='[\'Imp\']']    
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_ACT(Metric):
    category = Odmiana
    name_en = "Verbs in active voice"
    name_local = "Czasowniki w stronie czynnej"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'VERB'
        and str(token.morph.get('Voice'))=='[\'Act\']'
        and str(token.morph.get('VerbForm'))!='[\'Inf\']'
        and str(token.morph.get('VerbForm'))!='[\'Conv\']']    
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_PASS(Metric):
    category = Odmiana
    name_en = "Verbs in passive voice"
    name_local = "Czasowniki w stronie biernej"

    def count(doc):
        nlp = IN_V_PASS.get_nlp()
        matcher = Matcher(nlp.vocab)
        adjs = [token for token in doc if token.pos_ == 'ADJ' and str(token.morph.get('VerbForm')) == '[\'Part\']']
        pattern = [{"POS": "AUX"}, {"OP": "?"}, { "TEXT": { "IN": [token.text for token in adjs]}}]
        matcher.add("verb_pass", [pattern])
        matches = matcher(doc)
        debug = {"FOUND": [(doc[start].text, doc[end - 1].text) for _, start, end in matches]}
        bi_gram_count = len(matches) * 2
        return ratio(bi_gram_count, len(doc)), debug
		
class IN_V_GER(Metric):
    category = Odmiana
    name_en = "Gerunds"
    name_local = "Rzeczowniki odczasownikowe"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'NOUN'
        and str(token.morph.get('VerbForm'))=='[\'Vnoun\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_PRES(Metric):
    category = Odmiana
    name_en = "Verbs in present tense"
    name_local = "Czasowniki w czasie teraźniejszym"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['VERB', 'AUX']
        and str(token.morph.get('Tense'))=='[\'Pres\']'
        and str(token.morph.get('VerbForm'))!='[\'Conv\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_PAST(Metric):
    category = Odmiana
    name_en = "Verbs in past tense"
    name_local = "Czasowniki w czasie przeszłym"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['VERB', 'AUX']
        and str(token.morph.get('Tense'))=='[\'Past\']'
        and str(token.morph.get('VerbForm'))!='[\'Conv\']'
        and str(token.morph.get('Mood'))!='[\'Cnd\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_FUTS(Metric):
    category = Odmiana
    name_en = "Verbs in simple future tense"
    name_local = "Czasowniki w czasie przyszłym prostym"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'VERB'
        and str(token.morph.get('Tense'))=='[\'Fut\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_FUTC(Metric):
    category = Odmiana
    name_en = "Verbs in combound future tense"
    name_local = "Czasowniki w czasie przyszłym złożonym"

    def count(doc):
        nlp = IN_V_FUTC.get_nlp()
        matcher = Matcher(nlp.vocab)
        auxs = [token for token in doc if token.pos_ == 'AUX'
                and str(token.morph.get('Tense')) == '[\'Fut\']'
                and token.lemma_ == 'być']
        verbs = [token for token in doc if token.pos_ == 'VERB'
                 and str(token.morph.get('Aspect')) == '[\'Imp\']'
                 and (str(token.morph.get('VerbForm')) == '[\'Inf\']'
                    or str(token.morph.get('VerbForm')) == '[\'Fin\']')]
        pattern = [{"TEXT": {"IN": [token.text for token in auxs]}}, {"OP": "?"}, {"TEXT": {"IN": [token.text for token in verbs]}}]
        matcher.add("verb_pass", [pattern])
        matches = matcher(doc)
        debug = {"FOUND": [(doc[start].text, doc[end - 1].text) for _, start, end in matches]}
        bi_gram_count = len(matches) * 2
        return ratio(bi_gram_count, len(doc)), debug
		
class IN_V_IMP(Metric):
    category = Odmiana
    name_en = "Verbs in imperative mood"
    name_local = "Czasowniki w trybie rozkazujacym"

    def count(doc):
        debug = [token.text for token in doc if 'impt' in token.tag_.split(":")
                 or (any(ch.dep_ == 'aux:imp' for ch in token.children)
                 and token.pos_ == 'VERB')]
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class IN_V_COND(Metric):
    category = Odmiana
    name_en = "Verbs in conditional mood"
    name_local = "Czasowniki w trybie przypuszczajacym"
    
    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ['VERB', 'AUX']
        and str(token.morph.get('Mood'))=='[\'Cnd\']']
        result = len(debug)
        return ratio(result, len(doc)), debug