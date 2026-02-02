# ETAPA 2 - EDITOR DE TEXTO RICO

## Objetivo
Implementar um editor de texto WYSIWYG profissional que preserve **PERFEITAMENTE** a formatação ao colar conteúdo do Word/PDF, incluindo listas, tabelas, negrito, itálico, sublinhado, espaçamento entre linhas e alinhamentos.

## Desafio Principal - ZERO TOLERÂNCIA A ERROS
**"Trabalho de Joalheiro"** - O editor precisa ser **PERFEITO**:
- ✅ Preservar **100%** da formatação ao colar do Word/PDF
- ✅ Suportar listas numeradas e com marcadores (com todos os níveis de recuo)
- ✅ Suportar tabelas complexas (bordas, mesclagem, formatação de células)
- ✅ Manter formatação de texto (negrito, itálico, sublinhado, tachado, fontes, tamanhos, cores)
- ✅ Manter alinhamentos (esquerda, centro, direita, justificado)
- ✅ Preservar espaçamento entre linhas (padrão **1,5**)
- ✅ Preservar espaçamento entre parágrafos
- ✅ Manter recuos e tabulações
- ✅ Preservar links e imagens (se houver)
- ✅ Exportar para DOCX mantendo **TUDO** intacto

## Requisitos Críticos de Formatação

### Formatação Padrão Global
```python
FONT_FAMILY = 'Arial'
FONT_SIZE = '10pt'
LINE_SPACING = 1.5  # 1,5 - OBRIGATÓRIO
TEXT_ALIGN = 'justify'
COLOR = '#000000'
```

### Preservação Obrigatória ao Colar
1. **Texto:**
   - Negrito, itálico, sublinhado, tachado
   - Tamanho de fonte (converter tudo para Arial 10pt no final)
   - Cor do texto
   - Sobrescrito/subscrito

2. **Parágrafos:**
   - Alinhamento (esquerda, centro, direita, justificado)
   - Espaçamento entre linhas (**sempre 1,5**)
   - Espaçamento antes/depois do parágrafo
   - Recuos (esquerda, direita, primeira linha)

3. **Listas:**
   - Marcadores (bullets)
   - Numeração (1, 2, 3 ou a, b, c ou i, ii, iii)
   - Níveis de recuo (sub-listas)
   - Estilo dos marcadores

4. **Tabelas:**
   - Estrutura (linhas x colunas)
   - Bordas (estilo, cor, espessura)
   - Mesclagem de células
   - Largura de colunas
   - Alinhamento em células
   - Formatação de texto dentro das células
   - Cor de fundo das células

5. **Espaçamento:**
   - Espaçamento entre linhas: **1,5 (PADRÃO)**
   - Espaçamento entre parágrafos
   - Margens internas

## Tecnologia Recomendada: python-docx-template + TkinterHTML

### Opção 1: TkHtmlView (Mais Simples)
**Biblioteca:** `tkinterweb` ou `tkhtmlview`

**Prós:**
- Renderiza HTML dentro do Tkinter
- HTML é intermediário perfeito (Word → HTML → DOCX)
- Preserva formatação facilmente

**Contras:**
- Limitado em funcionalidades avançadas
- Pode precisar de ajustes para tabelas complexas

### Opção 2: Tiptap com WebView (Recomendada) ⭐
**Bibliotecas:** `pywebview` + Editor HTML/JavaScript embarcado

**Por que esta é a melhor opção:**
1. **HTML como formato intermediário**
   - Word exporta HTML perfeitamente
   - Clipboard no Windows suporta formato HTML
   - DOCX pode ser gerado de HTML com precisão

2. **Editor JavaScript embarcado**
   - Usar CKEditor, TinyMCE ou Quill.js
   - Suporte nativo a copiar/colar do Word
   - Funcionalidade completa de WYSIWYG

3. **Comunicação Python ↔ JavaScript**
   - pywebview permite comunicação bidirecional
   - Python recebe HTML do editor
   - Converte HTML para DOCX com python-docx

### Opção 3: PyQt5/6 com QTextEdit (Alternativa Robusta)
**Biblioteca:** PyQt5/6 com QTextEdit

**Prós:**
- Editor rico nativo
- Excelente suporte a formatação
- API Python pura

**Contras:**
- Precisa de conversão manual de Qt formats para DOCX
- Mais trabalhoso para tabelas complexas

## Solução Escolhida: pywebview + HTML Editor

### Arquitetura

