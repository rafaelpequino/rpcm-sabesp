# TESTES CRÍTICOS DO EDITOR - ZERO TOLERÂNCIA A ERROS

## Objetivo
Este documento descreve os testes **OBRIGATÓRIOS** que o editor precisa passar para ser considerado perfeito.

---

## 🎯 TESTE 1: Copiar/Colar Texto Simples do Word

### Preparação
1. Criar documento Word com:
   - 3 parágrafos de texto
   - Alguns com **negrito**, outros com *itálico*
   - Um com <u>sublinhado</u>
   - Mix de formatações (negrito + itálico, etc.)

### Procedimento
1. Selecionar todo o texto no Word
2. Copiar (Ctrl+C)
3. Colar no editor (Ctrl+V)

### Critérios de Aprovação ✅
- [ ] Todo o texto foi colado
- [ ] Negrito preservado em todos os lugares corretos
- [ ] Itálico preservado
- [ ] Sublinhado preservado
- [ ] Mix de formatações preservado
- [ ] **Espaçamento entre linhas é 1,5**
- [ ] Fonte convertida para Arial 10pt
- [ ] Alinhamento justificado mantido

---

## 🎯 TESTE 2: Copiar/Colar Lista do Word

### Preparação - Lista Simples
```
1. Primeiro item
2. Segundo item
3. Terceiro item
```

### Preparação - Lista Aninhada
```
1. Item principal 1
   a. Sub-item 1a
   b. Sub-item 1b
2. Item principal 2
   • Marcador nível 2
   • Outro marcador
```

### Procedimento
1. Copiar lista do Word
2. Colar no editor

### Critérios de Aprovação ✅
- [ ] Lista numerada mantém numeração
- [ ] Lista com marcadores mantém marcadores
- [ ] Níveis de recuo preservados
- [ ] Sub-listas funcionam corretamente
- [ ] **Espaçamento 1,5 em cada item**
- [ ] Formatação dentro dos itens preservada

---

## 🎯 TESTE 3: Copiar/Colar Tabela do Word

### Preparação - Tabela Simples 3x3
```
┌─────────────┬─────────────┬─────────────┐
│ Cabeçalho 1 │ Cabeçalho 2 │ Cabeçalho 3 │
├─────────────┼─────────────┼─────────────┤
│ Célula 1,1  │ Célula 1,2  │ Célula 1,3  │
│ Célula 2,1  │ Célula 2,2  │ Célula 2,3  │
└─────────────┴─────────────┴─────────────┘
```

### Preparação - Tabela Complexa
- Mesclagem de células
- Células com fundo colorido
- Bordas diferentes
- Texto com formatação dentro das células

### Procedimento
1. Copiar tabela do Word
2. Colar no editor

### Critérios de Aprovação ✅
- [ ] Estrutura da tabela preservada (linhas x colunas)
- [ ] Bordas visíveis
- [ ] Conteúdo de todas as células preservado
- [ ] Formatação dentro das células preservada
- [ ] Mesclagem de células funciona (se aplicável)
- [ ] Cores de fundo preservadas (se aplicável)
- [ ] **Espaçamento 1,5 dentro das células**
- [ ] Alinhamento de texto nas células preservado

---

## 🎯 TESTE 4: Copiar/Colar Documento Complexo do Word

### Preparação - Documento "Real"
Criar documento Word com:
1. Título (fonte maior)
2. Parágrafo introdutório (justificado)
3. Lista numerada com 5 itens
4. Parágrafo de transição
5. Tabela 4x3 com cabeçalho
6. Lista com marcadores (3 itens)
7. Parágrafo final

### Procedimento
1. Copiar TODO o documento
2. Colar no editor

### Critérios de Aprovação ✅
- [ ] TODOS os elementos preservados na ordem correta
- [ ] Título destacado (pode ser fonte maior ou negrito)
- [ ] Parágrafos com formatação correta
- [ ] Listas funcionando
- [ ] Tabela perfeita
- [ ] **Espaçamento 1,5 em TUDO**
- [ ] Visual idêntico ao documento original

---

## 🎯 TESTE 5: Copiar/Colar de PDF

### Preparação
1. Criar PDF a partir de um documento Word formatado
2. PDF deve conter:
   - Texto com formatações
   - Lista
   - Tabela (se possível)

### Procedimento
1. Abrir PDF
2. Selecionar e copiar conteúdo
3. Colar no editor

### Critérios de Aprovação ✅
- [ ] Texto colado corretamente
- [ ] Formatação preservada (pode ter limitações do PDF)
- [ ] Estrutura geral mantida
- [ ] **Espaçamento 1,5 aplicado**
- [ ] Sem caracteres estranhos ou quebras indesejadas

---

## 🎯 TESTE 6: Edição Manual no Editor

