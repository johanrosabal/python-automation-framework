import pytest
from core.config.logger_config import setup_logger
from appium.webdriver.common.appiumby import AppiumBy
import time

from core.ui.driver.DriverManager import DriverManager

logger = setup_logger('Desktop')


class TestDesktop:

    application = "C:\\Windows\\System32\\notepad.exe"
    driver = DriverManager.windows_pc(application)

    @pytest.fixture(scope="class", autouse=True)
    def set_up(self) -> None:
        try:
            # Pause to allow the application to open
            time.sleep(5)

            if self.driver is None:
                raise ValueError("Driver initialization returned None.")

        except Exception as e:
            logger.error(f"Error initializing Windows PC driver: {e}")
            pytest.fail(f"Setup failed: {e}")

        yield  # Return Control to Pytest
        if self.driver:
            self.driver.quit()
        else:
            logger.error("Driver was not initialized; skipping cleanup.")

    def test_notepad(self) -> None:
        if self.driver:
            text_editor = self.driver.find_element(AppiumBy.CLASS_NAME, "Edit")
            text_editor.send_keys("Hello, this is a test with Appium and Python!")
            time.sleep(5)
        else:
            logger.error("Driver is not initialized, skipping test.")
