#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_metadata.py - Trích xuất toàn bộ chuỗi văn bản tiếng Trung từ global-metadata.dat (Unity IL2CPP v31).
Dự án Việt Hóa Plants vs. Zombies Fusion v4.0.5.
"""

import os
import sys
import struct
import re
import json
import argparse
from pathlib import Path

# Cấu hình UTF-8 cho console Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DEFAULT_METADATA_PATH = r"c:\Mod\PvZ_Fusion\PlantsVsZombiesRH_Data\il2cpp_data\Metadata\global-metadata.dat"

def extract_strings(metadata_path):
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Không tìm thấy file metadata tại: {metadata_path}")

    with open(metadata_path, 'rb') as f:
        header = f.read(128)
        magic, version = struct.unpack('<II', header[:8])
        if magic != 0xFAB11BAF:
            raise ValueError(f"Magic header không hợp lệ: {hex(magic)} (Yêu cầu 0xFAB11BAF)")

        # IL2CPP v31 header:
        # offset 8: stringLiteralOffset (256)
        # offset 12: stringLiteralSize (159096)
        # offset 16: stringLiteralDataOffset (159352)
        # offset 20: stringLiteralDataSize (637048)
        offsets = struct.unpack('<' + 'I'*20, header[:80])
        literal_offset = offsets[2]
        literal_size = offsets[3]
        data_offset = offsets[4]
        data_size = offsets[5]

        literal_count = literal_size // 8
        f.seek(literal_offset)
        literals = [struct.unpack('<II', f.read(8)) for _ in range(literal_count)]

        f.seek(data_offset)
        data = f.read(data_size)

    seen = set()
    chinese_strings = []

    for length, data_idx in literals:
        if data_idx + length <= len(data):
            raw_bytes = data[data_idx:data_idx+length]
            try:
                s = raw_bytes.decode('utf-8')
                # Lọc các chuỗi chứa ít nhất một ký tự Hán tự
                if re.search(r'[\u4e00-\u9fff]', s) and s not in seen:
                    seen.add(s)
                    chinese_strings.append(s)
            except UnicodeDecodeError:
                pass

    return chinese_strings

def categorize_strings(strings):
    categories = {
        'ui': {},
        'plants': {},
        'zombies': {},
        'buffs_synergies': {},
        'dialogues': {},
        'misc': {}
    }

    plant_keywords = ['射手', '向日葵', '坚果', '大嘴花', '大喷菇', '西瓜', '卷心菜', '玉米', '杨桃', '樱桃', '土豆', '火炬', '蘑菇', '睡莲', '荷叶', '蒜', '南瓜', '植物', '魅惑菇', '寒冰菇', '毁灭菇', '墓碑', '杨桃', '三叶草', '仙人掌', '杨桃', '星星', '磁力菇']
    zombie_keywords = ['僵尸', '读报', '橄榄', '路障', '铁桶', '撑杆', '舞王', '潜水', '冰车', '小丑', '气球', '矿工', '跳跳', '雪人', '蹦极', '梯子', '投石', '巨人', '加刚特尔', '小鬼', '武士', '团长']
    buff_keywords = ['【SP进化】', '【元素反应】', '【', '】', '羁绊', '词条', '强化', '神话', '究极', '专属', '属性', '伤害', '暴击', '冷却', '攻速', '护甲', '诸神币', '合成', '配方', '品质', '难度积分']
    ui_keywords = ['点击', '选择', '确认', '取消', '设置', '开始', '退出', '暂停', '关卡', '模式', '金币', '商店', '购买', '存档', '音量', '全屏', '返回', '下一页', '上一页', '刷新', '确定', '价格']

    for s in strings:
        # 1. Phân loại Buffs / Synergies / SP
        if any(k in s for k in buff_keywords):
            categories['buffs_synergies'][s] = ""
        # 2. Phân loại Cây lai (Plants)
        elif any(k in s for k in plant_keywords):
            categories['plants'][s] = ""
        # 3. Phân loại Zombie (Zombies)
        elif any(k in s for k in zombie_keywords):
            categories['zombies'][s] = ""
        # 4. Phân loại Giao diện / UI (ngắn, nút bấm, menu)
        elif any(k in s for k in ui_keywords) and len(s) < 30:
            categories['ui'][s] = ""
        # 5. Phân loại Lời thoại / Hướng dẫn
        elif len(s) > 40 or any(k in s for k in ['戴夫', '歪比巴卜', '提示：', '规则：', '胜利条件']):
            categories['dialogues'][s] = ""
        # 6. Các chuỗi khác
        else:
            categories['misc'][s] = ""

    return categories

def main():
    parser = argparse.ArgumentParser(description="Trích xuất text tiếng Trung từ global-metadata.dat PvZ Fusion")
    parser.add_argument("--metadata", default=DEFAULT_METADATA_PATH, help="Đường dẫn tới global-metadata.dat")
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parent.parent / "data" / "raw"), help="Thư mục xuất file json")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[+] Đang đọc metadata từ: {args.metadata}")
    strings = extract_strings(args.metadata)
    print(f"[✓] Đã tìm thấy {len(strings)} chuỗi tiếng Trung duy nhất!")

    # Lưu toàn bộ raw
    all_path = out_dir / "all_strings.json"
    with open(all_path, 'w', encoding='utf-8') as f:
        json.dump({s: "" for s in strings}, f, ensure_ascii=False, indent=2)
    print(f"[✓] Đã lưu toàn bộ chuỗi vào: {all_path}")

    # Phân loại
    categorized = categorize_strings(strings)
    for cat_name, items in categorized.items():
        cat_path = out_dir / f"{cat_name}.json"
        with open(cat_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"    - {cat_name}.json: {len(items)} chuỗi")

    print("[✓] Hoàn tất trích xuất và phân loại!")

if __name__ == '__main__':
    main()
