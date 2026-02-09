# 📋 Funcionalidade: Copiar do Excel

## Como Usar

### Passo 1: Preparar os Dados no Excel

Organize seus dados no Excel com as seguintes colunas **nesta ordem exata**:

| GRUPO | SUBGRUPO | Nº PREÇO | DESCRIÇÃO | UNIDADE |
|-------|----------|----------|-----------|---------|
| Grupo 1 | Subgrupo 1 | 100001 | Exemplo de Descrição 1 | Un |
| Grupo 2 | Subgrupo 2 | 100002 | Exemplo de Descrição 2 | Un |
| Grupo 3 | Subgrupo 3 | 100003 | Exemplo de Descrição 3 | Un |

**Observações:**
- A coluna SUBGRUPO é opcional (pode estar vazia)
- A primeira linha (cabeçalho) será automaticamente ignorada se contiver "Nº PREÇO" ou similar
- Certifique-se de que os números de preço sejam únicos

### Passo 2: Copiar os Dados

1. Selecione as linhas com dados no Excel (incluindo ou não o cabeçalho)
2. Pressione `Ctrl + C` para copiar

### Passo 3: Colar no Sistema

1. Abra o sistema de Automação RPCM
2. Clique no botão **"📋 Copiar do Excel"**
3. O sistema irá automaticamente:
   - Ler os dados da área de transferência
   - Validar cada linha
   - Adicionar os itens válidos à lista
   - Ignorar duplicatas
   - Mostrar um relatório com o resultado

## Validações

O sistema valida automaticamente:
- ✅ Grupo (obrigatório, não pode estar vazio)
- ✅ Nº Preço (obrigatório, apenas números)
- ✅ Descrição (obrigatória)
- ✅ Unidade (obrigatória)
- ✅ Duplicatas (itens com mesmo Nº Preço são ignorados)

## Mensagens de Erro

### "Clipboard Vazio"
- Você não copiou nenhum dado antes de clicar no botão
- **Solução:** Copie os dados do Excel primeiro (Ctrl+C)

### "Formato inválido (esperado 5 colunas)"
- A linha não tem as 5 colunas necessárias
- **Solução:** Verifique se copiou todas as colunas corretamente

### "Itens duplicados ignorados"
- Alguns números de preço já estão na lista
- **Solução:** Normal, o sistema ignora automaticamente duplicatas

## Exemplo de Uso

```
Dados copiados do Excel:
Grupo 1	Subgrupo 1	100001	Exemplo de Descrição 1	Un
Grupo 2	Subgrupo 2	100002	Exemplo de Descrição 2	Un
Grupo 3	Subgrupo 3	100003	Exemplo de Descrição 3	Un

Resultado:
✓ 3 itens adicionados à lista
```

## Teste Rápido

Para testar a funcionalidade, execute:

```bash
python test_clipboard.py
```

Este script irá:
1. Copiar dados de exemplo para o clipboard
2. Executar o sistema
3. Você pode então clicar em "Copiar do Excel" para ver a funcionalidade em ação
