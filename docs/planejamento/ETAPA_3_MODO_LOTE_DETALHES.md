# DETALHES DO MODO LOTE - Funcionalidade Adicional

## Visão Geral

O **Modo Lote** permite gerar múltiplos documentos RPCM que compartilham a mesma regulamentação, mas possuem dados diferentes (Grupo, Subgrupo, Nº Preço, Descrição, Unidade).

### Caso de Uso Típico
Você tem uma regulamentação padrão para "Tubulação PVC" e precisa gerar 50 documentos diferentes, cada um com:
- Diferentes diâmetros (descrição)
- Diferentes números de preço
- Mesmos grupo e subgrupo
- Mesma unidade (m)
- **Mesma regulamentação**

Sem o Modo Lote: você precisaria copiar/colar a regulamentação 50 vezes.
Com o Modo Lote: você preenche a regulamentação uma vez e apenas adiciona os dados variáveis.

---

## Fluxo de Trabalho - Modo Lote

### 1. Ativar Modo Lote
```
[Interface]
┌─────────────────────────────────────┐
│ ⚪ Modo Individual  🔵 Modo Lote    │
└─────────────────────────────────────┘
```

### 2. Preencher Regulamentação (Uma Única Vez)
- Digitar ou colar do Word
- Formatação rica (listas, tabelas, etc.)
- Esta regulamentação será usada em **todos** os documentos da lista

### 3. Adicionar Documentos à Lista

**Opção A: Preencher Manualmente**
1. Preencher campos: Grupo, Subgrupo (opcional), Nº Preço, Descrição, Unidade
2. Clicar em **[+ Adicionar à Lista]** ou pressionar **Enter**
3. Campos de dados são limpos (regulamentação permanece)
4. Foco volta para campo Grupo
5. Repetir para próximo documento

**Opção B: Importar de Excel**
1. Preparar arquivo Excel com colunas:
   - Grupo
   - Subgrupo (opcional)
   - Nº Preço
   - Descrição
   - Unidade
2. Clicar em **[Importar Excel]**
3. Selecionar arquivo
4. Todos os itens são adicionados automaticamente

### 4. Revisar Lista
```
┌─────────────────────────────────────────────────────────┐
│ LISTA DE DOCUMENTOS                                      │
├────────────┬─────────────┬──────────────┬──────────┬────┤
│ Nº Preço   │ Grupo       │ Descrição    │ Unidade  │ [X]│
├────────────┼─────────────┼──────────────┼──────────┼────┤
│ 123456     │ INFRA       │ Tubo Ø 50mm  │ m        │ [X]│
│ 123457     │ INFRA       │ Tubo Ø 75mm  │ m        │ [X]│
│ 123458     │ INFRA       │ Tubo Ø 100mm │ m        │ [X]│
└────────────┴─────────────┴──────────────┴──────────┴────┘
```

- Visualizar todos os documentos que serão gerados
- Remover itens indesejados (botão [X])
- Editar itens (clique duplo - opcional)

### 5. Gerar Todos os Documentos
1. Clicar em **[Gerar Documentos]**
2. Selecionar **pasta de destino**
3. Sistema gera todos os documentos automaticamente
4. Barra de progresso mostra andamento
5. Resumo final com estatísticas

---

## Interface Detalhada - Modo Lote

### Componente: Tabela de Lista

```python
# src/gui/widgets/document_list_table.py

import tkinter as tk
from tkinter import ttk

class DocumentListTable(ttk.Frame):
    """Tabela para exibir lista de documentos no Modo Lote"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Criar Treeview
        self.tree = ttk.Treeview(
            self,
            columns=('numero', 'grupo', 'subgrupo', 'descricao', 'unidade'),
            show='headings',
            height=10
        )
        
        # Definir cabeçalhos
        self.tree.heading('numero', text='Nº Preço')
        self.tree.heading('grupo', text='Grupo')
        self.tree.heading('subgrupo', text='Subgrupo')
        self.tree.heading('descricao', text='Descrição')
        self.tree.heading('unidade', text='Unidade')
        
        # Definir larguras
        self.tree.column('numero', width=80)
        self.tree.column('grupo', width=150)
        self.tree.column('subgrupo', width=120)
        self.tree.column('descricao', width=250)
        self.tree.column('unidade', width=60)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Menu de contexto (botão direito)
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Remover", command=self.remover_selecionado)
        self.context_menu.add_command(label="Editar", command=self.editar_selecionado)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Limpar Todos", command=self.limpar_todos)
        
        # Bind eventos
        self.tree.bind("<Button-3>", self.mostrar_menu_contexto)
        self.tree.bind("<Delete>", lambda e: self.remover_selecionado())
        self.tree.bind("<Double-1>", lambda e: self.editar_selecionado())
        
        # Layout
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def adicionar_item(self, documento):
        """Adiciona item à tabela"""
        self.tree.insert('', 'end', values=(
            documento.numero_preco,
            documento.grupo,
            documento.subgrupo,
            documento.descricao,
            documento.unidade
        ))
    
    def remover_item(self, numero_preco):
        """Remove item da tabela"""
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == numero_preco:
                self.tree.delete(item)
                break
    
    def limpar_todos(self):
        """Remove todos os itens"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def obter_todos_items(self):
        """Retorna lista de todos os itens"""
        items = []
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            items.append({
                'numero_preco': values[0],
                'grupo': values[1],
                'subgrupo': values[2],
                'descricao': values[3],
                'unidade': values[4]
            })
        return items
    
    def get_count(self):
        """Retorna número de itens na lista"""
        return len(self.tree.get_children())
```

