# ETAPA 3 - FUNCIONALIDADES DE AUTOMAÇÃO

## Objetivo
Implementar a lógica de automação que pega os dados do formulário e o texto do editor, processa o template DOCX com as variáveis `{{variavel}}`, e gera o documento final.

## Visão Geral do Processo

```
┌─────────────────┐
│  Interface      │
│  - Grupo        │
│  - Subgrupo     │
│  - Nº Preço     │
│  - Descrição    │
│  - Unidade      │
│  - Regulamentação│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validação      │
│  de Dados       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Usar Template  │
│  do Projeto     │
│  (incluído)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Substituir     │
│  Variáveis      │
│  {{GRUPO}}      │
│  {{SUBGRUPO}}   │
│  {{N_PRECO}}    │
│  {{DESCRICAO}}  │
│  {{UNIDADE}}    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Inserir        │
│  Regulamentação │
│  (HTML→DOCX)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Salvar como    │
│  NumPreco_      │
│  Descricao.docx │
└─────────────────┘
```

## Tecnologias Principais

### 1. python-docx-template ⭐
**Biblioteca:** `docxtpl`

**Por quê?**
- Projetada especificamente para templates com variáveis `{{var}}`
- Usa Jinja2 syntax (poderoso e flexível)
- Mantém 100% da formatação do template
- Fácil de usar

**Alternativa:** `python-docx` puro (mais trabalhoso)

### 2. python-docx
Para manipulação adicional do documento após processamento do template.

### 3. Conversor da Etapa 2
Usar o `HTMLtoDOCXConverter` já implementado para inserir a regulamentação.

## Estrutura de Dados

### Classe de Dados do Documento

**Arquivo: `src/models/documento_rpcm.py`**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class DocumentoRPCM:
    """
    Representa os dados de um documento RPCM
    """
    grupo: str
    subgrupo: str  # Opcional - pode estar vazio
    numero_preco: str
    descricao: str
    unidade: str
    regulamentacao_html: str
    
    def __post_init__(self):
        """Validações após inicialização"""
        self._validar_campos_obrigatorios()
        self._limpar_campos()
    
    def _validar_campos_obrigatorios(self):
        """Valida se campos obrigatórios estão preenchidos (subgrupo é opcional)"""
        campos_obrigatorios = {
            'Grupo': self.grupo,
            'Número Preço': self.numero_preco,
            'Descrição': self.descricao,
            'Unidade': self.unidade,
            'Regulamentação': self.regulamentacao_html
        }
        
        vazios = [nome for nome, valor in campos_obrigatorios.items() 
                  if not valor or not valor.strip()]
        
        if vazios:
            raise ValueError(f"Campos obrigatórios vazios: {', '.join(vazios)}")
    
    def _limpar_campos(self):
        """Remove espaços em branco extras"""
        self.grupo = self.grupo.strip()
        self.subgrupo = self.subgrupo.strip() if self.subgrupo else ""  # Pode estar vazio
        self.numero_preco = self.numero_preco.strip()
        self.descricao = self.descricao.strip()
        self.unidade = self.unidade.strip()
    
    def get_nome_arquivo(self) -> str:
        """
        Gera nome do arquivo no formato: NumPreco_Descricao.docx
        Remove caracteres inválidos da descrição
        Exemplo: 123456_Tubulacao PVC.docx
        """
        descricao_limpa = self._limpar_nome_arquivo(self.descricao)
        return f"{self.numero_preco}_{descricao_limpa}.docx"
    
    @staticmethod
    def _limpar_nome_arquivo(nome: str) -> str:
        """Remove caracteres inválidos para nome de arquivo"""
        caracteres_invalidos = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        
        for char in caracteres_invalidos:
            nome = nome.replace(char, '')
        
        # Substituir múltiplos espaços por um único
        nome = ' '.join(nome.split())
        
        # Limitar tamanho (Windows tem limite de 255 chars no caminho)
        if len(nome) > 100:
            nome = nome[:100]
        
        return nome
    
    def to_dict(self) -> dict:
        """Converte para dicionário para uso com docxtpl"""
        return {
            'GRUPO': self.grupo,
            'SUBGRUPO': self.subgrupo,
            'N_PRECO': self.numero_preco,
            'DESCRICAO': self.descricao,
            'UNIDADE': self.unidade
        }
