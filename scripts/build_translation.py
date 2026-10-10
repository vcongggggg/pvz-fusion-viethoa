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
import re

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

        regex_rules = []

        for raw, trans in merged_translations.items():
            # XUnity.AutoTranslator format: Original=Translated
            # Nếu key chứa dấu '=' (như các thẻ rich text <color=red>), AutoTranslator sẽ parse sai
            # -> Chuyển sang dạng regex rule r:"^pattern$"="replacement"
            if "=" in raw:
                # Escape cho regex
                safe_r = re.escape(raw).replace("\\\n", "\\n").replace("\\\r", "")
                safe_t = trans.replace('"', '\\"').replace("\r", "").replace("\n", "\\n")
                regex_rules.append(f'r:"^{safe_r}$"="{safe_t}"')
            else:
                safe_raw = escape_entry(raw)
                safe_trans = escape_entry(trans)
                f.write(f"{safe_raw}={safe_trans}\n")
                line_count += 1

        # Task 3: Regex Suffix Rules (xử lý Tên(số) và các pattern số liệu)
        f.write("\n# ========================================================\n")
        f.write("# REGEX RULES (Xử lý suffix (số) và pattern số liệu)\n")
        f.write("# ========================================================\n\n")

        # STAT & HUD LABELS REGEX
        from generate_stat_regex import generate_stat_regex_rules
        stat_rules = generate_stat_regex_rules()
        regex_rules.extend(stat_rules)

        seen_regex = set()
        for cat in ['plants', 'zombies', 'buffs_synergies', 'ui', 'misc']:
            cat_file = TRANS_DIR / f"{cat}.json"
            if not cat_file.exists():
                continue
            with open(cat_file, 'r', encoding='utf-8') as cf:
                cdata = json.load(cf)
                for raw_name, trans_name in cdata.items():
                    if not raw_name or not trans_name or raw_name in seen_regex:
                        continue
                    seen_regex.add(raw_name)
                    if ('\n' not in raw_name and '<' not in raw_name and 
                        '{' not in raw_name and '}' not in raw_name and 
                        '+' not in raw_name and '*' not in raw_name and '?' not in raw_name and
                        ':' not in raw_name and '：' not in raw_name and
                        len(raw_name) <= 25 and not raw_name.startswith('r:')):
                        safe_r = re.escape(raw_name)
                        safe_t = trans_name.replace('"', '\\"')
                        regex_rules.append(f'r:"^{safe_r}\\((\\d+)\\)$"="{safe_t}($1)"')
                        regex_rules.append(f'r:"^{safe_r}（(\\d+)）$"="{safe_t}($1)"')

        for r_rule in regex_rules:
            f.write(f"{r_rule}\n")
            line_count += 1

        print(f"[✓] Đã tạo và ghi {len(regex_rules)} regex rules.")

    print(f"[✓] Đã ghi file dịch hoàn chỉnh vào: {out_file} (Mỗi entry đúng 1 dòng)")

    if sync_game:
        # Đường dẫn XUnity.AutoTranslator thực tế trong game (MelonLoader)
        target_dirs = [
            game_dir / "Translation" / "vi" / "Text",
            game_dir / "AutoTranslator" / "Translation" / "vi" / "Text",
            game_dir / "UserData" / "AutoTranslator" / "Translation" / "vi" / "Text",
        ]
        for t_dir in target_dirs:
            t_dir.mkdir(parents=True, exist_ok=True)
            target_file = t_dir / "Translation.txt"
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