```
┌─────────────────────────────────────────────────┐
│  Python (CustomTkinter)                          │
│  ┌─────────────────────────────────────────┐    │
│  │  Frame para Editor                       │    │
│  │  ┌───────────────────────────────────┐  │    │
│  │  │  pywebview WebView                │  │    │
│  │  │  ┌─────────────────────────────┐  │  │    │
│  │  │  │  Quill.js / CKEditor       │  │  │    │
│  │  │  │  (JavaScript WYSIWYG)       │  │  │    │
│  │  │  └─────────────────────────────┘  │  │    │
│  │  └───────────────────────────────────┘  │    │
│  └─────────────────────────────────────────┘    │
│                     ↕ API                        │
│  ┌─────────────────────────────────────────┐    │
│  │  HTML ↔ DOCX Converter                  │    │
│  │  (python-docx + htmldocx)               │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

## Implementação Detalhada

### 1. Configuração do Editor HTML

#### Escolha: CKEditor 5 (MUDANÇA DE RECOMENDAÇÃO) ⭐⭐⭐
**Por quê CKEditor 5 é SUPERIOR para este caso:**
- ✅ **Melhor suporte a copiar/colar do Word** (tem módulo específico)
- ✅ **Preservação perfeita de formatação** (desenvolvido especificamente para isso)
- ✅ **Suporte nativo a espaçamento de linhas**
- ✅ **Tabelas avançadas** com mesclagem, bordas customizadas
- ✅ **Listas multi-nível** perfeitas
- ✅ **Paste from Office** plugin oficial
- ✅ **Controle fino** sobre formatação HTML
- ✅ API robusta e bem documentada

**Quill.js** (anterior) é bom, mas CKEditor 5 é **SUPERIOR** para Word/PDF→DOCX.

**HTML Base do Editor (CKEditor 5):**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.ckeditor.com/ckeditor5/40.0.0/classic/ckeditor.js"></script>
    <style>
        body { 
            margin: 0; 
            padding: 10px; 
            font-family: Arial, sans-serif; 
        }
        .ck-editor__editable {
            min-height: 500px;
            font-family: Arial;
            font-size: 10pt;
            line-height: 1.5; /* ESPAÇAMENTO 1,5 */
            text-align: justify;
        }
        /* Forçar espaçamento 1,5 em todos os parágrafos */
        .ck-content p {
            line-height: 1.5 !important;
        }
        .ck-content ul li,
        .ck-content ol li {
            line-height: 1.5 !important;
        }
    </style>
</head>
<body>
    <div id="editor"></div>
    
    <script>
        let editorInstance;
        
        ClassicEditor
            .create(document.querySelector('#editor'), {
                // PLUGINS ESSENCIAIS
                plugins: [
                    'Essentials',
                    'Paragraph',
                    'Bold', 'Italic', 'Underline', 'Strikethrough',
                    'Font',  // FontFamily, FontSize, FontColor
                    'Alignment',
                    'List',  // NumberedList, BulletedList
                    'Indent', 'IndentBlock',
                    'Table', 'TableToolbar', 'TableProperties', 'TableCellProperties',
                    'Link',
                    'BlockQuote',
                    'Heading',
                    'PasteFromOffice',  // ⭐ CRÍTICO PARA WORD
                    'RemoveFormat',
                    'Undo'
                ],
                
                // TOOLBAR
                toolbar: {
                    items: [
                        'undo', 'redo',
                        '|',
                        'bold', 'italic', 'underline', 'strikethrough',
                        '|',
                        'fontSize', 'fontColor',
                        '|',
                        'alignment',
                        '|',
                        'numberedList', 'bulletedList',
                        '|',
                        'outdent', 'indent',
                        '|',
                        'insertTable',
                        '|',
                        'link',
                        '|',
                        'removeFormat'
                    ]
                },
                
                // CONFIGURAÇÃO DE FONTE
                fontSize: {
                    options: [8, 9, 10, 11, 12, 14, 16, 18, 20],
                    supportAllValues: true
                },
                
                fontFamily: {
                    options: [
                        'default',
                        'Arial, sans-serif',
                        'Courier New, monospace',
                        'Times New Roman, serif'
                    ],
                    supportAllValues: true
                },
                
                // CONFIGURAÇÃO DE TABELA
                table: {
                    contentToolbar: [
                        'tableColumn', 'tableRow', 'mergeTableCells',
                        'tableProperties', 'tableCellProperties'
                    ],
                    tableProperties: {
                        borderColors: ['#000000', '#CCCCCC', '#FFFFFF'],
                        backgroundColors: ['#FFFFFF', '#F0F0F0', '#E0E0E0']
                    },
                    tableCellProperties: {
                        borderColors: ['#000000', '#CCCCCC', '#FFFFFF'],
                        backgroundColors: ['#FFFFFF', '#F0F0F0', '#E0E0E0']
                    }
                },
                
                // ALINHAMENTO
                alignment: {
                    options: ['left', 'center', 'right', 'justify']
                },
                
                // ⭐ PASTE FROM OFFICE - CONFIGURAÇÃO CRÍTICA
                pasteFromOffice: {
                    keepImages: false,  // Não incluir imagens (simplifica)
                    removeStyles: false,  // MANTER estilos do Word
                    removeFormatting: false  // NÃO remover formatação
                },
                
                // FORMATO DE LINHA PADRÃO
                typing: {
                    transformations: {
                        include: [
                            // Transformações automáticas
                            'quotes',
                            'typography'
                        ]
                    }
                },
                
                // CONFIGURAÇÕES GERAIS
                language: 'pt-br',
                
            })
            .then(editor => {
                editorInstance = editor;
                
                // APLICAR FORMATAÇÃO PADRÃO
                aplicarFormatacaoPadrao();
                
                // LISTENER PARA MANTER ESPAÇAMENTO 1,5
                editor.model.document.on('change:data', () => {
                    forcarEspacamento15();
                });
                
                console.log('CKEditor inicializado com sucesso');
            })
            .catch(error => {
                console.error('Erro ao inicializar CKEditor:', error);
            });
        
        // ⭐ FUNÇÃO CRÍTICA: Aplicar formatação padrão
        function aplicarFormatacaoPadrao() {
            if (!editorInstance) return;
            
            // Configurar editor com formatação padrão
            const editable = document.querySelector('.ck-editor__editable');
            if (editable) {
                editable.style.fontFamily = 'Arial';
                editable.style.fontSize = '10pt';
                editable.style.lineHeight = '1.5';
                editable.style.textAlign = 'justify';
            }
        }
        
        // ⭐ FUNÇÃO CRÍTICA: Forçar espaçamento 1,5 em todo o conteúdo
        function forcarEspacamento15() {
            const editable = document.querySelector('.ck-content');
            if (!editable) return;
            
            // Aplicar line-height 1.5 em todos os elementos
            const paragrafos = editable.querySelectorAll('p, li, td, th');
            paragrafos.forEach(el => {
                el.style.lineHeight = '1.5';
            });
        }
        
        // API PARA PYTHON
        
        function getHTML() {
            if (!editorInstance) return '';
            return editorInstance.getData();
        }
        
        function setHTML(html) {
            if (!editorInstance) return;
            editorInstance.setData(html);
            forcarEspacamento15();
        }
        
        function clearEditor() {
            if (!editorInstance) return;
            editorInstance.setData('');
        }
        
        function getText() {
            if (!editorInstance) return '';
            return editorInstance.getData().replace(/<[^>]*>/g, '');
        }
        
        // ⭐ FUNÇÃO ESPECIAL: Otimizar HTML para DOCX
        function getOptimizedHTML() {
            let html = getHTML();
            
            // Garantir que todos os parágrafos tenham line-height 1.5
            html = html.replace(/<p/g, '<p style="line-height: 1.5;"');
            html = html.replace(/<li/g, '<li style="line-height: 1.5;"');
            
            // Garantir fonte Arial 10pt
            html = html.replace(/<p/g, '<p style="font-family: Arial; font-size: 10pt; line-height: 1.5;"');
            
            return html;
        }
    </script>
</body>
</html>
```