### Componente: Janela de Progresso

```python
# src/gui/widgets/progress_window.py

import tkinter as tk
from tkinter import ttk

class ProgressWindow:
    """Janela modal para mostrar progresso de geração em lote"""
    
    def __init__(self, parent, total_documentos):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerando Documentos")
        self.window.geometry("500x150")
        self.window.resizable(False, False)
        
        # Centralizar janela
        self.window.transient(parent)
        self.window.grab_set()
        
        # Label de status
        self.label_status = tk.Label(
            self.window,
            text="Preparando geração...",
            font=("Arial", 10)
        )
        self.label_status.pack(pady=20)
        
        # Barra de progresso
        self.progress_bar = ttk.Progressbar(
            self.window,
            mode='determinate',
            length=450,
            maximum=100
        )
        self.progress_bar.pack(pady=10)
        
        # Label de porcentagem
        self.label_percent = tk.Label(
            self.window,
            text="0%",
            font=("Arial", 9)
        )
        self.label_percent.pack()
        
        # Botão cancelar (opcional)
        self.btn_cancelar = ttk.Button(
            self.window,
            text="Cancelar",
            command=self.cancelar
        )
        self.btn_cancelar.pack(pady=10)
        
        self.total = total_documentos
        self.cancelado = False
    
    def update_progress(self, porcentagem, mensagem):
        """Atualiza barra de progresso"""
        self.progress_bar['value'] = porcentagem
        self.label_status.config(text=mensagem)
        self.label_percent.config(text=f"{int(porcentagem)}%")
        self.window.update()
    
    def cancelar(self):
        """Marca geração como cancelada"""
        self.cancelado = True
        self.close()
    
    def close(self):
        """Fecha a janela"""
        self.window.destroy()
```

---

## Formato do Arquivo Excel para Importação

### Estrutura Esperada

```excel
┌──────────────────────┬────────────┬──────────┬─────────────────────────┬─────────┐
│ Grupo                │ Subgrupo   │ Nº Preço │ Descrição               │ Unidade │
├──────────────────────┼────────────┼──────────┼─────────────────────────┼─────────┤
│ INFRAESTRUTURA ÁGUA  │ ADUÇÃO     │ 123456   │ Tubo PVC Ø 50mm         │ m       │
│ INFRAESTRUTURA ÁGUA  │ ADUÇÃO     │ 123457   │ Tubo PVC Ø 75mm         │ m       │
│ INFRAESTRUTURA ÁGUA  │ ADUÇÃO     │ 123458   │ Tubo PVC Ø 100mm        │ m       │
│ INFRAESTRUTURA ÁGUA  │            │ 123459   │ Válvula gaveta Ø 50mm   │ un      │
│ SERVIÇOS GERAIS      │ LIMPEZA    │ 234001   │ Limpeza área externa    │ m²      │
└──────────────────────┴────────────┴──────────┴─────────────────────────┴─────────┘
```

**Notas:**
- Primeira linha deve conter os cabeçalhos exatos
- Coluna "Subgrupo" pode estar vazia (opcional)
- Todas as outras colunas são obrigatórias
- Formatos aceitos: .xlsx, .xls, .csv

### Exemplo CSV

```csv
Grupo,Subgrupo,Nº Preço,Descrição,Unidade
INFRAESTRUTURA ÁGUA,ADUÇÃO,123456,Tubo PVC Ø 50mm,m
INFRAESTRUTURA ÁGUA,ADUÇÃO,123457,Tubo PVC Ø 75mm,m
INFRAESTRUTURA ÁGUA,,123459,Válvula gaveta Ø 50mm,un
SERVIÇOS GERAIS,LIMPEZA,234001,Limpeza área externa,m²
```

---

## Validações no Modo Lote

### 1. Ao Adicionar Item
- ✅ Verificar se campos obrigatórios estão preenchidos
- ✅ Verificar se Nº Preço já existe na lista (não permitir duplicatas)
- ✅ Validar formato do Nº Preço (apenas números)
- ✅ Validar caracteres da descrição (remover inválidos)

