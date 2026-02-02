"""
Ponto de entrada da aplicação Automação RPCM
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para imports
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.gui.main_window import main

if __name__ == "__main__":
    main()
