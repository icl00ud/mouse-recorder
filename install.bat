@echo off
echo Instalando dependencias do Mouse Recorder...
echo.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Instalacao concluida!
echo Para executar a aplicacao, use: python mouse_recorder.py
pause
