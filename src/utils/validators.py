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
        Valida se a descrição não contém caracteres inválidos para nome de arquivo
        
        Args:
            value: Descrição a validar
            
        Returns:
            Tupla (is_valid, error_message)
        """
        if not value or not value.strip():
            return False, "Descrição é obrigatória"
        
        # Verificar caracteres inválidos
        invalid_chars_found = []
        for char in Validator.INVALID_FILENAME_CHARS:
            if char in value:
                invalid_chars_found.append(char)
        
        if invalid_chars_found:
            chars_str = ', '.join([f'"{c}"' for c in invalid_chars_found])
            return False, f"Descrição contém caracteres inválidos: {chars_str}"
        
        return True, ""
    
    @staticmethod
    def validate_subgrupo(value: str) -> Tuple[bool, str]:
        """
        Valida subgrupo (campo OPCIONAL)
        
        Args:
            value: Subgrupo a validar
            
        Returns:
            Tupla (is_valid, error_message) - sempre válido pois é opcional
        """
        # Subgrupo é opcional, sempre válido
        return True, ""
    
    @staticmethod
    def validate_all_fields(grupo: str, subgrupo: str, numero_preco: str, 
                          descricao: str, unidade: str) -> Tuple[bool, list]:
        """
        Valida todos os campos de uma vez
        
        Args:
            grupo: Grupo do documento
            subgrupo: Subgrupo (opcional)
            numero_preco: Número de preço
            descricao: Descrição
            unidade: Unidade
            
        Returns:
            Tupla (all_valid, list_of_errors)
        """
        errors = []
        
        # Validar Grupo (obrigatório)
        valid, msg = Validator.validate_required(grupo, "Grupo")
        if not valid:
            errors.append(msg)
        
        # Subgrupo é opcional, não validar
        
        # Validar Número de Preço
        valid, msg = Validator.validate_numero_preco(numero_preco)
        if not valid:
            errors.append(msg)
        
        # Validar Descrição
        valid, msg = Validator.validate_filename(descricao)
        if not valid:
            errors.append(msg)
        
        # Validar Unidade (obrigatório)
        valid, msg = Validator.validate_required(unidade, "Unidade")
        if not valid:
            errors.append(msg)
        
        return len(errors) == 0, errors