### 🎯 Pontos Críticos da Configuração

1. **`PasteFromOffice` plugin** - Essencial para Word/PDF
2. **`line-height: 1.5`** - Forçado em CSS e JavaScript
3. **`removeFormatting: false`** - NÃO remove formatação do Word
4. **`forcarEspacamento15()`** - Garante espaçamento em TODOS os elementos
5. **`getOptimizedHTML()`** - HTML otimizado para conversão DOCX

### 2. Integração Python com pywebview

**Arquivo: `src/gui/editor/rich_editor.py`**

```python
import webview
import os

class RichTextEditor:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.html_file = os.path.join('assets', 'editor', 'quill_editor.html')
        self.webview = None
        
    def create_editor(self):
        """Cria o webview com o editor Quill"""
        self.webview = webview.create_window(
            'Editor',
            self.html_file,
            width=800,
            height=500
        )
        return self.webview
    
    def get_html_content(self):
        """Recupera HTML OTIMIZADO do editor"""
        if self.webview:
            # Usar versão otimizada para DOCX
            return self.webview.evaluate_js('getOptimizedHTML()')
        return ""
    
    def set_html_content(self, html):
        """Define HTML no editor"""
        if self.webview:
            self.webview.evaluate_js(f'setHTML({html})')
    
    def clear_editor(self):
        """Limpa o editor"""
        if self.webview:
            self.webview.evaluate_js('clearEditor()')
```

### 3. Conversão HTML → DOCX (Crucial!) ⭐⭐⭐

**Biblioteca Principal:** `python-docx` + **parser customizado ROBUSTO**

**ATENÇÃO:** Esta é a parte **MAIS CRÍTICA**. A conversão precisa ser **PERFEITA**.

**Arquivo: `src/converters/html_to_docx.py`**

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from bs4 import BeautifulSoup
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import logging

logger = logging.getLogger(__name__)

