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

from ...utils import incidence
from pathlib import Path
import pandas as pd
import os

ANIM = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data\\hurtlex\\animals.txt'), sep="\t", header=None, encoding='utf-8')
DDP_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/hurtlex/cognitive_disabilities.txt'), sep="\t", header=None, encoding='utf-8')
SVP_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/hurtlex/deadly_sins.txt'), sep="\t", header=None, encoding='utf-8')
CDS_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/derogatory_words.txt"), sep="\t", header=None, encoding='utf-8')
DDF_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/disabilities.txt"), sep="\t", header=None, encoding='utf-8')
IS_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/economic_disadvantage.txt"), sep="\t", header=None, encoding='utf-8')
PS_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/ethnic_slurs.txt"), sep="\t", header=None, encoding='utf-8')
RE_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/felonies.txt"), sep="\t", header=None, encoding='utf-8')
ASF_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/female_genetalia.txt"), sep="\t", header=None, encoding='utf-8')
ASM_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/male_genetalia.txt"), sep="\t", header=None, encoding='utf-8')
OM_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/homosexuality.txt"), sep="\t", header=None, encoding='utf-8')
RCI_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/locations.txt"), sep="\t", header=None, encoding='utf-8')
DMC_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/moral.txt"), sep="\t", header=None, encoding='utf-8')
OR_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/plants.txt"), sep="\t", header=None, encoding='utf-8')
QAS_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/potential.txt"), sep="\t", header=None, encoding='utf-8')
PA_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/professions.txt"), sep="\t", header=None, encoding='utf-8')
PR_ = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/hurtlex/prostitution.txt"), sep="\t", header=None, encoding='utf-8')

class Hurtlex(Category):
    """
    Lexical metric based on Hurtlex: https://github.com/valeriobasile/hurtlex
    Each class is a category of profanity words. 
    """
    lang = 'en'
    name_en = "Hurtlex"

class AN(Metric):
    category = Hurtlex
    name_en = "Animals"

    def count(doc):
        words = ANIM.iloc[0].values.tolist()
        search = [token.text for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}
        

class DDP(Metric):
    category = Hurtlex
    name_en = "cognitive disabilities and diversity"

    def count(doc):
        words = DDP_.iloc[0].values.tolist()
        search = [token.text for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}


class SVP(Metric):
    category = Hurtlex
    name_en = "words related to the seven deadly sins of the Christian tradition"

    def count(doc):
        words = SVP_.iloc[0].values.tolist()
        search = [token.text for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}


class CDS(Metric):
    category = Hurtlex
    name_en = "derogatory words"

    def count(doc):
        words = CDS_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}


class DDF(Metric):
    category = Hurtlex
    name_en = "physical disabilities and diversity"

    def count(doc):
        
        words = DDF_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}
        
class IS(Metric):
    category = Hurtlex
    name_en = "words related to social and economic disadvantage"

    def count(doc):
        words = IS_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}


class PS(Metric):
    category = Hurtlex
    name_en = "negative stereotypes ethnic slurs"

    def count(doc):
        words = PS_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}


class RE(Metric):
    category = Hurtlex
    name_en = "felonies and words related to crime and immoral behavior"

    def count(doc):
        words = RE_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}
        

class ASF(Metric):
    category = Hurtlex
    name_en = "female genitalia"

    def count(doc):
        words = ASF_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}


class ASM(Metric):
    category = Hurtlex
    name_en = "male genitalia"

    def count(doc):
        words = ASM_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}
        

class OM(Metric):
    category = Hurtlex
    name_en = "words related to homosexuality"

    def count(doc):
        words = OM_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}

class RCI(Metric):
    category = Hurtlex
    name_en = "locations and demonyms"

    def count(doc):
        words = RCI_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}
        

class DMC(Metric):
    category = Hurtlex
    name_en = "moral and behavioral defects"

    def count(doc):
        words = DMC_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}


class OR(Metric):
    category = Hurtlex
    name_en = "plants"

    def count(doc):
        words = OR_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}


class QAS(Metric):
    category = Hurtlex
    name_en = "with potential negative connotations"

    def count(doc):
        words = QAS_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}
        

class PA(Metric):
    category = Hurtlex
    name_en = "professions and occupations"

    def count(doc):
        words = PA_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}
        

class PR(Metric):
    category = Hurtlex
    name_en = "words related to prostitution"

    def count(doc):
        words = PR_.iloc[0].values.tolist()
        search = [token for token in doc if token.lemma_ in words]
        result = incidence(doc, search)
        return result, {}


