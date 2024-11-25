from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from core.config.logger_config import setup_logger
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from core.ui.actions.Element import Element
from core.ui.actions.ElementHighlighter import ElementHighlighter
from core.ui.common.BaseApp import BaseApp

logger = setup_logger('Table')


class Table:
    def __init__(self, driver: WebDriver):
        """
        Initialize the TableHelper with the WebDriver instance and the locator for the table.
        """
        self._name = self.__class__.__name__
        self._driver = driver
        self._element = None
        self._locator = None
        self._page = None
        self._table_headers = None
        self._old_table = None

    def set_locator(self, locator: tuple, page='Page', explicit_wait=10):
        """
        Set the locator for the element, wait for it to become available, and log the result.

        Args:
            locator (tuple): Tuple with the locating strategy and value (e.g., By.ID, 'element_id').
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

    def get_element(self):
        return self._element

    def pause(self, seconds: int):
        """
        Pause the execution for a specified number of seconds.

        Args:
            seconds (int): Duration of the pause.
        """
        BaseApp.pause(seconds)
        return self

    def get_table_headers(self, old_table=False):
        """
        Get the headers of the table and return a dictionary mapping header names to their column indices.
        """
        self._old_table = old_table
        if old_table:
            xpath = ".//thead//div[contains(@class,'ui-jqgrid-sortable')]/span/span[1]"
        else:
            xpath = ".//thead//th"

        headers = self._element.find_elements(By.XPATH, xpath)  # Adjust based on your table structure

        header_map = {}
        for idx, header in enumerate(headers):
            try:
                ElementHighlighter(self._driver).set_element(header).highlight_temporarily(0)
                # Scroll Cell
                self._driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'nearest', inline: 'center'});",
                    header
                )
                # Wait For Text
                WebDriverWait(self._driver, 1, poll_frequency=0.5).until(
                    lambda driver: header.text.strip()
                )
                header_text = header.text.strip()
            except TimeoutException as e:
                # logger.warning(f"Header {idx + 1}: no se pudo capturar el texto. Error: {e}")
                header_text = ""

            if header_text:  # Agregar solo si tiene texto visible
                #logger.info(f"Header {idx + 1}: '{header_text}'")
                header_map[header_text] = idx + 1  # Guardar en el diccionario

        if not header_map:
            logger.warning("No headers were processed. Returning an empty dictionary.")
        else:
            logger.info(f"Processed Headers: {header_map}")

        return header_map

    def get_table_headers_without_index(self):
        """
        Get the headers of the table and return a list of header names, excluding empty headers.
        """
        if self._old_table:
            xpath = ".//thead//div[contains(@class,'ui-jqgrid-sortable')]/span/span[1]"
        else:
            xpath = ".//thead//th"
        headers = self._element.find_elements(By.XPATH, xpath)  # Adjust based on your table structure
        return [header.text.strip() for header in headers if header.text.strip()]

    def get_row_count(self):
        """
        Get the number of rows in the table.
        """
        rows = self._element.find_elements(By.XPATH, 'tbody/tr')
        return len(rows)

    def get_row_data_by_header(self, row_index: int, header_name: str, headers=None, old_table=False):
        """
        Get the data from a specific row and column by header name.
        """
        if headers:
            header_map = headers
        else:
            header_map = self.get_table_headers()

        if header_name not in header_map:
            raise ValueError(f"Header '{header_name}' not found in table.")

        # Search Index Value From Headers Map
        column_index = header_map[header_name]

        # Special Condition over old table design, we need to add 2 on Index Value,
        # because it has hide Cells After the first 4 <TD>s
        if old_table:
            column_index = column_index+2
            logger.info(f"OLD:{old_table}")

        cell = self._element.find_element(By.XPATH, f".//tbody/tr[{row_index}]/td[{column_index}]")
        ElementHighlighter(self._driver).set_element(cell).highlight_temporarily(0)
        # Scroll Cell
        self._driver.execute_script(
            "arguments[0].scrollIntoView({block: 'nearest', inline: 'center'});",
            cell
        )
        return cell.text.strip()

    def get_row_data_by_index(self, row_index: int, column_index: int):
        """
        Get the data from a specific row and column by column index.
        """
        table_element = self._element
        cell = table_element.find_element(By.XPATH, f".//tbody/tr[{row_index}]/td[{column_index}]")
        ElementHighlighter(self._driver).set_element(cell).highlight_temporarily(0)
        return cell.text.strip()

    def get_all_data(self):
        """
        Get all table data as a list of dictionaries, where keys are header names and values are cell data.
        """
        header_map = self.get_table_headers()
        rows = self._element.find_elements(By.XPATH, ".//tbody/tr")
        table_data = []

        for row in rows:
            row_data = {}
            for header, col_index in header_map.items():
                cell = row.find_element(By.XPATH, f"./td[{col_index}]")
                row_data[header] = cell.text.strip()
            table_data.append(row_data)

        return table_data

    def check_all_rows(self):
        """
        Get all table data as a list of cell data.
        """
        checkbox = self._element.find_element(By.XPATH, "/thead/tr/th[2]//input[@type='checkbox']")
        if checkbox and checkbox.is_displayed():
            checkbox.click()

    def check_rows(self, index: int = 1, column: int = 2):
        """
        Get all table data as a list of cell data.
        """
        xpath = f"tbody/tr[{str(index)}]/td[{str(column)}]/input[@type='checkbox']"
        checkbox = self._element.find_element(By.XPATH, xpath)
        if checkbox and checkbox.is_displayed():
            ElementHighlighter(self._driver).set_element(checkbox).highlight_temporarily(0)
            checkbox.click()

    def get_table_element(self, index: int = 1, column: int = 2, explicit_wait = 10):
        """
        Get Table Specific Web Element with Index Row and Column
        """
        root = self._locator[1]
        xpath = f"{root}/tbody/tr[{str(index)}]/td[{str(column)}]"
        locator = (By.XPATH, xpath, f"Table Web Element: Row {index}, Column {column},")

        return Element.wait_for_element(driver=self._driver, locator=locator, timeout=explicit_wait)
