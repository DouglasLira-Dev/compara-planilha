@echo off
echo ========================================
echo  Comparador de Planilhas - Build
echo ========================================
echo.

echo [1/5] Removendo builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist comparador.spec del comparador.spec
echo.

echo [2/5] Verificando dependências...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)
echo.

echo [3/5] Instalando dependências necessárias...
pip install PyQt6 pandas openpyxl pydantic python-dateutil python-dotenv loguru cryptography xlrd
echo.

echo [4/5] Gerando executável com PyQt6...
pyinstaller --onefile --windowed --name comparador ^
    --hidden-import PyQt6 ^
    --hidden-import PyQt6.QtCore ^
    --hidden-import PyQt6.QtGui ^
    --hidden-import PyQt6.QtWidgets ^
    --hidden-import pandas ^
    --hidden-import openpyxl ^
    --hidden-import pydantic ^
    --hidden-import dateutil ^
    --hidden-import dotenv ^
    --hidden-import loguru ^
    --hidden-import cryptography ^
    --hidden-import xlrd ^
    --collect-all PyQt6 ^
    src/main.py
echo.

echo [5/5] Build concluído!
echo.
echo 📁 Executável gerado em: dist\comparador.exe
echo.
echo Para testar: dist\comparador.exe
echo.
pause