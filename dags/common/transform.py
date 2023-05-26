import pandas as pd

from dataclasses import dataclass


def alg_transform(data):
    trim_data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    filter_data = trim_data[trim_data['application_id'].notnull()]
    return filter_data.assign(has_specific_prefix=[True if x != 'shopify_' else False for x in filter_data['index_prefix']])

