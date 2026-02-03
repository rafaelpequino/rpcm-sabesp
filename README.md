# 📋 Automação RPCM - Sabesp

Sistema de geração automatizada de documentos RPCM com interface gráfica moderna.

## 🚀 Status do Desenvolvimento

✅ **ETAPA 1 - Interface e Usabilidade** - CONCLUÍDA (02/02/2026)
✅ **ETAPA 3 - Funcionalidades de Automação** - CONCLUÍDA (03/02/2026)

**Progresso:** 50% (2 de 4 etapas)

| Etapa | Status | Descrição |
|-------|--------|-----------|
| Etapa 1 | ✅ 100% | Interface e Usabilidade |
| Etapa 2 | 📋 0% | Editor de Texto Rico |
| Etapa 3 | ✅ 100% | Funcionalidades de Automação |
| Etapa 4 | 📋 0% | Testes e Refinamentos |

Próximas etapas:
- 🔨 Etapa 2 - Editor de Texto Rico (PRÓXIMA - mais crítica)
- 📋 Etapa 4 - Testes e Refinamentos

## 📦 Instalação

### Requisitos
- Python 3.8 ou superior
- Windows 10/11

### Passos

1. Clone ou baixe o projeto

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Coloque o template DOCX:
   - Arquivo: `template_rpcm.docx`
   - Local: pasta `templates/`
   - Veja instruções em `templates/README.md`

## ▶️ Como Usar

### Executar a Aplicação

```bash
python src/main.py
```

### Modo Individual
1. Selecione "Modo Individual"
2. Preencha os campos:
   - Grupo *
   - Subgrupo (opcional)
   - Nº Preço * (apenas números, ex: 123456)
   - Descrição *
   - Unidade *
3. Preencha a regulamentação
4. Clique em "Gerar Documento"
5. Escolha onde salvar

### Modo Lote
1. Selecione "Modo Lote"
2. Preencha a regulamentação (UMA VEZ para todos)
3. Adicione documentos:
   - Preencha os campos e clique "Adicionar à Lista"
   - OU clique "Importar Excel" (formato: Grupo, Subgrupo, Nº Preço, Descrição, Unidade)
4. Clique em "Gerar Documentos"
5. Escolha a pasta de destino
6. ✓ Todos os documentos serão gerados!

## 📁 Estrutura do Projeto

```
AutomacaoRPCMs/
├── src/                       # Código-fonte principal
│   ├── main.py               # Ponto de entrada
│   ├── gui/                  # Interface gráfica
│   │   ├── main_window.py    # Janela principal (✅ Etapas 1 e 3)
│   │   └── styles.py         # Estilos Sabesp
│   ├── models/               # ✅ Etapa 3
│   │   └── documento_rpcm.py # Modelo de dados
│   ├── core/                 # ✅ Etapa 3
│   │   └── document_generator.py # Geradores
│   ├── converters/           # ✅ Etapa 3
│   │   ├── html_to_docx.py   # Conversor HTML→DOCX
│   │   └── word_html_cleaner.py # Limpador de HTML
│   └── utils/
│       ├── validators.py     # Validações (✅ Etapa 1)
│       ├── logger_config.py  # Sistema de logging (✅ Etapa 3)
│       └── config_manager.py # Configurações (✅ Etapa 3)
├── templates/
│   ├── template_rpcm.docx    # Template (você deve criar)
│   └── README.md             # Instruções para template
├── docs/                     # 📚 Documentação
│   ├── planejamento/         # Planejamento das etapas
│   │   ├── README_PLANEJAMENTO_FINAL.md  # Visão geral
│   │   ├── ETAPA_1_*.md      # ✅ Etapa 1 concluída
│   │   ├── ETAPA_2_*.md      # 📋 Próxima
│   │   ├── ETAPA_3_*.md      # ✅ Etapa 3 concluída
│   │   └── ETAPA_4_*.md      # 📋 Planejada
│   └── projeto/              # Documentação do projeto
│       ├── INICIO_RAPIDO.md  # Guia rápido
│       └── ESTRUTURA_PROJETO.md  # Estrutura detalhada
├── tests/                    # Testes automatizados
│   ├── test_etapa1.py        # ✅ 13 testes (100%)
│   └── test_etapa3.py        # ✅ 24 testes (100%)
├── requirements.txt          # Dependências
└── README.md                 # Este arquivo
```

## ✅ Funcionalidades Implementadas

