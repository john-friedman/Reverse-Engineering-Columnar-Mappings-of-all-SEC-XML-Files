import json
from pathlib import Path

_DIR = Path(__file__).parent


def _load(filename: str):
    return json.loads((_DIR / filename).read_text())


SEC_DOCUMENTS_MAPPING = {
    "INFORMATION TABLE": _load("information_table.json"),
    "QUALIF" : _load("qualif.json"),
    "EFFECT" : _load("effect.json"),
    "25-NSE" : _load("25nse.json"),
    "25-NSE/A" : _load("25nse.json"),
    "C-TR" : _load("ctr.json"), # lot more Cs actually
    "C-TR-W" : _load("ctr.json"),
    "X-17A-5" : _load("x17a5.json"),
    "X-17A-5/A" : _load("x17a5.json")
}
