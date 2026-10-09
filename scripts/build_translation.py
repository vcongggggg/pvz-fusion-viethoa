#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
build_translation.py - Hợp nhất toàn bộ các module dịch thành file Translation.txt (chuẩn XUnity.AutoTranslator).
Dự án Việt Hóa Plants vs. Zombies Fusion v4.0.5.

QUY TẮC BẮT BUỘC: Mỗi entry trong Translation.txt phải nằm trên ĐÚNG 1 DÒNG VĂN BẢN.
Mọi ký tự xuống dòng (\r, \n) và dấu gạch chéo (\) đều phải được escape cẩn thận.
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

def escape_entry(s):
    """
    Escape ký tự xuống dòng và dấu gạch chéo để đảm bảo 1 entry = đúng 1 dòng trong Translation.txt.
    """
    if not s:
        return ""
    # Chuyển đổi escape: \ -> \\, \r -> \r, \n -> \n
    return s.replace('\\', '\\\\').replace('\r', '\\r').replace('\n', '\\n')

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
                    merged_translations[raw] = trans

    print(f"[+] Tổng hợp được {len(merged_translations)} chuỗi đã dịch.")

    line_count = 0
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# ========================================================\n")
        f.write("# BẢN DỊCH VIỆT HÓA PLANTS VS. ZOMBIES FUSION (v4.0.5)\n")
        f.write("# Dự án cộng tác mã nguồn mở giữa các AI Agents\n")
        f.write(f"# Tổng số chuỗi đã dịch: {len(merged_translations)}\n")
        f.write("# ========================================================\n\n")

        for raw, trans in merged_translations.items():
            # XUnity.AutoTranslator format: Original=Translated
            # Thoát ký tự \r, \n để không vỡ dòng, thoát dấu = trong key
            safe_raw = escape_entry(raw).replace("=", "\\=")
            safe_trans = escape_entry(trans)
            f.write(f"{safe_raw}={safe_trans}\n")
            line_count += 1

    print(f"[✓] Đã ghi file dịch hoàn chỉnh vào: {out_file} (Mỗi entry đúng 1 dòng)")

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
