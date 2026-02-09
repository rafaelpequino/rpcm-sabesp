"""
Modelo de dados para documento RPCM
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentoRPCM:
    """
    Representa os dados de um documento RPCM
    
    Attributes:
        grupo: Grupo do documento (obrigatório)
        subgrupo: Subgrupo do documento (OPCIONAL - pode estar vazio)
        numero_preco: Número do preço (obrigatório, apenas números)
        descricao: Descrição do documento (obrigatório)
        unidade: Unidade de medida (obrigatório)
    """
    grupo: str
    subgrupo: str  # OPCIONAL - pode estar vazio
    numero_preco: str
    descricao: str
    unidade: str
    
    def __post_init__(self):
        """Validações após inicialização"""
        self._validar_campos_obrigatorios()
        self._limpar_campos()
    
    def _validar_campos_obrigatorios(self):
        """
        Valida se campos obrigatórios estão preenchidos
        
        IMPORTANTE: Subgrupo é OPCIONAL e pode estar vazio!
        """
        campos_obrigatorios = {
            'Grupo': self.grupo,
            'Número Preço': self.numero_preco,
            'Descrição': self.descricao,
            'Unidade': self.unidade
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
        Remove caracteres inválidos e substitui espaços por underline
        
        Returns:
            Nome do arquivo (ex: 123456_Tubulacao_PVC.docx)
        """
        descricao_limpa = self._limpar_nome_arquivo(self.descricao)
        return f"{self.numero_preco}_{descricao_limpa}.docx"
    
    @staticmethod
    def _limpar_nome_arquivo(nome: str) -> str:
        """
        Remove caracteres inválidos para nome de arquivo e substitui espaços por underscore
        
        Args:
            nome: Nome original (ex: "Nome da RPCM")
            
        Returns:
            Nome limpo e válido para arquivo (ex: "Nome_da_RPCM")
        """
        # Remove caracteres inválidos para nomes de arquivo no Windows
        caracteres_invalidos = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        
        for char in caracteres_invalidos:
            nome = nome.replace(char, '')
        
        # Substituir espaços por underscore
        nome = nome.replace(' ', '_')
        
        # Substituir múltiplos underscores por um único
        while '__' in nome:
            nome = nome.replace('__', '_')
        
        # Remover underscores do início e do fim
        nome = nome.strip('_')
        
        # Limitar tamanho (Windows tem limite de 255 chars no caminho)
        if len(nome) > 100:
            nome = nome[:100]
            # Remover underscore do final se foi cortado
            nome = nome.rstrip('_')
        
        return nome
    
    def to_dict(self) -> dict:
        """
        Converte para dicionário para uso com docxtpl
        
        Returns:
            Dicionário com variáveis em uppercase para template
        """
        return {
            'GRUPO': self.grupo,
            'SUBGRUPO': self.subgrupo,
            'N_PRECO': self.numero_preco,
            'DESCRICAO': self.descricao,
            'UNIDADE': self.unidade
        }
