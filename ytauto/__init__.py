import sys
from pathlib import Path
project = Path(__file__).resolve().parent
sys.path.append(str(project))
print(sys.path)
