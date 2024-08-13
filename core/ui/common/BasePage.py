from core.config.logger_config import setup_logger
from core.ui.actions.AlertPrompt import AlertPrompt
from core.ui.actions.Click import Click
from core.ui.actions.Frame import Frame
from core.ui.actions.GetText import GetText
from core.ui.actions.SendKeys import SendKeys
from core.ui.actions.Dropdown import Dropdown
from core.ui.actions.SwitchWindow import SwitchWindow
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('BasePage')


class BasePage(BaseApp):

    def __init__(self, driver=None):
        super().__init__()
        if driver:
            self.driver = driver

    def navigation(self):
        return Click(self.get_driver())

    def send_keys(self):
        return SendKeys(self.get_driver())

    def click_element(self):
        return Click(self.get_driver())

    def dropdown(self):
        return Dropdown(self.get_driver())

    def get_text(self):
        return GetText(self.get_driver())

    def alert(self):
        return AlertPrompt(self.get_driver())

    def frame(self):
        return Frame(self.get_driver())

    def switch_windows(self):
        return SwitchWindow(self.get_driver())
