import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "log.log"


def _setup_logging(logger: logging.Logger):
    """Configura os handlers e o nível de logging do logger informado."""

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
    """Retorna um logger configurado.
    
    Me dê um logger com esse nome. Se ele ainda não 
    tiver sido configurado pela minha aplicação, configure-o 
    primeiro. Se já tiver sido configurado, simplesmente devolva 
    o logger existente.
    """

    logger = logging.getLogger(name)

    if not getattr(logger, "_configured", False):
        _setup_logging(logger)
        logger._configured = True

    return logger

if __name__ == '__main__':
    logger = get_logger("licita_match_logger")

    logger.info("Logger configurado!")