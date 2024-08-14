from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element
from selenium.webdriver.common.keys import Keys

logger = setup_logger('UploadFile')


class UploadFile:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._path = None
        self._file_name = None

    def set_locator(self, locator: tuple, page='Page'):
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self

    def set_path(self, path: str):
        logger.info("Setting Path of the File")
        self._path = path
        return self

    def set_file_name(self, file_name: str):
        logger.info("Setting File Name of the File")
        self._file_name = file_name
        return self

    def upload(self):
        if self._element:
            logger.info("Uploading File...")
            file_path = self._path + "\\" + self._file_name
            if self._path is not None:
                if self._file_name is not None:
                    logger.info("Uploading File ["+file_path+"]")
                    self._element.clear()
                    self._element.send_keys(file_path)
                else:
                    logger.error("Unable to upload file, Specify the File Name.")
            else:
                logger.error("Unable to upload file, Specify the Path of the File.")
        else:
            logger.error("Unable to upload file, WebElement is None.")
