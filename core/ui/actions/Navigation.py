from core.config.logger_config import setup_logger
from core.ui.actions.Element import Element

logger = setup_logger('Navigation')


class Navigation:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None

    def set_locator(self, locator: tuple, page='Page'):
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def get_title(self):
        title = None
        if self._driver:
            title = self._driver.title
            logger.info("Get Page Navigation title:[" + title + "]")
            return title
        else:
            logger.error("Unable to Refresh page WebDriver is None.")
        return title

    def get_back(self):
        if self._driver:
            logger.info("Move Back Navigation Page")
            self._driver.back()
        else:
            logger.error("Unable to move Back WebDriver is None.")
        return self

    def get_forward(self):
        if self._driver:
            logger.info("Move Forward Navigation Page")
            self._driver.forward()
        else:
            logger.error("Unable to move Forward WebDriver is None.")
        return self

    def get_refresh(self):
        if self._driver:
            logger.info("Refresh Navigation Page")
            self._driver.refresh()
        else:
            logger.error("Unable to Refresh page WebDriver is None.")
        return self

    def get_current_url(self):
        url = None
        if self._driver:
            url = self._driver.current_url
            logger.info("Get current url page [" + url + "]")
        else:
            logger.error("Unable to get current url page WebDriver is None.")
        return url

    def go(self, base_url, url):
        if self._driver:
            url = str(base_url) + str(url)
            self._driver.get(url)
            logger.debug(f"Go to: {url}")
        else:
            logger.error("Unable to Load page WebDriver is None.")
        return self



