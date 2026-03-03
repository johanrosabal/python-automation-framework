import time
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

    def set_locator(self, locator: tuple, page='Page', explicit_wait=10):
        self._element = Element(self._driver).get_element(locator=locator, timeout=explicit_wait)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def set_element(self, element=None):
        self._element = element
        return self

    def pause(self, seconds: int):
        BaseApp.pause(seconds)
        return self

    def to_bottom(self):
        if self._driver:
            logger.info("Scroll to Bottom page.")
            # Scroll hacia abajo incrementalmente
            scroll_pause_time = 1  # Tiempo de pausa entre scrolls
            last_height = self._driver.execute_script("return document.body.scrollHeight")

            while True:
                # Realiza scroll hasta el fondo actual de la página
                self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Espera para que se cargue el contenido
                time.sleep(scroll_pause_time)

                # Calcula la nueva altura de la página
                new_height = self._driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    # Si no hay más contenido para cargar, sal del bucle
                    break
                last_height = new_height
        else:
            logger.error("Unable to Scroll to Bottom page WebElement is None.")
        return self

    def to_top(self):
        if self._driver:
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

    def to_element(self, pixels=0):
        if not self._element:
            logger.error("WebElement is None.")
            return self

        # 1. Use scrollIntoView with 'center' to avoid fixed headers
        self._driver.execute_script("""
            arguments[0].scrollIntoView({
                behavior: 'auto',
                block: 'center'
            });
        """, self._element)

        # 2. If you need an offset, use a positive value to go down, not a negative one.
        if pixels != 0:
            self._driver.execute_script(f"window.scrollBy(0, {pixels});")

        logger.info(f"Scrolled to element with offset {pixels}")
        return self
