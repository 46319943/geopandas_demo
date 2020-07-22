from pathlib2 import Path
import traceback
# shp文件使用geopandas
import geopandas
# 生成的OD文件，只读dbf
from simpledbf import Dbf5

'''
geopandas创建的geodataframe占用内存过大
因此，对于OD矩阵的shp文件，不应用它读取。
而是直接读取dbf文件，创建dataframe
'''

Origins_folder = r'D:\Document\ArcMapDemo\AllData\RentPrice_Jan'
OD_folder = r'D:\Document\ArcMapDemo\ODSHP'
output_folder = r'D:\Document\ArcMapDemo\MergeResult'
output_path = Path(output_folder)

# 首先获得生成OD矩阵的文件夹中的所有Origin房租城市
origin_filename_list = []
for matrix_filepath in Path(OD_folder).glob(f'*_*.shp'):
    matrix_filename = matrix_filepath.stem
    origin_filename, destination_filename = matrix_filename.split('_')
    origin_filename_list.append(origin_filename)
origin_filename_list = list(set(origin_filename_list))

for origin_filename in origin_filename_list:
    origin_filepath = Path(Origins_folder) / (origin_filename + '.shp')
    output_filepath = output_path / origin_filepath.name

    # 如果输出文件存在，则打开已经输出的文件进行追加。否则打开源房租SHP文件
    if output_filepath.exists():
        origin_df = geopandas.read_file(str(output_filepath))
    else:
        origin_df = geopandas.read_file(str(origin_filepath))

    # 不存在元素则跳过
    if origin_df.shape[0] == 0:
        continue

    for matrix_filepath in Path(OD_folder).glob(f'{origin_filename}_*.shp'):
        matrix_filename = matrix_filepath.stem
        _, destination_filename = matrix_filename.split('_')

        # OriginID: 不能使用，内部维护，在Origins图层从1开始
        # Destinat_1: 目的地等级，1为最近的
        # matrix_df[['OriginID', 'Destinatio', 'Destinat_1', 'Total_长']]
        # Name: 源名称 - 目标名称

        # matrix_df = geopandas.read_file(str(matrix_filepath))
        # 不读取shp，读取dbf
        matrix_dbf = Dbf5(str(matrix_filepath).replace('.shp', '.dbf'))
        matrix_df = matrix_dbf.to_dataframe()

        # 判断dataframe的元素个数，为0则不进行处理
        if matrix_df.shape[0] == 0:
            continue

        # 根据源名称，重新生成有效的OriginID
        origin_id = [int(name.split(' - ')[0])
                     for name in matrix_df['Name'].values]
        matrix_df.loc[:, 'OriginID'] = origin_id

        # POI计数。先删除重复列
        if (destination_filename + 'Num') in origin_df.columns:
            origin_df = origin_df.drop(columns=destination_filename + 'Num')

        matrix_count_df = matrix_df[['OriginID']]
        try:
            matrix_count_df.loc[:, destination_filename + 'Num'] = 0
        except:
            traceback.print_exc()
            print(matrix_filepath)

        matrix_count_df = matrix_count_df.groupby('OriginID').count()
        origin_df = origin_df.merge(matrix_count_df, 'left',
                                    left_on='ID', right_index=True)

        # POI最短距离。先删除重复列
        if (destination_filename + 'Len') in origin_df.columns:
            origin_df = origin_df.drop(columns=destination_filename + 'Len')

        matrix_len_df = matrix_df[matrix_df['Destinat_1'] == 1][[
            'OriginID', 'Total_长']]
        matrix_len_df = matrix_len_df.rename(
            columns={'Total_长': destination_filename + 'Len'})
        matrix_len_df = matrix_len_df.set_index('OriginID')
        origin_df = origin_df.merge(
            matrix_len_df, 'left', left_on='ID', right_index=True)

        origin_df = origin_df.fillna(0)

    origin_df.to_file(
        str(output_filepath), encoding='utf-8')


def clear_dir(dir_path_str):
    for file_path in Path(dir_path_str).glob('*_*.*'):
        file_path.unlink()


def test():
    for matrix_filepath in Path(OD_folder).glob(f'*_*.shp'):
        matrix_filename = matrix_filepath.stem
        origin_filename, destination_filename = matrix_filename.split('_')

        origin_filepath = Path(Origins_folder) / (origin_filename + '.shp')

        origin_df = geopandas.read_file(str(origin_filepath))
        matrix_df = geopandas.read_file(str(matrix_filepath))

        # OriginID: 不能使用，内部维护，在Origins图层从1开始
        # Destinat_1: 目的地等级，1为最近的
        # matrix_df[['OriginID', 'Destinatio', 'Destinat_1', 'Total_长']]
        # Name: 源名称 - 目标名称
        origin_id = [int(name.split(' - ')[0])
                     for name in matrix_df['Name'].values]
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
