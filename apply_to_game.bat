@echo off
chcp 65001 >nul
echo ========================================================
echo  ĐANG BUILD VÀ NẠP BẢN DỊCH VIỆT HÓA VÀO PVZ FUSION
echo ========================================================
python "%~dp0scripts\build_translation.py" --sync
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [THÀNH CÔNG] Bản dịch đã được nạp vào game!
) else (
    echo.
    echo [LỖI] Quá trình build thất bại, vui lòng kiểm tra lại Python!
)
pause
