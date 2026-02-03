"""
Gerador de documentos RPCM

Este módulo é responsável por:
1. Carregar o template DOCX incluído no projeto
2. Substituir variáveis {{VAR}} com dados fornecidos
3. Inserir regulamentação HTML convertida para DOCX
4. Gerar documentos individuais ou em lote
"""

from docxtpl import DocxTemplate
from docx import Document
from pathlib import Path
import logging
from typing import Optional
import tempfile
import shutil

from src.models.documento_rpcm import DocumentoRPCM
from src.converters.html_to_docx import HTMLtoDOCXConverter

logger = logging.getLogger(__name__)


class DocumentGenerationError(Exception):
    """Exceção customizada para erros na geração de documentos"""
    pass


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
            raise FileNotFoundError(
                f"Template não encontrado: {self.template_path}\n"
                f"Por favor, certifique-se de que o arquivo template_rpcm.docx "
                f"está na pasta templates/"
            )
        
        if not self.template_path.suffix.lower() == '.docx':
            raise ValueError("Template deve ser um arquivo .docx")
        
        try:
            # Tentar abrir para validar
            DocxTemplate(str(self.template_path))
        except Exception as e:
            raise ValueError(f"Template inválido ou corrompido: {str(e)}")
    
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
            doc_template = DocxTemplate(str(self.template_path))
            logger.debug("Template carregado")
            
            # 2. Preparar contexto com variáveis
            context = dados.to_dict()
            logger.debug(f"Contexto preparado: {context}")
            
            # 3. Renderizar template com variáveis
            doc_template.render(context)
            logger.debug("Template renderizado com variáveis")
            
            # 4. Salvar temporariamente
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
                temp_path = Path(temp_file.name)
            
            doc_template.save(str(temp_path))
            logger.debug(f"Documento temporário salvo: {temp_path}")
            
            # 5. Reabrir com python-docx para inserir regulamentação
            doc = Document(str(temp_path))
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
            doc.save(str(output_path))
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
        marcador_encontrado = False
        
        for i, paragraph in enumerate(doc.paragraphs):
            if '{{REGULAMENTACAO}}' in paragraph.text:
                logger.debug(f"Marcador {{{{REGULAMENTACAO}}}} encontrado no parágrafo {i}")
                marcador_encontrado = True
                
                # Remover o marcador
                paragraph.text = paragraph.text.replace('{{REGULAMENTACAO}}', '')
                
                # Converter HTML para DOCX
                converter = HTMLtoDOCXConverter()
                temp_doc = Document()
                temp_doc = converter.convert(html_content, temp_doc)
                
                # Inserir elementos após este parágrafo
                self._inserir_elementos_apos_paragrafo(doc, i, temp_doc)
                
                logger.debug("Conteúdo da regulamentação inserido")
                break
        
        # Se não encontrou o marcador, adicionar no final
        if not marcador_encontrado:
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
            # Importar o elemento para o documento destino
            imported = body.append(element)
            
            # Encontrar posição de inserção
            idx = list(body).index(p_ref) + 1
            
            # Mover para a posição correta
            body.remove(imported)
            body.insert(idx, imported)
            
            # Atualizar referência
            p_ref = imported
    
    def _aplicar_formatacao_padrao(self, doc: Document):
        """
        Aplica formatação padrão Arial 10pt em todo o documento
        EXCETO em títulos e cabeçalhos (que mantêm formatação original)
        """
        from docx.shared import Pt
        
        for paragraph in doc.paragraphs:
            # Pular cabeçalhos e títulos (que têm estilo específico)
            if paragraph.style.name.startswith('Heading') or paragraph.style.name == 'Title':
                continue
                
            for run in paragraph.runs:
                # Se o texto já tem formatação especial (negrito + maior que 10pt), manter
                if run.bold and run.font.size and run.font.size > Pt(10):
                    # Manter formatação de título
                    continue
                    
                run.font.name = 'Arial'
                run.font.size = Pt(10)
        
        # Aplicar também em tabelas (mas respeitar cabeçalhos em negrito)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            # Se está em negrito, pode ser cabeçalho - manter
                            if run.bold:
                                run.font.name = 'Arial'
                                # Manter tamanho se for maior que 10pt
                                if not run.font.size or run.font.size <= Pt(10):
                                    run.font.size = Pt(10)
                            else:
                                run.font.name = 'Arial'
                                run.font.size = Pt(10)


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
                raise ValueError(
                    f"Número de preço {documento.numero_preco} já existe na lista"
                )
        
        self.documentos.append(documento)
        logger.info(f"Documento adicionado à lista: {documento.numero_preco}")
    
    def remover_documento(self, numero_preco: str):
        """Remove documento da lista pelo número de preço"""
        self.documentos = [doc for doc in self.documentos 
                          if doc.numero_preco != numero_preco]
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
                raise ValueError(
                    f"Colunas faltando no arquivo: {', '.join(colunas_faltando)}"
                )
            
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
