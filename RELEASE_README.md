# Mouse Recorder - Executáveis

Este diretório contém os executáveis compilados do Mouse Recorder para diferentes plataformas.

## Downloads

### Windows
- **MouseRecorder.exe**: Executável para Windows (Vista/7/8/10/11)
  - Tamanho: ~15-25 MB
  - Não requer instalação do Python
  - Interface gráfica completa
  - Suporte a hotkeys globais

### macOS  
- **MouseRecorder**: Executável para macOS (10.13+)
  - Tamanho: ~20-30 MB
  - Não requer instalação do Python
  - Interface gráfica nativa
  - **Nota**: Pode requerer permissões de acessibilidade

## Instruções de Uso

### Windows
1. Baixe o arquivo `MouseRecorder.exe`
2. Execute o arquivo (pode aparecer aviso do Windows Defender - clique em "Mais informações" e "Executar assim mesmo")
3. A aplicação será iniciada automaticamente

### macOS
1. Baixe o arquivo `MouseRecorder`
2. Abra o Terminal e navegue até a pasta de download
3. Execute: `chmod +x MouseRecorder` (torna o arquivo executável)
4. Execute: `./MouseRecorder`
5. **Importante**: Quando solicitado, conceda permissões de acessibilidade em:
   - Preferências do Sistema → Segurança e Privacidade → Privacidade → Acessibilidade

## Permissões Necessárias

### Windows
- Acesso ao mouse e teclado (para gravação e reprodução)
- Criação de arquivos (para salvar gravações)

### macOS
- **Acessibilidade**: Necessária para controlar mouse e teclado
- **Automação**: Pode ser solicitada para algumas funcionalidades

## Troubleshooting

### Windows
- **Antivírus bloqueia**: Adicione exceção para o arquivo
- **Erro de DLL**: Instale Visual C++ Redistributable mais recente
- **Interface não aparece**: Execute como administrador

### macOS
- **"Não é possível abrir"**: Execute `xattr -d com.apple.quarantine MouseRecorder`
- **Permissões negadas**: Verifique configurações de acessibilidade
- **Crash ao iniciar**: Verifique versão do macOS (requer 10.13+)

## Funcionalidades

✅ Gravação de movimentos do mouse
✅ Gravação de cliques (esquerdo, direito, meio)
✅ Gravação de scroll
✅ Reprodução com controle de velocidade
✅ Repetições configuráveis
✅ Hotkeys globais (F9, F10, ESC)
✅ Salvamento/carregamento de gravações
✅ Interface gráfica intuitiva
✅ Configurações avançadas

## Código Fonte

O código fonte completo está disponível em: https://github.com/icl00ud/mouse-recorder

## Suporte

Para reportar bugs ou solicitar funcionalidades, abra uma issue no GitHub:
https://github.com/icl00ud/mouse-recorder/issues
