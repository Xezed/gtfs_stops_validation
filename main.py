import pandas as pd
import re
import utm
import sys

from simpledbf import Dbf5
from mmqgis import mmqgis_library as ml


def main():
    input_file = sys.argv[1]

    if input_file.endswith('xlsx'):
        for_id = re.findall(r'_([A-Z])\.xlsx', input_file)[0]

        def id_lon_lat(row):
            new_id = for_id + '--' + unicode(int(row[0]))
            lat, lon = utm.to_latlon(row[1], row[2], 18, 'N')
            return new_id, lat, lon

        df = pd.read_excel(input_file, parse_cols='F,H,I', names=['stop_id', 'stop_lat', 'stop_lon'])
        df = df.drop_duplicates(subset='stop_id')
        df = df.apply(id_lon_lat, axis=1)
        df = pd.DataFrame(df.tolist(), columns=['stop_id', 'stop_lat', 'stop_lon'], index=df.index)

        df = df.to_csv(index=False)

    else:
        df = pd.read_csv(input_file)

    # dbf = Dbf5('Cenefas.dbf')
    # dbf = dbf.to_dataframe()

    geo = ml.mmqgis_geometry_import_from_csv('adsf', 'output.txt', 'stop_lat', 'stop_lon',
                                            'stop_id', 'Point','output.shp', False)
    print geo


if __name__ == '__main__':
    main()