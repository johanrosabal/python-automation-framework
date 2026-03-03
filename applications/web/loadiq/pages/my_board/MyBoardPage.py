import time           
import allure
from selenium.webdriver.common.by import By
from core.config.logger_config import setup_logger
from core.ui.common.BaseApp import BaseApp
from core.ui.common.BasePage import BasePage
from core.utils.table_formatter import TableFormatter

logger = setup_logger('MyBoardPage')


class MyBoardPage(BasePage):

    def __init__(self, driver):
        """
        Initialize the MyBoardPage instance.
        """
        super().__init__(driver)
        # Driver
        self._driver = driver
        # Name
        self._name = self.__class__.__name__
        # Relative URL
        self.relative = "/shipment/my-board"
        # Locator definitions
        self._no_load = (By.XPATH, '//h5[contains(text(),"Sorry, we couldn\'t find any results.")]', "[Sorry, we couldn't find any results.]")
        self._list_container = "//div[contains(@class,'load-list')]//div[contains(@class, 'loadboard-card')]"
        self._input_search_by = (By.XPATH, "//input[@type='text' and contains(@mattooltip,'Search by')]", "Search by [Input Box]")
        self._button_search = (By.XPATH, "//button[@mattooltip='Search']", "Search [Button]")
        self._checkbox_include_close = (By.XPATH, "//input[@type='checkbox' and @id='switchViewClosedLoads']/..", "Include Close [Checkbox]")
        self._checkbox_include_expired = (By.XPATH, "//input[@type='checkbox' and @id='switchViewExpiredLoads']/..", "Include Close [Checkbox]")
        self._dropdown_sort_by = (By.XPATH, "//select[@name='sortingField']", "Sort By [Dropdown Options]")
        self._button_sort_asc_desc = (By.XPATH, "//label[contains(text(),'Sort By')]/..//span", "Sort Ascending/Descending [Button]")
        self._button_show_details = (By.XPATH, "//app-myboard//div[8]/span/span","Show details [Button]")
        self._checkbox_include_close_verification = (By.XPATH, "//input[@id='switchViewClosedLoads']", "Include Close [Checkbox]")
        self._checkbox_include_expired_verification = (By.XPATH, "//input[@id='switchViewExpiredLoads']", "Include Close [Checkbox]")

        self._extend_bid = (By.XPATH, "//*[@id='dropdownMenuButton']","Extend bid [Button]")
        self._extend_bid_time = (By.XPATH, "//app-load-details//a[1]","Extend bid time [Button]")
        self._extend_bid_time_confirmation = (By.XPATH, "//app-confirmation-dialog//button[2]/span","Extend bid time confirmation [Output]")
        self._extend_bid_avoid= (By.XPATH, "//app-confirmation-dialog//button[3]/span","Extend bid avoid [Button]")
        self._close_bid_confirmation = (By.XPATH, "//app-confirmation-dialog//button[2]/span","Close bid confirmation [Button]")
        self._close_bid_avoid = (By.XPATH, "//app-confirmation-dialog//button[3]/span","Close bid avoid [Button]")
        self._close_bid = (By.XPATH, "//load-address-header-with-action//button/span","Close bid [Button]")
        self._assign_carrier_button = (By.XPATH, "//app-load-details/div/div[1]//button/span[1]","Assign carrier [Button]")
        self._bid_status=(By.XPATH,"//book-load-header-details//div[9]/span","Bit Status [Button]")
        self._feedback_my_board = (By.XPATH, "//*[@id='mybutton']/button","Feedback [Button]")
        self._feedback_my_board_comment = (By.XPATH, "//div[@class='note-editable']", "Feedback Comment [Input]")
        self._feedback_my_board_submit = (By.XPATH, " //span[contains(text(), 'Submit')]","Feedback Submit [Button]")
        self._feedback_my_board_avoid_submit = (By.XPATH, " //span[contains(text(), 'Cancel')]","Feedback Submit avoid[Button]")
        self._assert_feedback = (By.XPATH, "//*[@id='cdk-overlay-4']/snack-bar-container/div/div/simple-snack-bar/span","Assert Feedback [Output]")
        self._upload_documents = (By.XPATH, "//*[@id='bolAttachments']/div[2]/div[1]/div/button","Upload File [Button]")
        
        self._lbl_load_no_found = (By.XPATH, "//app-myboard/div[3]//h5","Message [Output text]")
        self._lbl_extend_bid_time_confirmation  = (By.XPATH, "//span[@class='mat-simple-snack-bar-content' and contains(text(), 'Bidding on this shipment is extended by 30 minutes')]","Message [Output text]")
        self._lbl_closed_bid_time_confirmation  = (By.XPATH, "// span[ @class ='mat-simple-snack-bar-content' and contains(text(), 'Bid has been closed successfully.')]","Message [Output text]")
        self._lbl_feedback_confirmation = (By.XPATH,"//span[contains(text(), 'Feedback submitted successfully')]","Message [Output text]")
        self._lbl_document_upload_confirmation = (By.XPATH, "//span[contains(text(), 'Feedback submitted successfully')]", "Message [Output text]")
        
        #-------------------------------------------- COMPANY NAME SECTION ---------------------------------------------
        # Locators for the bids table and its content
        self._tbl_bids = (By.XPATH, "//book-load-customer-grid//table[@mat-table]", "Bids Table")

        # Locators for the first row in the bids table
        self._txt_first_row_company_name = (By.XPATH, "(//tbody/tr[@mat-row])[1]/td[contains(@class, 'mat-column-carrierName')]", "First Row Company Name [Text]")
        self._txt_first_row_bid_submitted = (By.XPATH, "(//tbody/tr[@mat-row])[1]/td[contains(@class, 'mat-column-dateModified')]", "First Row Bid Submitted [Text]")
        self._chk_first_row_expedite = (By.XPATH, "(//tbody/tr[@mat-row])[1]/td[contains(@class, 'mat-column-isExpedited')]/mat-checkbox", "First Row Expedite [Checkbox]")
        self._txt_first_row_rate = (By.XPATH, "(//tbody/tr[@mat-row])[1]/td[contains(@class, 'mat-column-bidAmount')]", "First Row Rate [Text]")
        self._txt_first_row_on_time = (By.XPATH, "(//tbody/tr[@mat-row])[1]/td[contains(@class, 'mat-column-onTime')]",  "First Row On Time % [Text]")
        self._txt_first_row_offer_ends = (By.XPATH, "(//tbody/tr[@mat-row])[1]/td[contains(@class, 'mat-column-offerEnds')]", "First Row Offer Ends [Text]")
        self._txt_first_row_auto_accept = (By.XPATH,"(//tbody/tr[@mat-row])[1]/td[contains(@class, 'mat-column-autoAcceptText')]", "First Row Auto Accept [Text]")
        self._btn_first_row_accept_offer = (By.XPATH, "(//tbody/tr[@mat-row])[1]/td[contains(@class, 'mat-column-action')]//button", "First Row Accept Offer [Button]")
        self._lbl_first_row_action = (By.XPATH,"(//tbody/tr[@mat-row])[1]/td[contains(@class, 'mat-column-action')]/label", "First Row Action [Label]")
        self._txt_first_row_bid_type = (By.XPATH, "(//tbody/tr[@mat-row])[1]/td[contains(@class, 'mat-column-isBookNowBid')]", "First Row Bid Type [Text]")

        # Locators for pagination controls
        self._select_rows_per_page = (By.XPATH, "//mat-paginator//mat-select", "Rows per page [Select]")
        self._txt_pagination_range = (By.XPATH, "//div[@class='mat-paginator-range-label']", "Pagination Range [Text]")

        # MODAL ACCEPT OFFER
        # Modal container
        self._modal_accept_offer = (By.XPATH, "//div[@class='modal-content'][.//h4[text()='Accept Offer']]","Accept Offer [Modal]")
        self._txt_modal_title = (By.XPATH, "//h4[text()='Accept Offer']", "Accept Offer Title [Text]")
        self._txt_confirmation_message = (By.XPATH, "//span[contains(text(),'Are you sure you want to accept this offer?')]", "Confirmation Message [Text]")
        self._btn_close_modal = (By.XPATH, "//button[@data-cy='closebtn']", "Close Modal [Button]")
        self._ico_question_mark = (By.XPATH, "//div[@class='modal-body']//span[contains(@class, 'load-icon')]", "Question Mark [Icon]")
        self._lbl_company_name = (By.XPATH, "//li/span[text()='Company Name']", "Company Name [Label]")
        self._txt_company_name_value = (By.XPATH, "//li/span[text()='Company Name']/following-sibling::span", "Company Name Value [Text]")
        self._lbl_rate = (By.XPATH, "//li/span[text()='Rate']", "Rate [Label]")
        self._txt_rate_value = (By.XPATH, "//li/span[text()='Rate']/following-sibling::span", "Rate Value [Text]")
        self._btn_yes = (By.XPATH, "//button[.//span[text()='Yes']]", "Yes [Button]")
        self._btn_no = (By.XPATH, "//button[.//span[text()='NO']]", "NO [Button]")

        #UPLOAD MODAL

        #The upload modal is identified (modal screen)
        self._upload_modal=(By.XPATH, "//upload-documents")
        #Clicks choose file button(Normally this button is not displayed) and add data
        self._input_add_file = (By.XPATH, "//div[contains(@class,'uploaddoc p-0')]//input[@type='file']", "Add file [Input]")
        self._input_description_modal = (By.XPATH, "//div[4]/ul/li/div/div[3]/input","Description [Input]")
        #Update button is visible
        self._button_upload_file_modal = (By.XPATH, "//span[text()='Upload File']","Upload File [Button]")
        #Operations functionalities after record creation
        self._button_delete_file=(By.XPATH,"//app-upload-bol//table//tr//td[8]", "Delete file [Button]")
        self._button_view_file = (By.XPATH, "//app-upload-bol//table//tr//td[6]/a", "View file [Button]")
        self._button_download_file = (By.XPATH, "//app-upload-bol//table//tr//td[7]","Download file [Button]")
        self._button_delete_record_yes = (By.XPATH, "//app-confirmation-dialog//div[3]/button[2]/span","Delete Record > Yes [Button]")
        self._button_cancel_record_no = (By.XPATH, "//app-confirmation-dialog//div[3]/button[3]/span","Cancel Record > No [Button]")
        self._button_cancel = (By.XPATH, "//upload-documents//form//div[2]/div/button[2]/span","Cancel [Button]")
        self._msg_closed_record_confirmation = (By.XPATH, "//span[text()='Bid has been closed successfully.']","Message [Output text]")


    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = MyBoardPage(BaseApp.get_driver())
            cls._name = __class__.__name__
        return cls._instance

    def load_page(self):
        base_url = BaseApp.get_base_url()
        logger.info("LOAD PAGE: " + base_url + self.relative)
        self.navigation().go(base_url, self.relative)
        return self

    def no_load_results(self):
        try:
            element = self.element().wait(self._no_load, 5)
            return element is not None
        except Exception as e:
            logger.error(f"{e.msg}")
            return False

    def _enter_search_by(self, text: str):
        self.send_keys().set_locator(self._input_search_by, self._name).set_text(text)
        return self

    def _click_search(self):
        self.click().set_locator(self._button_search, self._name).single_click().pause(1)
        return self

    def click_include_closed(self):
        self.click().set_locator(self._checkbox_include_close, self._name).single_click().pause(1)
        return self

    def click_include_expired(self):
        self.click().set_locator(self._checkbox_include_expired, self._name).single_click().pause(1)
        return self

    def search_by(self, text: str):
        self._enter_search_by(text)
        self._click_search()
        return self

    def get_shipment_tracker_number(self, index: int):
        xpath = f"({self._list_container}//span[contains(@class,'load-number-text')])[{str(index)}]"
        locator = (By.XPATH, xpath, "Shipment Number [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def _get_status(self, index: int):
        xpath = f"({self._list_container}//span[contains(@class,'badge')])[{str(index)}]"
        locator = (By.XPATH, xpath, "Status [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_origin_address_title_track(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//span[contains(@class,'address-details')]/span)[1]"
        locator = (By.XPATH, xpath, "Origin Address Title [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_origin_address_date_time_track(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//span[contains(@class,'datetime-value')])[1]"
        locator = (By.XPATH, xpath, "Origin Address Date Time[Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_address_origin_tooltip(self, index: int):
        xpath_title = f"(({self._list_container})[{str(index)}]//span[contains(@class,'address-details m-origin')])[1]"
        locator_title = (By.XPATH, xpath_title, f"Origin Address Title [{index}] [Text]")

        xpath_type = f"(({self._list_container})[{str(index)}]//span[contains(@class,'address-details m-origin')]/div/div/span)[1]"
        locator_type = (By.XPATH, xpath_type, f"Origin Address Details Type [{index}] [Text]")

        xpath_line_1 = f"(({self._list_container})[{str(index)}]//span[contains(@class,'address-details m-origin')]/div/div/span)[2]"
        locator_l1 = (By.XPATH, xpath_line_1, f"Origin Address Details Line 1 [{index}] [Text]")

        xpath_line_2 = f"(({self._list_container})[{str(index)}]//span[contains(@class,'address-details m-origin')]/div/div/span)[3]"
        locator_l2 = (By.XPATH, xpath_line_2, f"Origin Address Details Line 2 [{index}] [Text]")

        xpath_line_3 = f"(({self._list_container})[{str(index)}]//span[contains(@class,'address-details m-origin')]/div/div/span)[4]"
        locator_l3 = (By.XPATH, xpath_line_3, f"Origin Address Details Line 3 [{index}] [Text]")

        self.click().set_locator(locator_title, self._name).mouse_over().pause(1)

        details = {
            "type": self.get_text().set_locator(locator_type, self._name).by_text(),
            "line_1": self.get_text().set_locator(locator_l1, self._name).by_text(),
            "line_2": self.get_text().set_locator(locator_l2, self._name).by_text(),
            "line_3": self.get_text().set_locator(locator_l3, self._name).by_text(),
        }

        return details

    def _get_destination_address_title_track(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//span[contains(@class,'address-details')]/span)[2]"
        locator = (By.XPATH, xpath, f"Destination Address [{index}] [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_destination_address_date_time_track(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//span[contains(@class,'datetime-value')])[2]"
        locator = (By.XPATH, xpath, f"Destination Address Date Time [{index}] [Text]")
        return self.get_text().set_locator(locator, self._name).by_text()

    def _get_address_destination_tooltip(self, index: int):
        xpath_title = f"(({self._list_container})[{str(index)}]//span[contains(@class,'m-dest address-details')])[1]"
        locator_title = (By.XPATH, xpath_title, f"Destination Address Title [{index}] [Text]")

        xpath_type = f"(({self._list_container})[{str(index)}]//span[contains(@class,'m-dest address-details')]/div/div/span)[1]"
        locator_type = (By.XPATH, xpath_type, f"Destination Address Details Type [{index}] [Text]")

        xpath_line_1 = f"(({self._list_container})[{str(index)}]//span[contains(@class,'m-dest address-details')]/div/div/span)[2]"
        locator_l1 = (By.XPATH, xpath_line_1, f"Destination Address Details Line 1 [{index}] [Text]")

        xpath_line_2 = f"(({self._list_container})[{str(index)}]//span[contains(@class,'m-dest address-details')]/div/div/span)[3]"
        locator_l2 = (By.XPATH, xpath_line_2, f"Destination Address Details Line 2 [{index}] [Text]")

        xpath_line_3 = f"(({self._list_container})[{str(index)}]//span[contains(@class,'m-dest address-details')]/div/div/span)[4]"
        locator_l3 = (By.XPATH, xpath_line_3, f"Destination Address Details Line 3 [{index}] [Text]")

        self.click().set_locator(locator_title, self._name).mouse_over().pause(1)

        details = {
            "type": self.get_text().set_locator(locator_type, self._name).by_text(),
            "line_1": self.get_text().set_locator(locator_l1, self._name).by_text(),
            "line_2": self.get_text().set_locator(locator_l2, self._name).by_text(),
            "line_3": self.get_text().set_locator(locator_l3, self._name).by_text(),
        }

        return details

    def _get_requested_equipment(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//label[contains(text(),'Requested Equipment')]//../span)"
        locator = (By.XPATH, xpath, f"Request Equipment [{index}]  [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def _get_weight(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//label[contains(text(),'Weight')]//../span)"
        locator = (By.XPATH, xpath, f"Weight [{index}] [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def _get_miles(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//label[contains(text(),'Miles')]//../span)"
        locator = (By.XPATH, xpath, "Miles [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def _get_lowest_bid(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//label[contains(text(),'Lowest Bid')]//../span)"
        locator = (By.XPATH, xpath, f"Lowest Bid [{index}]  [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def _get_no_of_bids(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//label[contains(text(),'No. of Bids')]//../span)"
        locator = (By.XPATH, xpath, f"No. of Bids [{index}]  [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def _get_time_remaining_hours(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//ul[@class='time-remaining'])[2]//li[1]"
        locator = (By.XPATH, xpath, f"Time Remaining [{index}] : Hours [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def _get_time_remaining_minutes(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//ul[@class='time-remaining'])[2]//li[2]"
        locator = (By.XPATH, xpath, f"Time Remaining [{index}] : Minutes [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def _get_time_remaining_seconds(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//ul[@class='time-remaining'])[2]//li[3]"
        locator = (By.XPATH, xpath, f"Time Remaining [{index}] : Seconds [Text]")
        return self.get_text().set_locator(locator, self._name).by_text().strip()

    def click_show_details(self, index: int):
        xpath = f"(({self._list_container})[{str(index)}]//span[contains(text(),'Show Details')])"
        locator = (By.XPATH, xpath, f"Show Details [{index}] [Button]")
        return self.click().set_locator(locator, self._name).single_click().pause()

    @allure.step("Get Message")
    def validate_load_not_found(self):
        return self.get_text().set_locator(self._lbl_load_no_found, self._name).by_text()

    def get_shipment_item(self, index: int):

        data = []

        tooltip1 = self._get_address_origin_tooltip(index)
        tooltip1 = ", ".join(str(v) if v is not None else "-" for v in tooltip1.values()) or "-"

        tooltip2 = self._get_address_destination_tooltip(index)
        tooltip2 = ", ".join(str(v) if v is not None else "-" for v in tooltip2.values()) or "-"

        shipment_number = self.get_shipment_tracker_number(index) or "-"
        status = self._get_status(index) or "-"

        address_origin = self._get_origin_address_title_track(index) or "-"
        address_origin_tooltip = tooltip1 or "-"
        address_origin_date_time = self._get_origin_address_date_time_track(index) or "-"

        address_destination = self._get_destination_address_title_track(index) or "-"
        address_destination_tooltip = tooltip2 or "-"
        address_destination_date_time = self._get_destination_address_date_time_track(index) or "-"

        requested_equipment = self._get_requested_equipment(index) or "-"
        weight = self._get_weight(index) or "-"
        miles = self._get_miles(index) or "-"
        lowest_bid = self._get_lowest_bid(index) or "-"
        no_of_bids = self._get_no_of_bids(index) or "-"

        time_remaining_hours = self._get_time_remaining_hours(index) or "-"
        time_remaining_minutes = self._get_time_remaining_minutes(index) or "-"
        time_remaining_seconds = self._get_time_remaining_seconds(index) or "-"

        headers = [
            "Shipment Number",
            "Status",

            "Address Origin",
            "Address Origin Tooltip",
            "Address Origin Pickup Date/Time",

            "Address Destination",
            "Address Destination Tooltip",
            "Address Destination Delivery Date/Time",

            "Requested Equipment",
            "Weight",
            "Miles",
            "Lowest Bid",
            "No of Bids",

            "Time Remaining HH",
            "Time Remaining MM",
            "Time Remaining SS",
        ]

        data.append([
            shipment_number,
            status,

            address_origin,
            address_origin_tooltip,
            address_origin_date_time,

            address_destination,
            address_destination_tooltip,
            address_destination_date_time,

            requested_equipment,
            weight,
            miles,
            lowest_bid,
            no_of_bids,

            time_remaining_hours,
            time_remaining_minutes,
            time_remaining_seconds
        ])

        TableFormatter().set_headers(headers).set_data(data).to_grid()
        return data[0]

    def select_sort_by(self, option):
        self.dropdown().set_locator(self._dropdown_sort_by, self._name).by_text_contains(option)
        return self

    def click_asc_desc_order(self):
        self.click().set_locator(self._button_sort_asc_desc, self._name).single_click()
        return self

    def click_show_details_my_board(self):
        self.click().set_locator(self._button_show_details, self._name).single_click().pause(3)
        return self

    def extend_bid_time(self):
        self.click().set_locator(self._extend_bid, self._name).single_click().pause()
        self.click().set_locator(self._extend_bid_time, self._name).single_click().pause()
        self.click().set_locator(self._extend_bid_time_confirmation, self._name).single_click().pause()
        return self

    def extend_bid_time_avoid(self):
        self.click().set_locator(self._extend_bid, self._name).single_click().pause()
        self.click().set_locator(self._extend_bid_time, self._name).single_click().pause()
        self.click().set_locator(self._extend_bid_avoid, self._name).single_click().pause()
        return self

    def close_bid(self):
        self.click().set_locator(self._close_bid, self._name).single_click().pause()
        self.click().set_locator(self._close_bid_avoid, self._name).single_click().pause()
        self.click().set_locator(self._close_bid, self._name).single_click().pause()
        self.click().set_locator(self._close_bid_confirmation, self._name).single_click().pause()
        return self

    def send_feedback(self, text):
        self.click().set_locator(self._feedback_my_board, self._name).single_click().pause()
        self.click().set_locator(self._feedback_my_board_avoid_submit, self._name).single_click().pause()
        self.click().set_locator(self._feedback_my_board, self._name).single_click().pause()
        self.send_keys().set_locator(self._feedback_my_board_comment, self._name).clear().set_text(text)
        self.click().set_locator(self._feedback_my_board_submit, self._name).single_click().pause()
        return self

    def click_upload_documents(self):
        self.click().set_locator(self._upload_documents, self._name).single_click().pause()
        return self

    # ---------------------------------------- Methods for Company Name Section ----------------------------------------
    def get_first_row_company_name_text(self):
        return self.get_text().set_locator(self._txt_first_row_company_name, self._name).by_text()

    def get_first_row_bid_submitted_text(self):
        return self.get_text().set_locator(self._txt_first_row_bid_submitted, self._name).by_text()

    def get_first_row_rate_text(self):
        return self.get_text().set_locator(self._txt_first_row_rate, self._name).by_text()

    def get_first_row_on_time_text(self):
        return self.get_text().set_locator(self._txt_first_row_on_time, self._name).by_text()

    def get_first_row_offer_ends_text(self):
        return self.get_text().set_locator(self._txt_first_row_offer_ends, self._name).by_text()

    def get_first_row_auto_accept_text(self):
        return self.get_text().set_locator(self._txt_first_row_auto_accept, self._name).by_text()

    def get_first_row_bid_type_text(self):
        return self.get_text().set_locator(self._txt_first_row_bid_type, self._name).by_text()

    def get_pagination_range_text(self):
        return self.get_text().set_locator(self._txt_pagination_range, self._name).by_text()

    # --- Métodos de acción (Clicks) ---

    def click_first_row_accept_offer_button(self):
        self.click().set_locator(self._btn_first_row_accept_offer, self._name).single_click().pause(2)
        return self

    def get_action_text(self):
         text = self.get_text().set_locator(self._lbl_first_row_action, self._name).by_text()
         time.sleep(5)
         return text

    def click_add_file(self, file_name: str, description: str):

        # Wait For Modal Should be visible
        self.element().wait_for_element(self.driver, self._upload_modal)

        # Display Temporarily Input Chosen File
        self.element().set_css_property(self._input_add_file, "display: block;")

        # Send Path File
        # self.click().set_locator(self._button_add_file, self._name).single_click().pause(2) # Avoid to Click the "Add File" to not display the dialog box for search the file
        self.upload_file().set_locator(self._input_add_file, self._name).set_file_name(file_name).upload().pause(1)

        # Hidden Temporarily Input Chosen File
        self.element().set_css_property(self._input_add_file, "display: none;")

        # Add some Description to the upload File
        self.send_keys().set_locator(self._input_description_modal, self._name).clear().set_text(description)

        # Click to Upload Current File
        self.click().set_locator(self._button_upload_file_modal, self._name).single_click().pause()
    
    def get_modal_title(self):
        return self.get_text().set_locator(self._txt_modal_title, self._name).by_text()

    def is_filter_active(self, filter_name: str) -> bool:
        if filter_name == "Include Closed":
            locator = self._checkbox_include_close_verification
        elif filter_name == "Include Expired":
            locator = self._checkbox_include_expired_verification
        else:
            raise ValueError(f"Unknown filter name: {filter_name}")

        checkbox = self.driver.find_element(*locator[:2])  # Use only the By and XPath
        return checkbox.get_attribute("ng-reflect-model") == "true"

    def get_selected_sort_option(self) -> str:
        dropdown = self.driver.find_element(*self._dropdown_sort_by[:2])
        return dropdown.get_attribute("ng-reflect-model")

    @allure.step("Get Bidding Confirmation Message")
    def get_bidding_confirmation_message(self):
        return self.get_text().set_locator(self._lbl_extend_bid_time_confirmation, self._name).by_text()

    @allure.step("Get Closed Confirmation Message")
    def get_closed_confirmation_message(self):
        return self.get_text().set_locator(self._lbl_closed_bid_time_confirmation, self._name).by_text()

    @allure.step("Get Feedback Confirmation Message")
    def get_feedback_confirmation_message(self):
        return self.get_text().set_locator(self._lbl_feedback_confirmation, self._name).by_text()

    @allure.step("Check if Assign Load button is enabled")
    def is_assign_load_button_enabled(self):
        assign_button = self.driver.find_element(By.XPATH, "//button[contains(., 'Assign Load')]")
        is_disabled = assign_button.get_attribute("disabled")
        return is_disabled is None  # True if not disabled

    @allure.step("Get Document Upload Confirmation Message")
    def get_document_upload_confirmation_message(self):
        return self.get_text().set_locator(self._lbl_document_upload_confirmation, self._name).by_text()

    def get_modal_confirmation_message(self):
        return self.get_text().set_locator(self._txt_confirmation_message, self._name).by_text()
        
    def click_btn_close_modal(self):
        self.click().set_locator(self._btn_close_modal, self._name).single_click()
        return self

    def get_company_name_value(self):
        return self.get_text().set_locator(self._txt_company_name_value, self._name).by_text()
 
    def get_rate_value(self):
        return self.get_text().set_locator(self._txt_rate_value, self._name).by_text()

    def click_btn_yes_modal(self):
        self.click().set_locator(self._btn_yes, self._name).single_click().pause(2)
        return self

    def click_btn_no_modal(self):
        self.click().set_locator(self._btn_no, self._name).single_click()
        return self

    def get_closed_confirmation_message_confirmation_message(self):
        return self.get_text().set_locator(self._msg_closed_record_confirmation, self._name).by_text()