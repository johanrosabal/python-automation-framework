from core.config.logger_config import setup_logger
import time

logger = setup_logger('AlertPrompt')


class AlertPrompt:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._alert = driver.switch_to.alert
        self._simple_alert = self.Simple(self._alert)
        self._confirm_alert = self.Confirm(self._alert)

    class Simple:
        _alert = None

        def __init__(self, alert):
            self._alert = alert

        def accept(self):
            logger.info("Simple Alert Accept")
            self._alert.accept()
            time.sleep(1)

    class Confirm:
        _alert = None

        def __init__(self, alert):
            self._alert = alert

        def cancel(self):
            logger.info("Confirm Alert Cancel")
            self._alert.dismiss()
            time.sleep(1)

        def accept(self):
            logger.info("Confirm Alert Accept")
            self._alert.accept()
            time.sleep(1)

    def simple_accept(self):
        self._simple_alert.accept()

    def confirm_accept(self):
        return self._confirm_alert.accept()

    def confirm_cancel(self):
        return self._confirm_alert.cancel()

    def send_keys(self, text: str):
        self._alert.send_keys(text)
        time.sleep(1)

    def get_text(self):
        return self._alert.text
