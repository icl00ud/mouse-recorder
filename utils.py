"""
Utilitários para Mouse Recorder
Funções auxiliares e ferramentas de suporte
"""

import json
import os
import datetime
from typing import Dict, List, Any, Tuple
import tkinter as tk
from tkinter import messagebox


class RecordingAnalyzer:
    """
    Analisador de gravações para estatísticas e otimizações
    Fornece insights sobre padrões de uso do mouse
    """
    
    def __init__(self, recording_data: Dict[str, Any]):
        self.data = recording_data
        self.events = recording_data.get("events", [])
        
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas detalhadas da gravação"""
        if not self.events:
            return {}
            
        stats = {
            "total_events": len(self.events),
            "duration": self.data.get("duration", 0),
            "event_types": {},
            "click_stats": {},
            "movement_stats": {},
            "scroll_stats": {},
            "timing_stats": {}
        }
        
        # Análise por tipo de evento
        for event in self.events:
            event_type = event.get("type", "unknown")
            stats["event_types"][event_type] = stats["event_types"].get(event_type, 0) + 1
            
        # Análise de cliques
        clicks = [e for e in self.events if e.get("type") == "click"]
        if clicks:
            left_clicks = len([c for c in clicks if c.get("button") == "left" and c.get("action") == "press"])
            right_clicks = len([c for c in clicks if c.get("button") == "right" and c.get("action") == "press"])
            middle_clicks = len([c for c in clicks if c.get("button") == "middle" and c.get("action") == "press"])
            
            stats["click_stats"] = {
                "total_clicks": left_clicks + right_clicks + middle_clicks,
                "left_clicks": left_clicks,
                "right_clicks": right_clicks,
                "middle_clicks": middle_clicks
            }
            
        # Análise de movimentos
        moves = [e for e in self.events if e.get("type") == "move"]
        if moves:
            distances = []
            for i in range(1, len(moves)):
                prev_x, prev_y = moves[i-1]["x"], moves[i-1]["y"]
                curr_x, curr_y = moves[i]["x"], moves[i]["y"]
                distance = ((curr_x - prev_x) ** 2 + (curr_y - prev_y) ** 2) ** 0.5
                distances.append(distance)
                
            if distances:
                stats["movement_stats"] = {
                    "total_movements": len(moves),
                    "total_distance": sum(distances),
                    "average_distance": sum(distances) / len(distances),
                    "max_distance": max(distances),
                    "min_distance": min(distances)
                }
                
        # Análise de timing
        if len(self.events) > 1:
            intervals = []
            for i in range(1, len(self.events)):
                interval = self.events[i]["timestamp"] - self.events[i-1]["timestamp"]
                intervals.append(interval)
                
            if intervals:
                stats["timing_stats"] = {
                    "average_interval": sum(intervals) / len(intervals),
                    "max_interval": max(intervals),
                    "min_interval": min(intervals),
                    "events_per_second": len(self.events) / self.data.get("duration", 1)
                }
                
        return stats
        
    def optimize_recording(self, remove_redundant_moves: bool = True) -> Dict[str, Any]:
        """
        Otimiza a gravação removendo eventos redundantes
        Melhora performance e reduz tamanho do arquivo
        """
        if not self.events:
            return self.data
            
        optimized_events = []
        last_move_pos = None
        
        for event in self.events:
            if event["type"] == "move" and remove_redundant_moves:
                # Remove movimentos redundantes para a mesma posição
                current_pos = (event["x"], event["y"])
                if current_pos != last_move_pos:
                    optimized_events.append(event)
                    last_move_pos = current_pos
            else:
                optimized_events.append(event)
                
        # Cria nova estrutura otimizada
        optimized_data = self.data.copy()
        optimized_data["events"] = optimized_events
        optimized_data["total_events"] = len(optimized_events)
        optimized_data["optimized"] = True
        optimized_data["optimization_date"] = datetime.datetime.now().isoformat()
        
        return optimized_data


class FileManager:
    """
    Gerenciador de arquivos para gravações
    Organiza e mantém histórico de gravações
    """
    
    def __init__(self, recordings_dir: str = "recordings"):
        self.recordings_dir = recordings_dir
        self.ensure_directory()
        
    def ensure_directory(self) -> None:
        """Garante que o diretório de gravações existe"""
        if not os.path.exists(self.recordings_dir):
            os.makedirs(self.recordings_dir)
            
    def list_recordings(self) -> List[Dict[str, Any]]:
        """Lista todas as gravações disponíveis"""
        recordings = []
        
        try:
            for filename in os.listdir(self.recordings_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.recordings_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        file_stats = os.stat(filepath)
                        recordings.append({
                            "filename": filename,
                            "filepath": filepath,
                            "name": data.get("name", filename),
                            "duration": data.get("duration", 0),
                            "total_events": data.get("total_events", 0),
                            "created_at": data.get("created_at", ""),
                            "file_size": file_stats.st_size,
                            "modified_at": datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                        })
                    except (json.JSONDecodeError, KeyError):
                        # Ignora arquivos inválidos
                        continue
                        
        except OSError:
            pass
            
        # Ordena por data de modificação (mais recente primeiro)
        recordings.sort(key=lambda x: x["modified_at"], reverse=True)
        return recordings
        
    def backup_recording(self, recording_data: Dict[str, Any], prefix: str = "backup") -> str:
        """Cria backup de uma gravação"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.json"
        filepath = os.path.join(self.recordings_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(recording_data, f, indent=2, ensure_ascii=False)
            
        return filepath
        
    def cleanup_old_files(self, max_files: int = 50, max_days: int = 30) -> int:
        """
        Remove arquivos antigos para economizar espaço
        Retorna número de arquivos removidos
        """
        recordings = self.list_recordings()
        removed_count = 0
        
        # Remove por quantidade
        if len(recordings) > max_files:
            excess_files = recordings[max_files:]
            for recording in excess_files:
                try:
                    os.remove(recording["filepath"])
                    removed_count += 1
                except OSError:
                    pass
                    
        # Remove por idade
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=max_days)
        for recording in recordings:
            try:
                modified_date = datetime.datetime.fromisoformat(recording["modified_at"])
                if modified_date < cutoff_date:
                    os.remove(recording["filepath"])
                    removed_count += 1
            except (ValueError, OSError):
                pass
                
        return removed_count


