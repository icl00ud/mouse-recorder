# 🎮 Como Usar o Mouse Recorder - Guia Completo

## 🚀 Primeiros Passos

### 1. Instalação e Execução
```bash
# Método 1: Execução Rápida (Recomendado)
start.bat

# Método 2: Execução Manual
python mouse_recorder.py

# Método 3: Com instalação automática
python setup.py
```

### 2. Interface Principal
Ao abrir a aplicação, você verá:
- **Status**: Mostra o estado atual (Pronto/Gravando/Reproduzindo)
- **Timer**: Cronômetro durante gravação/reprodução
- **Barra de Progresso**: Progresso da reprodução
- **Controles Principais**: Botões para gravar, reproduzir e parar
- **Configurações**: Repetições, velocidade e ação final
- **Arquivos**: Salvar, carregar e configurações
- **Informações**: Detalhes da gravação atual
- **Log**: Histórico de atividades

## 📹 Como Gravar Movimentos

### Gravação Básica
1. **Clique no botão "🔴 Gravar"** ou pressione **F9**
2. **Execute as ações desejadas** no jogo ou aplicação
3. **Clique em "⏹️ Parar Gravação"** ou pressione **F9** novamente

### Dicas para Gravação
- ✅ **Planeje suas ações** antes de gravar
- ✅ **Movimente o mouse suavemente** para melhor precisão
- ✅ **Aguarde alguns segundos** entre ações importantes
- ✅ **Evite movimentos desnecessários** para otimizar o arquivo
- ✅ **Teste em tela pequena** antes de gravar sequências longas

### Durante a Gravação
- O **timer** mostra a duração atual
- O **status** indica "Gravando..."
- **ESC** para parar emergencialmente
- **Auto-save** salva automaticamente na pasta `recordings/`

## ▶️ Como Reproduzir Gravações

### Reprodução Simples
1. **Tenha uma gravação** (recém-gravada ou carregada)
2. **Configure repetições** (padrão: 1)
3. **Ajuste velocidade** se necessário (padrão: 1.0x)
4. **Clique em "▶️ Reproduzir"** ou pressione **F10**
5. **Aguarde o delay inicial** (padrão: 3 segundos)

### Configurações Avançadas

#### Repetições
- **1-9999**: Número de vezes para repetir
- **Útil para**: Farming, crafting, ações repetitivas

#### Velocidade
- **0.1x - 3.0x**: Multiplicador de velocidade
- **0.5x**: Mais lento (maior precisão)
- **1.0x**: Velocidade original
- **2.0x**: Duas vezes mais rápido

#### Ações Finais
- **Parar**: Não faz nada após completar
- **Repetir infinitamente**: Continua até parar manualmente
- **Tocar som**: Notificação sonora ao finalizar
- **Minimizar janela**: Oculta a aplicação

### Durante a Reprodução
- **Barra de progresso** mostra andamento
- **Status** indica repetição atual (Ex: "Reproduzindo - 2/5")
- **ESC** para parar imediatamente

## 💾 Gerenciamento de Arquivos

### Salvamento
1. **Grave uma sequência** de movimentos
2. **Clique em "💾 Salvar"**
3. **Escolha local e nome** do arquivo
4. **Formato**: JSON com todas as informações

### Carregamento
1. **Clique em "📁 Carregar"**
2. **Selecione arquivo .json** de gravação
3. **Arquivo é validado** automaticamente
4. **Informações aparecem** na seção "Informações da Gravação"

### Auto-Save
- **Habilitado por padrão**
- **Pasta**: `recordings/`
- **Formato**: `auto_save_YYYYMMDD_HHMMSS.json`
- **Automático**: Sempre que para uma gravação

## ⌨️ Atalhos de Teclado (Hotkeys)

| Tecla | Função | Descrição |
|-------|--------|-----------|
| **F9** | Gravar/Parar | Inicia ou para gravação |
| **F10** | Reproduzir | Inicia reprodução |
| **ESC** | Parar Tudo | Para gravação E reprodução |

### Hotkeys Globais
- ✅ **Funcionam mesmo** quando a aplicação não está em foco
- ✅ **Úteis durante jogos** em tela cheia
- ✅ **Personalizáveis** nas configurações avançadas

## ⚙️ Configurações Avançadas

### Acessando Configurações
1. **Clique em "⚙️ Configurações"**
2. **Navegue pelas abas**:
   - **Geral**: Configurações básicas
   - **Gravação**: Filtros e precisão
   - **Reprodução**: Timing e comportamento
   - **Hotkeys**: Personalização de atalhos
   - **Performance**: Estatísticas de uso
   - **Sobre**: Informações da aplicação

### Configurações Importantes

