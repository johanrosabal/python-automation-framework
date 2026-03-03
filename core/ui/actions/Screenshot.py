from allure_commons._allure import step
from selenium.webdriver.support.wait import WebDriverWait

from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.actions.Element import Element
from PIL import Image, ImageDraw, ImageFont
from core.utils import random_utils
import time
import allure
import os
import base64


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

    def save_screenshot(self, description, page="", force_scroll_top=True, capture_full_page=True):
        """
        Captures and saves a screenshot using Chrome DevTools Protocol.

        Args:
            description (str): Description for the screenshot filename.
            page (str): Page identifier for the filename.
            force_scroll_top (bool): If True, scrolls to top before capture.
                                     If False, preserves current scroll position.
            capture_full_page (bool): If True, captures entire page height.
                                      If False, captures only current viewport.
        """
        self._page = page
        file_path = os.path.join(self._root, "screenshots")
        os.makedirs(file_path, exist_ok=True)
        file_name = f"{self._page}_{description.replace(' ', '_')}.png"
        full_path = os.path.join(file_path, file_name)

        driver = self._driver
        if not driver:
            logger.error("Driver is None. Cannot take screenshot.")
            return self

        try:
            # 1. Wait for page to be fully loaded
            wait = WebDriverWait(driver, 10)
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            time.sleep(0.5)

            # 2. Save current scroll position BEFORE any manipulation
            current_scroll = driver.execute_script("""
                return {
                    scrollX: window.scrollX || window.pageXOffset,
                    scrollY: window.scrollY || window.pageYOffset,
                    docHeight: document.documentElement.scrollHeight,
                    viewportHeight: window.innerHeight
                };
            """)
            logger.info(f"Current scroll position: X={current_scroll['scrollX']}, Y={current_scroll['scrollY']}")

            # 3. Get real page metrics
            metrics = driver.execute_cdp_cmd('Page.getLayoutMetrics', {})
            width = metrics['contentSize']['width']
            height = metrics['contentSize']['height']

            # 4. Configure virtual viewport for full-page capture
            if capture_full_page:
                driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
                    'width': int(width),
                    'height': int(height),
                    'deviceScaleFactor': 1,
                    'mobile': False,
                    'screenOrientation': {'angle': 0, 'type': 'portraitPrimary'}
                })

            # 5. Handle scroll behavior
            if force_scroll_top:
                # Scroll to top for consistent full-page capture
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(0.3)  # Allow scroll to complete
                logger.info("Scrolled to top for screenshot")
            else:
                # Restore scroll position in case CDP commands altered it
                driver.execute_script(
                    f"window.scrollTo({current_scroll['scrollX']}, {current_scroll['scrollY']});"
                )
                time.sleep(0.3)
                logger.info(f"Preserved scroll position: Y={current_scroll['scrollY']}")

            # 6. Capture screenshot
            screenshot = driver.execute_cdp_cmd('Page.captureScreenshot', {
                'format': 'png',
                'fromSurface': True,
                'captureBeyondViewport': capture_full_page  # Only capture beyond viewport if full page requested
            })

            # 7. Restore original scroll position AFTER capture (important for test continuity)
            if not force_scroll_top:
                driver.execute_script(
                    f"window.scrollTo({current_scroll['scrollX']}, {current_scroll['scrollY']});"
                )

            # 8. Save the file
            with open(full_path, 'wb') as f:
                f.write(base64.b64decode(screenshot['data']))
            logger.info(f"Screenshot saved: {full_path}")

            # 9. Clear device metrics override
            driver.execute_cdp_cmd('Emulation.clearDeviceMetricsOverride', {})

            return full_path

        except Exception as e:
            logger.error(f"CDP screenshot failed: {e}. Falling back to traditional method.")
            return self._fallback_screenshot(full_path)

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

    def attach_to_allure(self, name="screenshot", page="", remove_screenshot_file=False, usePrefix=False, force_scroll_top=True, capture_full_page=True):
        file_name = name

        if usePrefix:
            file_name = random_utils.generate_random_code("screen") + name

        screenshot_path = self.save_screenshot(description=name, page=page, force_scroll_top=force_scroll_top, capture_full_page=capture_full_page)

        logger.info(f"[Allure] Trying to attach screenshot: {screenshot_path}")

        if screenshot_path and os.path.exists(screenshot_path):
            try:
                with step(f"Origin Destination: {file_name}"):
                    allure.attach.file(
                        screenshot_path,
                        name=file_name,
                        attachment_type=allure.attachment_type.PNG
                    )
                logger.info(f"✅ Screenshot attached to Allure: {screenshot_path}")
                if remove_screenshot_file:
                    os.remove(screenshot_path)
            except Exception as e:
                logger.error(f"❌ Error attaching to Allure: {e}")
        else:
            logger.error(f"❌ Screenshot does not exist or is None: {screenshot_path}")
        return self

    def pause(self, seconds: int):
        """Pauses execution for a specified number of seconds."""
        BaseApp.pause(seconds)
        return self

    def _fallback_screenshot(self, full_path):
        """Backup method if CDP is unavailable (e.g., Firefox)."""
        try:
            # Scroll to bottom to ensure all content is rendered
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self._driver.execute_script("window.scrollTo(0, 0);")

            # Get total size
            total_width = self._driver.execute_script("return document.body.scrollWidth")
            total_height = self._driver.execute_script("return document.body.scrollHeight")

            # Adjust window (better with a margin)
            self._driver.set_window_size(
                max(total_width, 1024),
                max(total_height, 768)
            )
            time.sleep(1)  # Allow time for rendering

            self._driver.save_screenshot(full_path)
            return full_path
        except Exception as e:
            logger.error(f"[Screenshot][attach_to_allure]The backup screenshot failed: {e}")
            return self
