"""Check that essential repository assets and metadata exist (no TF required)."""
import json
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
needed = ["requirements.txt", "interface/app_ui.py", "interface/inference.py", "models/smart_drug_model.keras", "results/confusion_matrix/evaluation_summary.json"]
for rel in needed:
    path = root / rel
    if not path.is_file():
        raise SystemExit(f"MISSING: {rel}")
    print(f"OK: {rel}")
model_path = root / "models/smart_drug_model.keras"
with zipfile.ZipFile(model_path) as model_zip:
    if not any(name.endswith("config.json") for name in model_zip.namelist()):
        raise SystemExit("Keras archive missing config.json")
record = json.loads((root / "results/confusion_matrix/evaluation_summary.json").read_text(encoding="utf-8"))
if record["class_names"] != ["counterfeit", "original"]:
    raise SystemExit("Recorded label order differs from inference mapping")
print("OK: Keras archive format and saved label order")
print("NOTE: Does not execute TensorFlow or verify prediction accuracy.")
