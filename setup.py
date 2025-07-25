#!/usr/bin/env python3
"""
Configuração inicial e instalação de dependências
"""
import subprocess
import sys
import os

def install_dependencies():
    """Instala as dependências necessárias"""
    try:
        print("Instalando dependências...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import pynput
        import tkinter
        print("✅ Todas as dependências estão disponíveis!")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

def main():
    print("=== Mouse Recorder - Setup ===")
    print()
    
    if not check_dependencies():
        print("Instalando dependências automaticamente...")
        if install_dependencies():
            if check_dependencies():
                print()
                print("🎉 Setup concluído com sucesso!")
                print("Execute 'python mouse_recorder.py' para iniciar a aplicação.")
            else:
                print("❌ Erro na verificação pós-instalação.")
        else:
            print("❌ Falha na instalação. Execute manualmente:")
            print("pip install -r requirements.txt")
    else:
        print("🎉 Tudo pronto! Execute 'python mouse_recorder.py' para iniciar.")

if __name__ == "__main__":
    main()
