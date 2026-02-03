"""
Módulo de conversores (HTML → DOCX)
"""

from .html_to_docx import HTMLtoDOCXConverter
from .word_html_cleaner import WordHTMLCleaner

__all__ = ['HTMLtoDOCXConverter', 'WordHTMLCleaner']
