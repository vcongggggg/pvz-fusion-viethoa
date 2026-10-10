# BÁO CÁO KỸ THUẬT: SỰ CỐ KHÔNG HIỂN THỊ VIỆT HÓA TRONG GAME (HOOKING ISSUE)

> **Dự án:** Việt Hóa Plants vs. Zombies Fusion v4.0.5  
> **Người lập báo cáo:** Agent Dịch thuật & Triển khai Mod  
> **Thời gian:** 10/10/2026  
> **Trạng thái:** Dữ liệu dịch hoàn tất 100% (4.598 chuỗi), nhưng game chưa áp dụng được text dịch vào runtime.

---

## 1. Môi trường & Thông số Game
* **Tựa game:** Plants vs. Zombies Fusion (PlantsVsZombiesRH.exe) v4.0.5
* **Unity Version:** `2022.3.62f1c1` (64-bit)
* **Backend:** `IL2CPP`
* **Metadata Version:** `31.1` (Yêu cầu Cpp2IL v2022.1.0-pre.21 trở lên)

---

## 2. Dữ liệu bản dịch đã sẵn sàng
* **File nguồn:** `data/translated/*.json` (ui, plants, zombies, buffs_synergies, dialogues, misc)
* **Tổng số chuỗi đã dịch:** **4.598 chuỗi** (đã bao gồm toàn bộ menu chính, bảng thông báo cập nhật, Đồ Giám, lời thoại).
* **Kiểm tra chất lượng:**
  * `scripts/validate.py`: **0 lỗi cú pháp**, bảo toàn 100% biến `{0}`, thẻ màu `<color>`.
  * `scripts/audit.py`: **0 ERROR** (PASS tiêu chuẩn).
* **File build hoàn chỉnh:** `data/output/Translation.txt` (đã format đúng chuẩn `Gốc=Dịch`).

---

## 3. Bản chất nguyên nhân kỹ thuật gặp phải (The Root Cause)

### Vấn đề 1: BepInEx 6 IL2CPP bị crash ngay từ đầu
* Ban đầu dự án thử dùng `BepInEx-Unity.IL2CPP-win-x64-6.0.0-pre.2`.
* **Kết quả:** Bị crash văng game với mã lỗi `0xe0434352`.
* **Nguyên nhân:** Cpp2IL đi kèm của BepInEx 6 pre-2 chỉ hỗ trợ Unity metadata từ `v23 đến v29`. Game PvZ Fusion v4.0.5 sử dụng **metadata v31**, khiến Cpp2IL văng exception.

### Vấn đề 2: Chuyển sang MelonLoader v0.7.3 giải quyết được metadata v31 nhưng AutoTranslator không hook được TextMeshPro
* Đã cài đặt thành công **MelonLoader v0.7.3 Open-Beta** + runtime **.NET 6**.
* Cpp2IL của MelonLoader đã dump thành công 72 file DLL và sinh toàn bộ assemblies trong `MelonLoader/Il2CppAssemblies/` (Bao gồm `Unity.TextMeshPro.dll`, `UnityEngine.UI.dll`, `Assembly-CSharp.dll`).
* Cài đặt mod dịch: `XUnity.AutoTranslator-MelonMod-IL2CPP-5.6.2`.
* Cấu hình [AutoTranslator/Config.ini]:
  * `Language=vi`
  * `FromLanguage=zh`
  * `Directory=Translation\{Lang}\Text`
  * `EnableUGUI=True`, `EnableTextMeshPro=True`, `EnableIMGUI=False`
  * `OverrideFont=Arial`

### HIỆN TƯỢNG LỖI CỤ THỂ TRONG LOG:
Khi vào game, log của MelonLoader ghi nhận:
```log
[07:12:32.298] Hooked UnityEngine.UI.Text.set_text through Harmony hooks.
[07:12:32.315] Hooked UnityEngine.UI.Text.OnEnable through Harmony hooks.
[07:12:32.333] Hooked UnityEngine.UIElements.TextElement.set_text through Harmony hooks.
...
[07:12:32.482] --- Loading Global Translations ---
[07:12:32.503] Loaded translation text files (took 0.02 seconds)
[07:12:32.528] Loaded XUnity.AutoTranslator into Unity [2022.3.62f1c1] game.
...
[07:12:43.988] Toggling translations of 0 objects.
```

👉 **ĐIỂM NGHẼN:**
1. Game PvZ Fusion sử dụng **TextMeshPro (`TMPro.TMP_Text` / `TMPro.TextMeshProUGUI`)** cho 100% giao diện (Menu chính, nút bấm, bảng thông báo, Đồ Giám Cây, Đồ Giám Zombie).
2. `XUnity.AutoTranslator 5.6.2` chỉ hook được `UnityEngine.UI.Text` và `UnityEngine.UIElements.TextElement`. Nó **HOÀN TOÀN BỎ QUA không hook TextMeshPro**.
3. Do đó, khi bấm `Alt + T` hoặc khi game render, log thông báo `Toggling translations of 0 objects` — không có bất kỳ component text nào được nạp vào bộ xử lý dịch, dẫn đến toàn bộ màn hình 100% vẫn là tiếng Trung.

---

## 4. Đề xuất phương án giải quyết (Cần Agent / Reviewer phối hợp)

### Phương án A: Fix hook TextMeshPro cho XUnity AutoTranslator trên Unity 2022.3 IL2CPP
* Kiểm tra xem XUnity AutoTranslator 5.6.2 IL2CPP tại sao không nhận diện được `TMP_Text` trong `Unity.TextMeshPro.dll`.
* Có cần patch thêm plugin / wrapper chuyên dụng cho TextMeshPro của MelonLoader không?

### Phương án B: Viết một MelonMod C# độc lập cực kỳ nhỏ gọn (Lightweight Native Translator)
* Thay vì phụ thuộc vào toàn bộ bộ thư viện cồng kềnh của XUnity AutoTranslator:
  * Viết 1 file C# plugin MelonMod:
    * Khi game load, đọc file `Translation.txt` vào `Dictionary<string, string>`.
    * Dùng Harmony hook trực tiếp vào `TMPro.TMP_Text.set_text(string value)` và `TMPro.TMP_Text.text`.
    * Nếu text đưa vào nằm trong Dictionary thì gán bằng chuỗi tiếng Việt.
  * Vì `Unity.TextMeshPro.dll` đã được MelonLoader sinh sẵn trong `Il2CppAssemblies/`, việc hook trực tiếp qua Harmony của MelonLoader rất sạch sẽ, nhẹ và tránh được toàn bộ lỗi tương thích của AutoTranslator.

### Phương án C: Cập nhật Cpp2IL của BepInEx 6 để dùng BepInEx
* Nếu BepInEx 6 có bản build CI mới nhất hỗ trợ metadata 31, quay lại BepInEx với XUnity.AutoTranslator-BepInEx-IL2CPP.

---
*Vui lòng xem log chi tiết tại `MelonLoader/Latest.log` trên máy hoặc trao đổi thêm giải pháp xử lý.*
