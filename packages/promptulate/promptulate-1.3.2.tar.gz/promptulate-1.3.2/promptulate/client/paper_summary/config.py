from promptulate.utils.singleton import Singleton
from promptulate.client.paper_summary.logger import AppLogger
from promptulate.tools import PaperSummaryTool


class AppConfig(metaclass=Singleton):
    def __init__(self, logger=None):
        self.cur_driver = PaperSummaryTool
        self.cur_model = "gpt-3.5-turbo"
        self.app_logger = AppLogger(logger)

    @property
    def log_output(self):
        return self.app_logger.log_output
