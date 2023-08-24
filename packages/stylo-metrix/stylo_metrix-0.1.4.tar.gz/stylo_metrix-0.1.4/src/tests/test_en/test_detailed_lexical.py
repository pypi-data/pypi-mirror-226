import unittest

from ...stylo_metrix.stylo_metrix import StyloMetrix
from ...stylo_metrix.structures.language import Lang
from ...stylo_metrix.tools.metric_tools import get_all_metrics, get_all_categories, custom_metric


class TestDetailedLexical(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        lang = 'en'
        cls.sm = StyloMetrix(lang, debug=True)

    def test_L_I_PRON(self):
        metric = 'L_I_PRON'
        test_text = 'Ala have kota.'
        expected_out = 0.99
        expected_debug = ['have', 'kota']

        out, debug = self.sm.transform([test_text])
        out = out[metric][0]
        debug = [token.text for token in debug[metric][0]['TOKENS']]

        self.assertEqual(expected_out, out)
        self.assertSequenceEqual(expected_debug, debug)