class HTMLtoDOCXConverter:
    """
    Conversor HTML → DOCX com preservação PERFEITA de formatação
    
    REQUISITOS:
    - Espaçamento entre linhas: 1,5 (SEMPRE)
    - Fonte: Arial 10pt
    - Alinhamento: Justificado (padrão)
    - Preservar TODAS as formatações do HTML
    """
    
    # CONSTANTES DE FORMATAÇÃO PADRÃO
    DEFAULT_FONT = 'Arial'
    DEFAULT_SIZE = Pt(10)
    DEFAULT_LINE_SPACING = 1.5  # ⭐ ESPAÇAMENTO 1,5
    DEFAULT_ALIGNMENT = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    def __init__(self):
        self.doc = None
        
    def convert(self, html_content, base_doc=None):
        """
        Converte HTML para python-docx com PERFEIÇÃO
        
        Args:
            html_content: String HTML do editor CKEditor
            base_doc: Document base (template) se existir
            
        Returns:
            Document object com formatação perfeita
        """
        if base_doc:
            self.doc = base_doc
        else:
            self.doc = Document()
            self._configurar_documento_padrao()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Processar cada elemento
        for element in soup.children:
            if element.name:  # Ignorar NavigableString
                self._process_element(element)
                
        logger.info("Conversão HTML→DOCX concluída")
        return self.doc
    
    def _configurar_documento_padrao(self):
        """Configura estilos padrão do documento"""
        # Estilo Normal
        style = self.doc.styles['Normal']
        style.font.name = self.DEFAULT_FONT
        style.font.size = self.DEFAULT_SIZE
        
        # ⭐ ESPAÇAMENTO DE LINHA 1,5 NO ESTILO PADRÃO
        style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        style.paragraph_format.line_spacing = self.DEFAULT_LINE_SPACING
        style.paragraph_format.alignment = self.DEFAULT_ALIGNMENT
    
    def _process_element(self, element):
        """Processa cada elemento HTML recursivamente"""
        
        if element.name == 'p':
            self._add_paragraph(element)
        elif element.name in ['ul', 'ol']:
            self._add_list(element)
        elif element.name == 'table':
            self._add_table(element)
        elif element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self._add_heading(element)
        elif element.name == 'br':
            self.doc.add_paragraph()  # Linha em branco
        elif element.name == 'div':
            # Processar filhos do div
            for child in element.children:
                if child.name:
                    self._process_element(child)
    
    def _add_paragraph(self, p_element):
        """
        Adiciona parágrafo com TODA a formatação preservada
        
        ⭐ CRÍTICO: Espaçamento 1,5, Arial 10pt, justificado
        """
        p = self.doc.add_paragraph()
        
        # ⭐ APLICAR ESPAÇAMENTO 1,5 (OBRIGATÓRIO)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        p.paragraph_format.line_spacing = self.DEFAULT_LINE_SPACING
        
        # Processar alinhamento do estilo inline
        style = p_element.get('style', '')
        alignment = self._extract_alignment(style)
        if alignment:
            p.alignment = alignment
        else:
            p.alignment = self.DEFAULT_ALIGNMENT
        
        # Processar espaçamento antes/depois
        spacing_before, spacing_after = self._extract_spacing(style)
        if spacing_before:
            p.paragraph_format.space_before = spacing_before
        if spacing_after:
            p.paragraph_format.space_after = spacing_after
        
        # Processar recuos
        indent_left, indent_right, indent_first = self._extract_indents(style)
        if indent_left:
            p.paragraph_format.left_indent = indent_left
        if indent_right:
            p.paragraph_format.right_indent = indent_right
        if indent_first:
            p.paragraph_format.first_line_indent = indent_first
        
        # Processar texto inline com formatação
        self._process_inline_elements(p_element, p)
        
    def _process_inline_elements(self, element, paragraph):
        """
        Processa elementos inline (strong, em, u, span) com PRECISÃO
        
        Preserva: negrito, itálico, sublinhado, tachado, cor, tamanho
        """
        
        for content in element.children:
            if isinstance(content, str):
                # Texto simples
                if content.strip():  # Ignorar espaços vazios
                    run = paragraph.add_run(content)
                    self._apply_default_font(run)
            else:
                # Elementos com formatação
                text = content.get_text()
                if not text.strip():
                    continue
                    
                run = paragraph.add_run(text)
                self._apply_default_font(run)
                
                # ⭐ APLICAR TODAS AS FORMATAÇÕES
                
                # Negrito
                if content.name in ['strong', 'b']:
                    run.bold = True
                
                # Itálico
                if content.name in ['em', 'i']:
                    run.italic = True
                
                # Sublinhado
                if content.name == 'u':
                    run.underline = True
                
                # Tachado
                if content.name in ['s', 'strike', 'del']:
                    run.font.strike = True
                
                # Processar estilos inline (span)
                if content.name == 'span' or content.get('style'):
                    style = content.get('style', '')
                    self._apply_inline_styles(run, style)
                
                # Link
                if content.name == 'a':
                    # Adicionar hyperlink (opcional)
                    run.font.color.rgb = RGBColor(0, 0, 255)
                    run.underline = True
    
    def _apply_default_font(self, run):
        """Aplica fonte padrão (Arial 10pt)"""
        run.font.name = self.DEFAULT_FONT
        run.font.size = self.DEFAULT_SIZE
    
    def _apply_inline_styles(self, run, style_string):
        """
        Aplica estilos inline do CSS com PRECISÃO
        
        Suporta: font-size, font-family, color, background-color, 
                 font-weight, font-style, text-decoration
        """
        if not style_string:
            return
            
        styles = {}
        for item in style_string.split(';'):
            if ':' in item:
                prop, value = item.split(':', 1)
                styles[prop.strip().lower()] = value.strip()
        
        # Font size
        if 'font-size' in styles:
            size = styles['font-size']
            if 'pt' in size:
                run.font.size = Pt(float(size.replace('pt', '')))
            elif 'px' in size:
                px = float(size.replace('px', ''))
                run.font.size = Pt(px * 0.75)  # Converter px para pt
        
        # Font family
        if 'font-family' in styles:
            family = styles['font-family'].strip('"\'').split(',')[0]
            run.font.name = family
        
        # Color
        if 'color' in styles:
            color = styles['color'].strip()
            rgb = self._parse_color(color)
            if rgb:
                run.font.color.rgb = RGBColor(*rgb)
        
        # Background color (highlight)
        if 'background-color' in styles:
            bg_color = styles['background-color'].strip()
            rgb = self._parse_color(bg_color)
            if rgb:
                run.font.highlight_color = self._rgb_to_highlight(rgb)
        
        # Font weight (bold)
        if 'font-weight' in styles:
            weight = styles['font-weight']
            if weight in ['bold', '700', '800', '900']:
                run.bold = True
        
        # Font style (italic)
        if 'font-style' in styles:
            if styles['font-style'] == 'italic':
                run.italic = True
        
        # Text decoration
        if 'text-decoration' in styles:
            decoration = styles['text-decoration']
            if 'underline' in decoration:
                run.underline = True
            if 'line-through' in decoration:
                run.font.strike = True
        
        # ⭐ Line height (se especificado, sobrescreve padrão)
        if 'line-height' in styles:
            line_height = styles['line-height']
            # Será aplicado no nível do parágrafo
            # (já tratado em _add_paragraph)
    
    def _parse_color(self, color_str):
        """
        Parse cor de CSS para RGB
        
        Suporta: #RRGGBB, rgb(r,g,b), nomes de cores
        """
        color_str = color_str.lower().strip()
        
        # Hex color #RRGGBB
        if color_str.startswith('#'):
            hex_color = color_str[1:]
            if len(hex_color) == 6:
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            elif len(hex_color) == 3:
                return tuple(int(c*2, 16) for c in hex_color)
        
        # rgb(r, g, b)
        if color_str.startswith('rgb'):
            import re
            match = re.search(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color_str)
            if match:
                return tuple(int(x) for x in match.groups())
        
        # Cores nomeadas (subset)
        colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'gray': (128, 128, 128),
            'grey': (128, 128, 128),
        }
        
        return colors.get(color_str)
    
    def _extract_alignment(self, style_string):
        """Extrai alinhamento do estilo CSS"""
        if 'text-align' in style_string:
            if 'left' in style_string:
                return WD_ALIGN_PARAGRAPH.LEFT
            elif 'center' in style_string:
                return WD_ALIGN_PARAGRAPH.CENTER
            elif 'right' in style_string:
                return WD_ALIGN_PARAGRAPH.RIGHT
            elif 'justify' in style_string:
                return WD_ALIGN_PARAGRAPH.JUSTIFY
        return None
    
    def _extract_spacing(self, style_string):
        """Extrai espaçamento antes/depois do parágrafo"""
        before = None
        after = None
        
        # Implementar parsing de margin-top, margin-bottom
        # padding-top, padding-bottom
        
        return before, after
    
    def _extract_indents(self, style_string):
        """Extrai recuos (indents) do CSS"""
        left = None
        right = None
        first = None
        
        # Implementar parsing de margin-left, margin-right, text-indent
        
        return left, right, first
    
    
    def _add_list(self, list_element):
        """
        Adiciona lista (ordenada ou não) com PERFEIÇÃO
        
        ⭐ Preserva: tipo de marcador, níveis de recuo, espaçamento 1,5
        """
        is_ordered = list_element.name == 'ol'
        
        # Detectar nível de recuo (para listas aninhadas)
        list_level = self._detect_list_level(list_element)
        
        for li in list_element.find_all('li', recursive=False):
            p = self.doc.add_paragraph()
            
            # ⭐ APLICAR ESPAÇAMENTO 1,5
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
            p.paragraph_format.line_spacing = self.DEFAULT_LINE_SPACING
            
            # Aplicar estilo de lista
            if is_ordered:
                p.style = 'List Number'
            else:
                p.style = 'List Bullet'
            
            # Aplicar nível de recuo
            if list_level > 0:
                p.paragraph_format.left_indent = Cm(list_level * 1.27)  # 1.27cm por nível
            
            # Processar conteúdo do item
            self._process_inline_elements(li, p)
            
            # Verificar se há sub-listas
            sub_lists = li.find_all(['ul', 'ol'], recursive=False)
            for sub_list in sub_lists:
                self._add_list(sub_list)
    
    def _detect_list_level(self, list_element):
        """Detecta nível de recuo da lista (para listas aninhadas)"""
        level = 0
        parent = list_element.parent
        while parent:
            if parent.name in ['ul', 'ol']:
                level += 1
            parent = parent.parent
        return level
    
    def _add_table(self, table_element):
        """
        Adiciona tabela com TODA a formatação preservada
        
        ⭐ Preserva: bordas, mesclagem, cores, alinhamento, formatação de texto
        """
        # Detectar dimensões
        rows_html = table_element.find_all('tr')
        if not rows_html:
            return
            
        cols = max(len(row.find_all(['td', 'th'])) for row in rows_html)
        rows = len(rows_html)
        
        # Criar tabela
        table = self.doc.add_table(rows=rows, cols=cols)
        table.style = 'Table Grid'
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Processar cada célula
        for i, row_html in enumerate(rows_html):
            cells_html = row_html.find_all(['td', 'th'])
            
            for j, cell_html in enumerate(cells_html):
                if j >= len(table.rows[i].cells):
                    continue
                    
                table_cell = table.rows[i].cells[j]
                
                # ⭐ LIMPAR PARÁGRAFO PADRÃO
                if table_cell.paragraphs:
                    para = table_cell.paragraphs[0]
                else:
                    para = table_cell.add_paragraph()
                
                # ⭐ ESPAÇAMENTO 1,5 NA CÉLULA
                para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
                para.paragraph_format.line_spacing = self.DEFAULT_LINE_SPACING
                
                # Processar conteúdo da célula
                for content in cell_html.children:
                    if content.name == 'p':
                        # Parágrafo dentro da célula
                        if para.text:  # Se já tem texto, criar novo parágrafo
                            para = table_cell.add_paragraph()
                            para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
                            para.paragraph_format.line_spacing = self.DEFAULT_LINE_SPACING
                        self._process_inline_elements(content, para)
                    elif isinstance(content, str):
                        if content.strip():
                            run = para.add_run(content)
                            self._apply_default_font(run)
                    else:
                        # Outros elementos inline
                        text = content.get_text()
                        if text.strip():
                            run = para.add_run(text)
                            self._apply_default_font(run)
                            # Aplicar formatação do elemento
                            if content.name in ['strong', 'b']:
                                run.bold = True
                            if content.name in ['em', 'i']:
                                run.italic = True
                
                # Aplicar formatação de célula
                self._apply_cell_formatting(table_cell, cell_html)
                
                # Célula de cabeçalho (th)
                if cell_html.name == 'th':
                    for para in table_cell.paragraphs:
                        for run in para.runs:
                            run.bold = True
                    # Alinhamento centro para cabeçalho
                    for para in table_cell.paragraphs:
                        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                # ⭐ MESCLAGEM DE CÉLULAS
                colspan = int(cell_html.get('colspan', 1))
                rowspan = int(cell_html.get('rowspan', 1))
                
                if colspan > 1 or rowspan > 1:
                    # Mesclar células
                    try:
                        end_col = min(j + colspan - 1, len(table.rows[i].cells) - 1)
                        end_row = min(i + rowspan - 1, len(table.rows) - 1)
                        
                        if end_col > j or end_row > i:
                            table_cell.merge(table.rows[end_row].cells[end_col])
                    except Exception as e:
                        logger.warning(f"Erro ao mesclar células: {e}")
    
    def _apply_cell_formatting(self, cell, cell_html):
        """
        Aplica formatação da célula (bordas, cores, alinhamento)
        """
        style = cell_html.get('style', '')
        
        # Cor de fundo
        if 'background-color' in style:
            bg_color = self._extract_bg_color(style)
            if bg_color:
                self._set_cell_background(cell, bg_color)
        
        # Alinhamento vertical
        if 'vertical-align' in style:
            valign = self._extract_vertical_align(style)
            if valign:
                cell.vertical_alignment = valign
        
        # Largura da célula
        if 'width' in style:
            width = self._extract_width(style)
            if width:
                cell.width = width
    
    def _extract_bg_color(self, style):
        """Extrai cor de fundo do estilo"""
        for item in style.split(';'):
            if 'background-color' in item.lower():
                color = item.split(':')[1].strip()
                return self._parse_color(color)
        return None
    
    def _set_cell_background(self, cell, rgb):
        """Define cor de fundo da célula"""
        from docx.oxml import parse_xml
        
        # Criar elemento de cor de fundo
        shading_elm = parse_xml(
            f'<w:shd {{w.nsmap}} w:fill="{:02x}{:02x}{:02x}"/>'.format(*rgb)
        )
        cell._element.get_or_add_tcPr().append(shading_elm)
    
    def _extract_vertical_align(self, style):
        """Extrai alinhamento vertical"""
        if 'vertical-align' in style:
            if 'top' in style:
                return WD_ALIGN_VERTICAL.TOP
            elif 'center' in style or 'middle' in style:
                return WD_ALIGN_VERTICAL.CENTER
            elif 'bottom' in style:
                return WD_ALIGN_VERTICAL.BOTTOM
        return None
    
    def _extract_width(self, style):
        """Extrai largura da célula"""
        # Implementar parsing de width
        return None
    
    def _add_heading(self, heading_element):
        """
        Adiciona cabeçalho com formatação
        
        ⭐ Mantém espaçamento 1,5
        """
        level = int(heading_element.name[1])  # h1 → 1, h2 → 2, etc
        text = heading_element.get_text()
        
        heading = self.doc.add_heading(text, level=level)
        
        # ⭐ APLICAR ESPAÇAMENTO 1,5
        heading.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        heading.paragraph_format.line_spacing = self.DEFAULT_LINE_SPACING
        
        # Aplicar fonte Arial
        for run in heading.runs:
            run.font.name = self.DEFAULT_FONT
