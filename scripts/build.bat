@echo off
echo ========================================
echo  Comparador de Planilhas - Build
echo ========================================
echo.

echo [1/4] Verificando PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)
echo.

echo [2/4] Criando arquivo .spec...
pyi-makespec --onefile --windowed --name comparador --icon src/gui/resources/icons/app.ico src/main.py
echo.

echo [3/4] Gerando executável...
pyinstaller --onefile --windowed --name comparador --icon src/gui/resources/icons/app.ico src/main.py
echo.

echo [4/4] Build concluído!
echo.
echo 📁 Executável gerado em: dist\comparador.exe
echo.
echo Para testar: dist\comparador.exe
echo.
pause