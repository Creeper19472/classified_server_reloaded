import logging


class log:
    def __init__(
        self, logname, level=(logging.DEBUG, logging.INFO), filepath="./logs.log"
    ):
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(level=logging.DEBUG)  # This level must be 'logging.DEBUG'.
        self.logger.propagate = 0
        self.lfhandler = logging.FileHandler(filename=filepath)
        self.cshandler = logging.StreamHandler()
        formatter1 = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        formatter2 = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
        self.lfhandler.setLevel(level[0])
        self.cshandler.setLevel(level[1])
        self.lfhandler.setFormatter(formatter1)
        self.cshandler.setFormatter(formatter2)
        self.logger.addHandler(self.lfhandler)
        self.logger.addHandler(self.cshandler)
