import os
import sys
import pandas as pd

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'
)
CENSUS_DIRS = ['2000', '2010', '2015']


def join_census_data(census_year):
    bg_df = pd.read_csv(os.path.join(DATA_PATH, census_year, 'bg_comm.csv'))
    race_df = pd.read_csv(os.path.join(DATA_PATH, census_year, 'census_race.csv'))
    merge_df = race_df.merge(bg_df, on='geoid', how='left')
    merge_df.to_csv(os.path.join(DATA_PATH, census_year, 'comm_bg_race.csv'), index=False)


if __name__ == '__main__':
    join_census_data(sys.argv[1])