### 2. Ao Gerar Documentos
- ✅ Verificar se lista não está vazia
- ✅ Verificar se regulamentação foi preenchida
- ✅ Validar cada documento individualmente
- ✅ Continuar geração mesmo se houver erro em um item

### 3. Ao Importar Excel
- ✅ Verificar se arquivo existe e é legível
- ✅ Verificar se colunas obrigatórias existem
- ✅ Validar dados de cada linha
- ✅ Reportar erros por linha (não abortar importação completa)

---

## Melhorias Futuras (Opcional)

### 1. Edição Inline
- Clicar duplo em item da tabela abre para edição
- Salvar alterações diretamente

### 2. Reordenação
- Drag & drop para reordenar lista
- Botões "Mover para cima/baixo"

### 3. Filtros e Busca
- Campo de busca para filtrar lista
- Filtros por Grupo, Subgrupo, etc.

### 4. Templates de Lista
- Salvar lista em arquivo JSON
- Carregar lista salva
- Útil para lotes recorrentes

### 5. Pré-visualização
- Botão "Pré-visualizar" mostra como ficará o documento
- Sem gerar o arquivo final

### 6. Geração Assíncrona
- Não travar interface durante geração
- Usar threads para geração em background
- Permitir cancelamento durante geração

---

## Dependência Adicional

Para suporte a Excel, adicionar ao `requirements.txt`:

```txt
pandas>=2.0.0
openpyxl>=3.1.0  # Para .xlsx
xlrd>=2.0.1      # Para .xls (opcional)
```

---

## Casos de Teste Específicos - Modo Lote

### Teste 1: Adicionar Item à Lista
```python
def test_adicionar_item_lista():
    batch = BatchDocumentGenerator()
    
    doc = DocumentoRPCM(
        grupo="GRUPO1",
        subgrupo="SUB1",
        numero_preco="123456",
        descricao="DESC1",
        unidade="m",
        regulamentacao_html="<p>Reg</p>"
    )
    
    batch.adicionar_documento(doc)
    
    assert len(batch.documentos) == 1
    assert batch.documentos[0].numero_preco == "123456"
```

### Teste 2: Rejeitar Duplicata
```python
def test_rejeitar_duplicata():
    batch = BatchDocumentGenerator()
    
    doc1 = DocumentoRPCM(...)  # numero_preco="123456"
    doc2 = DocumentoRPCM(...)  # numero_preco="123456"
    
    batch.adicionar_documento(doc1)
    
    with pytest.raises(ValueError, match="já existe"):
        batch.adicionar_documento(doc2)
```

### Teste 3: Gerar Lote Completo
```python
def test_gerar_lote(tmp_path):
    batch = BatchDocumentGenerator()
    
    # Adicionar 5 documentos
    for i in range(5):
        doc = DocumentoRPCM(
            grupo=f"GRUPO{i}",
            subgrupo="",  # Vazio
            numero_preco=f"{100000+i}",
            descricao=f"DESC{i}",
            unidade="m",
            regulamentacao_html="<p>Reg comum</p>"
        )
        batch.adicionar_documento(doc)
    
    # Gerar todos
    resultados = batch.gerar_todos(str(tmp_path))
    
    assert resultados['sucesso'] == 5
    assert resultados['erro'] == 0
    assert len(resultados['arquivos']) == 5
```

### Teste 4: Importar Excel
```python
def test_importar_excel():
    # Criar Excel de teste
    df = pd.DataFrame({
        'Grupo': ['G1', 'G2'],
        'Subgrupo': ['S1', ''],
        'Nº Preço': ['123', '456'],
        'Descrição': ['D1', 'D2'],
        'Unidade': ['m', 'un']
    })
    
    arquivo = 'teste.xlsx'
    df.to_excel(arquivo, index=False)
    
    batch = BatchDocumentGenerator()
    num_importados = batch.importar_excel(arquivo, "<p>Reg</p>")
    
    assert num_importados == 2
    assert len(batch.documentos) == 2
```

---

## Resumo das Vantagens do Modo Lote

✅ **Eficiência:** Gera múltiplos documentos sem repetir regulamentação  
✅ **Produtividade:** Importação em massa via Excel  
✅ **Organização:** Visualiza lista completa antes de gerar  
✅ **Controle:** Adiciona/remove itens facilmente  
✅ **Feedback:** Barra de progresso e resumo final  
✅ **Robustez:** Continua gerando mesmo se houver erro em um item  
✅ **Flexibilidade:** Combina entrada manual e importação de arquivo  

---

**Tempo de Desenvolvimento Estimado para Modo Lote:** +3-4 dias  
**Total com Modo Lote:** 17-23 dias
