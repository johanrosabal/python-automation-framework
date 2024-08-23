from core.config.logger_config import setup_logger
import time

# Set up logger for the AlertPrompt class
logger = setup_logger('AlertPrompt')


class AlertPrompt:

    def __init__(self, driver):
        """
        Initialize the AlertPrompt with a WebDriver instance.

        :param driver: WebDriver instance.
        """
        self._name = self.__class__.__name__
        self._driver = driver
        # Switch to the alert window
        self._alert = driver.switch_to.alert
        # Initialize Simple and Confirm alert types
        self._simple_alert = self.Simple(self._alert)
        self._confirm_alert = self.Confirm(self._alert)

    class Simple:
        _alert = None

        def __init__(self, alert):
            """
            Initialize the Simple alert handler.

            :param alert: Alert instance from WebDriver.
            """
            self._alert = alert

        def accept(self):
            """
            Accept the simple alert if available.
            """
            if self._alert:
                logger.info("Simple Alert Accept")
                self._alert.accept()
                time.sleep(1)
            else:
                logger.error("Unable to Alert Simple Accept. WebDriver is None.")

    class Confirm:
        _alert = None

        def __init__(self, alert):
            """
            Initialize the Confirm alert handler.

            :param alert: Alert instance from WebDriver.
            """
            self._alert = alert

        def cancel(self):
            """
            Cancel the confirm alert if available.
            """
            if self._alert:
                logger.info("Confirm Alert Cancel")
                self._alert.dismiss()
                time.sleep(1)
            else:
                logger.error("Unable to Alert Confirm Cancel. WebDriver is None.")

        def accept(self):
            """
            Accept the confirm alert if available.
            """
            if self._alert:
                logger.info("Confirm Alert Accept")
                self._alert.accept()
                time.sleep(1)
            else:
                logger.error("Unable to Alert Confirm Accept. WebDriver is None.")

    def simple_accept(self):
        """
        Accept the simple alert using the Simple class handler.
        """
        if self._alert:
            self._simple_alert.accept()
        else:
            logger.error("Unable to Alert Simple Accept. WebDriver is None.")

    def confirm_accept(self):
        """
        Accept the confirm alert using the Confirm class handler.
        """
        return self._confirm_alert.accept()

    def confirm_cancel(self):
        """
        Cancel the confirm alert using the Confirm class handler.
        """
        return self._confirm_alert.cancel()

    def send_keys(self, text: str):
        """
        Send text input to the alert prompt.

        :param text: Text to send to the alert.
        """
        if self._alert:
            self._alert.send_keys(text)
            time.sleep(1)
        else:
            logger.error("Unable to Alert Send Keys. WebDriver is None.")

    def get_text(self):
        """
        Retrieve the text from the alert prompt.

        :return: The text from the alert.
        """
        if self._alert:
            return self._alert.text
        else:
            logger.error("Unable to Alert Get Text. WebDriver is None.")
