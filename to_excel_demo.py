from pathlib2 import Path
import geopandas

# 存放所有城市的目录
source_dir = Path(r'D:\Document\HousePricing\公司')
# 获取所有目录名字
city_dir_list = [x for x in source_dir.iterdir() if x.is_dir()]
# 输出目录
output_dir = Path(r'D:\Document\HousePricing\公司')

for city_dir in city_dir_list:
    if (city_dir/'公司.shp').exists():
        geodf = geopandas.read_file(str(city_dir/'公司.shp'),encoding="UTF-8")
        print(geodf.head())
        geodf.iloc[:, 0:-1].to_excel(str(city_dir/'公司.xlsx'),index=False)
