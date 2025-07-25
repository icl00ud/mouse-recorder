@echo off
echo Construindo executavel do Mouse Recorder...
echo.

REM Criar icone
echo [1/4] Criando icone...
python create_icon.py

REM Instalar PyInstaller se necessario
echo [2/4] Verificando PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

REM Limpar builds anteriores
echo [3/4] Limpando builds anteriores...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM Construir executavel
echo [4/4] Construindo executavel...
pyinstaller --onefile --windowed --name="MouseRecorder" --icon=icon.ico --add-data "advanced_settings.py;." --add-data "utils.py;." --hidden-import=pynput --hidden-import=tkinter --hidden-import=winsound mouse_recorder.py

echo.
if exist dist\MouseRecorder.exe (
    echo ✓ Executavel criado com sucesso em: dist\MouseRecorder.exe
    echo.
    echo Tamanho do arquivo:
    dir dist\MouseRecorder.exe | find "MouseRecorder.exe"
) else (
    echo ✗ Erro ao criar executavel
    exit /b 1
)

echo.
echo Pressione qualquer tecla para sair...
pause >nul
