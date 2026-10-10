import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
raw_file = ROOT_DIR / "data" / "raw" / "plants.json"
trans_file = ROOT_DIR / "data" / "translated" / "plants.json"

with open(raw_file, 'r', encoding='utf-8') as f:
    raw = json.load(f)
with open(trans_file, 'r', encoding='utf-8') as f:
    trans = json.load(f)

# Descriptions for basic plants
plant_descs = {
    # Peashooter
    "<color=#0E276C>豌豆射手发射豌豆来攻击僵尸，是你的第一道防线。\n\n<color=#3D1400>伤害：</color><color=red>20/1.5秒</color></color>\n\n<color=#3D1400>一株植物，怎么能这么高效的产出如此多的豌豆并发射呢？豌豆射手说：“全靠努力工作，奉献自我，以及阳光和高纤维二氧化碳均衡搭配的健康早餐。”</color>\n\n花费：<color=red>100</color>\n冷却时间：<color=red>7.5秒</color>":
    "<color=#0E276C>Đậu Bắn Súng bắn đậu để tấn công Zombie, là tuyến phòng thủ đầu tiên của bạn.\n\n<color=#3D1400>Sát thương: </color><color=red>20/1.5 giây</color></color>\n\n<color=#3D1400>Một loài thực vật, làm sao có thể sản sinh và bắn ra nhiều hạt đậu hiệu quả đến vậy? Đậu Bắn Súng nói: \"Tất cả là nhờ chăm chỉ làm việc, cống hiến hết mình, cùng bữa sáng lành mạnh kết hợp cân bằng giữa ánh sáng mặt trời và carbon dioxide giàu chất xơ.\"</color>\n\nChi phí: <color=red>100</color>\nThời gian hồi: <color=red>7.5 giây</color>",

    # Sunflower
    "<color=#0E276C>向日葵是生产额外阳光的关键，尽可能多的种植吧！\n\n<color=#3D1400>阳光产量：</color><color=red>25/25秒</color>\n<color=#3D1400>特点：</color><color=red>向日葵类植物出场4~7秒后首次生产</color></color>\n\n<color=#3D1400>向日葵情不自禁的随着节拍摇摆。是什么节拍呢？嗨，是大地那唤醒生机的爵士节拍。这种频率的节拍，只有向日葵才能听到。</color>\n\n花费：<color=red>50</color>\n冷却时间：<color=red>7.5秒</color>":
    "<color=#0E276C>Hoa Hướng Dương là chìa khóa để sản sinh thêm ánh sáng, hãy trồng càng nhiều càng tốt!\n\n<color=#3D1400>Sản lượng Nắng: </color><color=red>25/25 giây</color>\n<color=#3D1400>Đặc điểm: </color><color=red>Cây hệ Hướng Dương xuất hiện 4~7 giây sau sẽ sản sinh lần đầu</color></color>\n\n<color=#3D1400>Hoa Hướng Dương bất giác đung đưa theo điệu nhạc. Đó là nhịp điệu gì? Ha, chính là nhịp jazz đánh thức sự sống của đất mẹ. Tần số nhịp điệu này chỉ Hoa Hướng Dương mới có thể lắng nghe.</color>\n\nChi phí: <color=red>50</color>\nThời gian hồi: <color=red>7.5 giây</color>",

    # Cherry Bomb
    "<color=#0E276C>樱桃炸弹可以造成爆炸，消灭周围的僵尸。\n\n<color=#3D1400>伤害：</color><color=red>1800（灰烬）</color>\n<color=#3D1400>范围：</color><color=red>3×3（半径1.5格的圆）</color></color>\n\n<color=#3D1400>“我想要爆开。”樱桃一号说。“不，还是让我们炸开吧！”他弟弟樱桃二号说。经过激烈磋商，他们统一达成了“造成爆炸”这个说法。</color>\n\n花费：<color=red>150</color>\n冷却时间：<color=red>50秒</color>":
    "<color=#0E276C>Bom Anh Đào có thể tạo ra vụ nổ, tiêu diệt zombie xung quanh.\n\n<color=#3D1400>Sát thương: </color><color=red>1800 (Tro tàn)</color>\n<color=#3D1400>Phạm vi: </color><color=red>3×3 (hình tròn bán kính 1.5 ô)</color></color>\n\n<color=#3D1400>\"Tôi muốn nổ tung.\" Anh Đào số một nói. \"Không, hãy để chúng ta nổ tung đi!\" em trai Anh Đào số hai nói. Sau khi thương lượng gay gắt, cả hai đã thống nhất cách gọi \"tạo ra vụ nổ\".</color>\n\nChi phí: <color=red>150</color>\nThời gian hồi: <color=red>50 giây</color>",

    # Wall-nut
    "<color=#0E276C>坚果有坚硬的外壳，可以用于保护其他植物。\n\n<color=#3D1400>韧性：</color><color=red>4000</color>\n<color=#3D1400>特点：</color><color=red>难度5以下能防止爆炸樱桃产生溅射，融合后保留该特点</color></color>\n\n<color=#3D1400>“有人想知道经常被僵尸啃咬是什么感觉，”坚果说，“我比较钝感，只觉得麻麻的，就像是令人放松的背部按摩。”</color>\n\n花费：<color=red>50</color>\n冷却时间：<color=red>30秒</color>":
    "<color=#0E276C>Quả Óc Chó có lớp vỏ cứng chắc, có thể dùng để bảo vệ các loài thực vật khác.\n\n<color=#3D1400>Độ bền: </color><color=red>4000</color>\n<color=#3D1400>Đặc điểm: </color><color=red>Độ khó dưới 5 có thể ngăn nổ văng từ Bom Anh Đào, sau dung hợp vẫn giữ đặc điểm này</color></color>\n\n<color=#3D1400>\"Có người muốn biết cảm giác thường xuyên bị zombie cắn là như thế nào,\" Quả Óc Chó nói, \"Tôi khá chậm cảm giác, chỉ thấy tê tê, giống như một buổi massage lưng thư giãn vậy.\"</color>\n\nChi phí: <color=red>50</color>\nThời gian hồi: <color=red>30 giây</color>",

    # Potato Mine
    "<color=#0E276C>土豆雷蕴藏着强大威力，但需要时间来武装自己。出土后，接触僵尸时造成爆炸。\n\n<color=#3D1400>伤害：</color><color=red>1800</color>\n<color=#3D1400>范围：</color><color=red>半径0.74格（限1行）</color>\n<color=#3D1400>特性：</color><color=red>低矮</color>\n<color=#3D1400>特点：①</color><color=red>出场后，需要等待15~17秒才会出土（作为底座进行融合时，融合后的土豆雷类植物会继承已等待时间）</color>\n<color=#3D1400>②</color><color=red>出土后，接触僵尸时造成范围爆炸伤害</color></color>\n\n<color=#3D1400>有人说土豆雷很懒，因为他把事情都留到最后。土豆雷不予反驳，他忙着思考投资策略呢。</color>\n\n花费：<color=red>25</color>\n冷却时间：<color=red>30秒</color>":
    "<color=#0E276C>Mìn Khoai Tây chứa đựng uy lực mạnh mẽ, nhưng cần thời gian để tự vũ trang. Sau khi trồi lên, chạm vào zombie sẽ phát nổ.\n\n<color=#3D1400>Sát thương: </color><color=red>1800</color>\n<color=#3D1400>Phạm vi: </color><color=red>Bán kính 0.74 ô (giới hạn 1 hàng)</color>\n<color=#3D1400>Đặc tính: </color><color=red>Thấp bé</color>\n<color=#3D1400>Đặc điểm: ①</color><color=red>Sau khi ra trận, cần chờ 15~17 giây mới trồi lên (khi làm đế dung hợp, cây họ Mìn Khoai Tây sau dung hợp kế thừa thời gian đã chờ)</color>\n<color=#3D1400>②</color><color=red>Sau khi trồi lên, chạm vào zombie gây sát thương nổ diện rộng</color></color>\n\n<color=#3D1400>Có người nói Mìn Khoai Tây lười biếng vì hay để việc đến phút chót. Mìn Khoai Tây không phản bác, nó đang bận suy nghĩ chiến lược đầu tư cơ mà.</color>\n\nChi phí: <color=red>25</color>\nThời gian hồi: <color=red>30 giây</color>",
}

for k, v in plant_descs.items():
    raw[k] = ""
    trans[k] = v

with open(raw_file, 'w', encoding='utf-8') as f:
    json.dump(raw, f, ensure_ascii=False, indent=2)
with open(trans_file, 'w', encoding='utf-8') as f:
    json.dump(trans, f, ensure_ascii=False, indent=2)

print(f"Added {len(plant_descs)} plant descriptions to plants.json")
