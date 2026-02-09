"""
Gerador de documentos RPCM

Este módulo é responsável por:
1. Carregar o template DOCX incluído no projeto
2. Substituir variáveis {{VAR}} com dados fornecidos
3. Gerar documentos individuais ou em lote
"""

from docxtpl import DocxTemplate
from docx import Document
from pathlib import Path
import logging
from typing import Optional

from src.models.documento_rpcm import DocumentoRPCM

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
            
            # 4. Determinar caminho final
            if output_path is None:
                output_dir = self.template_path.parent / "documentos_gerados"
                output_dir.mkdir(exist_ok=True)
                output_path = output_dir / dados.get_nome_arquivo()
            else:
                output_path = Path(output_path)
            
            # 5. Salvar documento final
            doc_template.save(str(output_path))
            logger.info(f"Documento gerado com sucesso: {output_path}")
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Erro ao gerar documento: {str(e)}", exc_info=True)
            raise DocumentGenerationError(f"Falha na geração: {str(e)}") from e


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
    
    def importar_excel(self, arquivo_excel: str) -> int:
        """
        Importa lista de documentos de arquivo Excel/CSV
        
        Args:
            arquivo_excel: Caminho para arquivo .xlsx ou .csv
            
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
                        unidade=str(row['Unidade']).strip()
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
