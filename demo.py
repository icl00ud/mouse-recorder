"""
Demo Script - Mouse Recorder
Demonstra o uso programático das classes do Mouse Recorder
"""

from mouse_recorder import RecordingSession, PlaybackSession, SettingsManager
import time
import json

def demo_recording():
    """Demonstração de gravação programática"""
    print("=== Demo - Gravação Programática ===")
    
    # Cria sessão de gravação
    session = RecordingSession()
    
    print("Iniciando gravação em 3 segundos...")
    print("Mova o mouse e clique durante 5 segundos!")
    
    # Delay inicial
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Inicia gravação
    session.start_recording()
    print("🔴 GRAVANDO! (5 segundos)")
    
    # Grava por 5 segundos
    time.sleep(5)
    
    # Para gravação
    session.stop_recording()
    print("⏹️ Gravação finalizada!")
    
    # Mostra estatísticas
    print(f"Eventos capturados: {len(session.events)}")
    print(f"Duração: {session.get_duration():.2f} segundos")
    
    # Salva em arquivo de demo
    recording_data = session.to_dict("Demo_Recording")
    with open("demo_recording.json", "w", encoding="utf-8") as f:
        json.dump(recording_data, f, indent=2, ensure_ascii=False)
    
    print("Gravação salva em: demo_recording.json")
    return recording_data

def demo_playback(recording_data):
    """Demonstração de reprodução programática"""
    print("\n=== Demo - Reprodução Programática ===")
    
    events = recording_data.get("events", [])
    if not events:
        print("Nenhum evento para reproduzir!")
        return
    
    print("Iniciando reprodução em 3 segundos...")
    
    # Delay inicial
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Cria sessão de reprodução
    playback = PlaybackSession(events, speed_multiplier=1.0)
    
    def progress_callback(current_rep, total_rep, progress):
        """Callback de progresso"""
        print(f"Repetição {current_rep}/{total_rep} - {progress*100:.1f}%")
    
    def complete_callback():
        """Callback de conclusão"""
        print("✅ Reprodução concluída!")
    
    # Inicia reprodução
    print("▶️ REPRODUZINDO!")
    playback.play(
        repetitions=2,
        callback_progress=progress_callback,
        callback_complete=complete_callback
    )
    
    # Aguarda conclusão
    while playback.is_playing:
        time.sleep(0.1)

def demo_settings():
    """Demonstração do gerenciador de configurações"""
    print("\n=== Demo - Configurações ===")
    
    # Cria gerenciador de configurações
    settings = SettingsManager("demo_settings.json")
    
    # Mostra configurações atuais
    print("Configurações atuais:")
    for key, value in settings.settings.items():
        print(f"  {key}: {value}")
    
    # Modifica algumas configurações
    settings.set("initial_delay", 5.0)
    settings.set("default_speed", 2.0)
    settings.set("custom_setting", "valor_personalizado")
    
    print("\nConfigurações modificadas e salvas!")
    
    # Verifica se foram salvas
    new_settings = SettingsManager("demo_settings.json")
    print(f"Nova configuração de delay: {new_settings.get('initial_delay')}")
    print(f"Nova configuração de velocidade: {new_settings.get('default_speed')}")

def main():
    """Função principal do demo"""
    print("🖱️ Mouse Recorder - Demo Script")
    print("Este script demonstra o uso programático das classes")
    print()
    
    try:
        # Demo de configurações
        demo_settings()
        
        # Demo de gravação
        recording_data = demo_recording()
        
        # Demo de reprodução
        demo_playback(recording_data)
        
        print("\n🎉 Demo concluído com sucesso!")
        print("Arquivos gerados:")
        print("  - demo_recording.json")
        print("  - demo_settings.json")
        
    except KeyboardInterrupt:
        print("\n❌ Demo interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante demo: {e}")

if __name__ == "__main__":
    main()
