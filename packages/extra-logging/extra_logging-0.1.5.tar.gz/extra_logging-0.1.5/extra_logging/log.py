import logging
from logging.handlers import RotatingFileHandler


class Logging:
    def __init__(self, name: str = __name__,
                 path_to_file: str | None = None,
                 max_bytes: int = 0,
                 backup_count: int = 1,
                 date_fmt: str = '%m.%d.%Y %H:%M:%S',
                 level=logging.INFO,
                 format_s: str = '[%(asctime)s | %(levelname)s | %(name)s]: %(message)s',
                 stream: bool = True,
                 mode: str = 'a',
                 encoding: str = "utf-8"):
        """
        Class extending an 'logging'
        :param name:
        :param path_to_file:
        :param max_bytes:
        :param backup_count:
        :param date_fmt:
        :param level:
        :param format_s:
        :param stream:
        :param mode:
        :param encoding:
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        formatter = logging.Formatter(format_s, datefmt=date_fmt)

        if stream:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        if path_to_file is not None and max_bytes == 0:
            file_handler = logging.FileHandler(path_to_file, mode=mode, encoding=encoding)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        elif path_to_file is not None and max_bytes > 0:
            rotating_file_handler = logging.handlers.RotatingFileHandler(path_to_file, maxBytes=max_bytes,
                                                                         backupCount=backup_count, mode=mode,
                                                                         encoding=encoding)
            rotating_file_handler.setFormatter(formatter)
            logger.addHandler(rotating_file_handler)

        self.logger = logger

    @property
    def get_log(self) -> logging.Logger:
        """
        Get logger
        :return: logging.Logger
        """
        return self.logger
