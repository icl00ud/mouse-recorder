# 🎯 Mouse Recorder - Guia Rápido de Uso

## 🚀 Inicialização

```
1. Execute: start.bat
   OU
   python mouse_recorder.py
```

## 📝 Fluxo Básico de Uso

### 🔴 PASSO 1: GRAVAR
```
┌─────────────────────────┐
│   Clique "🔴 Gravar"    │
│        ou F9            │
└─────────────────────────┘
            ↓
┌─────────────────────────┐
│  Execute suas ações     │
│   (mouse + cliques)     │
└─────────────────────────┘
            ↓
┌─────────────────────────┐
│   Clique "⏹️ Parar"     │
│        ou F9            │
└─────────────────────────┘
```

### ▶️ PASSO 2: CONFIGURAR
```
┌─────────────────────────┐
│   Repetições: 1-9999    │
│   Velocidade: 0.1x-3x   │
│   Ação Final: escolher  │
└─────────────────────────┘
```

### 🎮 PASSO 3: REPRODUZIR
```
┌─────────────────────────┐
│  Clique "▶️ Reproduzir" │
│        ou F10           │
└─────────────────────────┘
            ↓
┌─────────────────────────┐
│   Aguarda 3 segundos    │
│     (delay inicial)     │
└─────────────────────────┘
            ↓
┌─────────────────────────┐
│   Executa sequência     │
│   (acompanhe progresso) │
└─────────────────────────┘
```

## ⌨️ Atalhos Principais

| Tecla | Função |
|-------|--------|
| **F9** | 🔴 Gravar / ⏹️ Parar Gravação |
| **F10** | ▶️ Reproduzir |
| **ESC** | 🛑 Parar Tudo (Emergência) |

## 💾 Arquivos

### Salvar
```
Gravar → Parar → "💾 Salvar" → Escolher local
```

### Carregar
```
"📁 Carregar" → Selecionar .json → Pronto!
```

### Auto-Save
```
Automático em: recordings/auto_save_YYYYMMDD_HHMMSS.json
```

## 🎯 Exemplos Práticos

### Para RPG/MMO
```
1. Grave rotação de habilidades
2. Configure 20 repetições
3. Ação final: "Tocar som"
4. Velocidade: 1.0x
```

### Para Farming
```
1. Grave rota de coleta
2. Configure 50+ repetições
3. Ação final: "Minimizar janela"
4. Velocidade: 1.5x
```

### Para Precision Games
```
1. Grave cliques precisos
2. Configure 5-10 repetições
3. Ação final: "Parar"
4. Velocidade: 0.8x
```

## ⚡ Dicas Rápidas

### ✅ DO (Recomendado)
- Teste com 1 repetição primeiro
- Use delay inicial de 3-5 segundos
- Grave movimentos suaves
- Monitore reproduções longas
- Mantenha ESC sempre disponível

### ❌ DON'T (Evite)
- Gravar movimentos muito rápidos
- Usar em jogos competitivos online
- Configurar repetições sem teste
- Ignorar validação de arquivos
- Executar sem supervisão

## 🔧 Solução Rápida de Problemas

### Reprodução Imprecisa?
```
Velocidade: 0.8x → Delay: 5s → Teste: 1 rep
```

### Hotkeys não funcionam?
```
Execute como Admin → Verifique antivírus
```

### Interface trava?
```
Reduza eventos → Reinicie aplicação
```

## 📊 Interface - O que cada coisa faz

```
┌─── STATUS ────────────┐
│ Pronto/Gravando/...   │ ← Estado atual
│ Timer: 00:00          │ ← Cronômetro
│ [████████░░] 80%      │ ← Progresso
└───────────────────────┘

┌─── CONTROLES ─────────┐
│ [🔴 Gravar] [▶️ Play] │ ← Ações principais
│ [⏹️ Parar]            │
└───────────────────────┘

┌─── CONFIGURAÇÕES ─────┐
│ Repetições: [5    ]   │ ← Quantas vezes
│ Velocidade: [1.0x]    │ ← Rapidez
│ Ação Final: [Parar▼]  │ ← O que fazer no fim
└───────────────────────┘

┌─── ARQUIVOS ──────────┐
│ [💾 Salvar] [📁 Load] │ ← Gerenciar gravações
│ [⚙️ Config]           │ ← Configurações avançadas
└───────────────────────┘

┌─── INFORMAÇÕES ───────┐
│ Nome: Minha_Gravacao  │ ← Detalhes da gravação
│ Duração: 15.5s        │
│ Eventos: 324          │
│ • move: 200           │
│ • click: 120          │
│ • scroll: 4           │
└───────────────────────┘

┌─── LOG ───────────────┐
│ [10:30] Gravação...   │ ← Histórico de ações
│ [10:31] Finalizada    │
│ [10:32] Reprodução... │
└───────────────────────┘
```

## 🎮 Casos de Uso por Tipo de Jogo

### 🗡️ RPG
- **Rotações de habilidades**
- **Craft repetitivo**
- **Fishing/Mining**

### 🏰 Estratégia
- **Build orders**
- **Patrulhamento**
- **Coleta de recursos**

### 🎯 Casuais
- **Mini-games**
- **Clicker games**
- **Tarefas diárias**

### 🌾 Simulação
- **Agricultura**
- **Produção em massa**
- **Rotas otimizadas**

---

## 🎉 Começe Agora!

1. **Execute `start.bat`**
2. **Grave 5 segundos de teste**
3. **Reproduza 2x para verificar**
4. **Explore as configurações**
5. **Crie suas automações!**

**Divirta-se automatizando! 🚀**
