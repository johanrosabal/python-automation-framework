from core.config.logger_config import setup_logger
from core.ui.actions.Click import Click
from core.ui.actions.SendKeys import SendKeys
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('BasePage')


class BasePage(BaseApp):

    def __init__(self, driver=None):
        super().__init__()
        if driver:
            self.driver = driver

    def navigation(self):
        logger.info("Navigation")
        return Click(self.get_driver())

    def send_keys(self):
        logger.info("Send Keys")
        return SendKeys(self.get_driver())

    def click_element(self):
        logger.info("Click")
        return Click(self.get_driver())