class HotkeyValidator:
    """
    Validador de hotkeys para evitar conflitos
    Verifica se combinações de teclas são válidas
    """
    
    VALID_KEYS = {
        'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
        'ESC', 'TAB', 'SPACE', 'ENTER', 'BACKSPACE', 'DELETE',
        'HOME', 'END', 'PAGEUP', 'PAGEDOWN', 'INSERT',
        'UP', 'DOWN', 'LEFT', 'RIGHT'
    }
    
    RESERVED_KEYS = {
        'CTRL+C', 'CTRL+V', 'CTRL+X', 'CTRL+Z', 'CTRL+Y',
        'ALT+F4', 'CTRL+ALT+DELETE', 'WIN+L'
    }
    
    @classmethod
    def validate_hotkey(cls, hotkey: str) -> Tuple[bool, str]:
        """
        Valida se uma hotkey é segura para uso
        Retorna (é_válida, mensagem)
        """
        if not hotkey:
            return False, "Hotkey não pode estar vazia"
            
        # Converte para maiúscula para padronização
        hotkey = hotkey.upper()
        
        # Verifica se é uma tecla reservada
        if hotkey in cls.RESERVED_KEYS:
            return False, f"Hotkey '{hotkey}' é reservada pelo sistema"
            
        # Verifica teclas individuais
        if hotkey in cls.VALID_KEYS:
            return True, "Hotkey válida"
            
        # Verifica combinações simples
        if '+' in hotkey:
            parts = hotkey.split('+')
            if len(parts) > 3:
                return False, "Combinação muito complexa"
                
            # Verifica modificadores válidos
            modifiers = parts[:-1]
            key = parts[-1]
            
            valid_modifiers = {'CTRL', 'ALT', 'SHIFT'}
            for modifier in modifiers:
                if modifier not in valid_modifiers:
                    return False, f"Modificador '{modifier}' inválido"
                    
            if key not in cls.VALID_KEYS:
                return False, f"Tecla '{key}' inválida"
                
            return True, "Combinação válida"
            
        return False, "Formato de hotkey inválido"