#### Gravação
- **Incluir movimentos do mouse**: Liga/desliga captura de movimentos
- **Máximo de eventos**: Limite para evitar travamentos
- **Precisão de captura**: Alta/Média/Baixa
- **Ignorar cliques rápidos**: Filtra cliques acidentais

#### Reprodução
- **Delay inicial**: Tempo de espera antes de começar
- **Velocidade padrão**: Velocidade inicial da interface
- **Movimentos suaves**: Interpolação entre pontos
- **Pausar em erro**: Para se algo der errado

## 🎮 Casos de Uso Práticos

### RPG/MMO
```
1. Grave sequência de craft
2. Configure 50 repetições
3. Escolha "Tocar som" como ação final
4. Inicie reprodução e faça outras atividades
```

### Jogos de Estratégia
```
1. Grave construção de unidades
2. Configure velocidade 1.5x
3. Use "Repetir infinitamente"
4. Pare manualmente quando necessário
```

### Jogos Casuais
```
1. Grave cliques em mini-game
2. Configure velocidade 0.8x para precisão
3. Use 10-20 repetições
4. Monitore através da barra de progresso
```

### Farming de Recursos
```
1. Grave rota de coleta
2. Configure 100+ repetições
3. Use "Minimizar janela" para não atrapalhar
4. Verifique periodicamente
```

## 🔧 Solução de Problemas

### Reprodução Imprecisa
- ✅ **Reduza a velocidade** para 0.8x ou 0.5x
- ✅ **Teste em resolução menor** primeiro
- ✅ **Aumente delay inicial** para 5 segundos
- ✅ **Grave movimentos mais lentos**

### Hotkeys Não Funcionam
- ✅ **Execute como administrador**
- ✅ **Verifique antivírus/firewall**
- ✅ **Teste outras combinações** nas configurações
- ✅ **Feche outros programas** que possam interferir

### Interface Travando
- ✅ **Reduza número de eventos** capturados
- ✅ **Desabilite movimentos do mouse** se não precisar
- ✅ **Feche outros programas** pesados
- ✅ **Reinicie a aplicação**

### Arquivo Não Carrega
- ✅ **Verifique se é .json válido**
- ✅ **Teste salvar nova gravação**
- ✅ **Veja logs na seção de atividades**
- ✅ **Use arquivo de exemplo** se disponível

## 📊 Análise de Gravações

### Informações Disponíveis
- **Nome**: Identificação da gravação
- **Duração**: Tempo total em segundos
- **Total de eventos**: Quantidade de ações capturadas
- **Data de criação**: Quando foi gravada
- **Tipos de eventos**: Quantos movimentos, cliques, etc.

### Otimização
- **Eventos redundantes**: Movimentos para mesma posição
- **Duração vs Eventos**: Relação eficiência
- **Tipos balanceados**: Mix ideal de ações

## 🎯 Dicas Avançadas

### Para Máxima Precisão
1. **Grave em velocidade normal**
2. **Use delay inicial de 5+ segundos**
3. **Reproduza a 0.8x inicialmente**
4. **Teste com 1 repetição primeiro**
5. **Ajuste velocidade conforme necessário**

### Para Máxima Eficiência
1. **Desabilite movimentos desnecessários**
2. **Use velocidade 1.5x-2.0x**
3. **Configure repetições altas**
4. **Use ação final automática**

### Para Jogos Específicos
1. **MMO**: Foque em rotações de habilidades
2. **Estratégia**: Grave padrões de construção
3. **Casual**: Otimize para cliques precisos
4. **Simulation**: Use repetições longas

## 🚨 Avisos Importantes

### Uso Responsável
- ⚠️ **Verifique termos de serviço** dos jogos
- ⚠️ **Use apenas para automação pessoal**
- ⚠️ **Não abuse em jogos online competitivos**
- ⚠️ **Mantenha controle manual** sempre disponível

### Segurança
- ✅ **ESC sempre para tudo**
- ✅ **Monitore reproduções longas**
- ✅ **Teste em ambiente seguro**
- ✅ **Mantenha backups** de gravações importantes

## 📈 Monitoramento

### Durante Uso
- **Log de atividades**: Mostra todas as ações
- **Barra de progresso**: Acompanha reprodução
- **Timer**: Controla duração
- **Status**: Estado atual sempre visível

### Estatísticas
- **Aba Performance**: Métricas de uso
- **Histórico**: Sessões anteriores
- **Erros**: Problemas encontrados
- **Eficiência**: Análise de performance

---

## 🎉 Começando Agora!

1. **Execute `start.bat`** para iniciar
2. **Faça uma gravação teste** de 5 segundos
3. **Reproduza com 2 repetições** para testar
4. **Explore as configurações** avançadas
5. **Crie suas primeiras automações** úteis!

**Pronto para automatizar seus jogos! 🎮**
