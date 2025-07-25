"""
Mouse Recorder para Automação de Jogos
Aplicação completa para gravar e reproduzir movimentos do mouse
Desenvolvido para automação de tarefas em jogos
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import time
import threading
from pynput import mouse, keyboard
from pynput.mouse import Button, Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyboardListener
import datetime
import os
import sys
import winsound
from typing import List, Dict, Any, Optional
import queue


class RecordingSession:
    """
    Gerencia uma sessão de gravação de mouse
    Captura movimentos, cliques e scroll com timestamps precisos
    """
    
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self.start_time: float = 0
        self.is_recording: bool = False
        self.mouse_listener: Optional[MouseListener] = None
        
    def start_recording(self) -> None:
        """Inicia a gravação dos eventos do mouse"""
        self.events.clear()
        self.start_time = time.time()
        self.is_recording = True
        
        # Configura listener do mouse para capturar todos os eventos
        self.mouse_listener = MouseListener(
            on_move=self._on_mouse_move,
            on_click=self._on_mouse_click,
            on_scroll=self._on_mouse_scroll
        )
        self.mouse_listener.start()
        
    def stop_recording(self) -> None:
        """Para a gravação e finaliza o listener"""
        self.is_recording = False
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
            
    def _on_mouse_move(self, x: int, y: int) -> None:
        """Callback para movimentos do mouse"""
        if self.is_recording:
            timestamp = time.time() - self.start_time
            self.events.append({
                "type": "move",
                "x": x,
                "y": y,
                "timestamp": timestamp
            })
            
    def _on_mouse_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        """Callback para cliques do mouse"""
        if self.is_recording:
            timestamp = time.time() - self.start_time
            button_name = "left" if button == Button.left else \
                         "right" if button == Button.right else "middle"
            action = "press" if pressed else "release"
            
            self.events.append({
                "type": "click",
                "x": x,
                "y": y,
                "button": button_name,
                "action": action,
                "timestamp": timestamp
            })
            
    def _on_mouse_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        """Callback para scroll do mouse"""
        if self.is_recording:
            timestamp = time.time() - self.start_time
            self.events.append({
                "type": "scroll",
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "timestamp": timestamp
            })
            
    def get_duration(self) -> float:
        """Retorna a duração total da gravação"""
        if not self.events:
            return 0.0
        return max(event["timestamp"] for event in self.events)
        
    def to_dict(self, name: str = "") -> Dict[str, Any]:
        """Converte a sessão para dicionário para salvamento"""
        return {
            "name": name or f"Gravacao_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "duration": self.get_duration(),
            "total_events": len(self.events),
            "created_at": datetime.datetime.now().isoformat(),
            "events": self.events
        }


class PlaybackSession:
    """
    Gerencia a reprodução de gravações
    Executa eventos com timing preciso e suporte a repetições
    """
    
    def __init__(self, events: List[Dict[str, Any]], speed_multiplier: float = 1.0):
        self.events = events
        self.speed_multiplier = speed_multiplier
        self.is_playing = False
        self.mouse_controller = mouse.Controller()
        self.current_repetition = 0
        self.total_repetitions = 1
        self.playback_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        
    def play(self, repetitions: int = 1, callback_progress=None, callback_complete=None) -> None:
        """
        Inicia a reprodução dos eventos
        
        Args:
            repetitions: Número de repetições
            callback_progress: Função chamada para atualizar progresso
            callback_complete: Função chamada ao completar
        """
        self.total_repetitions = repetitions
        self.current_repetition = 0
        self.is_playing = True
        self.stop_event.clear()
        
        self.playback_thread = threading.Thread(
            target=self._playback_worker,
            args=(callback_progress, callback_complete),
            daemon=True
        )
        self.playback_thread.start()
        
    def stop(self) -> None:
        """Para a reprodução"""
        self.is_playing = False
        self.stop_event.set()
        
    def _playback_worker(self, callback_progress=None, callback_complete=None) -> None:
        """Worker thread para reprodução dos eventos"""
        try:
            for rep in range(self.total_repetitions):
                if self.stop_event.is_set():
                    break
                    
                self.current_repetition = rep + 1
                
                if callback_progress:
                    callback_progress(self.current_repetition, self.total_repetitions, 0)
                
                # Reproduz todos os eventos da gravação
                last_timestamp = 0
                total_events = len(self.events)
                
                for i, event in enumerate(self.events):
                    if self.stop_event.is_set():
                        break
                        
                    # Calcula delay baseado no timestamp e velocidade
                    delay = (event["timestamp"] - last_timestamp) / self.speed_multiplier
                    if delay > 0:
                        time.sleep(delay)
                        
                    # Executa o evento
                    self._execute_event(event)
                    last_timestamp = event["timestamp"]
                    
                    # Atualiza progresso
                    if callback_progress:
                        progress = (i + 1) / total_events
                        callback_progress(self.current_repetition, self.total_repetitions, progress)
                        
        except Exception as e:
            print(f"Erro durante reprodução: {e}")
        finally:
            self.is_playing = False
            if callback_complete:
                callback_complete()
                
    def _execute_event(self, event: Dict[str, Any]) -> None:
        """Executa um evento específico"""
        try:
            if event["type"] == "move":
                self.mouse_controller.position = (event["x"], event["y"])
                
            elif event["type"] == "click":
                self.mouse_controller.position = (event["x"], event["y"])
                button = Button.left if event["button"] == "left" else \
                        Button.right if event["button"] == "right" else Button.middle
                        
                if event["action"] == "press":
                    self.mouse_controller.press(button)
                else:
                    self.mouse_controller.release(button)
                    
            elif event["type"] == "scroll":
                self.mouse_controller.position = (event["x"], event["y"])
                self.mouse_controller.scroll(event["dx"], event["dy"])
                
        except Exception as e:
            print(f"Erro ao executar evento: {e}")


class SettingsManager:
    """
    Gerencia configurações da aplicação
    Salva preferências do usuário em arquivo JSON
    """
    
    def __init__(self, config_file: str = "settings.json"):
        self.config_file = config_file
        self.default_settings = {
            "include_mouse_moves": True,
            "initial_delay": 3.0,
            "default_speed": 1.0,
            "hotkey_record": "F9",
            "hotkey_play": "F10",
            "hotkey_stop": "ESC",
            "max_events": 50000,
            "auto_save": True,
            "sound_notification": True
        }
        self.settings = self.load_settings()
        
    def load_settings(self) -> Dict[str, Any]:
        """Carrega configurações do arquivo ou usa padrões"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Mescla com padrões para garantir todas as chaves
                    settings = self.default_settings.copy()
                    settings.update(loaded)
                    return settings
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
        return self.default_settings.copy()
        
    def save_settings(self) -> None:
        """Salva configurações no arquivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            
    def get(self, key: str, default=None):
        """Obtém uma configuração"""
        return self.settings.get(key, default)
        
    def set(self, key: str, value: Any) -> None:
        """Define uma configuração"""
        self.settings[key] = value
        self.save_settings()


class MouseRecorder:
    """
    Classe principal da aplicação Mouse Recorder
    Gerencia interface gráfica e coordena todas as funcionalidades
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mouse Recorder - Automação de Jogos")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # Configuração de estilo
        self.setup_styles()
        
        # Gerenciadores
        self.settings = SettingsManager()
        self.recording_session: Optional[RecordingSession] = None
        self.playback_session: Optional[PlaybackSession] = None
        self.current_recording_data: Optional[Dict[str, Any]] = None
        
        # Estado da aplicação
        self.is_recording = False
        self.is_playing = False
        
        # Queue para comunicação thread-safe
        self.update_queue = queue.Queue()
        
        # Configuração da interface
        self.setup_ui()
        self.setup_hotkeys()
        
        # Timer para atualizar interface
        self.root.after(100, self.process_updates)
        
        # Configuração de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_styles(self) -> None:
        """Configura estilos da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores personalizadas
        style.configure('Record.TButton', foreground='white', background='#dc3545')
        style.configure('Play.TButton', foreground='white', background='#28a745')
        style.configure('Stop.TButton', foreground='white', background='#6c757d')
        style.configure('Save.TButton', foreground='white', background='#007bff')
        
    def setup_ui(self) -> None:
        """Configura a interface gráfica completa"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuração de redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # === SEÇÃO DE STATUS ===
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 1
        
        self.status_var = tk.StringVar(value="Pronto")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, font=('Arial', 12, 'bold'))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.timer_var = tk.StringVar(value="00:00")
        self.timer_label = ttk.Label(status_frame, textvariable=self.timer_var, font=('Arial', 10))
        self.timer_label.grid(row=0, column=1, sticky=tk.E)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, length=400)
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # === SEÇÃO DE CONTROLES PRINCIPAIS ===
        controls_frame = ttk.LabelFrame(main_frame, text="Controles Principais", padding="10")
        controls_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 1
        
        # Botões principais
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.record_btn = ttk.Button(buttons_frame, text="🔴 Gravar", command=self.toggle_recording, style='Record.TButton')
        self.record_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.play_btn = ttk.Button(buttons_frame, text="▶️ Reproduzir", command=self.start_playback, style='Play.TButton')
        self.play_btn.grid(row=0, column=1, padx=5)
        
        self.stop_btn = ttk.Button(buttons_frame, text="⏹️ Parar", command=self.stop_all, style='Stop.TButton')
        self.stop_btn.grid(row=0, column=2, padx=5)
        
        # === SEÇÃO DE CONFIGURAÇÕES DE REPRODUÇÃO ===
        playback_frame = ttk.LabelFrame(main_frame, text="Configurações de Reprodução", padding="10")
        playback_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 1
        
        # Repetições
        ttk.Label(playback_frame, text="Repetições:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.repetitions_var = tk.IntVar(value=1)
        repetitions_spinbox = ttk.Spinbox(playback_frame, from_=1, to=9999, textvariable=self.repetitions_var, width=10)
        repetitions_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Velocidade
        ttk.Label(playback_frame, text="Velocidade:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(playback_frame, from_=0.1, to=3.0, variable=self.speed_var, orient=tk.HORIZONTAL, length=200)
        speed_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        
        self.speed_label_var = tk.StringVar(value="1.0x")
        speed_label = ttk.Label(playback_frame, textvariable=self.speed_label_var)
        speed_label.grid(row=1, column=2, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Callback para atualizar label da velocidade
        def update_speed_label(*args):
            self.speed_label_var.set(f"{self.speed_var.get():.1f}x")
        self.speed_var.trace('w', update_speed_label)
        
        # Ação final
        ttk.Label(playback_frame, text="Ação Final:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.final_action_var = tk.StringVar(value="Parar")
        final_action_combo = ttk.Combobox(playback_frame, textvariable=self.final_action_var, 
                                        values=["Parar", "Repetir infinitamente", "Tocar som", "Minimizar janela"], 
                                        state="readonly", width=20)
        final_action_combo.grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # === SEÇÃO DE ARQUIVOS ===
        files_frame = ttk.LabelFrame(main_frame, text="Gerenciamento de Arquivos", padding="10")
        files_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 1
        
        file_buttons_frame = ttk.Frame(files_frame)
        file_buttons_frame.grid(row=0, column=0, columnspan=2)
        
        self.save_btn = ttk.Button(file_buttons_frame, text="💾 Salvar", command=self.save_recording, style='Save.TButton')
        self.save_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.load_btn = ttk.Button(file_buttons_frame, text="📁 Carregar", command=self.load_recording, style='Save.TButton')
        self.load_btn.grid(row=0, column=1, padx=5)
        
        self.settings_btn = ttk.Button(file_buttons_frame, text="⚙️ Configurações", command=self.open_settings, style='Save.TButton')
        self.settings_btn.grid(row=0, column=2, padx=5)
        
        # === SEÇÃO DE INFORMAÇÕES ===
        info_frame = ttk.LabelFrame(main_frame, text="Informações da Gravação", padding="10")
        info_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 1
        
        self.info_text = tk.Text(info_frame, height=8, width=60, wrap=tk.WORD)
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        # === SEÇÃO DE LOG ===
        log_frame = ttk.LabelFrame(main_frame, text="Log de Atividades", padding="10")
        log_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        row += 1
        
        self.log_text = tk.Text(log_frame, height=6, width=60, wrap=tk.WORD, state=tk.DISABLED)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(row-1, weight=1)
        
        # Inicializa interface
        self.update_ui_state()
        self.log_message("Aplicação iniciada. Use F9 para gravar, F10 para reproduzir, ESC para parar.")
        
    def setup_hotkeys(self) -> None:
        """Configura hotkeys globais"""
        try:
            self.keyboard_listener = KeyboardListener(on_press=self.on_key_press)
            self.keyboard_listener.start()
        except Exception as e:
            self.log_message(f"Erro ao configurar hotkeys: {e}")
            
    def on_key_press(self, key) -> None:
        """Callback para teclas pressionadas"""
        try:
            if key == keyboard.Key.f9:
                self.update_queue.put(('hotkey', 'record'))
            elif key == keyboard.Key.f10:
                self.update_queue.put(('hotkey', 'play'))
            elif key == keyboard.Key.esc:
                self.update_queue.put(('hotkey', 'stop'))
        except AttributeError:
            pass  # Teclas especiais podem não ter nome
            
    def process_updates(self) -> None:
        """Processa atualizações da queue (thread-safe)"""
        try:
            while True:
                action_type, data = self.update_queue.get_nowait()
                
                if action_type == 'hotkey':
                    if data == 'record':
                        self.toggle_recording()
                    elif data == 'play':
                        self.start_playback()
                    elif data == 'stop':
                        self.stop_all()
                        
                elif action_type == 'progress':
                    current_rep, total_rep, progress = data
                    self.update_progress(current_rep, total_rep, progress)
                    
                elif action_type == 'complete':
                    self.on_playback_complete()
                    
        except queue.Empty:
            pass
        
        # Agenda próxima verificação
        self.root.after(100, self.process_updates)
        
    def toggle_recording(self) -> None:
        """Alterna entre iniciar e parar gravação"""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
            
    def start_recording(self) -> None:
        """Inicia uma nova gravação"""
        if self.is_playing:
            messagebox.showwarning("Aviso", "Pare a reprodução antes de gravar.")
            return
            
        try:
            self.recording_session = RecordingSession()
            self.recording_session.start_recording()
            self.is_recording = True
            
            self.log_message("🔴 Gravação iniciada")
            self.update_ui_state()
            
            # Inicia timer para atualizar duração
            self.update_recording_timer()
            
        except Exception as e:
            self.log_message(f"Erro ao iniciar gravação: {e}")
            messagebox.showerror("Erro", f"Não foi possível iniciar a gravação:\n{e}")
            
    def stop_recording(self) -> None:
        """Para a gravação atual"""
        if not self.is_recording or not self.recording_session:
            return
            
        try:
            self.recording_session.stop_recording()
            self.is_recording = False
            
            # Salva dados da gravação
            self.current_recording_data = self.recording_session.to_dict()
            
            self.log_message(f"⏹️ Gravação finalizada - {len(self.recording_session.events)} eventos capturados")
            self.update_recording_info()
            self.update_ui_state()
            
            # Auto-save se habilitado
            if self.settings.get("auto_save", True):
                self.auto_save_recording()
                
        except Exception as e:
            self.log_message(f"Erro ao parar gravação: {e}")
            messagebox.showerror("Erro", f"Erro ao finalizar gravação:\n{e}")
            
    def start_playback(self) -> None:
        """Inicia reprodução da gravação"""
        if not self.current_recording_data:
            messagebox.showwarning("Aviso", "Nenhuma gravação carregada para reproduzir.")
            return
            
        if self.is_recording:
            messagebox.showwarning("Aviso", "Pare a gravação antes de reproduzir.")
            return
            
        if self.is_playing:
            messagebox.showwarning("Aviso", "Reprodução já está em andamento.")
            return
            
        try:
            events = self.current_recording_data.get("events", [])
            if not events:
                messagebox.showwarning("Aviso", "Gravação está vazia.")
                return
                
            # Delay inicial configurável
            initial_delay = self.settings.get("initial_delay", 3.0)
            if initial_delay > 0:
                self.log_message(f"⏱️ Aguardando {initial_delay} segundos antes de iniciar...")
                self.root.after(int(initial_delay * 1000), self._start_playback_delayed)
            else:
                self._start_playback_delayed()
                
        except Exception as e:
            self.log_message(f"Erro ao iniciar reprodução: {e}")
            messagebox.showerror("Erro", f"Erro ao iniciar reprodução:\n{e}")
            
    def _start_playback_delayed(self) -> None:
        """Inicia reprodução após delay"""
        try:
            events = self.current_recording_data["events"]
            speed = self.speed_var.get()
            repetitions = self.repetitions_var.get()
            
            self.playback_session = PlaybackSession(events, speed)
            self.is_playing = True
            
            self.log_message(f"▶️ Reprodução iniciada - {repetitions} repetições a {speed}x")
            self.update_ui_state()
            
            # Inicia reprodução com callbacks
            self.playback_session.play(
                repetitions=repetitions,
                callback_progress=lambda c, t, p: self.update_queue.put(('progress', (c, t, p))),
                callback_complete=lambda: self.update_queue.put(('complete', None))
            )
            
        except Exception as e:
            self.log_message(f"Erro durante reprodução: {e}")
            self.is_playing = False
            self.update_ui_state()
            
    def stop_all(self) -> None:
        """Para todas as operações (gravação e reprodução)"""
        if self.is_recording:
            self.stop_recording()
            
        if self.is_playing and self.playback_session:
            self.playback_session.stop()
            self.is_playing = False
            self.log_message("⏹️ Reprodução interrompida")
            self.update_ui_state()
            
    def update_progress(self, current_rep: int, total_rep: int, progress: float) -> None:
        """Atualiza barra de progresso"""
        overall_progress = ((current_rep - 1) + progress) / total_rep * 100
        self.progress_var.set(overall_progress)
        self.status_var.set(f"Reproduzindo - {current_rep}/{total_rep}")
        
    def on_playback_complete(self) -> None:
        """Callback chamado quando reprodução termina"""
        self.is_playing = False
        
        # Executa ação final
        final_action = self.final_action_var.get()
        
        if final_action == "Repetir infinitamente":
            self.log_message("🔄 Reiniciando reprodução infinita...")
            self.start_playback()
            return
            
        elif final_action == "Tocar som":
            if self.settings.get("sound_notification", True):
                try:
                    winsound.MessageBeep(winsound.MB_OK)
                    self.log_message("🔔 Som de notificação tocado")
                except:
                    self.log_message("❌ Erro ao tocar som de notificação")
                    
        elif final_action == "Minimizar janela":
            try:
                self.root.iconify()
                self.log_message("🗕 Janela minimizada")
            except:
                self.log_message("❌ Erro ao minimizar janela")
                
        self.log_message("✅ Reprodução concluída")
        self.progress_var.set(0)
        self.update_ui_state()
        
    def save_recording(self) -> None:
        """Salva gravação em arquivo"""
        if not self.current_recording_data:
            messagebox.showwarning("Aviso", "Nenhuma gravação para salvar.")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Salvar Gravação"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.current_recording_data, f, indent=2, ensure_ascii=False)
                    
                self.log_message(f"💾 Gravação salva: {os.path.basename(filename)}")
                messagebox.showinfo("Sucesso", "Gravação salva com sucesso!")
                
        except Exception as e:
            self.log_message(f"Erro ao salvar: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar gravação:\n{e}")
            
    def auto_save_recording(self) -> None:
        """Salva automaticamente a gravação"""
        try:
            if not os.path.exists("recordings"):
                os.makedirs("recordings")
                
            filename = f"recordings/auto_save_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.current_recording_data, f, indent=2, ensure_ascii=False)
                
            self.log_message(f"💾 Auto-save: {os.path.basename(filename)}")
            
        except Exception as e:
            self.log_message(f"Erro no auto-save: {e}")
            
    def load_recording(self) -> None:
        """Carrega gravação de arquivo"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Carregar Gravação"
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Valida estrutura do arquivo
                if not self.validate_recording_data(data):
                    messagebox.showerror("Erro", "Arquivo de gravação inválido.")
                    return
                    
                self.current_recording_data = data
                self.update_recording_info()
                
                self.log_message(f"📁 Gravação carregada: {os.path.basename(filename)}")
                messagebox.showinfo("Sucesso", "Gravação carregada com sucesso!")
                
        except Exception as e:
            self.log_message(f"Erro ao carregar: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar gravação:\n{e}")
            
    def validate_recording_data(self, data: Dict[str, Any]) -> bool:
        """Valida estrutura dos dados de gravação"""
        try:
            required_keys = ["events", "duration"]
            if not all(key in data for key in required_keys):
                return False
                
            events = data["events"]
            if not isinstance(events, list):
                return False
                
            # Valida alguns eventos
            for i, event in enumerate(events[:10]):  # Valida primeiros 10
                if not isinstance(event, dict) or "type" not in event or "timestamp" not in event:
                    return False
                    
            return True
            
        except:
            return False
            
    def update_recording_info(self) -> None:
        """Atualiza informações da gravação na interface"""
        if not self.current_recording_data:
            self.info_text.delete(1.0, tk.END)
            return
            
        info = []
        info.append(f"Nome: {self.current_recording_data.get('name', 'N/A')}")
        info.append(f"Duração: {self.current_recording_data.get('duration', 0):.2f} segundos")
        info.append(f"Total de eventos: {self.current_recording_data.get('total_events', 0)}")
        
        if "created_at" in self.current_recording_data:
            created_at = datetime.datetime.fromisoformat(self.current_recording_data["created_at"])
            info.append(f"Criado em: {created_at.strftime('%d/%m/%Y %H:%M:%S')}")
            
        # Análise dos eventos
        events = self.current_recording_data.get("events", [])
        if events:
            event_types = {}
            for event in events:
                event_type = event.get("type", "unknown")
                event_types[event_type] = event_types.get(event_type, 0) + 1
                
            info.append("\nTipos de eventos:")
            for event_type, count in event_types.items():
                info.append(f"  • {event_type}: {count}")
                
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, "\n".join(info))
        
    def update_recording_timer(self) -> None:
        """Atualiza timer durante gravação"""
        if self.is_recording and self.recording_session:
            duration = time.time() - self.recording_session.start_time
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            self.timer_var.set(f"{minutes:02d}:{seconds:02d}")
            
            # Agenda próxima atualização
            self.root.after(1000, self.update_recording_timer)
        else:
            self.timer_var.set("00:00")
            
    def update_ui_state(self) -> None:
        """Atualiza estado dos controles da interface"""
        # Botões de controle
        if self.is_recording:
            self.record_btn.configure(text="⏹️ Parar Gravação", style='Stop.TButton')
            self.play_btn.configure(state=tk.DISABLED)
            self.status_var.set("Gravando...")
        elif self.is_playing:
            self.record_btn.configure(state=tk.DISABLED)
            self.play_btn.configure(state=tk.DISABLED)
            self.status_var.set("Reproduzindo...")
        else:
            self.record_btn.configure(text="🔴 Gravar", style='Record.TButton', state=tk.NORMAL)
            self.play_btn.configure(state=tk.NORMAL if self.current_recording_data else tk.DISABLED)
            self.status_var.set("Pronto")
            
        # Botões de arquivo
        self.save_btn.configure(state=tk.NORMAL if self.current_recording_data and not self.is_recording else tk.DISABLED)
        self.load_btn.configure(state=tk.NORMAL if not self.is_recording and not self.is_playing else tk.DISABLED)
        
    def log_message(self, message: str) -> None:
        """Adiciona mensagem ao log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)
        
    def open_settings(self) -> None:
        """Abre janela de configurações avançadas"""
        try:
            from advanced_settings import AdvancedSettingsWindow
            settings_window = AdvancedSettingsWindow(parent=self.root, settings_manager=self.settings)
        except ImportError:
            messagebox.showwarning("Aviso", "Módulo de configurações avançadas não encontrado.")
        except Exception as e:
            self.log_message(f"Erro ao abrir configurações: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir configurações:\n{e}")
        
    def on_closing(self) -> None:
        """Callback para fechamento da aplicação"""
        try:
            # Para todas as operações
            self.stop_all()
            
            # Para listeners
            if hasattr(self, 'keyboard_listener'):
                self.keyboard_listener.stop()
                
            # Salva configurações
            self.settings.save_settings()
            
            self.log_message("👋 Aplicação finalizada")
            
        except Exception as e:
            print(f"Erro ao fechar aplicação: {e}")
        finally:
            self.root.destroy()
            
    def run(self) -> None:
        """Inicia a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
        except Exception as e:
            print(f"Erro na aplicação: {e}")
            self.on_closing()


def main():
    """Função principal"""
    try:
        app = MouseRecorder()
        app.run()
    except Exception as e:
        print(f"Erro fatal: {e}")
        input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
