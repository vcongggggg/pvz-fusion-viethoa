#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_translation.py - Hợp nhất toàn bộ các module dịch thành file Translation.txt (chuẩn XUnity.AutoTranslator).
Dự án Việt Hóa Plants vs. Zombies Fusion v4.0.5.
"""

import os
import sys
import json
import argparse
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
TRANS_DIR = ROOT_DIR / "data" / "translated"
OUTPUT_DIR = ROOT_DIR / "data" / "output"
DEFAULT_GAME_PATH = Path(r"c:\Mod\PvZ_Fusion")

def escape_translation_line(s):
    # Chuẩn hóa để tránh lỗi xuống dòng vỡ cấu trúc file từ điển
    return s.replace("\r\n", "\\r\\n").replace("\n", "\\n")

def build(sync_game=False, game_dir=DEFAULT_GAME_PATH):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / "Translation.txt"

    categories = ['ui', 'plants', 'zombies', 'buffs_synergies', 'dialogues', 'misc']
    merged_translations = {}

    for cat in categories:
        cat_file = TRANS_DIR / f"{cat}.json"
        if not cat_file.exists():
            continue
        with open(cat_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for raw, trans in data.items():
                if trans and trans.strip():
                    merged_translations[raw] = trans.strip()

    print(f"[+] Tổng hợp được {len(merged_translations)} chuỗi đã dịch.")

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# ========================================================\n")
        f.write("# BẢN DỊCH VIỆT HÓA PLANTS VS. ZOMBIES FUSION (v4.0.5)\n")
        f.write("# Dự án cộng tác mã nguồn mở giữa các AI Agents\n")
        f.write(f"# Tổng số chuỗi đã dịch: {len(merged_translations)}\n")
        f.write("# ========================================================\n\n")

        for raw, trans in merged_translations.items():
            # XUnity.AutoTranslator format: Original=Translated
            # Thoát ký tự = nếu nằm trong key
            safe_raw = raw.replace("=", "\\=")
            f.write(f"{safe_raw}={trans}\n")

    print(f"[✓] Đã ghi file dịch hoàn chỉnh vào: {out_file}")

    if sync_game:
        # Đường dẫn XUnity.AutoTranslator trong game
        target_dir = game_dir / "BepInEx" / "Translation" / "vi" / "Text"
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / "Translation.txt"
        with open(target_file, 'w', encoding='utf-8') as f:
            with open(out_file, 'r', encoding='utf-8') as src:
                f.write(src.read())
        print(f"[✓] Đã đồng bộ trực tiếp vào thư mục game: {target_file}")

def main():
    parser = argparse.ArgumentParser(description="Build file Translation.txt cho PvZ Fusion")
    parser.add_argument("--sync", action="store_true", help="Đồng bộ ngay vào thư mục game c:\\Mod\\PvZ_Fusion")
    parser.add_argument("--game-dir", default=str(DEFAULT_GAME_PATH), help="Đường dẫn thư mục game")
    args = parser.parse_args()

    build(sync_game=args.sync, game_dir=Path(args.game_dir))

if __name__ == '__main__':
    main()
