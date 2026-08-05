import unittest

from server import normalize_symbol


class ServerSymbolTests(unittest.TestCase):
    def test_normalize_symbol_handles_known_company_names(self):
        self.assertEqual(normalize_symbol('KPR Mill Ltd'), 'KPRMILL.NS')
        self.assertEqual(normalize_symbol('Apple Inc'), 'AAPL')
        self.assertEqual(normalize_symbol('Tesla'), 'TSLA')

    def test_normalize_symbol_keeps_valid_tickers(self):
        self.assertEqual(normalize_symbol('AAPL'), 'AAPL')
        self.assertEqual(normalize_symbol('kprmill.ns'), 'KPRMILL.NS')


if __name__ == '__main__':
    unittest.main()
