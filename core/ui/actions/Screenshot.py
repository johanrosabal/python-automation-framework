from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element
from PIL import Image, ImageDraw, ImageFont
import time
import allure
import os

from core.utils import random

# Logger setup for Screenshot actions
logger = setup_logger('Screenshot')


class Screenshot:
    """
    Screenshot class handles taking, saving, highlighting, and annotating screenshots.

    Attributes:
        _driver (WebDriver): The WebDriver instance used for browser interaction.
        _locator (tuple): Locator to find the element to be highlighted.
        _page (str): Name of the page, for logging purposes.
        _root (str): Project root directory for saving screenshots.
        _comment (str): Comment to add alongside the highlighted area.
        _highlighted_area (tuple): Coordinates of the highlighted element.
        _highlighted_screenshot_path (str): Path to the saved highlighted screenshot.
    """

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._locator = None
        self._page = None
        self._root = BaseApp.get_project_root()
        self._comment = None
        self._highlighted_area = None
        self._highlighted_screenshot_path = None

    def set_locator(self, locator: tuple, page='Page', explicit_wait=10):
        """
        Set the locator for the element, wait for it to become available, and log the result.

        Args:
            locator (tuple): Tuple with the locating strategy and value (e.g., By. ID, 'element_id').
            page (str): Name of the page to help with logging.
            explicit_wait (int): Time to wait for element visibility (default is 10 seconds).
        """
        self._locator = locator
        self._page = page
        # Wait for the element using Element class method, with specified timeout
        self._element = Element.wait_for_element(driver=self._driver, locator=locator, timeout=explicit_wait)
        # Log the action with page and element details
        logger.info(Element.log_console(self._page, self._name, locator))
        return self

    def set_element(self, element):
        self._element = element
        return self

    def save_screenshot(self, description, page='Page'):
        """Captures and saves a screenshot with a descriptive file name."""
        self._page = page
        file_path = os.path.join(self._root, "screenshots")
        os.makedirs(file_path, exist_ok=True)

        file_name = f"{self._page}_{description.replace(' ', '_')}.png"
        full_path = os.path.join(file_path, file_name)

        if self._driver:
            time.sleep(1)
            self._driver.save_screenshot(full_path)
            return full_path
        else:
            logger.error("Unable to take screenshot: WebElement is None.")
        return self

    def save_highlight(self, description, padding=10):
        """Highlights the target element by drawing a rectangle around it in the screenshot."""
        screenshot_path = self.save_screenshot(description)
        if screenshot_path and self._element:
            image = Image.open(screenshot_path)
            draw = ImageDraw.Draw(image)

            location = self._element.location
            size = self._element.size
            left = location['x'] - padding
            top = location['y'] - padding
            right = location['x'] + size['width'] + padding
            bottom = location['y'] + size['height'] + padding

            self._highlighted_area = (left, top, right, bottom)
            self._highlighted_screenshot_path = screenshot_path

            draw.rectangle(self._highlighted_area, outline="red", width=3)
            image.save(screenshot_path)
            logger.info(f"Highlighted element saved at {screenshot_path}")

        return self

    def add_comment(self, comment="Default Comment"):
        """Adds a comment with a red outline box and an arrow to the highlighted element."""
        padding = 5
        font_size = 20

        if self._highlighted_screenshot_path and self._highlighted_area:
            screenshot_path = self._highlighted_screenshot_path
            image = Image.open(screenshot_path)
            draw = ImageDraw.Draw(image)

            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()
                logger.warning("Custom font not found, using default font.")

            left, top, right, bottom = self._highlighted_area

            comment_x = right + 15
            comment_y = top - 30 if top - 30 > 30 else bottom + 15
            bbox = draw.textbbox((comment_x, comment_y), comment, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            box_left = comment_x - padding
            box_top = comment_y
            box_right = comment_x + text_width + padding
            box_bottom = comment_y + text_height + padding + padding

            draw.rectangle([box_left, box_top, box_right, box_bottom], outline="red", width=2)

            line_start = ((left + right) // 2, top)
            line_end = (comment_x, comment_y)
            draw.line([line_start, line_end], fill="red", width=2)

            draw.text((comment_x, comment_y), comment, fill="red", font=font)
            image.save(screenshot_path)

            logger.info(f"Added comment '{comment}' to screenshot saved at {screenshot_path}")

        return self

    def attach_to_allure(self, name="screenshot", page="page"):
        """Attaches the screenshot to the Allure report, optionally deleting the file afterward."""
        random_prefix = random.generate_random_code("screen_")
        screenshot_path = self.save_screenshot(description=name, page=page)
        if screenshot_path and name != "":
            allure.attach.file(
                screenshot_path,
                name=random_prefix+name,
                attachment_type=allure.attachment_type.PNG
            )
            logger.info(f"Screenshot attached to Allure report: {screenshot_path}")
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)
        else:
            logger.error("Failed to attach screenshot to Allure report.")
        return self

    def pause(self, seconds: int):
        """Pauses execution for a specified number of seconds."""
        BaseApp.pause(seconds)
        return self
