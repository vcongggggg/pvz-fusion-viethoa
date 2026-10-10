import sys
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
TRANS_DIR = ROOT_DIR / "data" / "translated"

# Map of module -> dict of {Chinese: Vietnamese}
BATCH_2 = {
    "ui": {
        "花费": "Tiêu tốn",
        "花费:": "Tiêu tốn:",
        "花费：": "Tiêu tốn:",
        "冷却时间": "Thời gian hồi chiêu",
        "冷却时间:": "Thời gian hồi chiêu:",
        "冷却时间：": "Thời gian hồi chiêu:",
        "秒": "giây",
        "出怪等级": "Cấp xuất hiện",
        "出怪等级:": "Cấp xuất hiện:",
        "出怪等级：": "Cấp xuất hiện:",
        "出怪权重": "Tỷ trọng xuất hiện",
        "出怪权重:": "Tỷ trọng xuất hiện:",
        "出怪权重：": "Tỷ trọng xuất hiện:",
        "玩法-融合": "Cách chơi - Dung hợp",
        "玩法-副卡": "Cách chơi - Thẻ phụ",
        "玩法-铲子": "Cách chơi - Xẻng",
        "玩法-手套": "Cách chơi - Găng tay",
        "玩法-锤子": "Cách chơi - Búa",
        "玩法-手推车": "Cách chơi - Xe đẩy",
        "玩法-时停": "Cách chơi - Ngưng đọng thời gian",
        "玩法-植物肥料": "Cách chơi - Phân bón thực vật",
        "基础植物 · 输出/辅助": "Thực vật cơ bản · Sát thương/Hỗ trợ",
        "7 条进化路线 · 点击卡牌查看词条": "7 lộ trình tiến hóa · Nhấn vào thẻ để xem thuộc tính",
        "可获得词条  5 项": "Có thể nhận 5 thuộc tính",
        "可获得词条 5 项": "Có thể nhận 5 thuộc tính",
        "终端植物 · 输出": "Thực vật tối thượng · Sát thương",
        "普通 · 最多 1000 次": "Phổ thông · Tối đa 1000 lần",
        "普通 · 最多 50 次": "Phổ thông · Tối đa 50 lần",
        "黄金 · 最多 10 次": "Hoàng kim · Tối đa 10 lần",
        "钻石 · 最多 1 次": "Kim cương · Tối đa 1 lần",
        "诅咒 · 最多 1 次 · 被动": "Nguyền rủa · Tối đa 1 lần · Bị động",
        "出现条件：仅炼狱模式可出现。": "Điều kiện xuất hiện: Chỉ xuất hiện trong Chế độ Luyện Ngục.",
        "出现条件：同一植物只能选择一个质变词条。": "Điều kiện xuất hiện: Cùng một cây chỉ được chọn một thuộc tính biến chất.",
        "路线 1  /  究极流光射手 · 50诸神币": "Lộ trình 1 / Đậu Xạ Thủ Lưu Quang Cực Hạn · 50 Xu Chư Thần",
        "路线 2  /  死神猎手 · 50诸神币": "Lộ trình 2 / Thợ Săn Tử Thần · 50 Xu Chư Thần",
        "路线 3  /  火焰狙击射手 · 50诸神币": "Lộ trình 3 / Đậu Bắn Tỉa Rực Lửa · 50 Xu Chư Thần",
        "路线 4  /  究极激光炮台 · 50诸神币": "Lộ trình 4 / Pháo Đài Laser Cực Hạn · 50 Xu Chư Thần",
        "路线 5  /  究极樱桃射手 · 已解锁": "Lộ trình 5 / Đậu Xạ Thủ Cherry Cực Hạn · Đã mở khóa",
        "路线 6  /  究极黑橄榄机枪射手 · 50诸神币": "Lộ trình 6 / Đậu Súng Máy Mũ Ô Liu Đen Cực Hạn · 50 Xu Chư Thần",
        "路线 7  /  究极魔法寒冰射手 · 50诸神币": "Lộ trình 7 / Đậu Băng Ma Pháp Cực Hạn · 50 Xu Chư Thần",
        "路线 1 / 究极流光射手 · 50诸神币": "Lộ trình 1 / Đậu Xạ Thủ Lưu Quang Cực Hạn · 50 Xu Chư Thần",
        "路线 2 / 死神猎手 · 50诸神币": "Lộ trình 2 / Thợ Săn Tử Thần · 50 Xu Chư Thần",
        "路线 3 / 火焰狙击射手 · 50诸神币": "Lộ trình 3 / Đậu Bắn Tỉa Rực Lửa · 50 Xu Chư Thần",
        "路线 4 / 究极激光炮台 · 50诸神币": "Lộ trình 4 / Pháo Đài Laser Cực Hạn · 50 Xu Chư Thần",
        "路线 5 / 究极樱桃射手 · 已解锁": "Lộ trình 5 / Đậu Xạ Thủ Cherry Cực Hạn · Đã mở khóa",
        "路线 6 / 究极黑橄榄机枪射手 · 50诸神币": "Lộ trình 6 / Đậu Súng Máy Mũ Ô Liu Đen Cực Hạn · 50 Xu Chư Thần",
        "路线 7 / 究极魔法寒冰射手 · 50诸神币": "Lộ trình 7 / Đậu Băng Ma Pháp Cực Hạn · 50 Xu Chư Thần",
    },
    "plants": {
        "坚果": "Quả Óc Chó",
        "土豆雷": "Mìn Khoai Tây",
        "大嘴花": "Hoa Răng Nhọn",
        "小喷菇": "Nấm Phun Nhỏ",
        "大喷菇": "Nấm Phun Lớn",
        "胆小菇": "Nấm Nhút Nhát",
        "窝瓜": "Bí Đè",
        "魅惑菇": "Nấm Thôi Miên",
        "云杉弓手": "Cung Thủ Vân Sam",
        "冬笋路障": "Măng Đông Rào Chắn",
        "叶子保护伞": "Lá Ô Che Phủ",
        "玉米投手": "Cây Bắn Ngô",
        "西瓜投手": "Cây Bắn Dưa Hấu",
        "卷心菜投手": "Cây Bắn Bắp Cải",
        "杨桃": "Khế Sao",
        "仙人掌": "Xương Rồng",
        "地刺": "Gai Đất",
        "三线射手": "Xạ Thủ Ba Nòng",
        "火爆辣椒": "Ớt Bốc Hỏa",
        "流光中继射手": "Đậu Xạ Thủ Lưu Quang Tiếp Sức",
        "究极流光射手": "Đậu Xạ Thủ Lưu Quang Cực Hạn",
        "狙击射手": "Đậu Bắn Tỉa",
        "死神猎手": "Thợ Săn Tử Thần",
        "火焰狙击射手": "Đậu Bắn Tỉa Rực Lửa",
        "究极激光炮台": "Pháo Đài Laser Cực Hạn",
        "樱桃机枪射手": "Đậu Súng Máy Cherry",
        "究极樱桃射手": "Đậu Xạ Thủ Cherry Cực Hạn",
        "橄榄机枪射手": "Đậu Súng Máy Ô Liu",
        "究极黑橄榄机枪射手": "Đậu Súng Máy Mũ Ô Liu Đen Cực Hạn",
        "寒冰射手": "Đậu Bắn Băng",
        "究极魔法寒冰射手": "Đậu Băng Ma Pháp Cực Hạn",
        "一株植物，怎么能这么高效的产出如此多的豌豆并发射呢？豌豆射手说：“全靠努力工作，奉献自我，以及阳光和高纤维二氧化碳均衡搭配的健康早餐。”": "Một loài cây, làm sao có thể sản sinh và bắn ra nhiều đậu một cách hiệu quả như vậy? Đậu Bắn Súng nói: \"Tất cả là nhờ chăm chỉ làm việc, cống hiến hết mình, cùng một bữa sáng lành mạnh kết hợp cân bằng giữa ánh sáng mặt trời và carbon dioxide giàu chất xơ.\"",
    },
    "zombies": {
        "普通僵尸讨厌他名字里的“普通”这个字眼。他不认为自己是什么不配拥有姓名的敌人抑或是随处可见的普通僵尸，他坚信自己是独一无二的。尽管从外观上，人们很难将他和他的同伴区分开来。": "Zombie thường ghét từ \"thường\" trong tên của mình. Hắn không nghĩ mình là kẻ địch không xứng đáng có tên hay là một zombie bình thường có thể bắt gặp ở bất cứ đâu, hắn kiên định tin rằng mình là độc nhất vô nhị. Mặc dù nhìn bề ngoài, mọi người khó mà phân biệt được hắn với đồng bọn.",
        "普通僵尸讨厌他名字里的“普通”这个字眼。他不认为自己是什么不配拥有姓名的敌人抑或是随处可见的普...": "Zombie thường ghét từ \"thường\" trong tên của mình. Hắn không nghĩ mình là kẻ địch không xứng đáng có tên hay là một zombie bình thường có thể bắt gặp ở bất cứ đâu, hắn kiên định tin rằng mình là độc nhất vô nhị. Mặc dù nhìn bề ngoài, mọi người khó mà phân biệt được hắn với đồng bọn.",
    },
    "buffs_synergies": {
        "撒豆成兵": "Rải Đậu Thành Binh",
        "精兵强将": "Tinh Binh Cường Tướng",
        "枕戈待旦": "Gối Giáo Chờ Trời Sáng",
        "核能威慑": "Răn Đe Hạt Nhân",
        "妙手回春": "Diệu Thủ Hồi Xuân",
        "无关痛痒": "Chẳng Hề Hấn Gì",
        "尸愁之路": "Con Đường Sầu Não",
        "百炼成钢": "Bách Luyện Thành Thép",
        "怒火攻心": "Nộ Hỏa Công Tâm",
        "百步穿杨": "Bách Bộ Xuyên Dương",
        "势如破竹": "Thế Như Chẻ Tre",
        "冻彻心扉": "Băng Giá Thấu Tim",
        "多多益善": "Càng Nhiều Càng Tốt",
        "等价交换": "Trao Đổi Đồng Giá",
        "弹射起步": "Khởi Động Phóng Tên",
        "人工智能": "Trí Tuệ Nhân Tạo",
        "我也是梦珞": "Tôi Cũng Là Mộng Lạc",
        "我是梦珞": "Tôi Là Mộng Lạc",
        "我也是梦珞：\n· 解锁魔法兔耳葱\n◆魔法猫尾草：追踪子弹伤害×5\n◆魔法兔耳葱：魔法闪电伤害×3": "Tôi Cũng Là Mộng Lạc:\n· Mở khóa Hành Tai Thỏ Ma Pháp\n◆Cỏ Đuôi Mèo Ma Pháp: Sát thương đạn đuổi ×5\n◆Hành Tai Thỏ Ma Pháp: Sát thương sét ma pháp ×3",
        "我是梦珞：\n◆魔法猫尾草：魔法浮游炮伤害×3\n◆魔法兔耳葱：协助召唤的浮游炮会发射6": "Tôi Là Mộng Lạc:\n◆Cỏ Đuôi Mèo Ma Pháp: Sát thương pháo nổi ma pháp ×3\n◆Hành Tai Thỏ Ma Pháp: Pháo nổi hỗ trợ triệu hồi sẽ bắn 6",
        "究极樱桃射手每次攻击多发射一发子弹": "Đậu Xạ Thủ Cherry Cực Hạn mỗi đòn tấn công bắn thêm một viên đạn",
        "究极樱桃射手获得20%速度增幅（普通品质基准，实际增幅随品质变化）。": "Đậu Xạ Thủ Cherry Cực Hạn tăng 20% tốc độ (chuẩn phẩm chất Phổ thông, tăng thực tế theo phẩm chất).",
        "究极樱桃射手获得30%独立伤害增幅（普通品质基准，实际增幅随品质变化）。": "Đậu Xạ Thủ Cherry Cực Hạn tăng 30% sát thương độc lập (chuẩn phẩm chất Phổ thông, tăng thực tế theo phẩm chất).",
    },
    "misc": {
        "<color=#ff7b00>融合</color>是《植物大战僵尸：融合版》的核心玩法。按照<color=#ff7b00>配方</color>将两株植物叠加在一起，即可融合出一株新的植物。\n\n一般的融合配方会在解锁对应的基础植物立即解锁。更高层次、更多形式的融合配方则等待你去探索！": "<color=#ff7b00>Dung hợp</color> là lối chơi cốt lõi của \"Plants vs. Zombies: Fusion\". Ghép hai cây lại với nhau theo <color=#ff7b00>công thức</color> là có thể dung hợp ra một loài cây mới.\n\nCông thức dung hợp thông thường sẽ mở khóa ngay khi mở khóa cây cơ bản tương ứng. Các công thức dung hợp cấp cao hơn, đa dạng hơn đang chờ bạn khám phá!",
        "一般的融合配方会在解锁对应的基础植物立即解锁。更高层次、更多形式的融合配方则等待你去探索！": "Công thức dung hợp thông thường sẽ mở khóa ngay khi mở khóa cây cơ bản tương ứng. Các công thức dung hợp cấp cao hơn, đa dạng hơn đang chờ bạn khám phá!",
        "融合是《植物大战僵尸：融合版》的核心玩法。按照配方将两株植物叠加在一起，即可融合出一株新的植物。": "Dung hợp là lối chơi cốt lõi của \"Plants vs. Zombies: Fusion\". Ghép hai cây lại với nhau theo công thức là có thể dung hợp ra một loài cây mới.",
    }
}

def apply_batch2():
    for mod, entries in BATCH_2.items():
        raw_p = RAW_DIR / f"{mod}.json"
        trans_p = TRANS_DIR / f"{mod}.json"
        
        with open(raw_p, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        with open(trans_p, 'r', encoding='utf-8') as f:
            trans_dict = json.load(f)
            
        added_count = 0
        for k, v in entries.items():
            if isinstance(raw_data, dict):
                if k not in raw_data:
                    raw_data[k] = ""
            elif isinstance(raw_data, list):
                if k not in raw_data:
                    raw_data.append(k)
            trans_dict[k] = v
            added_count += 1
            
        with open(raw_p, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=2)
        with open(trans_p, 'w', encoding='utf-8') as f:
            json.dump(trans_dict, f, ensure_ascii=False, indent=2)
            
        print(f"[✓] {mod}: added/updated {added_count} entries. Total raw: {len(raw_data)}, trans: {len(trans_dict)}")

if __name__ == '__main__':
    apply_batch2()
