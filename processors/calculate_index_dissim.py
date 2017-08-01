import os
import sys
import json
import pandas as pd

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'
)
RENAME_COLS = {
    'total': 'total_pop',
    'not_hl_white': 'white_pop',
    'black': 'black_pop',
    'asian': 'asian_pop',
    'hl': 'hispanic_pop'
}
CENSUS_YEARS = ['2000', '2010', '2015']

with open(os.path.join(DATA_PATH, 'chi_comm_areas.geojson')) as geo_f:
    comm_json = json.load(geo_f)

COMM_NAMES = [f['properties']['community'] for f in comm_json['features']]


# Calculating component of formula inside of set
def index_dissim(row, comm_dict, group_1, group_2):
    return abs((row[group_1] / comm_dict[group_1]) - (row[group_2] / comm_dict[group_2]))


def comm_dissim(census_year):
    comm_df = pd.read_csv(os.path.join(DATA_PATH, census_year, 'comm_bg_race.csv'))
    comm_df.rename(columns=RENAME_COLS, inplace=True)

    comm_dissim_dicts = []
    for c in COMM_NAMES:
        comm_dict = {'name': c}
        comm_dict['white_pop'] = comm_df.loc[comm_df[c] == True, 'white_pop'].sum()
        comm_dict['black_pop'] = comm_df.loc[comm_df[c] == True, 'black_pop'].sum()
        comm_dict['asian_pop'] = comm_df.loc[comm_df[c] == True, 'asian_pop'].sum()
        comm_dict['hispanic_pop'] = comm_df.loc[comm_df[c] == True, 'hispanic_pop'].sum()

        comm_dict['asian_black_index'] = (comm_df.loc[comm_df[c] == True].apply(
                lambda row: index_dissim(row, comm_dict, 'asian_pop', 'black_pop'), axis=1
            ).sum() / 2) * 100
        comm_dict['asian_hispanic_index'] = (comm_df.loc[comm_df[c] == True].apply(
                lambda row: index_dissim(row, comm_dict, 'asian_pop', 'hispanic_pop'), axis=1
            ).sum() / 2) * 100
        comm_dict['asian_white_index'] = (comm_df.loc[comm_df[c] == True].apply(
                lambda row: index_dissim(row, comm_dict, 'asian_pop', 'white_pop'), axis=1
            ).sum() / 2) * 100
        comm_dict['black_hispanic_index'] = (comm_df.loc[comm_df[c] == True].apply(
                lambda row: index_dissim(row, comm_dict, 'black_pop', 'hispanic_pop'), axis=1
            ).sum() / 2) * 100
        comm_dict['black_white_index'] = (comm_df.loc[comm_df[c] == True].apply(
                lambda row: index_dissim(row, comm_dict, 'black_pop', 'white_pop'), axis=1
            ).sum() / 2) * 100
        comm_dict['hispanic_white_index'] = (comm_df.loc[comm_df[c] == True].apply(
                lambda row: index_dissim(row, comm_dict, 'hispanic_pop', 'white_pop'), axis=1
            ).sum() / 2) * 100
        comm_dissim_dicts.append(comm_dict)

    comm_dissim_df = pd.DataFrame(comm_dissim_dicts)
    comm_dissim_df.to_csv(
        os.path.join(DATA_PATH, census_year, 'comm_dissim.csv'), index=False
    )


if __name__ == '__main__':
    comm_dissim(sys.argv[1])
