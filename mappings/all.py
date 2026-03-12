import json
from pathlib import Path

_DIR = Path(__file__).parent


def _load(filename: str):
    return json.loads((_DIR / filename).read_text())


SEC_DOCUMENTS_MAPPING = {
    "INFORMATION TABLE": _load("informationtable.json"),
    "QUALIF" : _load("qualif.json"),
    "EFFECT" : _load("effect.json"),
    "25-NSE" : _load("25nse.json"),
    "25-NSE/A" : _load("25nse.json"),
    "C-TR" : _load("ctr.json"), # lot more Cs actually
    "C-TR-W" : _load("ctr.json"),
    "X-17A-5" : _load("x17a5.json"),
    "X-17A-5/A" : _load("x17a5.json"),
    "1-K" : _load("1k.json"),
    "1-K/A" : _load("1k.json"),
    "D" :  _load("d.json"),
    "D/A" :  _load("d.json"),
    "N-PX" :  _load("npx.json"),
    "N-PX/A" :  _load("npx.json"),
    "144" :  _load("144.json"),
    "144/A" :  _load("144.json"),
    "SCHEDULE 13D" :  _load("schedule13d.json"),
    "SCHEDULE 13D/A" :  _load("schedule13d.json"),
    "1-Z" :  _load("1z.json"),
    "1-Z/A" :  _load("1z.json"),
    "1-A" :  _load("1a.json"),
    "1-A POS" :  _load("1a.json"),
    "DOS":   _load("dos.json"),
"DOS/A": _load("dos.json"),
"13F-HR" : _load("13fhr.json"),
"13F-HR/A" : _load("13fhr.json"),
}
