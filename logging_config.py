import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "log.log"


def _setup_logging(logger: logging.Logger):
    """Configura os handlers, formato e nível de logging de um logger. 
    Adiciona handlers para saída em arquivo e console, define o nível 
    DEBUG e impede a propagação das mensagens para loggers ancestrais. 
    """

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="a",
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger configurado para o nome informado. 
    
    Caso o logger ainda não tenha sido configurado pela aplicação, 
    seus handlers e configurações de logging são inicializados antes de 
    retorná-lo. 
    
    Args: 
        name: Nome utilizado para identificar o logger. 
    
    Returns: 
        logging.Logger: Logger configurado para a aplicação. 
    """

    logger = logging.getLogger(name)

    if not getattr(logger, "_configured", False):
        _setup_logging(logger)
        logger._configured = True

    return logger

if __name__ == '__main__':
    logger = get_logger("licita_match_logger")

    logger.info("Logger configurado!")