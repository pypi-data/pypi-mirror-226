import logging


class LogStream:
    def __init__(self):
        self.buffer = []

    def write(self, message):
        self.buffer.append(message)

    def flush(self):
        pass


class AppLogger:
    def __init__(self, logger: logging.Logger):
        self.log_stream = LogStream()
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(self.log_stream)
        stream_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    @property
    def log_output(self) -> str:
        print("--------------------", "".join(self.log_stream.buffer))
        return "".join(self.log_stream.buffer)
