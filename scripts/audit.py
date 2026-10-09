#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit.py - Công cụ Audit Độc Lập cho dự án Việt Hóa Plants vs. Zombies Fusion v4.0.5.

Kiểm tra nghiêm ngặt các tiêu chuẩn chất lượng:
1. Sót chữ Hán (ERROR)
2. Copy nguyên văn không dịch (ERROR)
3. Lệch biến format {0}, {1}... (ERROR)
4. Lệch thẻ Unity Rich Text <color>, <b>, <nobr>... (ERROR)
5. Lệch ký tự xuống dòng \n ở đầu/cuối chuỗi (ERROR)
6. Xung đột cùng key dịch khác nhau giữa các module (ERROR)
7. Tính nhất quán thuật ngữ theo GLOSSARY (WARNING)
8. Bất thường về độ dài chuỗi có nguy cơ vỡ layout UI (WARNING)
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
TRANS_DIR = ROOT_DIR / "data" / "translated"
GLOSSARY_PATH = ROOT_DIR / "glossary.json"

MODULES_LIST = ['ui', 'plants', 'zombies', 'buffs_synergies', 'dialogues', 'misc']

def extract_placeholders(text):
    return sorted(re.findall(r'\{[0-9]+(?::[^}]+)?\}', text))

def extract_tags(text):
    return sorted(re.findall(r'<[/]?[a-zA-Z0-9#=_%]+>', text))

