import logging


class Logging:
    def __init__(self, filename):
        self.log = logging.getLogger(filename)