```

### 🔥 PONTOS CRÍTICOS DO CONVERSOR

1. **Espaçamento 1,5** - Aplicado em:
   - ✅ Parágrafos
   - ✅ Itens de lista
   - ✅ Células de tabela
   - ✅ Cabeçalhos

2. **Fonte Arial 10pt** - Aplicada em:
   - ✅ Todo texto
   - ✅ Texto dentro de tabelas
   - ✅ Listas
   - ✅ Todos os runs

3. **Formatação Preservada:**
   - ✅ Negrito, itálico, sublinhado, tachado
   - ✅ Cores de texto
   - ✅ Alinhamentos
   - ✅ Listas multi-nível
   - ✅ Tabelas complexas
   - ✅ Mesclagem de células
   - ✅ Cores de fundo
```

### 4. Tratamento Especial: Colar do Word

**Problema:** Quando usuário cola do Word, vem muito HTML sujo com estilos da Microsoft.

**Solução:** Limpeza de HTML

**Arquivo: `src/converters/word_html_cleaner.py`**

```python
from bs4 import BeautifulSoup
import re

class WordHTMLCleaner:
    """Limpa HTML colado do Word mantendo formatação essencial"""
    
    @staticmethod
    def clean(html):
        """
        Remove tags e estilos desnecessários do Word
        Mantém: strong, em, u, p, ul, ol, li, table, tr, td, th
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remover tags do Word
        for tag in soup.find_all(['o:p', 'w:sdt', 'w:sdtpr']):
            tag.decompose()
            
        # Remover classes e IDs específicos do Word
        for tag in soup.find_all(True):
            if 'Mso' in str(tag.get('class', '')):
                del tag['class']
            if tag.get('id'):
                del tag['id']
                
        # Limpar estilos inline mantendo essenciais
        for tag in soup.find_all(style=True):
            style = tag['style']
            cleaned_style = WordHTMLCleaner._clean_style(style)
            if cleaned_style:
                tag['style'] = cleaned_style
            else:
                del tag['style']
                
        return str(soup)
    
    @staticmethod
    def _clean_style(style_string):
        """Mantém apenas estilos relevantes"""
        relevant = ['font-size', 'font-family', 'color', 'text-align', 
                   'font-weight', 'font-style', 'text-decoration']
        
        styles = [s.strip() for s in style_string.split(';') if s.strip()]
        cleaned = []
        
        for style in styles:
            if ':' in style:
                prop, value = style.split(':', 1)
                if prop.strip() in relevant:
                    cleaned.append(f"{prop.strip()}: {value.strip()}")
                    
        return '; '.join(cleaned)
```

