# 📋 Automação RPCM - Sabesp

Sistema simplificado de geração automatizada de documentos RPCM com interface gráfica moderna.

## 🚀 Funcionalidades

✅ **Modo Lote** - Gere múltiplos documentos de uma vez  
✅ **Copiar do Excel** - Cole dados diretamente da planilha  
✅ **Template Customizado** - Use seu próprio template .docx  
✅ **Validações Automáticas** - Sistema valida todos os campos  
✅ **Interface Moderna** - Design limpo e intuitivo

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

3. **(Opcional)** Coloque um template padrão:
   - Arquivo: `template_rpcm.docx`
   - Local: pasta `templates/`
   - Ou selecione um template na interface

## ▶️ Como Usar

### Executar a Aplicação

```bash
python src/main.py
```

### Passo 1: Selecionar Template

1. Clique em **"📁 Selecionar Template"**
2. Escolha um arquivo .docx com as variáveis:
   - `{{GRUPO}}`, `{{SUBGRUPO}}`, `{{N_PRECO}}`, `{{DESCRICAO}}`, `{{UNIDADE}}`
3. Veja confirmação: **"✓ Template carregado"**

📚 [Ver documentação completa de templates](docs/SELECIONAR_TEMPLATE.md)

### Passo 2: Adicionar Documentos

#### Opção A: Manual
1. Preencha os campos:
   - Grupo *
   - Subgrupo (opcional)
   - Nº Preço * (apenas números, ex: 123456)
   - Descrição *
   - Unidade *
2. Clique em **"➕ Adicionar à Lista"**

#### Opção B: Copiar do Excel ⭐
1. No Excel, copie as linhas (Ctrl+C):
   ```
   Grupo 1	Subgrupo 1	100001	Exemplo de Descrição 1	Un
   Grupo 2	Subgrupo 2	100002	Exemplo de Descrição 2	Un
   ```
2. No sistema, clique em **"📋 Copiar do Excel"**
3. ✓ Itens adicionados automaticamente!

📚 [Ver documentação completa do Copiar do Excel](docs/COPIAR_EXCEL.md)

### Passo 3: Gerar Documentos

1. Revise a lista de documentos
2. Clique em **"📄 Gerar Documentos"**
3. Escolha a pasta de destino
4. ✓ Todos os documentos serão gerados!

### Resultado

Arquivos gerados no formato:
```
100001_Exemplo_de_Descrição_1.docx
100002_Exemplo_de_Descrição_2.docx
```

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

### Interface Simplificada
- ✅ Interface moderna com CustomTkinter
- ✅ **Modo Lote** (único modo - mais simples)
- ✅ Campos de entrada validados
- ✅ Subgrupo como campo OPCIONAL
- ✅ Validação de Nº Preço (apenas números)
- ✅ Validação de caracteres inválidos na Descrição
- ✅ Tabela de lista interativa
- ✅ Adicionar/remover itens da lista
- ✅ Detecção de duplicatas (mesmo Nº Preço)
- ✅ Botões de ação com feedback visual
- ✅ Barra de status com cores

### Copiar do Excel ⭐ NOVO
- ✅ Cole dados diretamente do Excel (Ctrl+C → Copiar do Excel)
- ✅ Lê formato TSV (Tab-Separated Values)
- ✅ Validação automática de cada linha
- ✅ Ignora cabeçalho automaticamente
- ✅ Detecta e ignora duplicatas
- ✅ Relatório detalhado de importação

### Template Customizado ⭐ NOVO
- ✅ Selecione qualquer arquivo .docx como template
- ✅ Validação automática do template
- ✅ Indicador visual do template atual
- ✅ Suporte a múltiplos templates
- ✅ Template padrão opcional

### Geração de Documentos
- ✅ **Geração REAL de documentos DOCX**
- ✅ **Modo Lote funcionando**
- ✅ Processamento do template com variáveis `{{VAR}}`
- ✅ Sistema de logging completo
- ✅ Tratamento de erros robusto
- ✅ Callback de progresso para modo lote
- ✅ Nome de arquivo: `NumPreco_Descricao.docx`

## 🔮 Possíveis Melhorias Futuras

- Editor de texto rico para descrições mais complexas
- Importação direta de arquivo Excel (além do clipboard)
- Histórico de templates recentes
- Pré-visualização do documento antes de gerar
- Exportação para outros formatos (PDF, etc)

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
- Descrição
- Unidade

### Campo Opcional
- Subgrupo (pode ficar vazio)

### Validações Especiais
- **Nº Preço:** apenas números (ex: 123456)
- **Descrição:** não permite caracteres inválidos para nome de arquivo: / \ : * ? " < > |
- **Duplicatas:** não permite adicionar mesmo Nº Preço duas vezes
- **Template:** valida se é .docx e se pode ser aberto

## ⚙️ Configurações

As configurações de estilo estão em `src/gui/styles.py`:
- Cores da interface
- Fontes e tamanhos
- Espaçamentos
- Tema (claro/escuro)

## 🐛 Solução de Problemas

### "Nenhum template selecionado"
→ Clique em "📁 Selecionar Template" e escolha um arquivo .docx

### "Template Inválido"
→ Certifique-se de que o arquivo é .docx válido e pode ser aberto no Word

### "Clipboard Vazio"
→ Copie os dados do Excel primeiro (Ctrl+C) antes de clicar em "Copiar do Excel"

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
- 📚 [Documentação: Copiar do Excel](docs/COPIAR_EXCEL.md)
- 📚 [Documentação: Selecionar Template](docs/SELECIONAR_TEMPLATE.md)
- 📚 [Guia Rápido](docs/projeto/INICIO_RAPIDO.md)

## 📄 Licença

Uso interno - Sabesp

---

**Versão:** 3.0.0 (Sistema Simplificado)  
**Última atualização:** 06/02/2026  
**Funcionalidades:** Modo Lote + Copiar Excel + Template Customizado
