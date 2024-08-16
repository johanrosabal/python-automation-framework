from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element
from PIL import Image, ImageDraw, ImageFont
import time
import io
import os

logger = setup_logger('Screenshot')


class Screenshot:

    def __init__(self, driver):
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._locator = None
        self._page = None
        self._root = BaseApp.get_project_root()
        self._comment = None
        self._highlighted_area = None  # Store coordinates of the highlighted area
        self._highlighted_screenshot_path = None  # Path to the highlighted screenshot

    def set_locator(self, locator: tuple, page='Page'):
        self._locator = locator
        self._page = page
        self._element = Element.wait_for_element(self._driver, locator)
        logger.info(Element.log_console(page, self._name, locator))
        return self

    def save_screenshot(self):
        description = self._locator[2]
        file_path = self._root + "\\screenshots\\"

        # Create directory if it does not exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        file_name = f"{self._page}_{self._name}_{description.replace(' ', '_')}.png"
        full_path = os.path.join(file_path, file_name)

        if self._driver:
            time.sleep(1)
            logger.info("[Screenshot]:[Path]: " + file_path + file_name)
            self._driver.save_screenshot(full_path)
            return full_path
        else:
            logger.error("Unable to take Screenshot, WebElement is None.")
        return self

    def save_highlight(self, padding=10):
        screenshot_path = self.save_screenshot()
        if screenshot_path and self._element:
            image = Image.open(screenshot_path)
            draw = ImageDraw.Draw(image)

            location = self._element.location
            size = self._element.size
            left = location['x'] - padding
            top = location['y'] - padding
            right = location['x'] + size['width'] + padding
            bottom = location['y'] + size['height'] + padding

            # Store coordinates of the highlighted area
            self._highlighted_area = (left, top, right, bottom)
            self._highlighted_screenshot_path = screenshot_path

            draw.rectangle(self._highlighted_area, outline="red", width=3)
            image.save(screenshot_path)

            logger.info(f"Highlighted element saved at {screenshot_path}")

        return self

    def add_comment(self, comment="Default Comment"):
        padding = 5
        font_size = 20

        if self._highlighted_screenshot_path and self._highlighted_area:
            screenshot_path = self._highlighted_screenshot_path
            image = Image.open(screenshot_path)
            draw = ImageDraw.Draw(image)

            # Use a TrueType font with specified size
            try:
                font = ImageFont.truetype("arial.ttf",
                                          font_size)  # Ensure arial.ttf is available or provide a valid path
            except IOError:
                font = ImageFont.load_default()
                logger.warning("Custom font not found, using default font.")

            left, top, right, bottom = self._highlighted_area

            # Position the comment outside the highlighted rectangle
            comment_x = right + 15
            comment_y = top - 30 if top - 30 > 30 else bottom + 15

            # Calculate text size using textbbox
            bbox = draw.textbbox((comment_x, comment_y), comment, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Add padding around the text
            box_left = comment_x - padding
            box_top = comment_y
            box_right = comment_x + text_width + padding
            box_bottom = comment_y + text_height + padding + padding

            # Draw the rectangle around the text
            draw.rectangle([box_left, box_top, box_right, box_bottom], outline="red", width=2)

            # Draw the line from the top center of the highlighted area to the comment
            line_start = ((left + right) // 2, top)
            line_end = (comment_x, comment_y)
            draw.line([line_start, line_end], fill="red", width=2)

            # Draw the comment text in red
            draw.text((comment_x, comment_y), comment, fill="red", font=font)
            image.save(screenshot_path)

            logger.info(f"Added comment '{comment}' to screenshot saved at {screenshot_path}")

        return self
