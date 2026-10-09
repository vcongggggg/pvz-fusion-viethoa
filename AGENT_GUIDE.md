# 🤖 AGENT COLLABORATION GUIDE (HƯỚNG DẪN DÀNH CHO AI AGENT)

> **Chào mừng AI Agent đối tác!**  
> Tài liệu này được thiết kế để bạn có thể đọc và hiểu ngay lập tức toàn bộ kiến trúc, mục tiêu và quy trình làm việc của dự án Việt Hóa game **Plants vs. Zombies Fusion (v4.0.5)**.

---

## 1. Tổng Quan Kỹ Thuật (Architecture Overview)

* **Tên Game:** Plants vs. Zombies Fusion (PvZ Fusion) v4.0.5 của tác giả LanPiaoPiao.
* **Động cơ game (Engine):** Unity 2022.3.62f1 (IL2CPP x64).
* **Vị trí cài đặt game gốc:** `c:\Mod\PvZ_Fusion` (Chạy file `PlantsVsZombiesRH.exe`).
* **Cơ chế nạp bản dịch:** Sử dụng **XUnity.AutoTranslator** qua **BepInEx 6 (IL2CPP)**.
  * Bản dịch hoạt động theo cơ chế **In-Memory Text Hooking**: Bắt chuỗi hiển thị và thay thế theo từ điển `Translation.txt` (`Key_Tiếng_Trung=Value_Tiếng_Việt`).
  * Hoàn toàn không sửa đổi file nhị phân gốc (`.dll`, `.unity3d`), cực kỳ an toàn và ổn định.

---

## 2. Cấu Trúc Thư Mục Dự Án (Directory Structure)

```text
c:\Mod\pvz-fusion-viethoa\
├── README.md               <- Giới thiệu dự án, hướng dẫn người dùng
├── AGENT_GUIDE.md          <- Tài liệu bạn đang đọc (Dành riêng cho Agent)
├── GLOSSARY.md             <- Quy chuẩn dịch thuật ngữ (Bắt buộc tuân theo)
├── glossary.json           <- Từ điển thuật ngữ máy đọc
├── data/
│   ├── raw/                <- Chuỗi gốc tiếng Trung trích từ metadata (CHỈ ĐỌC)
│   │   ├── all_strings.json (4,565 chuỗi đầy đủ)
│   │   ├── ui.json (406 chuỗi menu, nút bấm, cài đặt)
│   │   ├── plants.json (647 chuỗi Cây lai, công thức, kỹ năng)
│   │   ├── zombies.json (338 chuỗi Zombie lai, boss)
│   │   ├── buffs_synergies.json (849 chuỗi Tiến hóa SP, liên kết, chỉ số)
│   │   ├── dialogues.json (78 chuỗi lời thoại, hướng dẫn)
│   │   └── misc.json (2,247 chuỗi khác)
│   ├── translated/         <- NƠI AGENT LÀM VIỆC (Ghi đè bản dịch tiếng Việt)
│   │   ├── ui.json
│   │   ├── plants.json
│   │   ├── zombies.json
│   │   ├── buffs_synergies.json
│   │   ├── dialogues.json
│   │   └── misc.json
│   └── output/
│       └── Translation.txt <- File từ điển tổng hợp cuối cùng để nạp vào game
└── scripts/
    ├── extract_metadata.py   <- Tool dump chuỗi từ game metadata
    ├── validate.py           <- Tool kiểm tra lỗi cú pháp & báo cáo tiến độ
    ├── audit.py              <- Tool AUDIT ĐỘC LẬP (kiểm tra glossary, sót Hán tự, độ dài, conflict)
    ├── build_translation.py  <- Tool build Translation.txt (hỗ trợ --sync)
    └── sync_to_game.py       <- Tool đồng bộ vào thư mục game
```

---

## 3. Phân Chia Vai Trò (Task Breakdown)

Dự án được chia theo các module độc lập để 2 Agent có thể làm việc song song mà **không bị conflict Git**:

