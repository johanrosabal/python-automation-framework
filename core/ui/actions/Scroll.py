from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element
from selenium.webdriver.common.keys import Keys

logger = setup_logger('Scroll')


class Scroll:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None

    def set_locator(self, locator: tuple, page='Page'):
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self

    def to_bottom(self):
        if self._element:
            logger.info("Scroll to Bottom page.")
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            self.pause(3)
        else:
            logger.error("Unable to Scroll to Bottom page WebElement is None.")
        return self

    def to_top(self):
        if self._element:
            logger.info("Scroll to bottom page.")
            self._driver.execute_script("window.scrollTo(0, document.body.scrollTop)")
            self.pause(3)
        else:
            logger.error("Unable to Scroll to Top page WebElement is None.")
        return self

    def to_center(self):
        if self._element:
            logger.info("Scroll to center page.")

            view_port_height = "var viewPortHeight = Math.max(document.documentElement.clientHeight, " \
                               "window.innerHeight || 0); "
            element_top = "var elementTop = arguments[0].getBoundingClientRect().top;"
            js_function = "window.scrollBy(0, elementTop-(viewPortHeight/2));"

            scroll_into_middle = view_port_height + element_top + js_function

            self._driver.execute_script(scroll_into_middle, self._element)
        else:
            logger.error("Unable to Execute Scroll To Center WebElement is None.")

        return self

    def to_element(self):
        if self._element:
            logger.info("Scroll to Element page.")
            # Scroll to Element
            self._driver.execute_script("arguments[0].scrollIntoView(true);", self._element)
            # Get Location
            location = self._element.location_once_scrolled_into_view
            logger.info("Scroll to Element -> Location["+location+"]")

            self._element.send_keys(Keys.ARROW_UP)
            self._element.send_keys(Keys.ARROW_UP)

        else:
            logger.error("Unable to Execute Scroll To Element WebElement is None.")
        return self
