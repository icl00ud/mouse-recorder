# 🖱️ Mouse Recorder - Automação de Jogos

Uma aplicação completa em Python para gravar e reproduzir movimentos do mouse, desenvolvida especialmente para automação de tarefas em jogos.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey.svg)
![Release](https://img.shields.io/github/v/release/icl00ud/mouse-recorder)

## 📦 Download Executáveis

### Executáveis Pré-compilados (Recomendado)
Não precisa instalar Python! Baixe e execute diretamente:

- **Windows**: [MouseRecorder.exe](https://github.com/icl00ud/mouse-recorder/releases/latest/download/MouseRecorder.exe)
- **macOS**: [MouseRecorder](https://github.com/icl00ud/mouse-recorder/releases/latest/download/MouseRecorder)

📖 [Ver instruções detalhadas de instalação](RELEASE_README.md)

## ✨ Funcionalidades Principais

### 🎮 Interface Gráfica Intuitiva
- **Botão Gravar**: Inicia captura de movimentos e cliques do mouse
- **Botão Reproduzir**: Executa a sequência gravada com precisão
- **Botão Parar**: Interrompe gravação ou reprodução
- **Controles avançados**: Repetições, velocidade e ações finais

### 🎯 Sistema de Gravação Avançado
- ✅ Captura movimentos do mouse (x, y, timestamp)
- ✅ Registra cliques (esquerdo, direito, meio)
- ✅ Detecta scroll (direção e intensidade)
- ✅ Timestamps precisos para reprodução fiel
- ✅ Suporte a double cliques

### ⚡ Reprodução Inteligente
- 🔄 Sistema de repetições configurável (1-9999x)
- 🏃‍♂️ Controle de velocidade (0.1x a 3.0x)
- 📊 Barra de progresso em tempo real
- 🎬 Ações finais programáveis:
  - Parar
  - Repetir infinitamente
  - Tocar som de notificação
  - Minimizar janela

### 💾 Gerenciamento de Arquivos
- 📁 Salvar/carregar gravações em JSON
- 💾 Auto-save automático
- 🔍 Validação de arquivos
- 📋 Informações detalhadas da gravação

### ⌨️ Hotkeys Globais
- **F9**: Iniciar/parar gravação
- **F10**: Reproduzir gravação
- **ESC**: Parar todas as operações

## 🚀 Instalação Rápida

### Método 1: Instalação Automática
```bash
# Clone o repositório
git clone https://github.com/icl00ud/mouse-recorder.git
cd mouse-recorder

# Execute o setup automático
python setup.py
```

### Método 2: Instalação Manual
```bash
# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python mouse_recorder.py
```

### Método 3: Windows Batch
```bash
# Execute o arquivo de instalação
install.bat
```

## 📋 Dependências

- **Python 3.7+**
- **pynput**: Captura e controle de mouse/teclado
- **tkinter**: Interface gráfica (incluído no Python)

## 🎯 Como Usar

### 1. Gravação Básica
1. Abra a aplicação: `python mouse_recorder.py`
2. Clique em **"🔴 Gravar"** ou pressione **F9**
3. Execute as ações desejadas no jogo
4. Clique em **"⏹️ Parar"** ou pressione **F9** novamente

### 2. Reprodução
1. Configure o número de **repetições** (padrão: 1)
2. Ajuste a **velocidade** se necessário (padrão: 1.0x)
3. Escolha a **ação final** (padrão: Parar)
4. Clique em **"▶️ Reproduzir"** ou pressione **F10**

### 3. Salvamento e Carregamento
- **Salvar**: Preserva a gravação em arquivo JSON
- **Carregar**: Restaura gravação previamente salva
- **Auto-save**: Salva automaticamente na pasta `recordings/`

## 🔧 Configurações Avançadas

### Arquivo `settings.json`
```json
{
  "include_mouse_moves": true,
  "initial_delay": 3.0,
  "default_speed": 1.0,
  "hotkey_record": "F9",
  "hotkey_play": "F10",
  "hotkey_stop": "ESC",
  "max_events": 50000,
  "auto_save": true,
  "sound_notification": true
}
```

### Personalizações Disponíveis
- **include_mouse_moves**: Incluir movimentos do mouse
- **initial_delay**: Delay antes da reprodução (segundos)
- **default_speed**: Velocidade padrão de reprodução
- **max_events**: Limite máximo de eventos
- **auto_save**: Salvamento automático
- **sound_notification**: Som de notificação

## 📁 Estrutura de Arquivos

```
mouse-recorder/
├── mouse_recorder.py      # Aplicação principal
├── requirements.txt       # Dependências
├── setup.py              # Script de instalação
├── install.bat           # Instalação Windows
├── settings.json         # Configurações (gerado automaticamente)
├── recordings/           # Gravações auto-salvas
│   └── auto_save_*.json
└── README.md            # Este arquivo
```

## 📊 Formato de Gravação

### Estrutura JSON
```json
{
  "name": "nome_da_gravacao",
  "duration": 15.5,
  "total_events": 324,
  "created_at": "2025-01-15T10:30:00",
  "events": [
    {
      "type": "move",
      "x": 100,
      "y": 200,
      "timestamp": 0.0
    },
    {
      "type": "click",
      "button": "left",
      "x": 150,
      "y": 250,
      "timestamp": 1.5,
      "action": "press"
    },
    {
      "type": "scroll",
      "x": 300,
      "y": 400,
      "dx": 0,
      "dy": -3,
      "timestamp": 3.2
    }
  ]
}
```

## 🎮 Casos de Uso para Jogos

### 🎯 RPG/MMO
- Automatizar craft repetitivo
- Farming de recursos
- Rotações de habilidades

### 🎲 Jogos de Estratégia
- Construção repetitiva
- Coleta de recursos
- Patrulhamento

### 🃏 Jogos Casuais
- Cliques repetitivos
- Mini-games
- Tarefas diárias

## 🔒 Funcionalidades de Segurança

- ✅ **Validação de arquivos**: Verifica integridade dos JSONs
- ✅ **Limite de eventos**: Previne travamentos (50k eventos)
- ✅ **Escape de emergência**: ESC para parar tudo
- ✅ **Verificação de coordenadas**: Valida se estão na tela
- ✅ **Threading seguro**: Interface responsiva
- ✅ **Tratamento de erros**: Logs detalhados

## 🐛 Solução de Problemas

### Erro: "pynput" não encontrado
```bash
pip install pynput
```

### Hotkeys não funcionam
- Execute como administrador
- Verifique antivírus/firewall

### Reprodução imprecisa
- Reduza a velocidade
- Verifique resolução da tela
- Teste com delay inicial maior

### Interface travando
- Feche outros programas
- Reduza número de eventos
- Reinicie a aplicação

## 🔄 Atualizações e Melhorias

### Versão Atual: 1.0.0
- ✅ Interface gráfica completa
- ✅ Gravação e reprodução precisa
- ✅ Hotkeys globais
- ✅ Sistema de arquivos
- ✅ Configurações avançadas

### Próximas Versões
- 🔜 Editor visual de gravações
- 🔜 Macros condicionais
- 🔜 Integração com OCR
- 🔜 Profiles de jogos

## 📝 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- 🐛 Reportar bugs
- 💡 Sugerir funcionalidades
- 🔧 Enviar pull requests
- 📚 Melhorar documentação

## ⚠️ Disclaimer

Esta ferramenta foi desenvolvida para fins educacionais e de automação pessoal. Certifique-se de que o uso está de acordo com os termos de serviço dos jogos que você utiliza.

## 📞 Suporte

Para suporte técnico ou dúvidas:
- 📧 Abra uma [Issue](https://github.com/icl00ud/mouse-recorder/issues)
- 📖 Consulte a documentação
- 💬 Participe das discussões

---

**Desenvolvido com ❤️ para a comunidade de gamers**
