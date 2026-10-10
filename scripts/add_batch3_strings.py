import sys
import json
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
TRANS_DIR = ROOT_DIR / "data" / "translated"

GUIDE_TOPICS = {
    "<color=#FF7400>融合</color>是《植物大战僵尸：融合版》的核心玩法。按照<color=#FF7400>配方</color>将两株植物叠加在一起，即可融合出一株新的植物。\n\n一般的融合配方会在解锁对应的基础植物立即解锁。更高层次、更多形式的融合配方则等待你去探索！": "<color=#FF7400>Dung Hợp</color> là lối chơi cốt lõi của \"Plants vs Zombies: Bản Dung Hợp\". Dựa theo <color=#FF7400>công thức</color> đặt hai cây trồng đè lên nhau, có thể dung hợp ra một loài cây mới.\n\nCông thức dung hợp thông thường sẽ được mở khóa ngay khi mở khóa cây cơ bản tương ứng. Các tầng bậc cao hơn và nhiều hình thức dung hợp đa dạng hơn đang chờ bạn khám phá!",
    "低矮、高大、巨型植物": "Cây Thấp, Cao, Khổng Lồ",
    "僵尸机制-BOSS及领袖": "Cơ Chế Zombie - BOSS & Thủ Lĩnh",
    "僵尸机制-临界值": "Cơ Chế Zombie - Ngưỡng Giới Hạn",
    "僵尸机制-僵尸肥料": "Cơ Chế Zombie - Phân Bón Zombie",
    "僵尸机制-护甲": "Cơ Chế Zombie - Giáp Thân",
    "僵尸机制-碾压": "Cơ Chế Zombie - Nghiền Ép",
    "僵尸机制-诅咒状态": "Cơ Chế Zombie - Trạng Thái Nguyền Rủa",
    "僵尸机制-防具": "Cơ Chế Zombie - Giáp Ngoài",
    "僵尸机制-防寒等级与冻结": "Cơ Chế Zombie - Kháng Lạnh & Đóng Băng",
    "可密植、坚实、金属植物": "Cây Trồng Dày, Kiên Cố, Kim Loại",
    "基本机制-僵尸身位": "Cơ Chế Cơ Bản - Vị Trí Zombie",
    "基本机制-关卡难度": "Cơ Chế Cơ Bản - Độ Khó Màn Chơi",
    "基本机制-植物占位": "Cơ Chế Cơ Bản - Vị Trí Cây Trồng",
    "基本机制-血量和韧性": "Cơ Chế Cơ Bản - Lượng Máu & Độ Bền",
    "基本机制-金钱": "Cơ Chế Cơ Bản - Tiền Vàng",
    "基本机制-阳光": "Cơ Chế Cơ Bản - Ánh Sáng",
    "我是僵尸模式": "Chế Độ Ta Là Zombie",
    "旅行生存模式": "Chế Độ Sinh Tồn Du Hành",
    "旅行：炼狱难度": "Du Hành: Độ Khó Địa Ngục",
    "旅行：诅咒难度": "Du Hành: Độ Khó Nguyền Rủa",
    "杂项-卡牌解锁I": "Mục Khác - Mở Khóa Thẻ I",
    "杂项-卡牌解锁II": "Mục Khác - Mở Khóa Thẻ II",
    "杂项-配方解锁": "Mục Khác - Mở Khóa Công Thức",
    "植物机制-中毒状态": "Cơ Chế Thực Vật - Trạng Thái Trúng Độc",
    "植物机制-传送状态": "Cơ Chế Thực Vật - Trạng Thái Dịch Chuyển",
    "植物机制-余烬状态": "Cơ Chế Thực Vật - Trạng Thái Tàn Tro",
    "植物机制-光照等级": "Cơ Chế Thực Vật - Cấp Chiếu Sáng",
    "植物机制-寒冷与冻结状态": "Cơ Chế Thực Vật - Trạng Thái Lạnh & Đóng Băng",
    "植物机制-护盾": "Cơ Chế Thực Vật - Khiên Chắn",
    "植物机制-水草值": "Cơ Chế Thực Vật - Điểm Bèo Nước",
    "植物机制-磁力系统": "Cơ Chế Thực Vật - Hệ Thống Từ Tính",
    "植物机制-红温状态": "Cơ Chế Thực Vật - Trạng Thái Quá Nhiệt",
    "环境机制-熔岩地块": "Cơ Chế Môi Trường - Ô Đất Dung Nham",
    "环境机制-雪原白天": "Cơ Chế Môi Trường - Đồng Tuyết Ban Ngày",
    "环境机制-雪原黑夜": "Cơ Chế Môi Trường - Đồng Tuyết Ban Đêm",
    "生存模式无尽：诅咒挑战": "Sinh Tồn Vô Tận: Thử Thách Nguyền Rủa",
}

