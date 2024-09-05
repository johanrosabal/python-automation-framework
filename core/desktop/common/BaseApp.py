from core.desktop.actions.Click import Click
from core.desktop.actions.GetText import GetText
from core.desktop.actions.SendKeys import SendKeys


class BaseApp:

    def __init__(self, driver):
        self._driver = driver

    def click(self):
        return Click(self._driver)

    def send_keys(self):
        return SendKeys(self._driver)

    def get_text(self):
        return GetText(self._driver)
