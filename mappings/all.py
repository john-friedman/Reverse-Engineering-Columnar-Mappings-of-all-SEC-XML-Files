import json
from pathlib import Path

_DIR = Path(__file__).parent

SCHEDULE_13D = json.loads((_DIR / "SCHEDULE_13D.json").read_text())
QUALIF       = json.loads((_DIR / "QUALIF.json").read_text())

SEC_DOCUMENTS_MAPPING = {
    "SCHEDULE 13D":   SCHEDULE_13D,
    "SCHEDULE 13D/A": SCHEDULE_13D,
    "QUALIF":         QUALIF,
}