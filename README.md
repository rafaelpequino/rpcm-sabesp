# 🏢 Automações RPCMS

Sistema integrado com 3 automações essenciais para otimizar o trabalho diário da Sabesp.

## 🚀 Funcionalidades

### 📄 Gerador de RPCM
✅ **Modo Lote** - Gere múltiplos documentos de uma vez  
✅ **Copiar do Excel** - Cole dados diretamente da planilha  
✅ **Template Customizado** - Use seu próprio template .docx  
✅ **Validações Automáticas** - Sistema valida todos os campos  
✅ **Interface Moderna** - Design limpo e intuitivo

### 📁 Organizador de Lotes
✅ **Organização Inteligente** - Copie PDFs do banco para a pasta do lote  
✅ **Verificação Automática** - Verifique quais arquivos estão faltando  
✅ **Detecção de Duplicatas** - Identifica números repetidos  
✅ **Histórico Detalhado** - Log completo de todas as operações

### 🔄 Conversor DOCX → PDF
✅ **Conversão de Alta Qualidade** - Preserva formatação, imagens e tabelas  
✅ **Múltiplos Métodos** - Fallback automático entre Word COM, docx2pdf e Aspose  
✅ **Modo Pasta ou Arquivos** - Converta uma pasta inteira ou arquivos específicos  
✅ **Processamento em Lote** - Converta múltiplos arquivos de uma vez

## 📦 Instalação

### Requisitos
- Python 3.8 ou superior
- Windows 10/11
- Microsoft Word (recomendado para melhor qualidade de conversão PDF)

### Passos

1. Clone ou baixe o projeto

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. **(Opcional)** Para o Gerador de RPCM, coloque um template padrão:
   - Arquivo: `template_rpcm.docx`
   - Local: pasta `templates/`
   - Ou selecione um template na interface

## ▶️ Como Usar

### Executar a Aplicação

```bash
python src/main.py
```

### Navegação

O sistema possui 3 botões principais na parte superior:

1. **📄 Gerador de RPCM** - Para gerar documentos RPCM
2. **📁 Organizador de Lotes** - Para organizar PDFs por lote
3. **🔄 Conversor DOCX → PDF** - Para converter documentos Word em PDF

Clique em qualquer botão para acessar a funcionalidade desejada.

---

## 📄 1. Gerador de RPCM

### Passo 1: Selecionar Template

1. Clique em **"📁 Selecionar Template"**
2. Escolha um arquivo .docx com as variáveis:
   - `{{DESCRICAO}}`, `{{UNIDADE}}`, `{{N_PRECO}}`
3. Veja confirmação: **"✓ Template carregado"**

📚 [Ver documentação completa de templates](docs/SELECIONAR_TEMPLATE.md)

### Passo 2: Adicionar Documentos

#### Opção A: Manual
1. Preencha os campos:
   - Descrição *
   - Unidade * (ex: m, un, kg)
   - Nº Preço (Código) * (apenas números, ex: 400726)
2. Clique em **"➕ Adicionar à Lista"**

#### Opção B: Copiar do Excel ⭐
1. No Excel, copie as linhas (Ctrl+C):
   ```
   Descrição	Unidade	Cód
   Esteira - CT DN400 SERRA TERMAS - PIRAT.	GB	400726
   Esteira - SES Cond Vitória (Beira Rio)	GB	400725
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
400726_Esteira_-_CT_DN400_SERRA_TERMAS_-_PIRAT.docx
400725_Esteira_-_SES_Cond_Vitoria_(Beira_Rio).docx
```

---

## 📁 2. Organizador de Lotes

### Funcionalidade

Copie arquivos PDF de uma pasta "banco" (onde estão todos os arquivos) para uma pasta "lote" (onde ficam apenas os arquivos de um lote específico).

### Como Usar

1. **Selecionar Pasta de Origem (Banco)**
   - Clique em "📂 Selecionar" na seção "Pasta de Origem"
   - Escolha a pasta onde estão TODOS os PDFs

2. **Selecionar Pasta de Destino (Lote)**
   - Clique em "📂 Selecionar" na seção "Pasta de Destino"
   - Escolha a pasta do lote específico

3. **Inserir Lista de Números**
   - Digite os números das RPCMs que deseja copiar
   - Formato: `400006, 400009, 400010` ou um por linha
   - Exemplo:
     ```
     400006
     400009
     400010
     ```

4. **Verificar (Opcional)**
   - Clique em "✓ Verificar Destino" para ver quais arquivos já estão na pasta
   - O sistema mostra:
     - Conformes (já copiados)
     - Ausentes (ainda não copiados)
     - Excedentes (não solicitados)
     - Números repetidos

5. **Organizar Lote**
   - Clique em "🚀 Organizar Lote"
   - Os arquivos serão copiados do banco para o lote
   - Veja o histórico completo no log

### Resultado

- Arquivos copiados da pasta origem para a pasta destino
- Relatório detalhado de quantos foram copiados
- Lista de números não encontrados (se houver)

---

