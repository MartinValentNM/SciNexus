@echo off
chcp 65001 >nul
title SciNexus

:: Aktivace venv (pokud existuje)
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [UPOZORNENI] .venv nenalezeno — spoustim v systemovem Pythonu.
    echo              Doporucujeme nejprve spustit install.bat
    echo.
)

echo Spouštím SciNexus...
echo Aplikace bude dostupná na: http://localhost:8501
echo Pro ukončení stiskni Ctrl+C v tomto okně.
echo.
streamlit run scinexus.py --server.headless false --server.port 8501
