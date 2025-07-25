"""
Configurações Avançadas - Mouse Recorder
Interface gráfica para configurações detalhadas da aplicação
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import json
from typing import Dict, Any
from utils import HotkeyValidator, PerformanceMonitor, show_about_dialog


class AdvancedSettingsWindow:
    """
    Janela de configurações avançadas
    Permite personalização completa da aplicação
    """
    
    def __init__(self, parent=None, settings_manager=None):
        self.parent = parent
        self.settings_manager = settings_manager
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Configurações Avançadas - Mouse Recorder")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Variáveis de configuração
        self.config_vars = {}
        
        # Performance monitor
        self.performance_monitor = PerformanceMonitor()
        
        self.setup_ui()
        
        # Carrega configurações atuais
        if self.settings_manager:
            self.load_current_settings()
            
        # Centraliza janela
        self.center_window()
        
    def center_window(self) -> None:
        """Centraliza a janela na tela"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_ui(self) -> None:
        """Configura a interface da janela de configurações"""
        # Notebook para abas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === ABA GERAL ===
        self.setup_general_tab(notebook)
        
        # === ABA GRAVAÇÃO ===
        self.setup_recording_tab(notebook)
        
        # === ABA REPRODUÇÃO ===
        self.setup_playback_tab(notebook)
        
        # === ABA HOTKEYS ===
        self.setup_hotkeys_tab(notebook)
        
        # === ABA PERFORMANCE ===
        self.setup_performance_tab(notebook)
        
        # === ABA SOBRE ===
        self.setup_about_tab(notebook)
        
        # Botões de ação
        self.setup_action_buttons()
        
    def setup_general_tab(self, notebook) -> None:
        """Configura aba de configurações gerais"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Geral")
        
        # Frame para configurações gerais
        general_frame = ttk.LabelFrame(frame, text="Configurações Gerais", padding="10")
        general_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        
        # Auto-save
        self.config_vars['auto_save'] = tk.BooleanVar()
        ttk.Checkbutton(general_frame, text="Auto-salvar gravações", 
                       variable=self.config_vars['auto_save']).grid(row=row, column=0, sticky=tk.W, pady=2)
        row += 1
        
        # Sound notification
        self.config_vars['sound_notification'] = tk.BooleanVar()
        ttk.Checkbutton(general_frame, text="Notificações sonoras", 
                       variable=self.config_vars['sound_notification']).grid(row=row, column=0, sticky=tk.W, pady=2)
        row += 1
        
        # Theme
        ttk.Label(general_frame, text="Tema:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.config_vars['theme'] = tk.StringVar()
        theme_combo = ttk.Combobox(general_frame, textvariable=self.config_vars['theme'],
                                  values=["clam", "alt", "default", "classic"], state="readonly", width=15)
        theme_combo.grid(row=row, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        row += 1
        
        # Language
        ttk.Label(general_frame, text="Idioma:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.config_vars['language'] = tk.StringVar()
        lang_combo = ttk.Combobox(general_frame, textvariable=self.config_vars['language'],
                                 values=["Português", "English", "Español"], state="readonly", width=15)
        lang_combo.grid(row=row, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        row += 1
        
    def setup_recording_tab(self, notebook) -> None:
        """Configura aba de configurações de gravação"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Gravação")
        
        # Frame de captura
        capture_frame = ttk.LabelFrame(frame, text="Configurações de Captura", padding="10")
        capture_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        
        # Include mouse moves
        self.config_vars['include_mouse_moves'] = tk.BooleanVar()
        ttk.Checkbutton(capture_frame, text="Incluir movimentos do mouse", 
                       variable=self.config_vars['include_mouse_moves']).grid(row=row, column=0, sticky=tk.W, pady=2)
        row += 1
        
        # Max events
        ttk.Label(capture_frame, text="Máximo de eventos:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.config_vars['max_events'] = tk.IntVar()
        max_events_spinbox = ttk.Spinbox(capture_frame, from_=1000, to=100000, 
                                        textvariable=self.config_vars['max_events'], width=10)
        max_events_spinbox.grid(row=row, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        row += 1
        
        # Capture precision
        ttk.Label(capture_frame, text="Precisão de captura:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.config_vars['capture_precision'] = tk.StringVar()
        precision_combo = ttk.Combobox(capture_frame, textvariable=self.config_vars['capture_precision'],
                                      values=["Alta", "Média", "Baixa"], state="readonly", width=15)
        precision_combo.grid(row=row, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        row += 1
        
        # Frame de filtros
        filter_frame = ttk.LabelFrame(frame, text="Filtros de Captura", padding="10")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        
        # Ignore rapid clicks
        self.config_vars['ignore_rapid_clicks'] = tk.BooleanVar()
        ttk.Checkbutton(filter_frame, text="Ignorar cliques muito rápidos", 
                       variable=self.config_vars['ignore_rapid_clicks']).grid(row=row, column=0, sticky=tk.W, pady=2)
        row += 1
        
        # Minimum movement distance
        ttk.Label(filter_frame, text="Distância mínima de movimento:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.config_vars['min_movement_distance'] = tk.IntVar()
        min_dist_spinbox = ttk.Spinbox(filter_frame, from_=0, to=50, 
                                      textvariable=self.config_vars['min_movement_distance'], width=10)
        min_dist_spinbox.grid(row=row, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        row += 1
        
    def setup_playback_tab(self, notebook) -> None:
        """Configura aba de configurações de reprodução"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Reprodução")
        
        # Frame de timing
        timing_frame = ttk.LabelFrame(frame, text="Configurações de Timing", padding="10")
        timing_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        
        # Initial delay
        ttk.Label(timing_frame, text="Delay inicial (segundos):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.config_vars['initial_delay'] = tk.DoubleVar()
        delay_spinbox = ttk.Spinbox(timing_frame, from_=0.0, to=30.0, increment=0.5,
                                   textvariable=self.config_vars['initial_delay'], width=10)
        delay_spinbox.grid(row=row, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        row += 1
        
        # Default speed
        ttk.Label(timing_frame, text="Velocidade padrão:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.config_vars['default_speed'] = tk.DoubleVar()
        speed_spinbox = ttk.Spinbox(timing_frame, from_=0.1, to=5.0, increment=0.1,
                                   textvariable=self.config_vars['default_speed'], width=10)
        speed_spinbox.grid(row=row, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        row += 1
        
        # Frame de comportamento
        behavior_frame = ttk.LabelFrame(frame, text="Comportamento", padding="10")
        behavior_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        
        # Smooth movements
        self.config_vars['smooth_movements'] = tk.BooleanVar()
        ttk.Checkbutton(behavior_frame, text="Movimentos suaves", 
                       variable=self.config_vars['smooth_movements']).grid(row=row, column=0, sticky=tk.W, pady=2)
        row += 1
        
        # Pause on error
        self.config_vars['pause_on_error'] = tk.BooleanVar()
        ttk.Checkbutton(behavior_frame, text="Pausar em caso de erro", 
                       variable=self.config_vars['pause_on_error']).grid(row=row, column=0, sticky=tk.W, pady=2)
        row += 1
        
        # Continue on screen change
        self.config_vars['continue_on_screen_change'] = tk.BooleanVar()
        ttk.Checkbutton(behavior_frame, text="Continuar se a tela mudar", 
                       variable=self.config_vars['continue_on_screen_change']).grid(row=row, column=0, sticky=tk.W, pady=2)
        row += 1
        
    def setup_hotkeys_tab(self, notebook) -> None:
        """Configura aba de hotkeys"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Hotkeys")
        
        hotkeys_frame = ttk.LabelFrame(frame, text="Atalhos de Teclado", padding="10")
        hotkeys_frame.pack(fill=tk.X, padx=10, pady=5)
        
        row = 0
        
        # Record hotkey
        ttk.Label(hotkeys_frame, text="Gravar/Parar:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.config_vars['hotkey_record'] = tk.StringVar()
        record_entry = ttk.Entry(hotkeys_frame, textvariable=self.config_vars['hotkey_record'], width=15)
        record_entry.grid(row=row, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        def validate_record_hotkey(*args):
            self.validate_hotkey('hotkey_record')
        self.config_vars['hotkey_record'].trace('w', validate_record_hotkey)
        row += 1
        
        # Play hotkey
        ttk.Label(hotkeys_frame, text="Reproduzir:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.config_vars['hotkey_play'] = tk.StringVar()
        play_entry = ttk.Entry(hotkeys_frame, textvariable=self.config_vars['hotkey_play'], width=15)
        play_entry.grid(row=row, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        def validate_play_hotkey(*args):
            self.validate_hotkey('hotkey_play')
        self.config_vars['hotkey_play'].trace('w', validate_play_hotkey)
        row += 1
        
        # Stop hotkey
        ttk.Label(hotkeys_frame, text="Parar Tudo:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.config_vars['hotkey_stop'] = tk.StringVar()
        stop_entry = ttk.Entry(hotkeys_frame, textvariable=self.config_vars['hotkey_stop'], width=15)
        stop_entry.grid(row=row, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        def validate_stop_hotkey(*args):
            self.validate_hotkey('hotkey_stop')
        self.config_vars['hotkey_stop'].trace('w', validate_stop_hotkey)
        row += 1
        
        # Status de validação
        self.hotkey_status_label = ttk.Label(hotkeys_frame, text="", foreground="green")
        self.hotkey_status_label.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        
    def setup_performance_tab(self, notebook) -> None:
        """Configura aba de performance"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Performance")
        
        # Frame de estatísticas
        stats_frame = ttk.LabelFrame(frame, text="Estatísticas de Uso", padding="10")
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Text widget para exibir relatório
        self.performance_text = tk.Text(stats_frame, height=15, width=70, wrap=tk.WORD, state=tk.DISABLED)
        performance_scrollbar = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=self.performance_text.yview)
        self.performance_text.configure(yscrollcommand=performance_scrollbar.set)
        
        self.performance_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        performance_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão para atualizar
        refresh_btn = ttk.Button(frame, text="🔄 Atualizar Estatísticas", command=self.refresh_performance)
        refresh_btn.pack(pady=5)
        
        # Carrega estatísticas iniciais
        self.refresh_performance()
        
    def setup_about_tab(self, notebook) -> None:
        """Configura aba sobre"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Sobre")
        
        # Frame de informações
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Logo/Título
        title_label = ttk.Label(info_frame, text="🖱️ Mouse Recorder", font=('Arial', 20, 'bold'))
        title_label.pack(pady=10)
        
        version_label = ttk.Label(info_frame, text="Versão 1.0.0", font=('Arial', 12))
        version_label.pack(pady=5)
        
        # Descrição
        desc_text = """
Aplicação completa para automação de jogos
Grave e reproduza movimentos do mouse com precisão

Desenvolvido com Python e muito ❤️
        """
        desc_label = ttk.Label(info_frame, text=desc_text, justify=tk.CENTER, font=('Arial', 10))
        desc_label.pack(pady=10)
        
        # Botões de ação
        buttons_frame = ttk.Frame(info_frame)
        buttons_frame.pack(pady=20)
        
        about_btn = ttk.Button(buttons_frame, text="📋 Sobre Detalhado", command=lambda: show_about_dialog(self.window))
        about_btn.pack(side=tk.LEFT, padx=5)
        
        github_btn = ttk.Button(buttons_frame, text="🌐 GitHub", command=self.open_github)
        github_btn.pack(side=tk.LEFT, padx=5)
        
    def setup_action_buttons(self) -> None:
        """Configura botões de ação da janela"""
        buttons_frame = ttk.Frame(self.window)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botões
        ttk.Button(buttons_frame, text="💾 Salvar", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="🔄 Restaurar Padrões", command=self.restore_defaults).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="❌ Cancelar", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
    def validate_hotkey(self, hotkey_var: str) -> None:
        """Valida uma hotkey específica"""
        hotkey_value = self.config_vars[hotkey_var].get()
        is_valid, message = HotkeyValidator.validate_hotkey(hotkey_value)
        
        if is_valid:
            self.hotkey_status_label.configure(text="✅ Hotkeys válidas", foreground="green")
        else:
            self.hotkey_status_label.configure(text=f"❌ {message}", foreground="red")
            
    def refresh_performance(self) -> None:
        """Atualiza estatísticas de performance"""
        report = self.performance_monitor.get_performance_report()
        
        self.performance_text.configure(state=tk.NORMAL)
        self.performance_text.delete(1.0, tk.END)
        self.performance_text.insert(1.0, report)
        self.performance_text.configure(state=tk.DISABLED)
        
    def load_current_settings(self) -> None:
        """Carrega configurações atuais do settings manager"""
        if not self.settings_manager:
            return
            
        settings = self.settings_manager.settings
        
        # Mapeia configurações para variáveis
        mapping = {
            'auto_save': 'auto_save',
            'sound_notification': 'sound_notification',
            'include_mouse_moves': 'include_mouse_moves',
            'max_events': 'max_events',
            'initial_delay': 'initial_delay',
            'default_speed': 'default_speed',
            'hotkey_record': 'hotkey_record',
            'hotkey_play': 'hotkey_play',
            'hotkey_stop': 'hotkey_stop'
        }
        
        for setting_key, var_key in mapping.items():
            if setting_key in settings and var_key in self.config_vars:
                self.config_vars[var_key].set(settings[setting_key])
                
        # Configurações com valores padrão
        self.config_vars.get('theme', tk.StringVar()).set(settings.get('theme', 'clam'))
        self.config_vars.get('language', tk.StringVar()).set(settings.get('language', 'Português'))
        self.config_vars.get('capture_precision', tk.StringVar()).set(settings.get('capture_precision', 'Alta'))
        
        # Configurações booleanas com padrão False
        bool_settings = ['ignore_rapid_clicks', 'smooth_movements', 'pause_on_error', 'continue_on_screen_change']
        for setting in bool_settings:
            if setting in self.config_vars:
                self.config_vars[setting].set(settings.get(setting, False))
                
        # Configurações numéricas com padrão
        self.config_vars.get('min_movement_distance', tk.IntVar()).set(settings.get('min_movement_distance', 5))
        
    def save_settings(self) -> None:
        """Salva todas as configurações"""
        if not self.settings_manager:
            messagebox.showwarning("Aviso", "Gerenciador de configurações não disponível.")
            return
            
        try:
            # Valida hotkeys antes de salvar
            for hotkey_var in ['hotkey_record', 'hotkey_play', 'hotkey_stop']:
                hotkey_value = self.config_vars[hotkey_var].get()
                is_valid, message = HotkeyValidator.validate_hotkey(hotkey_value)
                if not is_valid:
                    messagebox.showerror("Erro", f"Hotkey inválida: {message}")
                    return
                    
            # Salva todas as configurações
            for var_name, var_obj in self.config_vars.items():
                self.settings_manager.set(var_name, var_obj.get())
                
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações:\n{e}")
            
    def restore_defaults(self) -> None:
        """Restaura configurações padrão"""
        if messagebox.askyesno("Confirmar", "Restaurar todas as configurações padrão?"):
            if self.settings_manager:
                # Restaura configurações padrão
                self.settings_manager.settings = self.settings_manager.default_settings.copy()
                self.settings_manager.save_settings()
                
                # Recarrega na interface
                self.load_current_settings()
                
                messagebox.showinfo("Sucesso", "Configurações padrão restauradas!")
                
    def open_github(self) -> None:
        """Abre página do GitHub"""
        import webbrowser
        webbrowser.open("https://github.com/icl00ud/mouse-recorder")


def main():
    """Função principal para testar a janela de configurações"""
    from mouse_recorder import SettingsManager
    
    # Cria um settings manager de teste
    settings_manager = SettingsManager()
    
    # Cria e exibe janela de configurações
    app = AdvancedSettingsWindow(settings_manager=settings_manager)
    app.window.mainloop()


if __name__ == "__main__":
    main()