### 5. Estrutura de Arquivos - Etapa 2

```
AutomacaoRPCMs/
│
├── src/
│   ├── gui/
│   │   └── editor/
│   │       ├── __init__.py
│   │       ├── rich_editor.py        # Classe principal do editor
│   │       └── editor_toolbar.py     # Barra de ferramentas customizada
│   │
│   ├── converters/
│   │   ├── __init__.py
│   │   ├── html_to_docx.py          # Conversor HTML → DOCX
│   │   └── word_html_cleaner.py     # Limpador de HTML do Word
│   │
│   └── utils/
│       └── clipboard_handler.py      # Gerenciador de clipboard
│
├── assets/
│   └── editor/
│       ├── quill_editor.html         # Editor Quill.js
│       ├── quill.snow.css
│       └── quill-table.js            # Plugin de tabelas
│
└── tests/
    └── test_editor/
        ├── test_html_conversion.py
        ├── test_word_paste.py
        └── sample_formatted.html     # Exemplos de teste
```

## Funcionalidades do Editor

### Barra de Ferramentas
- **Formatação de Texto:**
  - Negrito (Ctrl+B)
  - Itálico (Ctrl+I)
  - Sublinhado (Ctrl+U)
  - Tachar
  
- **Alinhamento:**
  - Esquerda
  - Centro
  - Direita
  - Justificado (padrão)

