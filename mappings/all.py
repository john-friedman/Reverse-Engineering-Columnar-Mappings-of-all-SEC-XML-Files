import json
from pathlib import Path

_DIR = Path(__file__).parent

SCHEDULE_13D = json.loads((_DIR / "schedule_13d.json").read_text())
QUALIF       = json.loads((_DIR / "qualif.json").read_text())
EFFECT       = json.loads((_DIR / "effect.json").read_text())
THIRTEENF_HR = json.loads((_DIR / "13fhr.json").read_text())
THIRTEENF_HR_A = json.loads((_DIR / "13fhr_a.json").read_text())
FORM_D       = json.loads((_DIR / "form_d.json").read_text())
FORM_144 = json.loads((_DIR / "form_144.json").read_text())


SEC_DOCUMENTS_MAPPING = {
    "SCHEDULE 13D":   SCHEDULE_13D,
    "SCHEDULE 13D/A": SCHEDULE_13D,
    "QUALIF":         QUALIF,
    "EFFECT":         EFFECT,
    "13F-HR":         THIRTEENF_HR,
    "13F-HR/A":       THIRTEENF_HR_A,
    "D":              FORM_D,
    "D/A":            FORM_D,
    "144":   FORM_144,
    "144/A": FORM_144,
}