### Procedimento
1. Digitar texto novo no editor
2. Aplicar formatações usando toolbar:
   - Negrito
   - Itálico
   - Sublinhado
3. Criar lista numerada
4. Criar lista com marcadores
5. Inserir tabela 2x2
6. Mudar alinhamento (centro, direita, justificado)

### Critérios de Aprovação ✅
- [ ] Todos os botões da toolbar funcionam
- [ ] Formatações são aplicadas corretamente
- [ ] Listas são criadas corretamente
- [ ] Tabela inserida corretamente
- [ ] Alinhamentos funcionam
- [ ] **Espaçamento 1,5 aplicado automaticamente**
- [ ] Undo/Redo funcionam

---

## 🎯 TESTE 7: Conversão para DOCX - Texto e Formatações

### Preparação
1. Criar conteúdo no editor:
   - Texto com negrito, itálico, sublinhado
   - Diferentes alinhamentos
   - Cores de texto diferentes

### Procedimento
1. Preencher campos do formulário
2. Gerar documento DOCX
3. Abrir no Microsoft Word

### Critérios de Aprovação ✅
- [ ] Documento abre sem erros
- [ ] Fonte é Arial 10pt em TODO o documento
- [ ] **Espaçamento entre linhas é 1,5 SEMPRE**
- [ ] Negrito, itálico, sublinhado preservados
- [ ] Alinhamentos corretos
- [ ] Cores preservadas
- [ ] Visual idêntico ao editor

---

## 🎯 TESTE 8: Conversão para DOCX - Listas

### Preparação
1. Criar no editor:
   - Lista numerada (5 itens)
   - Lista com marcadores (4 itens)
   - Lista aninhada (2 níveis)

### Procedimento
1. Gerar documento DOCX
2. Abrir no Microsoft Word

### Critérios de Aprovação ✅
- [ ] Listas numeradas funcionam no Word
- [ ] Numeração está correta (1, 2, 3...)
- [ ] Marcadores aparecem corretamente
- [ ] Níveis de recuo preservados
- [ ] **Espaçamento 1,5 nos itens**
- [ ] Formatação dentro dos itens preservada

---

## 🎯 TESTE 9: Conversão para DOCX - Tabelas

### Preparação
1. Criar no editor:
   - Tabela 3x3
   - Preencher todas as células
   - Aplicar negrito no cabeçalho
   - Adicionar texto formatado em algumas células

### Procedimento
1. Gerar documento DOCX
2. Abrir no Microsoft Word

### Critérios de Aprovação ✅
- [ ] Tabela aparece corretamente
- [ ] Estrutura preservada (3x3)
- [ ] Bordas visíveis
- [ ] Conteúdo de todas as células presente
- [ ] Formatação nas células preservada
- [ ] **Espaçamento 1,5 nas células**
- [ ] Tabela editável no Word

---

## 🎯 TESTE 10: Conversão para DOCX - Documento Completo

### Preparação
1. Criar documento completo no editor:
   ```
   TÍTULO EM NEGRITO
   
   Parágrafo introdutório com texto justificado e alguma formatação.
   
   1. Item de lista um
   2. Item de lista dois com negrito
   3. Item de lista três
   
   Parágrafo de transição.
   
   ┌─────────┬─────────┬─────────┐
   │ Col 1   │ Col 2   │ Col 3   │
   ├─────────┼─────────┼─────────┤
   │ Dado 1  │ Dado 2  │ Dado 3  │
   └─────────┴─────────┴─────────┘
   
   • Marcador um
   • Marcador dois
   
   Parágrafo final.
   ```

### Procedimento
1. Gerar documento DOCX
2. Abrir no Microsoft Word
3. Verificar TUDO

### Critérios de Aprovação ✅
- [ ] Documento abre perfeitamente
- [ ] **TODO o documento em Arial 10pt**
- [ ] **TODO o documento com espaçamento 1,5**
- [ ] Todos os elementos preservados na ordem
- [ ] Todas as formatações corretas
- [ ] Listas funcionando
- [ ] Tabela perfeita
- [ ] Documento profissional e apresentável

---

## 🎯 TESTE 11: Stress Test - Documento Muito Grande

### Preparação
1. Criar documento Word com:
   - 10 páginas de conteúdo
   - 20+ parágrafos
   - 5+ listas
   - 3+ tabelas
   - Mix de formatações

### Procedimento
1. Copiar TODO o documento
2. Colar no editor
3. Gerar DOCX

### Critérios de Aprovação ✅
- [ ] Editor não trava
- [ ] Todo o conteúdo colado
- [ ] Scroll funciona
- [ ] Geração não demora mais de 10 segundos
- [ ] DOCX gerado está perfeito
- [ ] Sem perda de dados
- [ ] Sem corrupção de formatação