class PerformanceMonitor:
    """
    Monitor de performance para otimizar a aplicação
    Coleta métricas de uso e performance
    """
    
    def __init__(self):
        self.metrics = {
            "recording_sessions": 0,
            "playback_sessions": 0,
            "total_events_recorded": 0,
            "total_events_played": 0,
            "average_recording_duration": 0,
            "average_playback_duration": 0,
            "errors_count": 0,
            "last_session": None
        }
        self.load_metrics()
        
    def load_metrics(self) -> None:
        """Carrega métricas salvas"""
        try:
            if os.path.exists("performance_metrics.json"):
                with open("performance_metrics.json", 'r', encoding='utf-8') as f:
                    saved_metrics = json.load(f)
                    self.metrics.update(saved_metrics)
        except (json.JSONDecodeError, OSError):
            pass
            
    def save_metrics(self) -> None:
        """Salva métricas atuais"""
        try:
            with open("performance_metrics.json", 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2, ensure_ascii=False)
        except OSError:
            pass
            
    def record_recording_session(self, duration: float, events_count: int) -> None:
        """Registra uma sessão de gravação"""
        self.metrics["recording_sessions"] += 1
        self.metrics["total_events_recorded"] += events_count
        
        # Calcula nova média de duração
        total_duration = (self.metrics["average_recording_duration"] * 
                         (self.metrics["recording_sessions"] - 1) + duration)
        self.metrics["average_recording_duration"] = total_duration / self.metrics["recording_sessions"]
        
        self.metrics["last_session"] = {
            "type": "recording",
            "duration": duration,
            "events": events_count,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.save_metrics()
        
    def record_playback_session(self, duration: float, events_count: int, repetitions: int) -> None:
        """Registra uma sessão de reprodução"""
        self.metrics["playback_sessions"] += 1
        self.metrics["total_events_played"] += events_count * repetitions
        
        # Calcula nova média de duração
        total_duration = (self.metrics["average_playback_duration"] * 
                         (self.metrics["playback_sessions"] - 1) + duration)
        self.metrics["average_playback_duration"] = total_duration / self.metrics["playback_sessions"]
        
        self.metrics["last_session"] = {
            "type": "playback",
            "duration": duration,
            "events": events_count,
            "repetitions": repetitions,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.save_metrics()
        
    def record_error(self, error_type: str, error_message: str) -> None:
        """Registra um erro"""
        self.metrics["errors_count"] += 1
        
        # Adiciona erro ao log se não existir
        if "error_log" not in self.metrics:
            self.metrics["error_log"] = []
            
        self.metrics["error_log"].append({
            "type": error_type,
            "message": error_message,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # Mantém apenas os últimos 50 erros
        if len(self.metrics["error_log"]) > 50:
            self.metrics["error_log"] = self.metrics["error_log"][-50:]
            
        self.save_metrics()
        
    def get_performance_report(self) -> str:
        """Gera relatório de performance"""
        report = []
        report.append("=== RELATÓRIO DE PERFORMANCE ===")
        report.append(f"Sessões de gravação: {self.metrics['recording_sessions']}")
        report.append(f"Sessões de reprodução: {self.metrics['playback_sessions']}")
        report.append(f"Total de eventos gravados: {self.metrics['total_events_recorded']}")
        report.append(f"Total de eventos reproduzidos: {self.metrics['total_events_played']}")
        report.append(f"Duração média de gravação: {self.metrics['average_recording_duration']:.2f}s")
        report.append(f"Duração média de reprodução: {self.metrics['average_playback_duration']:.2f}s")
        report.append(f"Erros registrados: {self.metrics['errors_count']}")
        
        if self.metrics.get("last_session"):
            last = self.metrics["last_session"]
            report.append(f"\nÚltima sessão: {last['type']} - {last['duration']:.2f}s")
            
        return "\n".join(report)


def show_about_dialog(parent=None):
    """Exibe diálogo 'Sobre' da aplicação"""
    about_text = """
🖱️ Mouse Recorder v1.0.0

Aplicação completa para automação de jogos
Desenvolvida para gravar e reproduzir movimentos do mouse

✨ Funcionalidades:
• Gravação precisa de mouse e cliques
• Reprodução com controle de velocidade
• Sistema de repetições configurável
• Hotkeys globais (F9, F10, ESC)
• Auto-save e gerenciamento de arquivos
• Interface intuitiva e responsiva

🔧 Tecnologias:
• Python 3.7+
• Tkinter (Interface)
• Pynput (Controle de mouse/teclado)
• Threading (Performance)

👨‍💻 Desenvolvido com ❤️ para a comunidade gamer

📧 Suporte: GitHub Issues
🌐 Repositório: github.com/icl00ud/mouse-recorder

© 2025 Mouse Recorder - Licença MIT
    """
    
    messagebox.showinfo("Sobre - Mouse Recorder", about_text, parent=parent)


def validate_python_version() -> Tuple[bool, str]:
    """Verifica se a versão do Python é compatível"""
    import sys
    
    version = sys.version_info
    required = (3, 7)
    
    if version >= required:
        return True, f"Python {version.major}.{version.minor}.{version.micro} - Compatível"
    else:
        return False, f"Python {version.major}.{version.minor} - Requer Python 3.7+"


def check_dependencies() -> Dict[str, bool]:
    """Verifica se todas as dependências estão disponíveis"""
    dependencies = {}
    
    # Testa tkinter
    try:
        import tkinter
        dependencies["tkinter"] = True
    except ImportError:
        dependencies["tkinter"] = False
        
    # Testa pynput
    try:
        import pynput
        dependencies["pynput"] = True
    except ImportError:
        dependencies["pynput"] = False
        
    # Testa winsound (Windows apenas)
    try:
        import winsound
        dependencies["winsound"] = True
    except ImportError:
        dependencies["winsound"] = False
        
    return dependencies


if __name__ == "__main__":
    # Testes das funcionalidades
    print("🧪 Testando utilitários do Mouse Recorder...")
    
    # Testa validação de Python
    is_valid, version_msg = validate_python_version()
    print(f"Versão Python: {version_msg}")
    
    # Testa dependências
    deps = check_dependencies()
    print(f"Dependências: {deps}")
    
    # Testa validação de hotkeys
    test_hotkeys = ["F9", "CTRL+C", "ALT+F4", "INVALID", "CTRL+SHIFT+F1"]
    for hotkey in test_hotkeys:
        is_valid, msg = HotkeyValidator.validate_hotkey(hotkey)
        print(f"Hotkey '{hotkey}': {'✅' if is_valid else '❌'} {msg}")
    
    print("✅ Testes concluídos!")
