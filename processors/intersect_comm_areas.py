import os
import sys
import pandas as pd
import geopandas as gpd

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'
)
ID_PROP_MAP = {
    '2015': 'GEOID',
    '2010': 'GEOID10',
    '2000': 'BKGPIDFP00'
}

comm_df = gpd.read_file(os.path.join(DATA_PATH, 'chi_comm_areas.geojson'))
comm_dicts = comm_df.to_dict(orient='records')
comm_names = [c['community'] for c in comm_dicts]


def intersect_comm(filename, id_prop='GEOID'):
    bg_df = gpd.read_file(filename)
    for d in comm_dicts:
        bg_df[d['community']] = bg_df.geometry.intersects(d['geometry'])
    output_filename = os.path.join(os.path.dirname(filename), 'bg_comm.csv')
    bg_clean_df = bg_df[[id_prop] + comm_names].copy()
    bg_clean_df.columns = [['geoid'] + comm_names]
    bg_clean_df.to_csv(output_filename, index=False)


if __name__ == '__main__':
    intersect_comm(
        os.path.join(DATA_PATH, sys.argv[1], 'block_groups.geojson'),
        id_prop=ID_PROP_MAP.get(sys.argv[1])
    )