def extract_tags(text):
    return sorted(re.findall(r'<[/]?[a-zA-Z0-9#=_%]+>', text))

def main():
    matched_file = Path(r"C:\Users\ADMIN\.gemini\antigravity-ide\brain\e14cb371-e381-483d-b1e3-96a99e39f038\scratch\matched_buffs.json")
    with open(matched_file, 'r', encoding='utf-8') as f:
        matched_buffs = json.load(f)

    # Fix any specific tag mismatches
    if "【<nobr>真正的毁灭菇</nobr>】" in matched_buffs:
        matched_buffs["【<nobr>真正的毁灭菇</nobr>】"] = "【<nobr>Nấm Hủy Diệt Chân Chính</nobr>】"

    # Verify all tags match
    for k, v in matched_buffs.items():
        kt = extract_tags(k)
        vt = extract_tags(v)
        if kt != vt:
            print(f"Warning tag mismatch: {k} -> {v}")

    # Add buff standalone names to buffs_synergies.json
    buff_raw_path = RAW_DIR / "buffs_synergies.json"
    buff_trans_path = TRANS_DIR / "buffs_synergies.json"

    with open(buff_raw_path, 'r', encoding='utf-8') as f:
        buff_raw = json.load(f)
    with open(buff_trans_path, 'r', encoding='utf-8') as f:
        buff_trans = json.load(f)

    added_buffs = 0
    for k, v in matched_buffs.items():
        if k not in buff_trans:
            buff_raw[k] = ""
            buff_trans[k] = v
            added_buffs += 1

    with open(buff_raw_path, 'w', encoding='utf-8') as f:
        json.dump(buff_raw, f, ensure_ascii=False, indent=2)
    with open(buff_trans_path, 'w', encoding='utf-8') as f:
        json.dump(buff_trans, f, ensure_ascii=False, indent=2)

    print(f"[✓] Added {added_buffs} standalone buff strings to buffs_synergies.json")

    # Add mechanic guide strings to misc.json
    misc_raw_path = RAW_DIR / "misc.json"
    misc_trans_path = TRANS_DIR / "misc.json"

    with open(misc_raw_path, 'r', encoding='utf-8') as f:
        misc_raw = json.load(f)
    with open(misc_trans_path, 'r', encoding='utf-8') as f:
        misc_trans = json.load(f)

    added_misc = 0
    for k, v in GUIDE_TOPICS.items():
        if k not in misc_trans:
            misc_raw[k] = ""
            misc_trans[k] = v
            added_misc += 1

    with open(misc_raw_path, 'w', encoding='utf-8') as f:
        json.dump(misc_raw, f, ensure_ascii=False, indent=2)
    with open(misc_trans_path, 'w', encoding='utf-8') as f:
        json.dump(misc_trans, f, ensure_ascii=False, indent=2)

    print(f"[✓] Added {added_misc} guide strings to misc.json")

if __name__ == '__main__':
    main()
