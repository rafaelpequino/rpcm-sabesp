"""
Configuração do sistema de logging
"""

import logging
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = 'AutomacaoRPCM') -> logging.Logger:
    """
    Configura sistema de logging
    
    Args:
        name: Nome do logger
        
    Returns:
        Logger configurado
    """
    
    # Criar diretório de logs
    log_dir = Path.home() / '.automacao_rpcm' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Arquivo de log com data
    log_file = log_dir / f"automacao_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configurar logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Console
        ]
    )
    
    logger = logging.getLogger(name)
    logger.info("=" * 50)
    logger.info("Aplicação iniciada")
    logger.info("=" * 50)
    
    return logger
