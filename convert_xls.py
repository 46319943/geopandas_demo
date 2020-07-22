import pandas as pd
from pathlib2 import Path

for filepath in Path(r'D:\Document\ArcMapDemo\data00_416after\POI').glob('**/*.xls'):
    pd.read_excel(filepath).to_excel(str(filepath) + 'x', index=False)
    print(filepath)