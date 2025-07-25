"""
Teste Rápido - Mouse Recorder
Verifica se todas as dependências estão funcionando corretamente
"""

def test_imports():
    """Testa todas as importações necessárias"""
    print("🔍 Testando importações...")
    
    try:
        import tkinter as tk
        print("  ✅ tkinter - OK")
    except ImportError as e:
        print(f"  ❌ tkinter - ERRO: {e}")
        return False
    
    try:
        from tkinter import ttk, filedialog, messagebox
        print("  ✅ tkinter.ttk - OK")
    except ImportError as e:
        print(f"  ❌ tkinter.ttk - ERRO: {e}")
        return False
    
    try:
        import json
        print("  ✅ json - OK")
    except ImportError as e:
        print(f"  ❌ json - ERRO: {e}")
        return False
    
    try:
        import time
        print("  ✅ time - OK")
    except ImportError as e:
        print(f"  ❌ time - ERRO: {e}")
        return False
    
    try:
        import threading
        print("  ✅ threading - OK")
    except ImportError as e:
        print(f"  ❌ threading - ERRO: {e}")
        return False
    
    try:
        from pynput import mouse, keyboard
        print("  ✅ pynput - OK")
    except ImportError as e:
        print(f"  ❌ pynput - ERRO: {e}")
        print("    Execute: pip install pynput")
        return False
    
    try:
        from pynput.mouse import Button, Listener as MouseListener
        print("  ✅ pynput.mouse - OK")
    except ImportError as e:
        print(f"  ❌ pynput.mouse - ERRO: {e}")
        return False
    
    try:
        from pynput.keyboard import Key, Listener as KeyboardListener
        print("  ✅ pynput.keyboard - OK")
    except ImportError as e:
        print(f"  ❌ pynput.keyboard - ERRO: {e}")
        return False
    
    try:
        import datetime
        print("  ✅ datetime - OK")
    except ImportError as e:
        print(f"  ❌ datetime - ERRO: {e}")
        return False
    
    try:
        import os
        print("  ✅ os - OK")
    except ImportError as e:
        print(f"  ❌ os - ERRO: {e}")
        return False
    
    try:
        import sys
        print("  ✅ sys - OK")
    except ImportError as e:
        print(f"  ❌ sys - ERRO: {e}")
        return False
    
    try:
        import winsound
        print("  ✅ winsound - OK")
    except ImportError as e:
        print(f"  ❌ winsound - ERRO: {e}")
        print("    winsound só funciona no Windows")
        return False
    
    try:
        from typing import List, Dict, Any, Optional
        print("  ✅ typing - OK")
    except ImportError as e:
        print(f"  ❌ typing - ERRO: {e}")
        return False
    
    try:
        import queue
        print("  ✅ queue - OK")
    except ImportError as e:
        print(f"  ❌ queue - ERRO: {e}")
        return False
    
    return True

def test_mouse_controller():
    """Testa o controlador do mouse"""
    print("\n🖱️ Testando controlador do mouse...")
    
    try:
        from pynput.mouse import Controller
        mouse_controller = Controller()
        
        # Testa posição atual
        pos = mouse_controller.position
        print(f"  ✅ Posição atual do mouse: {pos}")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro no controlador do mouse: {e}")
        return False

def test_keyboard_listener():
    """Testa o listener do teclado"""
    print("\n⌨️ Testando listener do teclado...")
    
    try:
        from pynput.keyboard import Listener as KeyboardListener
        
        def on_press(key):
            pass
        
        # Cria listener (mas não inicia)
        listener = KeyboardListener(on_press=on_press)
        print("  ✅ Listener do teclado criado com sucesso")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro no listener do teclado: {e}")
        return False

def test_tkinter_window():
    """Testa criação de janela tkinter"""
    print("\n🖼️ Testando interface gráfica...")
    
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # Cria janela de teste
        root = tk.Tk()
        root.title("Teste")
        root.geometry("300x200")
        
        # Adiciona alguns widgets
        label = ttk.Label(root, text="Teste da interface")
        label.pack(pady=20)
        
        button = ttk.Button(root, text="OK", command=root.destroy)
        button.pack()
        
        print("  ✅ Interface gráfica criada com sucesso")
        print("  📝 Feche a janela de teste que apareceu")
        
        # Mostra janela
        root.mainloop()
        
        return True
    except Exception as e:
        print(f"  ❌ Erro na interface gráfica: {e}")
        return False

def test_file_operations():
    """Testa operações de arquivo"""
    print("\n📁 Testando operações de arquivo...")
    
    try:
        import json
        import os
        
        # Testa escrita
        test_data = {
            "test": True,
            "timestamp": "2025-01-01T00:00:00",
            "events": []
        }
        
        with open("test_file.json", "w", encoding="utf-8") as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        print("  ✅ Arquivo de teste criado")
        
        # Testa leitura
        with open("test_file.json", "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        
        print("  ✅ Arquivo de teste lido")
        
        # Remove arquivo de teste
        os.remove("test_file.json")
        print("  ✅ Arquivo de teste removido")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro nas operações de arquivo: {e}")
        return False

def main():
    """Função principal do teste"""
    print("🧪 Mouse Recorder - Teste de Sistema")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Executa todos os testes
    tests = [
        test_imports,
        test_mouse_controller,
        test_keyboard_listener,
        test_file_operations,
        test_tkinter_window
    ]
    
    for test in tests:
        try:
            if not test():
                all_tests_passed = False
        except Exception as e:
            print(f"❌ Erro durante teste {test.__name__}: {e}")
            all_tests_passed = False
    
    print("\n" + "=" * 50)
    
    if all_tests_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O Mouse Recorder está pronto para uso")
        print("\nPara executar a aplicação:")
        print("  python mouse_recorder.py")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("🔧 Verifique as dependências e tente novamente")
        print("\nPara instalar dependências:")
        print("  pip install -r requirements.txt")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