### Etapa 1 - Interface
- ✅ Interface gráfica moderna com CustomTkinter
- ✅ Seletor de Modo (Individual / Lote)
- ✅ Campos de entrada validados
- ✅ Subgrupo como campo OPCIONAL
- ✅ Validação de Nº Preço (apenas números)
- ✅ Validação de caracteres inválidos na Descrição
- ✅ Tabela de lista para Modo Lote
- ✅ Adicionar/remover itens da lista
- ✅ Detecção de duplicatas (mesmo Nº Preço)
- ✅ Área reservada para editor (placeholder temporário)
- ✅ Botões de ação com feedback visual
- ✅ Barra de status com cores
- ✅ Verificação de existência do template

### Etapa 3 - Automação
- ✅ **Geração REAL de documentos DOCX**
- ✅ **Modo Individual funcionando**
- ✅ **Modo Lote funcionando**
- ✅ **Importação de Excel/CSV funcionando**
- ✅ Processamento do template com variáveis `{{VAR}}`
- ✅ Inserção da regulamentação HTML convertida
- ✅ Conversor HTML→DOCX com preservação de formatação
- ✅ Espaçamento 1,5 e Arial 10pt aplicados
- ✅ Limpador de HTML do Word
- ✅ Sistema de logging completo
- ✅ Gerenciador de configurações
- ✅ Tratamento de erros robusto
- ✅ Callback de progresso para modo lote
- ✅ Nome de arquivo: `NumPreco_Descricao.docx`

## 🔮 Próximas Funcionalidades

### Etapa 2 - Editor de Texto Rico ⭐ (PRÓXIMA)
- CKEditor 5 embarcado via pywebview
- Plugin PasteFromOffice (colar do Word/PDF com 100% formatação)
- Espaçamento 1,5 automático e forçado
- Arial 10pt automático e forçado
- Suporte completo a listas multi-nível
- Suporte completo a tabelas complexas
- 13 testes críticos de validação

### Etapa 4 - Testes e Refinamentos
- Testes de integração completos
- Testes com dados reais da Sabesp
- Validação de compatibilidade (Word 2010-365)
- Otimizações de performance
- Correções finais

## 🎨 Características da Interface

- **Design moderno** com CustomTkinter
- **Cores Sabesp** (azul #0066CC)
- **Responsiva** e intuitiva
- **Feedback visual** em tempo real
- **Validações** antes de processar
- **Mensagens claras** de erro/sucesso

## 📝 Validações Implementadas

### Campos Obrigatórios (*)
- Grupo
- Nº Preço (apenas números)
- Descrição (sem caracteres especiais)
- Unidade
- Regulamentação

### Campo Opcional
- Subgrupo (pode ficar vazio)

### Validações Especiais
- **Nº Preço:** apenas números (ex: 123456)
- **Descrição:** não permite caracteres inválidos para nome de arquivo: / \ : * ? " < > |
- **Duplicatas:** não permite adicionar mesmo Nº Preço duas vezes no modo lote

## ⚙️ Configurações

As configurações de estilo estão em `src/gui/styles.py`:
- Cores da interface
- Fontes e tamanhos
- Espaçamentos
- Tema (claro/escuro)

## 🐛 Solução de Problemas

### "Template não encontrado"
→ Coloque `template_rpcm.docx` na pasta `templates/`

### Erro ao instalar CustomTkinter
```bash
pip install --upgrade pip
pip install customtkinter
```

### Interface não abre
→ Verifique se Python 3.8+ está instalado:
```bash
python --version
```

### Mais ajuda
- Consulte [docs/projeto/INICIO_RAPIDO.md](docs/projeto/INICIO_RAPIDO.md)
- Veja [docs/planejamento/ETAPA_1_CONCLUIDA.md](docs/planejamento/ETAPA_1_CONCLUIDA.md)

## 📄 Licença

Uso interno - Sabesp

## 👨‍💻 Desenvolvimento

Este projeto está sendo desenvolvido em 4 etapas. Consulte a documentação:

- **[docs/planejamento/README_PLANEJAMENTO_FINAL.md](docs/planejamento/README_PLANEJAMENTO_FINAL.md)** - Planejamento completo
- **[docs/planejamento/](docs/planejamento/)** - Detalhes de cada etapa

**Status Atual:**
- ✅ Etapa 1: Interface e Usabilidade (100%)
- 📋 Etapa 2: Editor de Texto Rico (0% - PRÓXIMA)
- ✅ Etapa 3: Funcionalidades de Automação (100%)
- 📋 Etapa 4: Testes e Refinamentos (0%)

**Observação:** A Etapa 3 foi concluída antes da Etapa 2. O editor atual é temporário (textbox simples). O editor rico PERFEITO será implementado na Etapa 2. Os conversores HTML→DOCX já estão prontos e testados.

---

**Versão:** 2.0.0 (Etapas 1 e 3 concluídas)  
**Última atualização:** 03/02/2026  
**Progresso:** 50% (2/4 etapas)
