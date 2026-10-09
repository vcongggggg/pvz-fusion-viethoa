#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate.py - Kiểm tra tính toàn vẹn và tiến độ của các bản dịch.
Dự án Việt Hóa Plants vs. Zombies Fusion v4.0.5.

Quy tắc kiểm tra:
1. Bảo toàn đầy đủ biến định dạng {0}, {1}, {0:F2},...
2. Bảo toàn các thẻ Unity Rich Text: <color=...>, </color>, <b>, </b>, <size=...>, </size>, <nobr>, </nobr>
3. Không chứa ký tự lỗi font hoặc biến mất chuỗi
4. Báo cáo tỷ lệ hoàn thành (%) của từng file trong data/translated/
"""

import os
import sys
import re
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
TRANS_DIR = ROOT_DIR / "data" / "translated"

def extract_placeholders(text):
    return sorted(re.findall(r'\{[0-9]+(?::[^}]+)?\}', text))

def extract_tags(text):
    return sorted(re.findall(r'<[/]?[a-zA-Z0-9#=_%]+>', text))

def validate_pair(raw, trans):
    errors = []

    # 1. Kiểm tra placeholder {0}, {1}...
    raw_phs = extract_placeholders(raw)
    trans_phs = extract_placeholders(trans)
    if raw_phs != trans_phs:
        errors.append(f"Lệch biến format: Gốc có {raw_phs} nhưng Dịch có {trans_phs}")

    # 2. Kiểm tra thẻ rich text
    raw_tags = extract_tags(raw)
    trans_tags = extract_tags(trans)
    if len(raw_tags) != len(trans_tags):
        errors.append(f"Lệch thẻ Rich Text: Gốc có {raw_tags} nhưng Dịch có {trans_tags}")

    # 3. Kiểm tra escape newline nếu gốc bắt đầu bằng \n
    if raw.startswith('\n') and not trans.startswith('\n'):
        errors.append("Thiếu ký tự xuống dòng '\\n' ở đầu câu giống bản gốc")
    if raw.endswith('\n') and not trans.endswith('\n'):
        errors.append("Thiếu ký tự xuống dòng '\\n' ở cuối câu giống bản gốc")

    return errors

def check_file(cat_name):
    raw_file = RAW_DIR / f"{cat_name}.json"
    trans_file = TRANS_DIR / f"{cat_name}.json"

    if not raw_file.exists():
        return

    with open(raw_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    trans_data = {}
    if trans_file.exists():
        with open(trans_file, 'r', encoding='utf-8') as f:
            trans_data = json.load(f)

    total = len(raw_data)
    translated_count = 0
    issues = []

    for raw_str in raw_data:
        val = trans_data.get(raw_str, "").strip()
        if val:
            translated_count += 1
            errs = validate_pair(raw_str, trans_data.get(raw_str, ""))
            if errs:
                issues.append((raw_str, trans_data.get(raw_str, ""), errs))

    pct = (translated_count / total * 100) if total > 0 else 0
    print(f"[{cat_name:16s}] Tiến độ: {translated_count:4d}/{total:4d} ({pct:6.2f}%) | Lỗi cú pháp: {len(issues)}")

    if issues:
        for raw_s, trans_s, err_list in issues[:3]:
            print(f"    ⚠ Gốc : {repr(raw_s)}")
            print(f"      Dịch: {repr(trans_s)}")
            for e in err_list:
                print(f"      -> {e}")
        if len(issues) > 3:
            print(f"      ... và {len(issues) - 3} lỗi khác.")

    return total, translated_count, len(issues)

def main():
    print("==================================================")
    print("   PVZ FUSION VIỆT HÓA - KIỂM TRA TIẾN ĐỘ & SYNTAX")
    print("==================================================")
    categories = ['ui', 'plants', 'zombies', 'buffs_synergies', 'dialogues', 'misc']

    total_all = 0
    trans_all = 0
    err_all = 0

    for cat in categories:
        res = check_file(cat)
        if res:
            t, tr, e = res
            total_all += t
            trans_all += tr
            err_all += e

    print("--------------------------------------------------")
    pct_all = (trans_all / total_all * 100) if total_all > 0 else 0
    print(f"[TỔNG CỘNG]       Tiến độ: {trans_all:4d}/{total_all:4d} ({pct_all:6.2f}%) | Tổng lỗi: {err_all}")
    print("==================================================")

if __name__ == '__main__':
    main()
