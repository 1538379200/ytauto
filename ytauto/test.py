from pathlib import Path
import json


log_dir = Path(__file__).resolve().parent / "log"

log = log_dir / "2024-06-28T16-44-58.log"

with log.open("r", encoding="utf8") as f:
    log_bytes = f.readlines()
    j_str = json.dumps(log_bytes)
    print(json.loads(j_str))


