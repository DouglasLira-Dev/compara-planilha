@echo off
echo ========================================
echo  Comparador de Planilhas - Build
echo ========================================
echo.

echo [1/3] Instalando PyInstaller...
pip install pyinstaller
echo.

echo [2/3] Gerando executável...
pyinstaller --onefile --windowed --name comparador --icon src/gui/resources/icons/app.ico src/main.py
echo.

echo [3/3] Build concluído!
echo.
echo Executável gerado em: dist\comparador.exe
echo.
pause