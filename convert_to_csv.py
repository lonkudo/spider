import pandas as pd
import sys
from pathlib import Path

# Get the .xlsx file path passed by PyCharm
xlsx_path = Path(sys.argv[1])
csv_path = xlsx_path.with_suffix('.csv')

# Load and convert
df = pd.read_excel(xlsx_path, engine='openpyxl')
df.to_csv(csv_path, index=False)

print(f"[✓] Converted {xlsx_path.name} → {csv_path.name}")