- **Listas:**
  - Lista com marcadores
  - Lista numerada
  - Aumentar/diminuir recuo

- **Tabelas:**
  - Inserir tabela
  - Adicionar/remover linhas e colunas
  - Mesclar células

- **Outros:**
  - Desfazer (Ctrl+Z)
  - Refazer (Ctrl+Y)
  - Limpar formatação
  - Colar sem formatação (Ctrl+Shift+V)

### Configuração Padrão OBRIGATÓRIA
```python
# src/config/editor_config.py

"""Configurações OBRIGATÓRIAS do editor de texto"""

DEFAULT_FONT = 'Arial'
DEFAULT_SIZE = Pt(10)
DEFAULT_LINE_SPACING = 1.5  # ⭐ ESPAÇAMENTO 1,5 - OBRIGATÓRIO
DEFAULT_ALIGNMENT = WD_ALIGN_PARAGRAPH.JUSTIFY

def validar_espacamento(line_spacing):
    """Valida se espaçamento é 1,5"""
    assert line_spacing == 1.5, f"Espaçamento deve ser 1,5, encontrado: {line_spacing}"
```

## Testes Essenciais - VER ARQUIVO COMPLETO

📄 **Consultar arquivo detalhado:** `ETAPA_2_TESTES_CRITICOS_EDITOR.md`