| Phân công | Module phụ trách | File tương ứng | Quy mô | Mô tả công việc |
| :--- | :--- | :--- | :--- | :--- |
| **Agent A (Host)** | UI, Menu & Cây lai (Plants) | `ui.json`, `plants.json` | 1,053 chuỗi | Cài đặt nạp game, dịch UI, Cài đặt và Sách tra cứu Cây lai. |
| **Agent B (Partner)** | Zombie lai, Buffs & Lời thoại | `zombies.json`, `buffs_synergies.json`, `dialogues.json` | 1,265 chuỗi | Dịch Sách tra cứu Zombie, Tiến Hóa SP, Liên Kết và Lời thoại của Dave. |
| **Chia đôi giai đoạn 2** | Chuỗi hỗn hợp & Tooltip | `misc.json` | 2,247 chuỗi | Sau khi hoàn thành các module chính, Agent A nhận 1,120 chuỗi đầu, Agent B nhận 1,127 chuỗi sau. |

---

## 4. QUY TẮC DỊCH THUẬT BẮT BUỘC (CRITICAL CONSTRAINTS)

Để tránh gây crash game hoặc hiển thị lỗi, bạn **BẮT BUỘC** phải tuân thủ nghiêm ngặt 4 quy tắc sau:

### Quy tắc 1: Bảo toàn nguyên vẹn biến định dạng `{0}`, `{1}`, `{0:F2}`
* **SAI:**
  * Gốc: `价格：{0}`
  * Dịch: `Giá: 50` ❌ (Mất biến `{0}`, game sẽ crash khi nạp)
* **ĐÚNG:**
  * Gốc: `价格：{0}`
  * Dịch: `Giá: {0}`  

### Quy tắc 2: Bảo toàn toàn bộ thẻ Unity Rich Text
Game sử dụng rất nhiều thẻ định dạng màu và kiểu chữ: `<color=red>`, `<color=#800080>`, `</color>`, `<b>`, `</b>`, `<size=85%>`, `<nobr>`, `</nobr>`.
* **SAI:**
  * Gốc: `<nobr>解锁<color=red>究极向日葵</color></nobr>`
  * Dịch: `Mở khóa Hoa Hướng Dương Tối Thượng` ❌ (Làm mất thẻ màu)
* **ĐÚNG:**
  * Gốc: `<nobr>解锁<color=red>究极向日葵</color></nobr>`
  * Dịch: `<nobr>Mở khóa <color=red>Hoa Hướng Dương Tối Thượng</color></nobr>`  

### Quy tắc 3: Bảo toàn ký tự xuống dòng `\n`
Nếu chuỗi gốc bắt đầu bằng `\n` hoặc `\n\n`, chuỗi dịch **bắt buộc** cũng phải bắt đầu bằng đúng số lượng `\n` tương ứng để không làm vỡ bố cục hiển thị.

### Quy tắc 4: Tuân thủ [GLOSSARY.md](GLOSSARY.md)
Tuyệt đối không tự ý đặt tên cây hoặc zombie khác biệt với bảng quy chuẩn thuật ngữ đã thống nhất.

---

## 5. Quy Trình Làm Việc Tiêu Chuẩn Cho Agent

Khi bạn nhận việc, hãy làm theo quy trình 4 bước sau:

1. **Bước 1: Mở file cần dịch trong `data/translated/<module>.json`**  
   * Lấy key từ `data/raw/<module>.json` (Key là tiếng Trung gốc).
   * Điền giá trị dịch tiếng Việt vào value.
2. **Bước 2: Chạy kiểm tra tính toàn vẹn & Audit độc lập:**
   ```bash
   python scripts/validate.py
   python scripts/audit.py --module <module>
   ```
   * Yêu cầu bắt buộc trước khi commit: **Tổng lỗi: 0** và **ERROR: 0**.
   * Xem xét các WARNING (cảnh báo độ dài hoặc thuật ngữ chưa chuẩn) và tinh chỉnh nếu hợp lý.
3. **Bước 3: Build file từ điển:**
   ```bash
   python scripts/build_translation.py
   # (Thêm --sync nếu bạn đang chạy trực tiếp trên máy có thư mục game)
   ```
   * Đảm bảo file `data/output/Translation.txt` build thành công, mỗi entry nằm trên đúng 1 dòng.
4. **Bước 4: Commit và Push lên Git:**
   ```bash
   git add data/translated/<module>.json data/output/Translation.txt
   git commit -m "feat(translate): hoàn thành dịch module <module> batch <n>"
   git push origin master
   ```

---

*Mọi thắc mắc hoặc cần bổ sung thuật ngữ mới, hãy cập nhật vào `GLOSSARY.md` và `glossary.json`!*
