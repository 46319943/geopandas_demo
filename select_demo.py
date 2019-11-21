from pathlib2 import Path
import geopandas

# 存放所有城市的目录
source_dir = Path(r'D:\Document\HousePricing\数据展点——合并\裁切')
# 获取所有目录名字
city_dir_list = [x for x in source_dir.iterdir() if x.is_dir()]
# 输出目录
output_dir = Path(r'D:\Document\HousePricing\公司')
output_dir.mkdir(parents=True,exist_ok=True)

for city_dir in city_dir_list:    
    geodf = geopandas.read_file(str(city_dir/'公司.shp'),encoding="gbk")
    selection = geodf.loc[lambda df : df['二类'] == '公司企业;公司']
    print(city_dir.name,selection.head(),selection.shape)
    output_file = output_dir/city_dir.name/'公司.shp'
    output_file.parent.mkdir(parents=True,exist_ok=True)
    selection.to_file(str(output_file),encoding="UTF-8")

