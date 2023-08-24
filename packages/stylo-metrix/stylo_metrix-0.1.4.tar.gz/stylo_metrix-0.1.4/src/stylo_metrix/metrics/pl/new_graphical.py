import re

from ...structures import Metric, Category
from ...utils import ratio

class Grafika(Category):
    lang='pl'
    name_en='Graphical'
    name_local='Grafika'

class GR_UPPER(Metric):
    category = Grafika
    name_en = "Capital letters"
    name_local = "Kapitaliki"
   
    def count(doc):
        debug = [token.text for i, token in enumerate(doc) if (not token.is_sent_start or len(token.text) > 1) and token.text.isupper()]
        result = len(debug)
        return ratio(result, len(doc)), debug


class GR_EMOJI(Metric):
    category = Grafika
    name_en = "Emojis"
    name_local = "Emoji"

    def count(doc):
        debug = [token.text for token in doc if token._.is_emoji]
        result = len(debug)
        return ratio(result, len(doc)), debug


class GR_MENTION(Metric):
    category = Grafika
    name_en = "Mentions"
    name_local = "Wzmianki"

    def count(doc):
        debug = [token.text for token in doc if token.text.startswith('@')
        and len(token.text) > 1]
        result = len(debug)
        return ratio(result, len(doc)), debug
		

class GR_HASH(Metric):
    category = Grafika
    name_en = "Hashtags"
    name_local = "Hasztagi"

    def count(doc):
        matches = re.findall(r'(^#\w+)|\s(#\w+)', doc.text)
        debug = [match[0] or match[1] for match in matches if any(match)]
        result = len(debug)
        return ratio(result, len(doc)), debug


class GR_LINK(Metric):
    category = Grafika
    name_en = "Hyperlinks"
    name_local = "Hiperlinki"

    def count(doc):
        debug = re.findall("(?:http|ftp|https):\/\/(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:\/~+_#-]*[\w@?^=%&\/~+#-])", doc.text)
        result = len(debug)
        return ratio(result, len(doc)), debug