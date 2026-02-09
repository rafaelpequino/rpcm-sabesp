# 📄 Funcionalidade: Selecionar Template Customizado

## Visão Geral

O sistema permite que você use **qualquer arquivo .docx** como template para gerar os documentos RPCM. Isso é útil quando você precisa usar diferentes formatos ou layouts.

## Como Usar

### Passo 1: Preparar seu Template

Crie um arquivo Word (.docx) com o layout desejado e use as seguintes **variáveis** onde os dados devem ser inseridos:

#### Variáveis Disponíveis:

- `{{GRUPO}}` - Nome do grupo
- `{{SUBGRUPO}}` - Nome do subgrupo (pode estar vazio)
- `{{N_PRECO}}` - Número do preço
- `{{DESCRICAO}}` - Descrição do item
- `{{UNIDADE}}` - Unidade de medida

#### Exemplo de Template:

```
RELATÓRIO DE PREÇO CUSTOMIZADO MUNICIPAL - RPCM

GRUPO: {{GRUPO}}
SUBGRUPO: {{SUBGRUPO}}

Nº DO PREÇO: {{N_PRECO}}

DESCRIÇÃO:
{{DESCRICAO}}

UNIDADE: {{UNIDADE}}

---
Documento gerado automaticamente
```

### Passo 2: Selecionar o Template no Sistema

1. Abra o sistema de Automação RPCM
2. Na seção **"📄 TEMPLATE"** no topo da tela
3. Clique no botão **"📁 Selecionar Template"**
4. Navegue até o arquivo .docx do seu template
5. Clique em **"Abrir"**

### Passo 3: Confirmar Carregamento

Você verá uma mensagem de confirmação e o nome do template aparecerá na tela:

```
✓ Template: meu_template_customizado.docx
```

### Passo 4: Gerar Documentos

Agora todos os documentos gerados usarão o template customizado!

## Template Padrão

Se você **não selecionar** nenhum template, o sistema usará o template padrão:
```
templates/template_rpcm.docx
```

Status mostrado:
```
✓ Template padrão: template_rpcm.docx
```

## Validações

O sistema valida automaticamente:
- ✅ Arquivo existe
- ✅ Formato é .docx
- ✅ Arquivo é um template válido (pode ser aberto)
- ✅ Arquivo contém as variáveis esperadas

## Mensagens de Erro

### "Formato inválido"
- O arquivo selecionado não é .docx
- **Solução:** Selecione apenas arquivos Word (.docx)

### "Template Inválido"
- O arquivo está corrompido ou não pode ser lido
- **Solução:** Verifique se o arquivo abre corretamente no Word

### "Nenhum template selecionado"
- Nenhum template foi carregado (nem padrão nem customizado)
- **Solução:** Selecione um template ou coloque o template padrão na pasta `templates/`

## Boas Práticas

### ✅ FAÇA:
- Use variáveis em MAIÚSCULAS entre chaves duplas: `{{VARIAVEL}}`
- Teste o template gerando um documento de exemplo
- Mantenha uma cópia de backup do template padrão
- Use formatação consistente no template

### ❌ NÃO FAÇA:
- Não use variáveis em minúsculas: `{{grupo}}` ❌
- Não esqueça as chaves duplas: `{GRUPO}` ❌
- Não use espaços nas variáveis: `{{ GRUPO }}` ❌

## Dicas

### Múltiplos Templates

Você pode ter vários templates e alternar entre eles:
1. Organize em pastas: `templates/modelo_a/`, `templates/modelo_b/`
2. Selecione conforme necessário antes de gerar documentos
3. O sistema sempre usa o último template selecionado

### Resetar para Template Padrão

Para voltar ao template padrão:
1. Feche e reabra o sistema, **OU**
2. Selecione manualmente `templates/template_rpcm.docx`

## Exemplo de Uso

```
1. Criar template customizado "rpcm_detalhado.docx"
2. Clicar em "📁 Selecionar Template"
3. Selecionar "rpcm_detalhado.docx"
4. Ver confirmação: "✓ Template: rpcm_detalhado.docx"
5. Adicionar itens à lista
6. Gerar documentos (agora com o layout customizado)
```

## Variáveis Especiais

### Subgrupo Vazio
Se o subgrupo estiver vazio, a variável `{{SUBGRUPO}}` será substituída por uma string vazia.

**Dica:** No template, você pode escrever:
```
Subgrupo: {{SUBGRUPO}}
```

Se não houver subgrupo, aparecerá:
```
Subgrupo: 
```

Para evitar a linha vazia, use formatação condicional ou deixe o campo opcional no template.

## Solução de Problemas

### Variável não é substituída
- Verifique se está usando MAIÚSCULAS
- Verifique se tem chaves duplas `{{` e `}}`
- Verifique o nome exato da variável

### Template não carrega
- Verifique se o arquivo não está aberto no Word
- Verifique permissões de leitura do arquivo
- Tente abrir o arquivo no Word manualmente

### Formatação perdida
- O sistema preserva a formatação do template
- Certifique-se de que as variáveis estejam formatadas corretamente no template original
