import unittest

from alerte_blanche import normalize_plate_number


class NormalizeLicensePlateTest(unittest.TestCase):

    def test_with_spaces(self):
        self.assertEqual('ABC123', normalize_plate_number('ABC 123'))

    def test_with_hyphens(self):
        self.assertEqual('ABC123', normalize_plate_number('ABC-_-123'))

    def test_case_sensitivity(self):
        self.assertEqual(normalize_plate_number('abc123'),
                         normalize_plate_number('ABC123'))