---

## 🎯 TESTE 12: Compatibilidade - Diferentes Versões do Word

### Procedimento
1. Criar documentos em:
   - Word 2010
   - Word 2016
   - Word 2019
   - Microsoft 365
2. Copiar e colar de cada versão no editor
3. Gerar DOCX
4. Abrir em cada versão

### Critérios de Aprovação ✅
- [ ] Funciona com Word 2010
- [ ] Funciona com Word 2016
- [ ] Funciona com Word 2019
- [ ] Funciona com Microsoft 365
- [ ] DOCX gerado abre em todas as versões
- [ ] Formatação preservada em todas as versões

---

## 🎯 TESTE 13: Espaçamento 1,5 - Verificação Técnica

### Procedimento
1. Criar parágrafo no editor
2. Gerar DOCX
3. Abrir no Word
4. Selecionar parágrafo
5. Abrir "Parágrafo" → "Espaçamento entre linhas"

### Critérios de Aprovação ✅
- [ ] Espaçamento está definido como "1,5 linhas"
- [ ] Aplicado em TODOS os parágrafos
- [ ] Aplicado em TODOS os itens de lista
- [ ] Aplicado em TODAS as células de tabela
- [ ] Consistente em TODO o documento

---

## 📊 RESUMO DOS TESTES

### Obrigatórios (Não Pode Falhar)
- ✅ Teste 1: Texto simples do Word
- ✅ Teste 2: Listas do Word
- ✅ Teste 3: Tabelas do Word
- ✅ Teste 4: Documento complexo do Word
- ✅ Teste 7: Conversão texto para DOCX
- ✅ Teste 8: Conversão listas para DOCX
- ✅ Teste 9: Conversão tabelas para DOCX
- ✅ Teste 10: Conversão documento completo para DOCX
- ✅ Teste 13: Verificação técnica espaçamento 1,5

### Importantes (Pode ter limitações menores)
- ⚠️ Teste 5: Copiar de PDF (PDF tem limitações naturais)
- ⚠️ Teste 11: Stress test (performance)
- ⚠️ Teste 12: Compatibilidade versões

### Essenciais
- ✅ Teste 6: Edição manual (funcionalidade básica)

---

## 🔥 CRITÉRIO FINAL DE APROVAÇÃO

Para o editor ser considerado **PERFEITO**, precisa passar:

1. **100%** dos testes obrigatórios ✅
2. **90%+** dos testes importantes ⚠️
3. **100%** dos testes essenciais ✅

### Requisitos Inegociáveis
1. ✅ **Espaçamento 1,5 em TUDO** - SEM EXCEÇÕES
2. ✅ **Arial 10pt em TUDO** - SEM EXCEÇÕES
3. ✅ **Copiar/colar do Word preserva formatação** - 100%
4. ✅ **Listas funcionam perfeitamente**
5. ✅ **Tabelas funcionam perfeitamente**
6. ✅ **Conversão DOCX é perfeita**

---

## 🛠️ Ferramentas de Teste

### Script de Teste Automatizado (Futuro)
```python
# tests/editor/test_perfeicao.py

import pytest
from docx import Document

def test_espacamento_15_em_tudo():
    """Testa se TUDO tem espaçamento 1,5"""
    doc = gerar_documento_teste()
    
    # Verificar todos os parágrafos
    for para in doc.paragraphs:
        assert para.paragraph_format.line_spacing == 1.5, \
            f"Parágrafo '{para.text[:30]}...' não tem espaçamento 1,5"
    
    # Verificar tabelas
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    assert para.paragraph_format.line_spacing == 1.5, \
                        f"Célula não tem espaçamento 1,5"
    
    print("✅ TODOS os elementos têm espaçamento 1,5")

def test_fonte_arial_10pt_em_tudo():
    """Testa se TUDO está em Arial 10pt"""
    doc = gerar_documento_teste()
    
    for para in doc.paragraphs:
        for run in para.runs:
            assert run.font.name == 'Arial', f"Fonte não é Arial: {run.font.name}"
            assert run.font.size == Pt(10), f"Tamanho não é 10pt: {run.font.size}"
    
    print("✅ TUDO está em Arial 10pt")
```

---

## 📝 Checklist de Validação Final

Antes de considerar o editor pronto:

- [ ] Todos os testes obrigatórios passando
- [ ] Documentação completa
- [ ] Código comentado e limpo
- [ ] Performance aceitável (< 5s para documentos grandes)
- [ ] Sem warnings no console
- [ ] Testado em ambiente real por usuário final
- [ ] Feedback positivo do usuário
- [ ] **Espaçamento 1,5 confirmado visualmente**
- [ ] **Arial 10pt confirmado visualmente**
- [ ] Revisão de código feita
- [ ] Pronto para produção ✅
