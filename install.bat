@echo off
chcp 65001 >nul
title SciNexus — Instalace

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║          SciNexus  — Instalace       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: ── Kontrola Pythonu ─────────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [CHYBA] Python nebyl nalezen. Nainstaluj Python 3.10+ z https://python.org
    pause
    exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo [OK] Python %PY_VER% nalezen.
echo.

:: ── Vytvoření virtuálního prostředí ──────────────────────────────────────────
if not exist ".venv\" (
    echo [1/4] Vytvářím virtuální prostředí (.venv) ...
    python -m venv .venv
    if errorlevel 1 (
        echo [CHYBA] Nepodařilo se vytvořit venv.
        pause
        exit /b 1
    )
    echo [OK] Virtuální prostředí vytvořeno.
) else (
    echo [1/4] Virtuální prostředí (.venv) již existuje, přeskakuji.
)
echo.

:: ── Aktivace venv ─────────────────────────────────────────────────────────────
call .venv\Scripts\activate.bat
echo [2/4] Virtuální prostředí aktivováno.
echo.

:: ── Aktualizace pip ──────────────────────────────────────────────────────────
echo [3/4] Aktualizuji pip ...
python -m pip install --upgrade pip --quiet
echo [OK] pip aktualizován.
echo.

:: ── Instalace závislostí ─────────────────────────────────────────────────────
echo [4/4] Instaluji závislosti z requirements.txt ...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [CHYBA] Instalace selhala. Zkontroluj připojení k internetu a výpis výše.
    pause
    exit /b 1
)
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              Instalace dokončena úspěšně!                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Pro spuštění aplikace použij:
echo   run.bat
echo nebo ručně:
echo   .venv\Scripts\activate
echo   streamlit run scinexus.py
echo.
pause
