# import geopandas
# import sys

# geodf = geopandas.read_file(
#     r'D:\Document\ArcMapDemo\MergeResult\Chengdu.dbf', encoding="gbk")
# print(geodf)

import pandas as pd
from simpledbf import Dbf5
dbf = Dbf5(r'D:\Document\ArcMapDemo\MergeResult\Chengdu.dbf')
df = dbf.to_dataframe()
print(df)