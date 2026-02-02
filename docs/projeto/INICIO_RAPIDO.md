# 🚀 INÍCIO RÁPIDO - Automação RPCM

## Instalação em 3 Passos

### 1. Instalar Dependências

Abra o terminal/prompt na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

### 2. Colocar o Template

Coloque o arquivo `template_rpcm.docx` na pasta `templates/`

**Formato do template:**
- Use variáveis: `{{GRUPO}}`, `{{SUBGRUPO}}`, `{{N_PRECO}}`, `{{DESCRICAO}}`, `{{UNIDADE}}`, `{{REGULAMENTACAO}}`
- Veja exemplo em `templates/README.md`

### 3. Executar

```bash
python src/main.py
```

## Como Usar - Modo Individual

1. Mantenha "Modo Individual" selecionado
2. Preencha os campos:
   - **Grupo** (obrigatório)
   - **Subgrupo** (opcional - pode deixar vazio)
   - **Nº Preço** (obrigatório - só números, ex: 123456)
   - **Descrição** (obrigatória)
   - **Unidade** (obrigatória - ex: m, un, kg)
3. Digite ou cole a regulamentação
4. Clique **"Gerar Documento"**
5. Escolha onde salvar
6. ✓ Pronto!

## Como Usar - Modo Lote

1. Selecione **"Modo Lote"**
2. Digite ou cole a regulamentação **UMA VEZ** (será usada para todos)
3. Adicione itens:
   - Preencha os 5 campos
   - Clique **"Adicionar à Lista"**
   - Repita para cada item
4. Clique **"Gerar Documentos"**
5. Escolha a pasta de destino
6. ✓ Todos os documentos serão criados!

**Dica:** No Modo Lote, a regulamentação é compartilhada entre todos os documentos.

## Importar Excel (Etapa 3)

O botão "Importar Excel" aparece no Modo Lote.

**Formato esperado:**
| Grupo | Subgrupo | Nº Preço | Descrição | Unidade |
|-------|----------|----------|-----------|---------|
| INFRA | ÁGUA     | 123456   | Tubo PVC  | m       |

- Subgrupo pode estar vazio
- Salve como .xlsx, .xls ou .csv

## Validações

### Campos Obrigatórios (*)
- Grupo
- Nº Preço
- Descrição
- Unidade
- Regulamentação

### Campo Opcional
- Subgrupo (pode ficar vazio)

### Regras Especiais
- **Nº Preço:** apenas números (ex: 123456, não 01.01.01)
- **Descrição:** não use estes caracteres: `/ \ : * ? " < > |`
- **Duplicatas:** Modo Lote não permite o mesmo Nº Preço duas vezes

## Atalhos de Teclado

- `Tab`: navegar entre campos
- `Enter` no último campo: adiciona à lista (Modo Lote)

## Solução de Problemas

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

## Status Atual

✅ **ETAPA 1 CONCLUÍDA** - Interface funcional  
🔨 **ETAPA 2** - Editor de texto (em planejamento)  
🔨 **ETAPA 3** - Geração real de documentos (em planejamento)  
🔨 **ETAPA 4** - Testes completos (em planejamento)

**Observação:** Nesta etapa, a geração de documentos é simulada (cria arquivos vazios). A geração real será implementada na Etapa 3.

## Testar a Aplicação

Execute os testes automatizados:
```bash
python tests/test_etapa1.py
```

Deve exibir: `[OK] TODOS OS TESTES PASSARAM!`

## Próximos Passos

1. ✅ Testar a interface
2. ✅ Validar que todas as funcionalidades básicas funcionam
3. 🔨 Aguardar implementação da Etapa 2 (Editor de Texto)

## Suporte

Consulte a documentação completa:
- [README.md](../../README.md) - Visão geral
- [ESTRUTURA_PROJETO.md](ESTRUTURA_PROJETO.md) - Estrutura detalhada
- [../planejamento/ETAPA_1_CONCLUIDA.md](../planejamento/ETAPA_1_CONCLUIDA.md) - Relatório da Etapa 1
- [../planejamento/README_PLANEJAMENTO_FINAL.md](../planejamento/README_PLANEJAMENTO_FINAL.md) - Planejamento completo

---

**Versão:** 1.0.0  
**Última atualização:** 02/02/2026
