import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TRANS_DIR = ROOT_DIR / "data" / "translated"
OUT_FILE = Path(r"C:\Mod\runtime_dict.json")

def main():
    merged = {}
    for p in sorted(TRANS_DIR.glob("*.json")):
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
            for k, v in d.items():
                if k and v and k != v:
                    merged[k] = v

    print(f"Total merged translations: {len(merged)}")
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"Saved runtime dictionary to {OUT_FILE}")

if __name__ == '__main__':
    main()
