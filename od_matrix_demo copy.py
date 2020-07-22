from pathlib2 import Path
import geopandas

Origins_folder = r'D:\Document\ArcMapDemo\data00_416after\temp\RentPrice_Jan'
OD_folder = r'D:\Document\ArcMapDemo\ODSHP'
output_folder = r'D:\Document\ArcMapDemo\MergeResult'
output_path = Path(output_folder)

for origin_filepath in Path(Origins_folder).glob('*.shp'):
    origin_filename = origin_filepath.stem

    origin_df = geopandas.read_file(str(origin_filepath))

    for matrix_filepath in Path(OD_folder).glob(f'{origin_filename}_*.shp'):
        matrix_filename = matrix_filepath.stem
        _, destination_filename = matrix_filename.split('_')

        # OriginID: 不能使用，内部维护，在Origins图层从1开始
        # Destinat_1: 目的地等级，1为最近的
        # matrix_df[['OriginID', 'Destinatio', 'Destinat_1', 'Total_长']]
        # Name: 源名称 - 目标名称
        matrix_df = geopandas.read_file(str(matrix_filepath))
        origin_id = [ int(name.split(' - ')[0]) for name in matrix_df['Name'].values]
        matrix_df.loc[:, 'OriginID'] = origin_id

        matrix_count_df = matrix_df[['OriginID']]
        matrix_count_df.loc[:, destination_filename + 'Num'] = 0
        matrix_count_df = matrix_count_df.groupby('OriginID').count()
        origin_df = origin_df.merge(matrix_count_df, 'left',
                                    left_on='ID', right_index=True)

        matrix_len_df = matrix_df[matrix_df['Destinat_1'] == 1][[
            'OriginID', 'Total_长']]
        matrix_len_df = matrix_len_df.rename(
            columns={'Total_长': destination_filename + 'Len'})
        matrix_len_df = matrix_len_df.set_index('OriginID')
        origin_df = origin_df.merge(
            matrix_len_df, 'left', left_on='ID', right_index=True)

        origin_df = origin_df.fillna(0)

    origin_df.to_file(str(output_path / origin_filepath.name))
