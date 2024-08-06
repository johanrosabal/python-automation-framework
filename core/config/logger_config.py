import logging
from datetime import datetime
from pathlib import Path

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Configuración del archivo de logging
        project_root = Path(__file__).parent.parent.parent
        logs_directory = project_root / 'logs'
        logs_directory.mkdir(parents=True, exist_ok=True)  # Crea el directorio si no existe

        file_handler = logging.FileHandler(
            filename=str(logs_directory / f'python-framework_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log')
        )
        file_handler.setLevel(logging.INFO)

        # Configuración del stream handler (consola)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
