import sys
import json
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
TRANS_DIR = ROOT_DIR / "data" / "translated"
RAW_DIR = ROOT_DIR / "data" / "raw"

# Comprehensive dictionary of stat labels and their official Vietnamese translation
STAT_LABELS = {
    "场上敌人数量": "Số lượng địch trên sân",
    "难度": "Độ khó",
    "游戏时长": "Thời gian chơi",
    "现实游戏时长": "Thời gian chơi thực tế",
    "波次": "Đợt",
    "击杀僵尸": "Tiêu diệt Zombie",
    "总伤害": "Tổng sát thương",
    "种植植物": "Trồng thực vật",
    "剩余阳光": "Nắng còn lại",
    "产生阳光": "Nắng đã tạo",
    "消耗阳光": "Nắng đã dùng",
    "剩余金币": "Vàng còn lại",
    "获得金币": "Nhận tiền vàng",
    "消耗金币": "Tiêu hao tiền vàng",
    "死亡植物": "Thực vật tử trận",
    "铲除植物": "Xới bỏ thực vật",
    "小推车使用": "Xe cắt cỏ đã dùng",
    "魅惑僵尸": "Zombie bị mê hoặc",
    "剩余可用步数": "Số bước còn lại",
    "剩余积分": "Điểm tích lũy còn lại",
    "当前分数": "Điểm hiện tại",
    "当前波数": "Đợt hiện tại",
    "当前游戏时长": "Thời gian chơi hiện tại",
    "当前诸神币": "Xu Chư Thần hiện tại",
    "总计": "Tổng cộng",
    "总雷数": "Tổng số mìn",
    "暴击伤害": "Sát thương bạo kích",
    "暴击率": "Tỷ lệ bạo kích",
    "幸运一击伤害": "Sát thương đòn may mắn",
    "幸运一击率": "Tỷ lệ đòn may mắn",
    "攻击力": "Sức tấn công",
    "攻击间隔": "Khoảng cách tấn công",
    "攻速加成": "Tăng tốc độ đánh",
    "伤害加成": "Tăng sát thương",
    "伤害增幅": "Tăng sát thương",
    "独立伤害增幅": "Tăng sát thương độc lập",
    "生命值": "Lượng máu",
    "耐久": "Độ bền",
    "护盾量": "Lượng giáp",
    "敌方护甲": "Giáp của địch",
    "连击数": "Số chuỗi đòn",
    "最大连击数": "Chuỗi đòn tối đa",
    "抽取次数": "Số lần rút",
    "抽奖券": "Vé rút thưởng",
    "等级": "Cấp độ",
    "难度阶数": "Bậc độ khó",
    "难度积分": "Điểm độ khó",
    "普通概率": "Xác suất phổ thông",
    "银色概率": "Xác suất bạc",
    "金色概率": "Xác suất vàng",
    "钻石概率": "Xác suất kim cương",
    "阳光增幅": "Tăng lượng Nắng",
    "关卡进度": "Tiến độ màn chơi",
    "出怪等级": "Cấp xuất hiện",
    "出怪权重": "Tỷ trọng xuất hiện",
    "花费": "Tiêu tốn",
    "冷却时间": "Thời gian hồi chiêu",
}

# Standalone UI strings in screenshot 2
EXTRA_UI_STRINGS = {
    "最后一波怪清完后\n如果卡关点这": "Sau khi dọn sạch đợt cuối\nNếu kẹt màn hãy nhấn vào đây",
    "最后一波怪清完后": "Sau khi dọn sạch đợt cuối",
    "如果卡关点这": "Nếu kẹt màn hãy nhấn vào đây",
}

def add_extra_ui():
    raw_ui_file = RAW_DIR / "ui.json"
    trans_ui_file = TRANS_DIR / "ui.json"
    
    with open(raw_ui_file, 'r', encoding='utf-8') as f:
        raw_ui = json.load(f)
    with open(trans_ui_file, 'r', encoding='utf-8') as f:
        trans_ui = json.load(f)
        
    for k, v in EXTRA_UI_STRINGS.items():
        if k not in raw_ui:
            raw_ui[k] = ""
        trans_ui[k] = v
        
    with open(raw_ui_file, 'w', encoding='utf-8') as f:
        json.dump(raw_ui, f, ensure_ascii=False, indent=2)
    with open(trans_ui_file, 'w', encoding='utf-8') as f:
        json.dump(trans_ui, f, ensure_ascii=False, indent=2)
    print(f"[✓] Added {len(EXTRA_UI_STRINGS)} extra UI strings to ui.json")

def generate_stat_regex_rules():
    rules = []
    
    # 1. Rules for all stat labels
    for zh, vi in STAT_LABELS.items():
        # Match both Chinese full-width colon '：' and standard colon ':' with optional spaces
        pattern = f"^{re.escape(zh)}[：:]\\s*(.+)$"
        replacement = f"{vi}: $1"
        rules.append(f'r:"{pattern}"="{replacement}"')
        
    # 2. Number + 万 (vạn = 10,000) or other units in stats
    rules.append(r'r:"^(.+)\s*万$"="$1 vạn"')
    rules.append(r'r:"^(.+)\s*秒$"="$1 giây"')
    
    return rules

if __name__ == '__main__':
    add_extra_ui()
    rules = generate_stat_regex_rules()
    print(f"[✓] Generated {len(rules)} stat regex rules.")
    for r in rules[:10]:
        print("  ", r)
