"""
Gerenciador de configurações persistentes
"""

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
    
    @classmethod
    def get_window_size(cls) -> list:
        """Retorna tamanho da janela salvo"""
        config = cls.load_config()
        return config.get('window_size', [1000, 800])
    
    @classmethod
    def set_window_size(cls, width: int, height: int):
        """Salva tamanho da janela"""
        config = cls.load_config()
        config['window_size'] = [width, height]
        cls.save_config(config)
