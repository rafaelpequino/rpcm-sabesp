# Alterações Realizadas - 03/02/2026

## ✅ Implementado:

### 1. ✅ Lista acima da Regulamentação
- Ordem alterada: Lista de Documentos → Editor de Regulamentação
- Mais prático para visualizar documentos enquanto adiciona

### 2. ✅ Sem perguntas após gerar
- Removidas todas as perguntas (abrir documento, abrir pasta, limpar lista)
- Apenas mostra mensagem de sucesso e pronto

### 3. ✅ Botão "Importar Excel" removido
- Botão completamente removido da interface
- Funcionalidade de importação desativada

### 4. ✅ Nome de arquivo sem espaços
- Espaços substituídos por underscore (_)
- Exemplo: "Descrição Teste" → "Descrição_Teste.docx"
- Múltiplos espaços viram um único underscore

### 5. ✅ Regulamentação corrigida
- Marcador {{REGULAMENTACAO}} no template será substituído
- Conteúdo HTML do editor será convertido e inserido
- Se marcador não existir, adiciona no final

### 6. ✅ Título mantém formatação
- Títulos em NEGRITO e MAIOR são preservados
- Formatação especial não é sobrescrita
- Apenas texto normal vira Arial 10pt

## Como usar:

1. **Criar template:**
   - Arquivo: `templates/template_rpcm.docx`
   - Adicionar marcador `{{REGULAMENTACAO}}` onde quer o texto
   - Títulos podem estar em negrito e maior

2. **Executar:**
   ```bash
   python src/main.py
   ```

3. **Modo Lote:**
   - Preencher campos
   - Adicionar à lista (lista aparece acima)
   - Preencher regulamentação (uma vez)
   - Gerar documentos
   - Pronto! Sem perguntas.

## Arquivos modificados:
- `src/models/documento_rpcm.py` - Nome arquivo sem espaços
- `src/gui/main_window.py` - Ordem layout, remover perguntas, remover botão Excel
- `src/core/document_generator.py` - Preservar formatação de títulos
