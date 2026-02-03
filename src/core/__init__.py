"""
Módulo core com geradores de documentos
"""

from .document_generator import (
    DocumentGenerator,
    BatchDocumentGenerator,
    DocumentGenerationError
)

__all__ = ['DocumentGenerator', 'BatchDocumentGenerator', 'DocumentGenerationError']
