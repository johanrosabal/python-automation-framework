from applications.web.loadiq.fixtures.fixtures import *
from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.fixtures.fixtures import *
from applications.web.loadiq.pages.my_payments.MyPaymentsPage import MyPaymentsPage
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test


logger = setup_logger('Testpayment')

@pytest.mark.web
@loadiq
class Testpayment(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    payments = MyPaymentsPage.get_instance()

    @test(test_case_id="CT-2316", test_description="Verify export function on my payments (EXCEL)",feature="My Payments", skip=False)
    def test_my_payments_export_excel(self, load_iq_login_carrier_portal):
        # Navigate to 'My Payments' page
        self.menu.carrier_portal.menu_my_payments()
        # Select the correct format for the report
        self.payments.click_export_button()
        self.payments.select_format_excel()
        # Enter date range for the export
        self.payments.enter_export_range(
            fromdate="04/28/2025",
            currentdate="05/28/2025"
        )
        # Click export in the popup
        self.payments.click_popup_export()
        # Get the actual message displayed after export
        actual_message = self.payments.validate_download_excel_and_csv_text()
        # Expected phrase that should always be part of the message
        expected_phrase = "payments exported successfully"
        # Assert that the actual message contains the expected phrase
        assert expected_phrase in actual_message, (
            f"Error: Expected message to contain '{expected_phrase}', but got '{actual_message}'."
        )

    @test(test_case_id="CT-3252", test_description="Verify export function on my payments (CSV)",feature="My Payments", skip=False)
    def test_my_payments_export_csv(self,):
        # ("Navigates to 'My payments' page...")
        self.menu.carrier_portal.menu_my_payments()
        # Select the correct format of the report
        self.payments.click_export_button()
        self.payments.select_format_csv()
        # Sends dates info and get the correct report
        self.payments.enter_export_range(
            fromdate="04/28/2025",
            currentdate="05/28/2025"
        )
        self.payments.click_popup_export()
        # Get the actual message displayed after export
        actual_message = self.payments.validate_download_excel_and_csv_text()
        # Expected phrase that should always be part of the message
        expected_phrase = "payments exported successfully"
        # Assert that the actual message contains the expected phrase
        assert expected_phrase in actual_message, (
            f"Error: Expected message to contain '{expected_phrase}', but got '{actual_message}'."
        )

    @test(test_case_id="CT-3589", test_description="Carrier portal - Verify the feedback option (MyPayments)",feature="My Payments", skip=False)
    def test_my_payments_feedback_creation(self,):
        # ("Navigates to 'My payments' page...")
        self.menu.carrier_portal.menu_my_payments()
        # CLick the feedback button on my payments
        self.payments.click_feedback()
        #Click cancel button and reopen the feedback table .
        self.payments.click_feedback_cancel()
        self.payments.click_feedback()
        #Send data to the table and submit message
        self.payments.enter_comment("QA TEST - TESTING FEEDBACK")
        self.payments.click_feedback_submit()
        # Assert that the actual message contains the expected phrase
        actual_message = self.payments.validate_feedback_text()
        # Expected phrase that should always be part of the message
        expected_text = "Feedback submitted successfully"
        # Assert that the actual message contains the expected phrase
        assert expected_text in actual_message, (
            f"Error: Expected message to contain '{expected_text}', but got '{actual_message}'."
        )