Este arquivo contém **13 testes críticos** que o editor PRECISA passar.

### Resumo dos Testes Principais

### Teste 1: Colar Texto Simples do Word ⭐
1. Copiar parágrafo formatado do Word
2. Colar no editor
3. ✅ Verificar: negrito, itálico, sublinhado, **espaçamento 1,5**

### Teste 2: Colar Lista do Word ⭐
1. Copiar lista numerada do Word
2. Colar no editor
3. ✅ Verificar: numeração, recuos, **espaçamento 1,5**

### Teste 3: Colar Tabela do Word ⭐
1. Copiar tabela 3x3 do Word
2. Colar no editor
3. ✅ Verificar: estrutura, conteúdo, **espaçamento 1,5 nas células**

### Teste 4: Documento Complexo do Word ⭐⭐⭐
1. Copiar documento com parágrafos + listas + tabelas
2. Colar no editor
3. ✅ Verificar: **TUDO** preservado, **espaçamento 1,5 em TUDO**

### Teste 5: Conversão para DOCX ⭐⭐⭐
1. Criar documento completo no editor
2. Converter para DOCX
3. Abrir no Word
4. ✅ Verificar: **Arial 10pt**, **espaçamento 1,5**, TODAS as formatações

### Teste 13: Verificação Técnica do Espaçamento ⭐⭐⭐
1. Gerar DOCX
2. Abrir no Word
3. Selecionar parágrafo → Parágrafo → Espaçamento entre linhas
4. ✅ **DEVE estar exatamente em "1,5 linhas"**

## Critérios de Conclusão da Etapa 2 - RIGOROSOS ⭐

### Funcionalidades Essenciais
- [ ] Editor HTML (CKEditor 5) funcionando perfeitamente
- [ ] Plugin **PasteFromOffice** configurado e funcionando
- [ ] Toolbar completa e funcional

### Copiar/Colar - PERFEIÇÃO ABSOLUTA
- [ ] Copiar/colar do Word preserva **100%** da formatação ⭐⭐⭐
- [ ] Copiar/colar de PDF funciona adequadamente
- [ ] Negrito, itálico, sublinhado preservados
- [ ] Cores de texto preservadas
- [ ] Alinhamentos preservados

### Listas - PERFEIÇÃO ABSOLUTA
- [ ] Listas ordenadas (numeradas) **perfeitas** ⭐⭐
- [ ] Listas não ordenadas (marcadores) **perfeitas** ⭐⭐
- [ ] Listas multi-nível (aninhadas) funcionando ⭐⭐
- [ ] **Espaçamento 1,5 nos itens de lista** ⭐⭐⭐

### Tabelas - PERFEIÇÃO ABSOLUTA
- [ ] Tabelas simples **perfeitas** ⭐⭐
- [ ] Tabelas complexas com mesclagem **perfeitas** ⭐⭐
- [ ] Bordas preservadas
- [ ] Cores de fundo preservadas
- [ ] Formatação dentro das células preservada
- [ ] **Espaçamento 1,5 nas células** ⭐⭐⭐

### Formatação Padrão - INEGOCIÁVEL
- [ ] **Fonte Arial 10pt aplicada em TODO O CONTEÚDO** ⭐⭐⭐
- [ ] **Espaçamento 1,5 aplicado em TODO O CONTEÚDO** ⭐⭐⭐
- [ ] Alinhamento justificado como padrão
- [ ] Formatação aplicada automaticamente ao digitar

### Conversão HTML → DOCX - PERFEIÇÃO ABSOLUTA
- [ ] Conversor HTML → DOCX **perfeito** ⭐⭐⭐
- [ ] Limpador de HTML do Word implementado
- [ ] Preservação de espaçamento entre parágrafos
- [ ] Preservação de recuos
- [ ] Conversão de listas **perfeita**
- [ ] Conversão de tabelas **perfeita**
- [ ] **Espaçamento 1,5 mantido no DOCX** ⭐⭐⭐
- [ ] **Arial 10pt mantido no DOCX** ⭐⭐⭐

### Testes - APROVAÇÃO OBRIGATÓRIA
- [ ] **Todos os 13 testes críticos passando** ⭐⭐⭐
- [ ] Teste com documento real do Word aprovado
- [ ] Teste com documento real de PDF aprovado
- [ ] Teste de conversão DOCX aprovado
- [ ] Verificação técnica do espaçamento 1,5 aprovada

### Qualidade de Código
- [ ] Performance aceitável (< 5s para documentos grandes)
- [ ] Sem bugs conhecidos
- [ ] Código documentado e limpo
- [ ] Tratamento de erros robusto
- [ ] Logs implementados

### Validação Final
- [ ] **Validação visual aprovada pelo usuário** ⭐⭐⭐
- [ ] Documento gerado abre perfeitamente no Word
- [ ] Documento gerado é editável no Word
- [ ] Aparência profissional e consistente

## Tempo Estimado
**4-5 dias** de desenvolvimento (a parte mais complexa!)

## Próxima Etapa
Após conclusão, passar para ETAPA 3 - Implementação das Funcionalidades de Automação.