## 🔄 3. Conversor DOCX → PDF

### Funcionalidade

Converte arquivos Word (.docx) para PDF com alta qualidade, preservando toda a formatação.

### Como Usar

1. **Escolher Modo**
   - ⚪ **Converter toda uma pasta** - Converte todos os DOCX de uma pasta
   - ⚪ **Selecionar arquivos específicos** - Escolhe quais arquivos converter

2. **Selecionar Entrada**
   - Se modo "pasta": clique em "📂 Selecionar Pasta" e escolha a pasta com os DOCX
   - Se modo "arquivos": clique em "📄 Selecionar Arquivos" e escolha os arquivos

3. **Selecionar Pasta de Saída**
   - Clique em "📂 Selecionar" na seção "Pasta de Saída"
   - Escolha onde os PDFs serão salvos

4. **Converter**
   - Clique em "🚀 CONVERTER"
   - Acompanhe o progresso no histórico
   - Veja o resumo ao final

### Métodos de Conversão

O sistema tenta automaticamente, nesta ordem:

1. **Microsoft Word COM** (melhor qualidade, requer Word instalado)
2. **docx2pdf** (ótima qualidade, gratuito)
3. **Aspose.Words** (opcional, comercial)

Se um método falhar, o sistema tenta o próximo automaticamente.

### Resultado

- Arquivos PDF salvos na pasta de saída
- Relatório com:
  - Quantidade convertida
  - Método usado para cada arquivo
  - Erros (se houver)

---

## 📁 Estrutura do Projeto

```
AutomacaoRPCMs/
├── src/                       # Código-fonte principal
│   ├── main.py               # Ponto de entrada
│   ├── gui/                  # Interface gráfica
│   │   ├── main_window.py    # Janela principal + navegação
│   │   ├── organizador_lotes.py  # Frame do organizador
│   │   ├── conversor_pdf.py  # Frame do conversor
│   │   └── styles.py         # Estilos Sabesp
│   ├── models/               # Modelos de dados
│   │   └── documento_rpcm.py
│   ├── core/                 # Lógica de negócio
│   │   └── document_generator.py
│   ├── converters/           # Conversores
│   │   ├── html_to_docx.py
│   │   └── word_html_cleaner.py
│   └── utils/                # Utilitários
│       ├── validators.py
│       ├── logger_config.py
│       └── config_manager.py
├── templates/
│   ├── template_rpcm.docx    # Template (você deve criar)
│   └── README.md             # Instruções
├── docs/                     # Documentação
├── tests/                    # Testes automatizados
├── requirements.txt          # Dependências
└── README.md                 # Este arquivo
```

## 🎨 Características da Interface

- **Design moderno** com CustomTkinter
- **Navegação por abas** - 3 funcionalidades integradas
- **Cores Sabesp** (azul #0066CC)
- **Responsiva** e intuitiva
- **Feedback visual** em tempo real
- **Validações** antes de processar
- **Mensagens claras** de erro/sucesso

## 📝 Validações do Gerador RPCM

### Campos Obrigatórios (*)
- Descrição
- Unidade
- Nº Preço (Código) - apenas números

### Validações Especiais
- **Nº Preço:** apenas números (ex: 400726)
- **Descrição:** não permite caracteres inválidos para nome de arquivo: / \ : * ? " < > |
- **Duplicatas:** não permite adicionar mesmo Nº Preço duas vezes
- **Template:** valida se é .docx e se pode ser aberto

## 🐛 Solução de Problemas

### Gerador de RPCM

**"Nenhum template selecionado"**
→ Clique em "📁 Selecionar Template" e escolha um arquivo .docx

**"Template Inválido"**
→ Certifique-se de que o arquivo é .docx válido e pode ser aberto no Word

**"Clipboard Vazio"**
→ Copie os dados do Excel primeiro (Ctrl+C) antes de clicar em "Copiar do Excel"

### Organizador de Lotes

**"Pasta de origem não existe"**
→ Verifique se selecionou a pasta correta do banco

**"Números não encontrados"**
→ Verifique se os números estão corretos e se os arquivos existem na pasta origem

### Conversor PDF

**"Nenhum método de conversão disponível"**
→ Instale pelo menos uma das bibliotecas de conversão:
```bash
pip install pywin32 docx2pdf
```

**"Erro no Word COM"**
→ Certifique-se de que o Microsoft Word está instalado

### Geral

**Erro ao instalar dependências**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Interface não abre**
→ Verifique se Python 3.8+ está instalado:
```bash
python --version
```

### Mais ajuda
- 📚 [Documentação: Copiar do Excel](docs/COPIAR_EXCEL.md)
- 📚 [Documentação: Selecionar Template](docs/SELECIONAR_TEMPLATE.md)

## 📄 Licença

Uso interno - Sabesp

---

**Versão:** 4.0.0 (Sistema Unificado)  
**Última atualização:** 10/02/2026  
**Funcionalidades:** Gerador RPCM + Organizador de Lotes + Conversor DOCX → PDF