```

## Processamento do Template

### Classe Principal de Geração

**Arquivo: `src/core/document_generator.py`**

```python
from docxtpl import DocxTemplate
from docx import Document
from pathlib import Path
import logging
from typing import Optional

from src.models.documento_rpcm import DocumentoRPCM
from src.converters.html_to_docx import HTMLtoDOCXConverter

logger = logging.getLogger(__name__)

class DocumentGenerator:
    """
    Classe responsável por gerar documentos RPCM a partir do template incluído no projeto
    """
    
    def __init__(self, template_path: Optional[str] = None):
        """
        Args:
            template_path: Caminho para o arquivo template .docx
                          Se None, usa o template padrão em templates/template_rpcm.docx
        """
        if template_path is None:
            # Usar template incluído no projeto
            projeto_root = Path(__file__).parent.parent.parent
            self.template_path = projeto_root / "templates" / "template_rpcm.docx"
        else:
            self.template_path = Path(template_path)
        
        self._validar_template()
    
    def _validar_template(self):
        """Valida se o template existe e é acessível"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template não encontrado: {self.template_path}")
        
        if not self.template_path.suffix.lower() == '.docx':
            raise ValueError("Template deve ser um arquivo .docx")
        
        try:
            # Tentar abrir para validar
            DocxTemplate(self.template_path)
        except Exception as e:
            raise ValueError(f"Template inválido: {str(e)}")
    
    def gerar_documento(
        self, 
        dados: DocumentoRPCM, 
        output_path: Optional[str] = None
    ) -> str:
        """
        Gera documento DOCX a partir dos dados fornecidos
        
        Args:
            dados: Objeto DocumentoRPCM com os dados
            output_path: Caminho para salvar (opcional, usa nome automático se None)
        
        Returns:
            Caminho completo do arquivo gerado
        """
        logger.info(f"Iniciando geração do documento para: {dados.numero_preco}")
        
        try:
            # 1. Carregar template
            doc_template = DocxTemplate(self.template_path)
            logger.debug("Template carregado")
            
            # 2. Preparar contexto com variáveis
            context = dados.to_dict()
            logger.debug(f"Contexto preparado: {context}")
            
            # 3. Renderizar template com variáveis
            doc_template.render(context)
            logger.debug("Template renderizado com variáveis")
            
            # 4. Salvar temporariamente
            temp_path = self.template_path.parent / "temp_output.docx"
            doc_template.save(temp_path)
            logger.debug(f"Documento temporário salvo: {temp_path}")
            
            # 5. Reabrir com python-docx para inserir regulamentação
            doc = Document(temp_path)
            logger.debug("Documento reaberto para inserção da regulamentação")
            
            # 6. Encontrar marcador {{REGULAMENTACAO}} e substituir
            self._inserir_regulamentacao(doc, dados.regulamentacao_html)
            logger.debug("Regulamentação inserida")
            
            # 7. Aplicar formatação padrão
            self._aplicar_formatacao_padrao(doc)
            logger.debug("Formatação padrão aplicada")
            
            # 8. Determinar caminho final
            if output_path is None:
                output_dir = self.template_path.parent / "documentos_gerados"
                output_dir.mkdir(exist_ok=True)
                output_path = output_dir / dados.get_nome_arquivo()
            else:
                output_path = Path(output_path)
            
            # 9. Salvar documento final
            doc.save(output_path)
            logger.info(f"Documento gerado com sucesso: {output_path}")
            
            # 10. Limpar arquivo temporário
            temp_path.unlink()
            logger.debug("Arquivo temporário removido")
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Erro ao gerar documento: {str(e)}", exc_info=True)
            raise DocumentGenerationError(f"Falha na geração: {str(e)}") from e
    
    def _inserir_regulamentacao(self, doc: Document, html_content: str):
        """
        Encontra o marcador {{REGULAMENTACAO}} e substitui pelo conteúdo HTML
        """
        # Procurar em todos os parágrafos
        for i, paragraph in enumerate(doc.paragraphs):
            if '{{REGULAMENTACAO}}' in paragraph.text:
                logger.debug(f"Marcador {{{{REGULAMENTACAO}}}} encontrado no parágrafo {i}")
                
                # Remover o marcador
                paragraph.text = paragraph.text.replace('{{REGULAMENTACAO}}', '')
                
                # Inserir conteúdo HTML convertido após este parágrafo
                converter = HTMLtoDOCXConverter()
                
                # Criar documento temporário para conversão
                temp_doc = Document()
                temp_doc = converter.convert(html_content, temp_doc)
                
                # Copiar elementos do temp_doc para o doc principal
                # Inserir após o parágrafo atual
                self._inserir_elementos_apos_paragrafo(doc, i, temp_doc)
                
                logger.debug("Conteúdo da regulamentação inserido")
                return
        
        # Se não encontrou o marcador, adicionar no final
        logger.warning("Marcador {{REGULAMENTACAO}} não encontrado, adicionando no final")
        converter = HTMLtoDOCXConverter()
        doc = converter.convert(html_content, doc)
    
    def _inserir_elementos_apos_paragrafo(
        self, 
        doc_destino: Document, 
        index: int, 
        doc_origem: Document
    ):
        """
        Insere todos os elementos de doc_origem após o parágrafo index em doc_destino
        """
        # Esta é uma operação complexa no python-docx
        # Precisamos copiar os elementos XML diretamente
        
        paragrafo_referencia = doc_destino.paragraphs[index]
        
        # Obter o elemento XML do parágrafo
        p_ref = paragrafo_referencia._element
        
        # Obter o body do documento
        body = doc_destino._element.body
        
        # Inserir cada elemento do doc_origem após p_ref
        for element in doc_origem._element.body:
            # Clonar o elemento
            cloned = element.__class__(element)
            
            # Encontrar posição de inserção
            idx = body.index(p_ref) + 1
            
            # Inserir
            body.insert(idx, cloned)
            
            # Atualizar referência
            p_ref = cloned
    
    def _aplicar_formatacao_padrao(self, doc: Document):
        """
        Aplica formatação padrão Arial 10pt em todo o documento
        """
        from docx.shared import Pt
        
        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(10)
        
        # Aplicar também em tabelas
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.name = 'Arial'
                            run.font.size = Pt(10)

class DocumentGenerationError(Exception):
    """Exceção customizada para erros na geração de documentos"""
    pass


class BatchDocumentGenerator:
    """
    Classe para geração em lote de documentos RPCM
    """
    
    def __init__(self, template_path: Optional[str] = None):
        """
        Args:
            template_path: Caminho para o template (opcional)
        """
        self.generator = DocumentGenerator(template_path)
        self.documentos = []
    
    def adicionar_documento(self, documento: DocumentoRPCM):
        """
        Adiciona documento à lista de geração
        
        Args:
            documento: Objeto DocumentoRPCM
            
        Raises:
            ValueError: Se número de preço já existe na lista
        """
        # Verificar duplicata
        for doc in self.documentos:
            if doc.numero_preco == documento.numero_preco:
                raise ValueError(f"Número de preço {documento.numero_preco} já existe na lista")
        
        self.documentos.append(documento)
        logger.info(f"Documento adicionado à lista: {documento.numero_preco}")
    
    def remover_documento(self, numero_preco: str):
        """Remove documento da lista pelo número de preço"""
        self.documentos = [doc for doc in self.documentos if doc.numero_preco != numero_preco]
        logger.info(f"Documento removido da lista: {numero_preco}")
    
    def limpar_lista(self):
        """Limpa todos os documentos da lista"""
        self.documentos = []
        logger.info("Lista de documentos limpa")
    
    def gerar_todos(
        self, 
        output_directory: str,
        callback_progresso: Optional[callable] = None
    ) -> dict:
        """
        Gera todos os documentos da lista
        
        Args:
            output_directory: Diretório onde salvar os documentos
            callback_progresso: Função callback(atual, total, nome_arquivo) para progresso
            
        Returns:
            dict com estatísticas: {'sucesso': 10, 'erro': 0, 'total': 10, 'arquivos': [...]}
        """
        if not self.documentos:
            raise ValueError("Lista de documentos está vazia")
        
        output_path = Path(output_directory)
        output_path.mkdir(parents=True, exist_ok=True)
        
        resultados = {
            'sucesso': 0,
            'erro': 0,
            'total': len(self.documentos),
            'arquivos': [],
            'erros': []
        }
        
        logger.info(f"Iniciando geração em lote de {resultados['total']} documentos")
        
        for i, documento in enumerate(self.documentos, 1):
            try:
                # Callback de progresso
                if callback_progresso:
                    callback_progresso(i, resultados['total'], documento.get_nome_arquivo())
                
                # Gerar documento
                arquivo_path = output_path / documento.get_nome_arquivo()
                resultado = self.generator.gerar_documento(documento, str(arquivo_path))
                
                resultados['sucesso'] += 1
                resultados['arquivos'].append(resultado)
                
                logger.info(f"[{i}/{resultados['total']}] Sucesso: {documento.numero_preco}")
                
            except Exception as e:
                resultados['erro'] += 1
                resultados['erros'].append({
                    'numero_preco': documento.numero_preco,
                    'erro': str(e)
                })
                logger.error(f"[{i}/{resultados['total']}] Erro: {documento.numero_preco} - {str(e)}")
        
        logger.info(f"Geração em lote concluída: {resultados['sucesso']} sucesso, {resultados['erro']} erros")
        
        return resultados
    
    def importar_excel(self, arquivo_excel: str, regulamentacao_html: str) -> int:
        """
        Importa lista de documentos de arquivo Excel/CSV
        
        Args:
            arquivo_excel: Caminho para arquivo .xlsx ou .csv
            regulamentacao_html: HTML da regulamentação (comum a todos)
            
        Returns:
            Número de documentos importados
            
        Formato esperado do Excel:
        | Grupo | Subgrupo | Nº Preço | Descrição | Unidade |
        """
        import pandas as pd
        
        try:
            # Ler arquivo
            if arquivo_excel.endswith('.csv'):
                df = pd.read_csv(arquivo_excel)
            else:
                df = pd.read_excel(arquivo_excel)
            
            # Validar colunas
            colunas_necessarias = ['Grupo', 'Nº Preço', 'Descrição', 'Unidade']
            colunas_faltando = [col for col in colunas_necessarias if col not in df.columns]
            
            if colunas_faltando:
                raise ValueError(f"Colunas faltando no arquivo: {', '.join(colunas_faltando)}")
            
            # Adicionar coluna Subgrupo se não existir
            if 'Subgrupo' not in df.columns:
                df['Subgrupo'] = ''
            
            # Importar cada linha
            importados = 0
            erros = []
            
            for idx, row in df.iterrows():
                try:
                    doc = DocumentoRPCM(
                        grupo=str(row['Grupo']).strip(),
                        subgrupo=str(row['Subgrupo']).strip() if pd.notna(row['Subgrupo']) else '',
                        numero_preco=str(row['Nº Preço']).strip(),
                        descricao=str(row['Descrição']).strip(),
                        unidade=str(row['Unidade']).strip(),
                        regulamentacao_html=regulamentacao_html
                    )
                    
                    self.adicionar_documento(doc)
                    importados += 1
                    
                except Exception as e:
                    erros.append(f"Linha {idx+2}: {str(e)}")
            
            if erros:
                logger.warning(f"Importação com erros:\n" + "\n".join(erros))
            
            logger.info(f"Importados {importados} documentos de {arquivo_excel}")
            
            return importados
            
        except Exception as e:
            logger.error(f"Erro ao importar Excel: {str(e)}")
            raise ImportError(f"Erro ao importar arquivo: {str(e)}") from e
```

## Integração com a Interface

### Conectar Botões e Modos

**Arquivo: `src/gui/main_window.py` (atualização)**

```python
from tkinter import filedialog, messagebox
from src.core.document_generator import DocumentGenerator, DocumentGenerationError, BatchDocumentGenerator
from src.models.documento_rpcm import DocumentoRPCM

class MainWindow:
    # ... código anterior ...
    
    def __init__(self):
        # ... código anterior ...
        
        # Modo de operação
        self.modo = "individual"  # "individual" ou "lote"
        
        # Inicializar geradores com template padrão
        try:
            self.generator = DocumentGenerator()  # Modo individual
            self.batch_generator = BatchDocumentGenerator()  # Modo lote
            self.update_status("Sistema pronto", "success")
        except FileNotFoundError:
            messagebox.showerror(
                "Template não encontrado",
                "O arquivo template_rpcm.docx não foi encontrado na pasta templates/.\n"
                "Por favor, certifique-se de que o template está no local correto."
            )
            self.update_status("Template não encontrado", "error")
            self.btn_gerar.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inicializar:\n{str(e)}")
            self.update_status("Erro na inicialização", "error")
    
    def on_modo_changed(self, novo_modo):
        """Handler quando usuário muda o modo (Individual/Lote)"""
        self.modo = novo_modo
        
        if novo_modo == "lote":
            # Mostrar elementos do modo lote
            self.tabela_lista.pack(fill="both", expand=True)
            self.btn_adicionar.pack()
            self.btn_importar.pack()
            self.btn_gerar.configure(text="Gerar Documentos")
        else:
            # Esconder elementos do modo lote
            self.tabela_lista.pack_forget()
            self.btn_adicionar.pack_forget()
            self.btn_importar.pack_forget()
            self.btn_gerar.configure(text="Gerar Documento")
        
        self.update_status(f"Modo alterado para: {novo_modo.title()}", "info")
    
    def on_adicionar_lista(self):
        """Handler para botão Adicionar à Lista (Modo Lote)"""
        try:
            # Coletar dados dos campos
            dados = self._coletar_dados_formulario()
            
            # Adicionar à lista do batch generator
            self.batch_generator.adicionar_documento(dados)
            
            # Adicionar à tabela visual
            self._adicionar_item_tabela(dados)
            
            # Limpar apenas campos de dados (manter regulamentação)
            self._limpar_campos_dados()
            
            # Focar no campo Grupo
            self.input_grupo.focus()
            
            self.update_status(f"Item adicionado: {dados.numero_preco}", "success")
            
        except ValueError as e:
            messagebox.showerror("Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar item:\n{str(e)}")
    
    def on_remover_item_lista(self, numero_preco):
        """Remove item da lista"""
        self.batch_generator.remover_documento(numero_preco)
        self._remover_item_tabela(numero_preco)
        self.update_status(f"Item removido: {numero_preco}", "info")
    
    def on_gerar_documento(self):
        """Handler para botão Gerar Documento(s) - Individual ou Lote"""
        
        if self.modo == "individual":
            self._gerar_documento_individual()
        else:
            self._gerar_documentos_lote()
    
    def _gerar_documento_individual(self):
        """Gera um único documento (Modo Individual)"""
        
        # 1. Validar se gerador foi inicializado corretamente
        if not self.generator:
            messagebox.showerror(
                "Erro de Sistema", 
                "O sistema não foi inicializado corretamente. Verifique se o template existe."
            )
            return
        
        # 2. Coletar dados da interface
        try:
            dados = self._coletar_dados_formulario()
        except ValueError as e:
            messagebox.showerror("Validação", str(e))
            return
        
        # 3. Perguntar onde salvar
        output_path = filedialog.asksaveasfilename(
            title="Salvar Documento",
            defaultextension=".docx",
            initialfile=dados.get_nome_arquivo(),
            filetypes=[("Word Documents", "*.docx")]
        )
        
        if not output_path:
            return  # Usuário cancelou
        
        # 4. Gerar documento
        self.update_status("Gerando documento...", "info")
        self.btn_gerar.configure(state="disabled")
        
        try:
            resultado = self.generator.gerar_documento(dados, output_path)
            
            messagebox.showinfo(
                "Sucesso", 
                f"Documento gerado com sucesso!\n\n{resultado}"
            )
            self.update_status("Documento gerado com sucesso!", "success")
            
            # Perguntar se quer abrir o documento
            if messagebox.askyesno("Abrir documento?", "Deseja abrir o documento gerado?"):
                import os
                os.startfile(resultado)  # Windows
            
        except DocumentGenerationError as e:
            messagebox.showerror("Erro na Geração", str(e))
            self.update_status("Erro na geração do documento", "error")
        
        finally:
            self.btn_gerar.configure(state="normal")
    
    def _gerar_documentos_lote(self):
        """Gera múltiplos documentos (Modo Lote)"""
        
        # 1. Validar se há documentos na lista
        if not self.batch_generator.documentos:
            messagebox.showwarning(
                "Lista vazia",
                "Adicione pelo menos um documento à lista antes de gerar."
            )
            return
        
        # 2. Selecionar pasta de destino
        output_dir = filedialog.askdirectory(
            title="Selecionar pasta para salvar documentos"
        )
        
        if not output_dir:
            return  # Usuário cancelou
        
        # 3. Criar janela de progresso
        progresso_window = self._criar_janela_progresso()
        
        # 4. Callback de progresso
        def atualizar_progresso(atual, total, nome_arquivo):
            porcentagem = (atual / total) * 100
            progresso_window.update_progress(porcentagem, f"Gerando {nome_arquivo}...")
            self.update_status(f"Gerando documento {atual} de {total}...", "info")
        
        # 5. Gerar todos os documentos
        self.btn_gerar.configure(state="disabled")
        
        try:
            resultados = self.batch_generator.gerar_todos(
                output_dir,
                callback_progresso=atualizar_progresso
            )
            
            progresso_window.close()
            
            # 6. Exibir resumo
            mensagem = f"Geração em lote concluída!\n\n"
            mensagem += f"✅ Sucesso: {resultados['sucesso']}\n"
            
            if resultados['erro'] > 0:
                mensagem += f"❌ Erros: {resultados['erro']}\n\n"
                mensagem += "Documentos com erro:\n"
                for erro in resultados['erros'][:5]:  # Mostrar até 5
                    mensagem += f"  - {erro['numero_preco']}: {erro['erro']}\n"
            
            messagebox.showinfo("Geração Concluída", mensagem)
            self.update_status(
                f"Lote concluído: {resultados['sucesso']} sucesso, {resultados['erro']} erros",
                "success" if resultados['erro'] == 0 else "warning"
            )
            
            # 7. Perguntar se quer abrir pasta
            if messagebox.askyesno("Abrir pasta?", "Deseja abrir a pasta com os documentos?"):
                import os
                os.startfile(output_dir)  # Windows
            
            # 8. Limpar lista após sucesso
            if resultados['erro'] == 0:
                self.batch_generator.limpar_lista()
                self._limpar_tabela()
            
        except Exception as e:
            progresso_window.close()
            messagebox.showerror("Erro na Geração", f"Erro ao gerar documentos:\n{str(e)}")
            self.update_status("Erro na geração em lote", "error")
        
        finally:
            self.btn_gerar.configure(state="normal")
    
    def on_importar_excel(self):
        """Handler para importar dados de Excel/CSV"""
        
        # 1. Validar se regulamentação foi preenchida
        regulamentacao = self.editor.get_html_content()
        if not regulamentacao or not regulamentacao.strip():
            messagebox.showwarning(
                "Regulamentação vazia",
                "Preencha a regulamentação antes de importar dados."
            )
            return
        
        # 2. Selecionar arquivo
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo Excel/CSV",
            filetypes=[
                ("Excel", "*.xlsx"),
                ("Excel 97-2003", "*.xls"),
                ("CSV", "*.csv"),
                ("Todos", "*.*")
            ]
        )
        
        if not arquivo:
            return
        
        # 3. Importar
        self.update_status("Importando dados...", "info")
        
        try:
            num_importados = self.batch_generator.importar_excel(arquivo, regulamentacao)
            
            # Atualizar tabela visual
            self._atualizar_tabela_completa()
            
            messagebox.showinfo(
                "Importação Concluída",
                f"Importados {num_importados} documentos com sucesso!"
            )
            self.update_status(f"{num_importados} itens importados", "success")
            
        except ImportError as e:
            messagebox.showerror("Erro na Importação", str(e))
            self.update_status("Erro ao importar arquivo", "error")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado:\n{str(e)}")
            self.update_status("Erro na importação", "error")
    
    def _coletar_dados_formulario(self) -> DocumentoRPCM:
        """Coleta e valida dados do formulário"""
        
        # Obter HTML do editor
        regulamentacao_html = self.editor.get_html_content()
        
        # Criar objeto de dados (subgrupo pode estar vazio)
        dados = DocumentoRPCM(
            grupo=self.input_grupo.get(),
            subgrupo=self.input_subgrupo.get() or "",  # Pode estar vazio
            numero_preco=self.input_numero_preco.get(),
            descricao=self.input_descricao.get(),
            unidade=self.input_unidade.get(),
            regulamentacao_html=regulamentacao_html
        )
        
        return dados
    
    def _limpar_campos_dados(self):
        """Limpa apenas os campos de dados (mantém regulamentação)"""
        self.input_grupo.delete(0, 'end')
        self.input_subgrupo.delete(0, 'end')
        self.input_numero_preco.delete(0, 'end')
        self.input_descricao.delete(0, 'end')
        self.input_unidade.delete(0, 'end')
    
    def on_limpar_tudo(self):
        """Handler para botão Limpar Tudo"""
        
        # Confirmar
        if messagebox.askyesno("Confirmar", "Deseja limpar todos os campos?"):
            # Limpar campos
            self.input_grupo.delete(0, 'end')
            self.input_subgrupo.delete(0, 'end')
            self.input_numero_preco.delete(0, 'end')
            self.input_descricao.delete(0, 'end')
            self.input_unidade.delete(0, 'end')
            
            # Limpar editor
            self.editor.clear_editor()
            
            self.update_status("Formulário limpo", "info")
```

## Configuração e Persistência

### Salvar Configurações do Usuário

**Arquivo: `src/utils/config_manager.py`**

```python
import json
from pathlib import Path
from typing import Optional

class ConfigManager:
    """Gerencia configurações persistentes do aplicativo"""
    
    CONFIG_FILE = Path.home() / '.automacao_rpcm' / 'config.json'
    
    @classmethod
    def load_config(cls) -> dict:
        """Carrega configurações salvas"""
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return cls._default_config()
        return cls._default_config()
    
    @classmethod
    def save_config(cls, config: dict):
        """Salva configurações"""
        cls.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    
    @classmethod
    def _default_config(cls) -> dict:
        return {
            'last_output_directory': None,
            'window_size': [1000, 800],
            'window_position': None
        }
    
    @classmethod
    def get_last_output_directory(cls) -> Optional[str]:
        """Retorna último diretório de saída usado"""
        config = cls.load_config()
        return config.get('last_output_directory')
    
    @classmethod
    def set_last_output_directory(cls, path: str):
        """Salva último diretório de saída usado"""
        config = cls.load_config()
        config['last_output_directory'] = path
        cls.save_config(config)
```

## Logging e Monitoramento

### Sistema de Logs

**Arquivo: `src/utils/logger_config.py`**

```python
import logging
from pathlib import Path
from datetime import datetime

def setup_logger():
    """Configura sistema de logging"""
    
    # Criar diretório de logs
    log_dir = Path.home() / '.automacao_rpcm' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Arquivo de log com data
    log_file = log_dir / f"automacao_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configurar logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Console
        ]
    )
    
    logger = logging.getLogger('AutomacaoRPCM')
    logger.info("=" * 50)
    logger.info("Aplicação iniciada")
    logger.info("=" * 50)
    
    return logger
```

## Estrutura de Arquivos - Etapa 3

```
AutomacaoRPCMs/
│
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   └── document_generator.py    # Gerador principal
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── documento_rpcm.py        # Modelo de dados
│   │
│   └── utils/
│       ├── config_manager.py        # Gerenciador de config
│       └── logger_config.py         # Configuração de logs
│
├── templates/
│   └── template_rpcm.docx           # Template fornecido pelo usuário
│
├── documentos_gerados/              # Documentos gerados
│
└── tests/
    └── test_generator/
        ├── test_document_generation.py
        ├── test_variable_substitution.py
        └── test_regulamentacao_insertion.py
```

## Tratamento de Erros

### Erros Possíveis e Tratamentos

1. **Template não encontrado**
   - Mensagem clara ao usuário
   - Solicitar seleção de novo template

2. **Campos vazios**
   - Validação antes de gerar
   - Destacar campos problemáticos

3. **Erro ao salvar arquivo**
   - Verificar permissões
   - Sugerir local alternativo

4. **Template corrompido**
   - Validar antes de usar
   - Mensagem descritiva

5. **Marcador {{REGULAMENTACAO}} não encontrado**
   - Warning, mas continuar
   - Adicionar no final do documento

## Testes

### Casos de Teste Essenciais

```python
# tests/test_generator/test_document_generation.py

import pytest
from src.core.document_generator import DocumentGenerator
from src.models.documento_rpcm import DocumentoRPCM

def test_gerar_documento_basico():
    """Testa geração básica de documento"""
    generator = DocumentGenerator('templates/template_rpcm.docx')
    
    dados = DocumentoRPCM(
        grupo="GRUPO TESTE",
        subgrupo="SUBGRUPO TESTE",
        numero_preco="01.01.01",
        descricao="Teste de descrição",
        unidade="m",
        regulamentacao_html="<p>Regulamentação de teste</p>"
    )
    
    output = generator.gerar_documento(dados)
    
    assert Path(output).exists()
    assert Path(output).name == "01.01.01_Teste de descrição.docx"

def test_validacao_campos_vazios():
    """Testa validação de campos obrigatórios"""
    with pytest.raises(ValueError):
        DocumentoRPCM(
            grupo="",  # Vazio
            subgrupo="SUB",
            numero_preco="01",
            descricao="DESC",
            unidade="m",
            regulamentacao_html="<p>Reg</p>"
        )

def test_nome_arquivo_caracteres_invalidos():
    """Testa limpeza de caracteres inválidos no nome"""
    dados = DocumentoRPCM(
        grupo="G",
        subgrupo="S",
        numero_preco="01",
        descricao="Teste / com : caracteres * inválidos",
        unidade="m",
        regulamentacao_html="<p>R</p>"
    )
    
    nome = dados.get_nome_arquivo()
    assert '/' not in nome
    assert ':' not in nome
    assert '*' not in nome
```

## Critérios de Conclusão da Etapa 3

- [ ] Classe `DocumentoRPCM` implementada com validações
- [ ] Validação de Nº Preço (apenas números) implementada
- [ ] Classe `DocumentGenerator` implementada
- [ ] Template incluído no projeto (templates/template_rpcm.docx)
- [ ] Gerador usa template do projeto automaticamente
- [ ] Substituição de variáveis {{VAR}} funcionando
- [ ] Inserção da regulamentação funcionando
- [ ] Formatação Arial 10pt aplicada
- [ ] Nome de arquivo gerado corretamente (NumPreco_Descricao.docx)
- [ ] Integração com interface funcionando
- [ ] Sistema de logging implementado
- [ ] Gerenciamento de configurações implementado
- [ ] Tratamento de erros robusto
- [ ] Todos os testes passando
- [ ] Documentação completa

## Tempo Estimado
**3-4 dias** de desenvolvimento

## Próxima Etapa
Após conclusão, passar para ETAPA 4 - Testes Completos e Refinamentos.
