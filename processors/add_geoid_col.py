import os
import numpy as np
import pandas as pd
import shapely

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'
)
CENSUS_DIRS = ['2000', '2010', '2015']
GEOID_COLS = ['state', 'county', 'tract', 'block_group']


def add_geoid_col(csv_filename):
    race_df = pd.read_csv(csv_filename, dtype={
        'state': 'object',
        'county': 'object',
        'tract': 'object',
        'block_group': 'object'
    })
    if 'geoid' not in race_df.columns.values.tolist():
        race_df['geoid'] = race_df[GEOID_COLS].apply(lambda x: ''.join(x), axis=1)
    race_df.to_csv(csv_filename, index=False)


if __name__ == '__main__':
    for d in CENSUS_DIRS:
        add_geoid_col(os.path.join(DATA_PATH, d, 'census_race.csv'))
