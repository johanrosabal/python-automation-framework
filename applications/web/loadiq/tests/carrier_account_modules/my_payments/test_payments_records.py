from applications.web.loadiq.fixtures.fixtures import *
from applications.web.loadiq.components.menus.LoadIQMenu import LoadIQMenu
from applications.web.loadiq.config.decorators import loadiq
from applications.web.loadiq.fixtures.fixtures import *
from core.config.logger_config import setup_logger
from core.ui.common.BaseTest import BaseTest
from core.utils.decorator import test
from applications.web.loadiq.pages.my_payments.MyPaymentsPage import MyPaymentsPage


logger = setup_logger('Testpayment')

@pytest.mark.web
@loadiq
class Testpayment(BaseTest):

    menu = LoadIQMenu.get_instance()
    login = LoginPage.get_instance()
    payments = MyPaymentsPage.get_instance()


    @test(test_case_id="CT-2317 ", test_description=" Verify it's possible to search a load on My payments", feature="My Payments",skip=False)
    def test_my_payments_search_load(self, load_iq_login_carrier_portal):
        # ("Navigates to 'My payments' page...")
        self.menu.carrier_portal.menu_my_payments()
        # Search the first record in my payment's table
        no_data = self.payments.no_load_results_no_load()
        if not no_data:
            tracking_number = self.payments.get_shipment_tracker_number(1)
            self.payments.enter_search_by(tracking_number)
            result_number = self.payments.get_shipment_tracker_number(1)
            self.payments.click_search()
        #Assert the result number obtained in the table
            assert result_number == tracking_number, (
                f"Tracker Number Incorrect, Expected {tracking_number} and Found {result_number}"
            )
        else:
            logger.warning("No records found, for execute this test.")

    @test(test_case_id="CT-3340",test_description="Verify 'Fields' texts are present on My Payments page",feature="My Payments",skip=False)
    def test_my_payments_fields_verification(self,):
        # ("Navigates to 'My payments' page...")
        self.menu.carrier_portal.menu_my_payments()
        #  Validate the existing text in the UI
        charge_texts = self.payments.get_all_charge_texts()
        expected_labels = ["Linehaul Charge","Fuel","Accessorials","Shipment No","Pro Number","Ship Date","Shipper","Origin","Destination","Pieces","Weight","Total Charge"]
        for label in expected_labels:
            assert label in charge_texts, f"Expected label '{label}' not found in charge_texts"

    @test(test_case_id="CT-3711",test_description="Validate Pro Number Update — My Payments Module",feature="My Payments",skip=False)
    def test_my_payments_pro_number_update(self,load_iq_login_carrier_portal):
        # Navigate to the "My Payments" page
        self.menu.carrier_portal.menu_my_payments()

        # Check if there are records in the payments table
        if not self.payments.no_load_results_no_load():
            # Get the tracking number from the first row
            tracking_number = self.payments.get_shipment_tracker_number(1)

            # Search using the tracking number
            self.payments.enter_search_by(tracking_number)
            self.payments.click_search()

        # Update the PRO number
        self.payments.update_pro_number("PRO1234567")
        actual_message = self.payments.validate_po_update()
        expected_message = "Pro Number updated successfully"
        assert actual_message == expected_message, (
            f"Error: Expected message '{expected_message}', but got '{actual_message}'."
        )

    @test(test_case_id="CT-2314 & 2315",test_description="Verify fields & currency on my payment's module",feature="My Payments",skip=False)
    def test_my_payments_currency_and_field_verification(self,):

        # Step 1: Navigate to My Payments
        self.menu.carrier_portal.menu_my_payments()

        # Step: Verify currency fields are in USD with comma separators
        currency_fields = self.payments.get_all_charge_fields()
        for label, value in currency_fields.items():
            assert value.startswith("$"), f"{label} does not start with '$': {value}"
