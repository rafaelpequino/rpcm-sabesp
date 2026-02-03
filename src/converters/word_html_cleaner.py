"""
Limpador de HTML colado do Microsoft Word
Remove tags e estilos desnecessários mantendo formatação essencial
"""

from bs4 import BeautifulSoup
import re


class WordHTMLCleaner:
    """Limpa HTML colado do Word mantendo formatação essencial"""
    
    @staticmethod
    def clean(html: str) -> str:
        """
        Remove tags e estilos desnecessários do Word
        Mantém: strong, em, u, p, ul, ol, li, table, tr, td, th, span (com estilos essenciais)
        
        Args:
            html: HTML bruto do Word
            
        Returns:
            HTML limpo com formatação essencial
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remover tags específicas do Word
        for tag in soup.find_all(['o:p', 'w:sdt', 'w:sdtpr', 'v:shapetype', 'v:shape']):
            tag.decompose()
        
        # Remover comentários
        for comment in soup.find_all(string=lambda text: isinstance(text, str) and '<!--' in text):
            comment.extract()
        
        # Remover classes e IDs específicos do Word
        for tag in soup.find_all(True):
            if tag.get('class'):
                classes = tag.get('class', [])
                # Remover classes que começam com 'Mso'
                has_mso = any('Mso' in str(c) for c in classes)
                if has_mso:
                    del tag['class']
            
            if tag.get('id'):
                del tag['id']
            
            # Limpar atributos específicos do Word
            for attr in ['lang', 'xml:lang']:
                if tag.get(attr):
                    del tag[attr]
        
        # Limpar estilos inline mantendo essenciais
        for tag in soup.find_all(style=True):
            style = tag['style']
            cleaned_style = WordHTMLCleaner._clean_style(style)
            if cleaned_style:
                tag['style'] = cleaned_style
            else:
                del tag['style']
        
        return str(soup)
    
    @staticmethod
    def _clean_style(style_string: str) -> str:
        """
        Mantém apenas estilos relevantes
        
        Args:
            style_string: String de estilos CSS
            
        Returns:
            String de estilos limpa
        """
        # Estilos que queremos manter
        relevant = [
            'font-size', 'font-family', 'color', 'background-color',
            'text-align', 'font-weight', 'font-style', 'text-decoration',
            'line-height', 'margin', 'padding', 'border',
            'vertical-align', 'width', 'height'
        ]
        
        styles = [s.strip() for s in style_string.split(';') if s.strip()]
        cleaned = []
        
        for style in styles:
            if ':' in style:
                prop, value = style.split(':', 1)
                prop_clean = prop.strip().lower()
                
                # Verificar se é uma propriedade relevante
                if any(rel in prop_clean for rel in relevant):
                    cleaned.append(f"{prop.strip()}: {value.strip()}")
        
        return '; '.join(cleaned)
