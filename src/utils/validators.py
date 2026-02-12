"""
Validadores de campos para a interface
Garante que os dados inseridos estão corretos antes de processar
"""

import re
from typing import Tuple


class Validator:
    """Classe de validações de campos"""
    
    # Caracteres inválidos para nome de arquivo
    INVALID_FILENAME_CHARS = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    
    @staticmethod
    def validate_required(value: str, field_name: str = "Campo") -> Tuple[bool, str]:
        """
        Valida se um campo obrigatório está preenchido
        
        Args:
            value: Valor a validar
            field_name: Nome do campo para mensagem de erro
            
        Returns:
            Tupla (is_valid, error_message)
        """
        if not value or not value.strip():
            return False, f"{field_name} é obrigatório"
        return True, ""
    
    @staticmethod
    def validate_numero_preco(value: str) -> Tuple[bool, str]:
        """
        Valida formato do número de preço (apenas números)
        Formato esperado: "123456" (apenas dígitos)
        
        Args:
            value: Número de preço a validar
            
        Returns:
            Tupla (is_valid, error_message)
        """
        if not value or not value.strip():
            return False, "Número de Preço é obrigatório"
        
        # Remover espaços
        value = value.strip()
        
        # Verificar se contém apenas números
        if not value.isdigit():
            return False, "Número de Preço deve conter apenas números (ex: 123456)"
        
        # Verificar tamanho mínimo
        if len(value) < 1:
            return False, "Número de Preço muito curto"
        
        return True, ""
    
    @staticmethod
    def validate_filename(value: str) -> Tuple[bool, str]:
        """
        Valida se a descrição está preenchida
        
        Nota: Caracteres especiais são permitidos na descrição.
        Eles serão automaticamente removidos ao gerar o nome do arquivo.
        
        Args:
            value: Descrição a validar
            
        Returns:
            Tupla (is_valid, error_message)
        """
        if not value or not value.strip():
            return False, "Descrição é obrigatória"
        
        # Permitir qualquer caractere - a limpeza será feita ao gerar o arquivo
        return True, ""
    
    @staticmethod
    def validate_all_fields(descricao: str, unidade: str, numero_preco: str) -> Tuple[bool, list]:
        """
        Valida todos os campos de uma vez
        
        Args:
            descricao: Descrição
            unidade: Unidade
            numero_preco: Número de preço
            
        Returns:
            Tupla (all_valid, list_of_errors)
        """
        errors = []
        
        # Validar Descrição
        valid, msg = Validator.validate_filename(descricao)
        if not valid:
            errors.append(msg)
        
        # Validar Unidade (obrigatório)
        valid, msg = Validator.validate_required(unidade, "Unidade")
        if not valid:
            errors.append(msg)
        
        # Validar Número de Preço
        valid, msg = Validator.validate_numero_preco(numero_preco)
        if not valid:
            errors.append(msg)
        
        return len(errors) == 0, errors
