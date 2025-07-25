@echo off
title Mouse Recorder - Inicializacao Rapida
color 0A

echo.
echo  ███╗   ███╗ ██████╗ ██╗   ██╗███████╗███████╗    
echo  ████╗ ████║██╔═══██╗██║   ██║██╔════╝██╔════╝    
echo  ██╔████╔██║██║   ██║██║   ██║███████╗█████╗      
echo  ██║╚██╔╝██║██║   ██║██║   ██║╚════██║██╔══╝      
echo  ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝███████║███████╗    
echo  ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝    
echo.
echo  ██████╗ ███████╗ ██████╗ ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
echo  ██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
echo  ██████╔╝█████╗  ██║     ██║   ██║██████╔╝██║  ██║█████╗  ██████╔╝
echo  ██╔══██╗██╔══╝  ██║     ██║   ██║██╔══██╗██║  ██║██╔══╝  ██╔══██╗
echo  ██║  ██║███████╗╚██████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
echo  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
echo.
echo  ===============================================================
echo   Mouse Recorder v1.0.0 - Automacao para Jogos
echo   Desenvolvido para a comunidade gamer
echo  ===============================================================
echo.

REM Verifica se Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python 3.7+ e tente novamente.
    echo Download: https://python.org/downloads
    pause
    exit /b 1
)

echo [INFO] Python encontrado: 
python --version

REM Verifica se as dependencias estao instaladas
echo [INFO] Verificando dependencias...
python -c "import pynput" >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Dependencia 'pynput' nao encontrada.
    echo [INFO] Instalando dependencias automaticamente...
    python -m pip install pynput
    if %errorlevel% neq 0 (
        echo [ERRO] Falha na instalacao das dependencias.
        echo Execute manualmente: pip install pynput
        pause
        exit /b 1
    )
)

echo [OK] Dependencias verificadas!
echo.

REM Executa a aplicacao
echo [INFO] Iniciando Mouse Recorder...
echo [DICA] Use F9 para gravar, F10 para reproduzir, ESC para parar
echo.
echo ===============================================================
echo.

python mouse_recorder.py

REM Se chegou ate aqui, a aplicacao foi fechada
echo.
echo ===============================================================
echo [INFO] Mouse Recorder foi fechado.
echo Obrigado por usar nossa aplicacao!
echo.
pause
