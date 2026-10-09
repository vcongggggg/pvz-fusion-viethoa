# 🌻 PLANTS VS. ZOMBIES FUSION - DỰ ÁN VIỆT HÓA TOÀN DIỆN (v4.0.5)

[![Game Version](https://img.shields.io/badge/Game-PvZ_Fusion_v4.0.5-brightgreen.svg)]()
[![Engine](https://img.shields.io/badge/Engine-Unity_2022.3_IL2CPP-blue.svg)]()
[![Status](https://img.shields.io/badge/Status-In_Progress-orange.svg)]()
[![Translation Tool](https://img.shields.io/badge/Hook-XUnity.AutoTranslator-purple.svg)]()

> **Dự án Việt Hóa mã nguồn mở dành riêng cho phiên bản Plants vs. Zombies Fusion (v4.0.5) của tác giả LanPiaoPiao.**  
> Hỗ trợ hợp tác dịch thuật song song giữa các AI Agent thông qua Git.

---

## 📌 Điểm Nổi Bật

* **Không can thiệp file nhị phân gốc:** Sử dụng cơ chế hook bộ nhớ qua BepInEx 6 IL2CPP + XUnity.AutoTranslator, đảm bảo không hỏng game, không xung đột khi cập nhật.
* **Hỗ trợ đầy đủ Font tiếng Việt:** Tích hợp bộ font Fallback chống lỗi ô vuông `□` và lỗi mất dấu.
* **Quy chuẩn hóa thuật ngữ:** Bảng [GLOSSARY.md](GLOSSARY.md) chi tiết cho hơn 100 loại Cây lai (Fusion Plants), Zombie lai và cơ chế Tiến hóa SP.
* **Tự động hóa hoàn toàn:** Có sẵn bộ công cụ trích xuất metadata, kiểm tra biến format `{0}` và xuất file từ điển tự động.

---

## 📂 Cấu Trúc Dự Án

```text
├── AGENT_GUIDE.md          # Hướng dẫn chi tiết cho AI Agent cộng tác
├── GLOSSARY.md             # Bảng quy chuẩn dịch thuật ngữ (Plants, Zombies, Buffs)
├── glossary.json           # Dữ liệu thuật ngữ máy đọc
├── data/
│   ├── raw/                # Chuỗi tiếng Trung gốc trích xuất từ metadata
│   ├── translated/         # Các module đã được dịch tiếng Việt
│   └── output/             # File Translation.txt tổng hợp để nạp vào game
├── scripts/
│   ├── extract_metadata.py # Trích xuất chuỗi từ global-metadata.dat
│   ├── validate.py         # Kiểm tra lỗi cú pháp và tính toán % tiến độ
│   └── build_translation.py# Ghép file từ điển và đồng bộ vào game
└── apply_to_game.bat       # Phím tắt 1-click để build và nạp bản dịch vào game
```

---

## 🎮 Cách Cài Đặt Bản Dịch Vào Game

1. Đảm bảo game đã được cài tại thư mục `c:\Mod\PvZ_Fusion`.
2. Mở file `apply_to_game.bat` hoặc chạy lệnh:
   ```bash
   python scripts/build_translation.py --sync
   ```
3. Khởi động game qua `Choi_Game_Co_AI.bat` hoặc `PlantsVsZombiesRH.exe`. Game sẽ tự động nạp ngôn ngữ tiếng Việt từ file từ điển.

---

## 🤖 Dành Cho AI Agent & Cộng Tác Viên

Nếu bạn là AI Agent kết nối vào dự án này để hỗ trợ dịch thuật, vui lòng đọc ngay tài liệu **[AGENT_GUIDE.md](AGENT_GUIDE.md)** để nắm rõ quy trình làm việc, phân công nhiệm vụ và các quy tắc cú pháp bắt buộc.
