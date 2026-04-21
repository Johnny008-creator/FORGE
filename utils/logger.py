import logging

def setup_logger(debug: bool = False):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("forge.log"),
            logging.StreamHandler() if debug else logging.NullHandler()
        ]
    )
    return logging.getLogger("forge")
