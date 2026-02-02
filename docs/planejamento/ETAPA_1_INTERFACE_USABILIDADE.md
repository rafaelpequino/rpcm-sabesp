# ETAPA 1 - INTERFACE E USABILIDADE

## Objetivo
Criar uma interface gráfica moderna, intuitiva e profissional para capturar os dados necessários para geração dos documentos RPCM.

## Tecnologias Sugeridas

### Framework de Interface
- **CustomTkinter** (Recomendado)
  - Interface moderna com tema escuro/claro
  - Widgets customizados e responsivos
  - Melhor visual que Tkinter tradicional
  
- **PyQt5/PyQt6** (Alternativa robusta)
  - Interface mais profissional
  - Maior flexibilidade de design
  - Curva de aprendizado um pouco maior

## Estrutura da Interface

### Janela Principal
```
┌─────────────────────────────────────────────────────────┐
│  Automação RPCM - Sabesp                   [Modo: ▼][_][□][X]│
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐ │
│  │ ⚪ Modo Individual    🔵 Modo Lote                   │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  DADOS DO DOCUMENTO                                       │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Grupo:        [____________________________]  *      │ │
│  │ Subgrupo:     [____________________________]         │ │
│  │ Nº Preço:     [____________________________]  *      │ │
│  │ Descrição:    [____________________________]  *      │ │
│  │ Unidade:      [____________________________]  *      │ │
│  │                                                       │ │
│  │ [+ Adicionar à Lista] (Modo Lote)                    │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  LISTA DE DOCUMENTOS (Modo Lote)                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Nº Preço  | Grupo          | Descrição      | [X]   │ │
│  │ ──────────────────────────────────────────────────── │ │
│  │ 123456    | INFRA          | Tubulação...   | [X]   │ │
│  │ 123457    | INFRA          | Válvula...     | [X]   │ │
│  │ ...                                                   │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  REGULAMENTAÇÃO (Compartilhada no Modo Lote)              │
│  ┌─────────────────────────────────────────────────────┐ │
│  │                                                       │ │
│  │    [Editor de Texto Rico - Etapa 2]                  │ │
│  │                                                       │ │
│  │                                                       │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  [Gerar Documento(s)]  [Limpar Tudo]  [Importar Excel]   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

**Legenda:** * = Campo obrigatório

## Componentes da Interface

### 1. Seletor de Modo
- **Radio Buttons:** Modo Individual / Modo Lote
- Modo Individual: gera um documento por vez
- Modo Lote: permite adicionar múltiplos documentos com a mesma regulamentação

### 2. Campos de Entrada
- **Grupo**: Entry field com validação (**obrigatório**)
- **Subgrupo**: Entry field (**opcional** - pode estar vazio)
- **Nº Preço**: Entry field numérico (apenas números) (**obrigatório**)
- **Descrição**: Entry field com validação de caracteres especiais (**obrigatório**)
- **Unidade**: Entry field com validação (**obrigatório**)

**Validações necessárias:**
- Grupo, Nº Preço, Descrição e Unidade são **obrigatórios**
- Subgrupo é **opcional** (pode ficar vazio)
- Nº Preço deve aceitar apenas números (ex: "123456")
- Descrição não pode ter caracteres inválidos para nome de arquivo (/, \, :, *, ?, ", <, >, |)

### 3. Tabela de Lista (Modo Lote)
- **Visível apenas no Modo Lote**
- Exibe lista de documentos a serem gerados
- Colunas: Nº Preço, Grupo, Subgrupo, Descrição, Unidade, [Remover]
- Botão [X] para remover item da lista
- Permite edição inline (opcional)
- Destaca linha selecionada

### 4. Área de Editor de Texto
- Área reservada para o editor rico (será implementado na Etapa 2)
- Deve ocupar boa parte da janela
- Scroll vertical quando necessário
- **No Modo Lote:** regulamentação é compartilhada por todos os documentos da lista

### 5. Botões de Ação

#### Adicionar à Lista (Modo Lote)
- **Visível apenas no Modo Lote**
- Valida campos obrigatórios (exceto subgrupo)
- Adiciona item à tabela de lista
- Limpa apenas os campos de dados (mantém regulamentação)
- Foca no campo Grupo para próxima entrada

#### Gerar Documento(s)
- **Modo Individual:** 
  - Valida todos os campos obrigatórios
  - Gera um documento
  - Abre diálogo para salvar
- **Modo Lote:**
  - Valida se há itens na lista
  - Valida se regulamentação foi preenchida
  - Gera todos os documentos da lista
  - Abre diálogo para selecionar pasta de destino
  - Mostra progresso de geração (barra de progresso)
  - Exibe resumo ao final (X documentos gerados)

#### Limpar Tudo
- Limpa todos os campos
- Limpa lista (Modo Lote)
- Limpa o editor de texto
- Reseta o formulário

#### Importar Excel (Opcional - Modo Lote)
- Abre diálogo para selecionar arquivo .xlsx ou .csv
- Importa dados das colunas: Grupo, Subgrupo, Nº Preço, Descrição, Unidade
- Preenche automaticamente a lista
- Valida dados importados

### 6. Barra de Status (rodapé)
- Mostra mensagens de feedback
- Indica status da operação
- **Modo Individual:** "Documento gerado com sucesso"
- **Modo Lote:** "Gerando documento 3 de 10..." com barra de progresso

## Layout e Design

### Paleta de Cores Sugerida
- **Tema Azul Sabesp:**
  - Primário: #0066CC (azul Sabesp)
  - Secundário: #FFFFFF (branco)
  - Fundo: #F5F5F5 (cinza claro)
  - Texto: #333333 (cinza escuro)
  - Sucesso: #28A745
  - Erro: #DC3545

### Tipografia
- **Fonte principal:** Segoe UI ou Arial
- **Tamanhos:**
  - Títulos: 12pt Bold
  - Labels: 10pt
  - Inputs: 10pt
  - Botões: 10pt Bold

### Espaçamento
- Padding interno: 20px
- Margem entre elementos: 10px
- Altura dos campos: 30px
- Largura mínima da janela: 800px
- Altura mínima da janela: 700px

## Estrutura de Arquivos - Etapa 1

```
AutomacaoRPCMs/
│
├── src/
│   ├── __init__.py
│   ├── main.py                 # Ponto de entrada da aplicação
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # Janela principal
│   │   ├── widgets/
│   │   │   ├── __init__.py
│   │   │   ├── input_fields.py # Campos de entrada customizados
│   │   │   └── buttons.py      # Botões customizados
│   │   └── styles.py           # Estilos e temas
│   │
│   └── utils/
│       ├── __init__.py
│       └── validators.py       # Validações de campos
│
├── assets/
│   ├── icons/                  # Ícones da interface
│   └── images/                 # Logo Sabesp, etc
│
├── requirements.txt
└── README.md
```

## Funcionalidades de Usabilidade

### 1. Validação em Tempo Real
- Destacar campos obrigatórios vazios em vermelho
- Mostrar mensagem de erro abaixo do campo inválido
- Desabilitar botão "Gerar Documento" se houver erros

### 2. Feedback Visual
- Animações suaves de transição
- Loading spinner durante geração do documento
- Mensagens de sucesso em verde
- Mensagens de erro em vermelho

### 3. Atalhos de Teclado
- `Ctrl+S`: Salvar/Gerar documento
- `Ctrl+L`: Limpar formulário
- `Tab`: Navegação entre campos
- `Esc`: Cancelar operação

### 4. Persistência de Dados
- Salvar último diretório de saída utilizado (config.json)
- Autocompletar campos baseado em histórico (opcional)
- Lembrar posição e tamanho da janela

### 5. Tratamento de Erros
- Try-catch em todas as operações
- Mensagens de erro amigáveis ao usuário
- Log de erros em arquivo (para debug)

## Implementação Passo a Passo

### Passo 1: Setup Inicial
1. Criar estrutura de pastas
2. Instalar dependências (`pip install customtkinter`)
3. Criar arquivo `main.py` básico

### Passo 2: Janela Principal
1. Criar classe `MainWindow` em `main_window.py`
2. Definir layout básico com CustomTkinter
3. Aplicar tema e cores

### Passo 3: Campos de Entrada
1. Criar componentes de input em `input_fields.py`
2. Adicionar labels e campos na janela
3. Implementar getters e setters

### Passo 4: Validadores
1. Criar classe `Validator` em `validators.py`
2. Implementar validações:
   - `validate_required(value)`: verifica se não está vazio
   - `validate_numero_preco(value)`: valida formato do número
   - `validate_filename(value)`: valida caracteres da descrição
3. Conectar validadores aos campos

### Passo 5: Botões e Ações
1. Criar botões em `buttons.py`
2. Implementar handlers (por enquanto com print/placeholder):
   - `on_gerar_documento()`
   - `on_limpar_tudo()`
3. Conectar botões aos handlers
4. Verificar existência do template na inicialização

### Passo 6: Área do Editor
1. Criar frame placeholder para o editor
2. Adicionar label "Editor será implementado na Etapa 2"
3. Configurar tamanho e scroll

### Passo 7: Barra de Status
1. Criar label de status no rodapé
2. Implementar método `update_status(message, type)`
3. Adicionar timer para auto-limpar mensagens

### Passo 8: Testes de Usabilidade
1. Testar navegação com Tab
2. Validar comportamento de todos os botões
3. Testar validações dos campos
4. Verificar responsividade da janela

## Funcionalidades Extras Modo Lote

### 1. Atalhos de Produtividade
- `Enter` no último campo (Unidade) adiciona à lista automaticamente
- `Ctrl+Enter` em qualquer campo adiciona à lista
- Foco automático no campo Grupo após adicionar

### 2. Validação Inteligente
- Não permite adicionar duplicatas (mesmo Nº Preço)
- Avisa se Nº Preço já existe na lista

### 3. Persistência
- Salvar lista em arquivo JSON (para retomar depois)
- Carregar lista salva

## Critérios de Conclusão da Etapa 1

- [ ] Interface gráfica funcional e apresentável
- [ ] Todos os 5 campos de entrada implementados
- [ ] Validação de campo obrigatório vs opcional (Subgrupo é opcional)
- [ ] Validação de Nº Preço (apenas números) funcionando
- [ ] Seletor de Modo Individual/Lote implementado
- [ ] Tabela de lista (Modo Lote) implementada
- [ ] Botão "Adicionar à Lista" funcionando
- [ ] Botões principais criados (mesmo sem funcionalidade completa)
- [ ] Layout responsivo e organizado
- [ ] Área reservada para editor de texto
- [ ] Feedback visual de erros
- [ ] Template incluído no projeto (templates/template_rpcm.docx)
- [ ] Validação de existência do template na inicialização
- [ ] Código organizado e documentado
- [ ] Requirements.txt criado

## Tempo Estimado
**2-3 dias** de desenvolvimento

## Próxima Etapa
Após conclusão, passar para ETAPA 2 - Implementação do Editor de Texto Rico.
