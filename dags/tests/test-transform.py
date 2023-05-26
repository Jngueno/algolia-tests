import unittest

import pandas as pd

from common.transform import alg_transform

class AlgoliaTransformTestCase(unittest.TestCase):

    def test_transform(self):
        df = pd.DataFrame({'application_id': ['HQRLIXFEYY', '9A685N5PXO', '', None], 'index_prefix': [' shopify_', 'shopify_test ', 'shopify_alg', 'shopify_']})
        res_expected = pd.DataFrame({'application_id': ['HQRLIXFEYY', '9A685N5PXO'], 'index_prefix': [' shopify_', 'shopify_test '], 'has_specific_prefix': [False, True]})

        self.assertEqual(alg_transform(df), res_expected, f'Should be ${res_expected}')