def load_glossary():
    if not GLOSSARY_PATH.exists():
        return {}
    with open(GLOSSARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def audit_entry(raw, trans, glossary):
    errors = []
    warnings = []

    # 1. Kiểm tra copy nguyên văn
    if raw.strip() == trans.strip() and re.search(r'[\u4e00-\u9fff]', raw):
        errors.append("Copy nguyên văn chuỗi gốc tiếng Trung (chưa dịch)")

    # 2. Kiểm tra sót chữ Hán trong bản dịch
    han_chars = re.findall(r'[\u4e00-\u9fff]', trans)
    if han_chars:
        errors.append(f"Sót {len(han_chars)} ký tự Hán tự trong bản dịch: {''.join(han_chars[:5])}...")

    # 3. Kiểm tra biến format {0}, {1}
    raw_phs = extract_placeholders(raw)
    trans_phs = extract_placeholders(trans)
    if raw_phs != trans_phs:
        errors.append(f"Lệch biến format: Gốc có {raw_phs} != Dịch có {trans_phs}")

    # 4. Kiểm tra thẻ Unity Rich Text
    raw_tags = extract_tags(raw)
    trans_tags = extract_tags(trans)
    if raw_tags != trans_tags:
        errors.append(f"Lệch thẻ Rich Text: Gốc có {raw_tags} != Dịch có {trans_tags}")

    # 5. Kiểm tra ký tự xuống dòng \n ở đầu/cuối chuỗi
    if raw.startswith('\n') and not trans.startswith('\n'):
        errors.append("Thiếu ký tự '\\n' ở đầu câu giống bản gốc")
    if raw.endswith('\n') and not trans.endswith('\n'):
        errors.append("Thiếu ký tự '\\n' ở cuối câu giống bản gốc")

    # 6. Kiểm tra nhất quán thuật ngữ theo Glossary
    for term_zh, term_vi in glossary.items():
        if term_zh in raw:
            # So sánh không phân biệt hoa thường
            if term_vi.lower() not in trans.lower():
                warnings.append(f"Chưa dùng thuật ngữ chuẩn: '{term_zh}' -> nên là '{term_vi}'")

    # 7. Cảnh báo độ dài (nguy cơ tràn khung UI)
    clean_raw = re.sub(r'<[^>]+>', '', raw).strip()
    clean_trans = re.sub(r'<[^>]+>', '', trans).strip()
    if len(clean_raw) > 5:
        ratio = len(clean_trans) / len(clean_raw)
        if ratio > 3.8:
            warnings.append(f"Độ dài bản dịch quá dài ({len(clean_trans)} ký tự vs gốc {len(clean_raw)}, tỉ lệ {ratio:.1f}x) - nguy cơ tràn UI")
        elif ratio < 0.25 and len(clean_raw) > 20:
            warnings.append(f"Độ dài bản dịch quá ngắn ({len(clean_trans)} ký tự vs gốc {len(clean_raw)}) - nghi vấn dịch thiếu ý")

    return errors, warnings

def check_cross_module_conflicts(all_translations):
    """
    Kiểm tra xem cùng 1 key tiếng Trung nhưng ở 2 module khác nhau lại dịch khác nhau.
    """
    conflicts = []
    seen = {}
    for mod_name, mod_data in all_translations.items():
        for raw, trans in mod_data.items():
            if not trans:
                continue
            if raw in seen:
                prev_mod, prev_trans = seen[raw]
                if prev_trans.strip() != trans.strip():
                    conflicts.append((raw, prev_mod, prev_trans, mod_name, trans))
            else:
                seen[raw] = (mod_name, trans)
    return conflicts

def run_audit(target_module=None):
    glossary = load_glossary()
    modules_to_audit = [target_module] if target_module else MODULES_LIST

    all_translations = {}
    for mod in MODULES_LIST:
        trans_file = TRANS_DIR / f"{mod}.json"
        if trans_file.exists():
            with open(trans_file, 'r', encoding='utf-8') as f:
                all_translations[mod] = json.load(f)
        else:
            all_translations[mod] = {}

    print("======================================================================")
    print("      BÁO CÁO AUDIT ĐỘC LẬP - DỰ ÁN VIỆT HÓA PVZ FUSION v4.0.5")
    print("======================================================================")

    total_checked = 0
    total_errors = 0
    total_warnings = 0

    for mod in modules_to_audit:
        raw_file = RAW_DIR / f"{mod}.json"
        if not raw_file.exists():
            continue

        with open(raw_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        trans_data = all_translations.get(mod, {})
        mod_translated = 0
        mod_errors = 0
        mod_warnings = 0

        issue_details = []

        for raw_str in raw_data:
            trans_str = trans_data.get(raw_str, "").strip()
            if trans_str:
                mod_translated += 1
                errs, warns = audit_entry(raw_str, trans_data.get(raw_str, ""), glossary)
                if errs or warns:
                    issue_details.append((raw_str, trans_data.get(raw_str, ""), errs, warns))
                    mod_errors += len(errs)
                    mod_warnings += len(warns)

        pct = (mod_translated / len(raw_data) * 100) if raw_data else 0
        print(f"[{mod:16s}] Đã dịch: {mod_translated:4d}/{len(raw_data):4d} ({pct:5.1f}%) | ERROR: {mod_errors:2d} | WARNING: {mod_warnings:2d}")

        if issue_details:
            for raw_s, trans_s, errs, warns in issue_details[:5]:
                print(f"  - Gốc : {repr(raw_s[:60])}")
                print(f"    Dịch: {repr(trans_s[:60])}")
                for e in errs:
                    print(f"    ❌ ERROR  : {e}")
                for w in warns:
                    print(f"    ⚠️ WARNING: {w}")
            if len(issue_details) > 5:
                print(f"    ... và {len(issue_details) - 5} vấn đề khác.")

        total_checked += mod_translated
        total_errors += mod_errors
        total_warnings += mod_warnings

    # Kiểm tra xung đột cross-module
    cross_conflicts = check_cross_module_conflicts(all_translations)
    if cross_conflicts:
        print("\n[!] XUNG ĐỘT CROSS-MODULE (Cùng key nhưng dịch khác nhau giữa các module):")
        for raw, m1, t1, m2, t2 in cross_conflicts:
            print(f"  ❌ Key: {repr(raw)}")
            print(f"     [{m1}]: {repr(t1)}")
            print(f"     [{m2}]: {repr(t2)}")
            total_errors += 1

    print("----------------------------------------------------------------------")
    print(f"TỔNG KẾT: Đã audit {total_checked} chuỗi | TỔNG ERROR: {total_errors} | TỔNG WARNING: {total_warnings}")
    print("======================================================================")

    if total_errors > 0:
        print("[FAIL] Audit thất bại! Có ERROR vi phạm quy tắc bắt buộc.")
        return 1
    else:
        print("[PASS] Audit đạt tiêu chuẩn chất lượng (0 ERROR).")
        return 0

def main():
    parser = argparse.ArgumentParser(description="Audit độc lập bản dịch PvZ Fusion")
    parser.add_argument("--module", choices=MODULES_LIST, help="Audit riêng một module cụ thể")
    args = parser.parse_args()

    exit_code = run_audit(target_module=args.module)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
