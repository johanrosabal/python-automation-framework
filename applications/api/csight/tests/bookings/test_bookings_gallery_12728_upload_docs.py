import json
import pytest

from core.config.logger_config import setup_logger
from core.utils import helpers
from core.utils.decorator import test
from core.utils.helpers import parse_dynamic_dates_values
from applications.api.csight.common.CsightBaseTest import CsightBaseTest, user
from applications.api.csight.config.decorators import csight
from applications.api.csight.endpoints.bookings.bookings_endpoint import BookingsEndpoint
from applications.web.csight.pages.login.LoginPage import LoginPage
from applications.web.csight.pages.bookings.BookingDetailsPage import BookingDetailsPage
from applications.web.csight.pages.search_menu.SearchMenu import SearchMenu
from applications.web.csight.pages.home.HomePage import HomePage
from core.data.sources.JSON_reader import JSONReader

logger = setup_logger('BaseTest')


@pytest.fixture(scope="session")
def shared_data():
    return {}


@pytest.mark.api
@csight
class TestBookingsGallery12728(CsightBaseTest):

    bookings = BookingsEndpoint.get_instance()
    test_path = "applications\\api\\csight\\tests\\bookings"

    login = LoginPage.get_instance()
    home = HomePage.get_instance()
    search_menu = SearchMenu.get_instance()
    bookings_details = BookingDetailsPage.get_instance()

    @test(test_case_id="CT-3178", test_description="[12805][Precondition] Create a Booking Container with 'New' Status and Changed to 'Active'", skip=False)
    def test_create_a_booking_container_new_status_changed_to_active(self, shared_data, user):
        # BASE REQUEST FOR BOOKING CREATION - PRE CONDITION
        path = "../../data/bookings/CT-3178_booking_container_port_to_port_new_to_active.json"
        data = JSONReader.import_json(path)
        data = parse_dynamic_dates_values(data)

        # Get Response Booking Creation
        response = self.bookings.create_booking(json=data)
        # Convert to Dict
        new_booking = json.loads(response.text)
        # Share Cat Number
        shared_data["carrierBookingRequestReference"] = new_booking["carrierBookingRequestReference"]
        # Wait Until Booking is active
        response_status = self.bookings.wait_for_status_change_with_carrier_booking_request(
            carrier_booking_request_reference=shared_data["carrierBookingRequestReference"],
            expected_status="Active",
            timeout=230
        )

        dict_status = JSONReader.text_to_dict(response_status.text)
        shared_data["crowleyBookingReferenceNumber"] = dict_status["crowleyBookingReferenceNumber"]
        logger.info("Precondition: Execute Once Before the First Test")

    @test(test_case_id="CT-3191", test_description="[12728] User can not upload a document if booking number does not exist", skip=False)
    def test_user_can_not_upload_a_document_booking_not_exist(self, shared_data):
        # https://crowley.atlassian.net/browse/CT-3191

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3192_user_can_upload_a_docx_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = "CAT999999"

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-3191_user_can_not_upload_a_document_booking_not_exist"
        )

        self.add_report(
            test_data="CT-3191 | User can not upload a Docx Document if booking not exist",
            status_code=400,
            response=response
        )

        confirmation = json.loads(response.text)

        assert (confirmation["OrderDataResponse"]["Result"] == "Fail", "Docx document was should not be uploaded")
        assert (confirmation["OrderDataResponse"]["ErrorCode"] == "400", "Error Code Should be 400")
        assert (confirmation["OrderDataResponse"]["ErrorMessage"] == "Booking CAT999999 not Available in CSIGHT", "Error Message not Match")

    @test(test_case_id="CT-3192", test_description="[12728] User can upload a Docx Document", skip=False)
    def test_user_can_upload_a_docx_document(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3192

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3192_user_can_upload_a_docx_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        # Login C-Sight
        self.login.load_page()
        self.login.login_user(user=user)

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-3192_user_can_upload_a_docx_document"
        )

        self.add_report(
            test_data="CT-3192 | User can upload a Docx Document",
            status_code=200,
            response=response
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Success", "Docx document was not uploaded")

        # UI Verification
        self.search_menu.search_booking(shared_data["crowleyBookingReferenceNumber"])
        # Get Status String From UI
        c_sight_status = self.bookings_details.get_booking_status()
        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3178_booking_container_active")
        # assert (c_sight_status == "Active"), "Booking Status Incorrect"

        self.bookings_details.click_tab_documents()
        self.bookings_details.screenshot().pause(3).save_screenshot(description="CT-3178_booking_documents_tab")
        csight_document_name = self.bookings_details.tab_content_documents_details.get_document_name(index=1)
        csight_document_type = self.bookings_details.tab_content_documents_details.get_document_type(index=1)
        csight_uploaded_by = self.bookings_details.tab_content_documents_details.get_uploaded_downloaded_by(index=1)

        assert (csight_document_name == attachment["OrderData"]["Document"]['DocumentName']+".docx"), "Document Name Incorrect"
        assert (csight_document_type == attachment["OrderData"]["Document"]['DocumentType']), "Document Type Incorrect"
        assert (csight_uploaded_by == "Integration Admin"),"Uploaded/Downloaded BY Incorrect"

    @test(test_case_id="CT-3193", test_description="[12728] User can upload a Doc Document", skip=False)
    def test_user_can_upload_a_doc_document(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3193

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3193_user_can_upload_a_doc_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-3193_user_can_upload_a_doc_document"
        )

        self.add_report(
            test_data="CT-3193 | User can upload a doc document",
            status_code=200,
            response=response
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Success", "Docx document was not uploaded")

    @test(test_case_id="CT-3194", test_description="[12728] User can upload a xls Document", skip=True)
    def test_user_can_upload_a_xls_document(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3194

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3194_user_can_upload_a_xls_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-3194_user_can_upload_a_xls_document"
        )

        self.add_report(
            test_data="CT-3194 | User can upload a xls document",
            status_code=200,
            response=response
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Success", "xls document was not uploaded")

    @test(test_case_id="CT-3195", test_description="[12728] User can upload a xlsx Document", skip=True)
    def test_user_can_upload_a_xlsx_document(self, shared_data, user):
        # https://crowley.atlassian.net/browse/CT-3195
        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3195_user_can_upload_a_xlsx_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-3195_user_can_upload_a_xlsx_document"
        )

        self.add_report(
            test_data="CT-3195 | User can upload a xlsx document",
            status_code=200,
            response=response
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Success", "xlsx document was not uploaded")

    @test(test_case_id="CT-3196", test_description="[12728] User can upload a PDF Document", skip=True)
    def test_user_can_upload_a_pdf_document(self, shared_data,user):
        # https://crowley.atlassian.net/browse/CT-3196
        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3196_user_can_upload_a_pdf_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-3196_user_can_upload_a_pdf_document"
        )

        self.add_report(
            test_data="CT-3196 | User can upload a PDF document",
            status_code=200,
            response=response
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Success", "pdf document was not uploaded")

    @test(test_case_id="CT-3197", test_description="[12728] User can upload a TXT Document", skip=True)
    def test_user_can_upload_a_txt_document(self, shared_data):
        # https://crowley.atlassian.net/browse/CT-3197

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-3197_user_can_upload_a_txt_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-3197_user_can_upload_a_txt_document"
        )

        self.add_report(
            test_data="CT-3197 | User can upload a TXT document",
            status_code=400,
            response=response,
            errors=""
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Fail", "TXT document was should not uploaded")

    @test(test_case_id="CT-4501", test_description="[12728] User can upload a Special Characters Document", skip=True)
    def test_user_can_upload_a_special_characters_document(self, shared_data):
        # https://crowley.atlassian.net/browse/CT-4501

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-4501_user_can_upload_a_special_characters_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-4501_user_can_upload_a_special_characters_document"
        )

        self.add_report(
            test_data="CT-4501 | User can upload a Special Characters document",
            status_code=200,
            response=response,
            errors=""
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Success", "doc document was not uploaded")

    @test(test_case_id="CT-4503", test_description="[12728] User can upload a Hazardous Document", skip=True)
    def test_user_can_upload_a_hazardous_document(self, shared_data):
        # https://crowley.atlassian.net/browse/CT-4503

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-4503_user_can_upload_a_hazardous_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-4503_user_can_upload_a_hazardous_document"
        )

        self.add_report(
            test_data="CT-4503 | User can upload a Hazardous document",
            status_code=200,
            response=response,
            errors=""
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Success", "pdf document was not uploaded")

    @test(test_case_id="CT-4504", test_description="[12728] User can upload a password protected Document", skip=True)
    def test_user_can_upload_a_password_protected_document(self, shared_data):
        # https://crowley.atlassian.net/browse/CT-4504
        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-4504_user_can_upload_a_password_protected_document.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-4504_user_can_upload_a_password_protected"
        )

        self.add_report(
            test_data="CT-4504 | User can upload a Password Protected",
            status_code=200,
            response=response,
            errors=""
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Success", "pdf document was not uploaded")

    @test(test_case_id="CT-4505", test_description="[12728] User can upload a File Document Type not in the list (Others)", skip=True)
    def test_user_can_upload_file_document_type_not_in_the_list_others(self, shared_data):
        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-4505_user_can_upload_document_type_not_on_list.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-4505_user_can_not_upload_file_with_document_type_not_in_the_list"
        )

        self.add_report(
            test_data="CT-4505 | User can upload a Password Protected",
            status_code=200,
            response=response,
            errors=""
        )

        # Checking this scenario, Other Type of Document will be automatically assign to "OTHERS"
        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Success", "pdf document was not uploaded")

    @test(test_case_id="CT-4506", test_description="[12728] User can not upload a Exe File", skip=True)
    def test_user_can_not_upload_exe_file(self, shared_data):
        # https://crowley.atlassian.net/browse/CT-4506

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        path = "../../data/bookings/CT-4506_user_can_not_upload_a_exe_file.json"
        attachment = JSONReader.import_json(path)
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["crowleyBookingReferenceNumber"]

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-4506_user_can_not_upload_a_exe_file"
        )

        self.add_report(
            test_data="CT-4506 | User can not upload a EXE File",
            status_code=400,
            response=response,
            errors=""
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Fail", "Document result should be Fail")

    @test(test_case_id="CT-4507", test_description="[12979] User cannot upload with Southbound BOL Complete", skip=True)
    def test_user_cannot_upload_with_southbound_bol_complete(self, shared_data):
        # https://crowley.atlassian.net/browse/CT-4507

        # PRE-CONDITON A BOL BOOKING
        # CAT194705 BOL COMPLETE

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        # This is a booking with SouthBound
        path = "../../data/bookings/CT-3196_user_can_upload_a_pdf_document.json"
        attachment = JSONReader.import_json(path)
        # attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["CAT_NUMBER"]
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = "CAT194705"  # BOL COMPLETE

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-4507_user_can_upload_southbound_bol_complete"
        )

        self.add_report(
            test_data="CT-4507 | User can not upload with southbound BOL Complete",
            status_code=400,
            response=response,
            errors=""
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Fail", "Document result should be Fail")
        assert (confirmation["OrderDataResponse"]["ErrorMessage"] == "Document cannot be uploaded at this time, please reach out to ‘documentation@crowley.com’ for assistance.", "Document should not be uploaded on southbound BOL Complete")

        # If the related BoL status of the booking is in ‘Bill Complete’ or ‘Export Bill Released’ and the booking
        # is southbound, then MuleSoft will not upload the document to the booking. Instead, a synchronous error message will be sent to the customer as
        # “Document cannot be uploaded at this time, please reach out to ‘documentation@crowley.com’ for assistance”.

    @test(test_case_id="CT-4508", test_description="[12979] User cannot upload with Southbound BOL Export Bill Released", skip=True)
    def test_user_can_not_upload_document_in_status_bol_complete_southbound_bol_export_bill_released(self, shared_data):
        # https://crowley.atlassian.net/browse/CT-4508

        # CAT194907 BOL EXPORT BILL RELEASED
        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        # This is a booking with SouthBound
        path = "../../data/bookings/CT-3196_user_can_upload_a_pdf_document.json"
        attachment = JSONReader.import_json(path)
        # attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["CAT_NUMBER"]
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = "CAT194907"  # BOL EXPORT BILL RELEASED

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-4508_user_can_upload_southbound_export_bill_release"
        )

        self.add_report(
            test_data="CT-4508 | User can not upload with southbound BOL Export Bill Release",
            status_code=400,
            response=response,
            errors=""
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Fail", "Document result should be Fail")
        assert (confirmation["OrderDataResponse"]["ErrorMessage"] == "Document cannot be uploaded at this time, please reach out to ‘documentation@crowley.com’ for assistance.", "Document should not be uploaded on southbound bol export release")

        # If the related BoL status of the booking is in ‘Bill Complete’ or ‘Export Bill Released’ and the booking
        # is southbound, then MuleSoft will not upload the document to the booking. Instead, a synchronous error message will be sent to the customer as
        # “Document cannot be uploaded at this time, please reach out to ‘documentation@crowley.com’ for assistance”.

    @test(test_case_id="CT-4509", test_description="[12979] User can not upload with Northbound BOL Complete", skip=True)
    def test_user_can_not_upload_document_in_status_bol_complete_northbound_bol_complete(self, shared_data):
        # https://crowley.atlassian.net/browse/CT-4509

        # CAT008570 BOL COMPLETE
        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        # This is a booking with NorthBound
        path = "../../data/bookings/CT-3196_user_can_upload_a_pdf_document.json"
        attachment = JSONReader.import_json(path)
        # attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["CAT_NUMBER"]
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = "CAT008570"  # BOL COMPLETE

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-4509user_can_upload_northbound_bol_complete"
        )

        self.add_report(
            test_data="CT-4509 | User can not upload with northbound BOL Complete",
            status_code=400,
            response=response,
            errors=""
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Fail", "Document result should be Fail")
        assert (confirmation["OrderDataResponse"]["ErrorMessage"] == "'Document cannot be uploaded at this time, please reach out to ‘PF_BLRevisionSB@crowley.com’ for assistance.", "Document should not be uploaded on northbound BOL Complete")

        # If the related BoL status of the booking is in ‘Bill Complete’ or ‘Export Bill Released’ and the booking
        # is southbound, then MuleSoft will not upload the document to the booking. Instead, a synchronous error message will be sent to the customer as
        # “Document cannot be uploaded at this time, please reach out to ‘documentation@crowley.com’ for assistance”.

    @test(test_case_id="CT-4510", test_description="[12979] User can not upload with Northbound BOL Export Bill Released", skip=True)
    def test_user_can_not_upload_document_in_status_bol_complete_northbound_bol_export_bill_released(self, shared_data):
        # https://crowley.atlassian.net/browse/CT-4510

        # 01. Create New Booking Status
        # --------------------------------------------------------------------------------------------------------------
        # This is a booking with NorthBound
        path = "../../data/bookings/CT-3196_user_can_upload_a_pdf_document.json"
        attachment = JSONReader.import_json(path)
        # attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = shared_data["CAT_NUMBER"]
        attachment["OrderData"]["ReferenceNums"][0]['RefNumValue'] = "CAT007940"  # NorthBound

        response = self.bookings.upload_document_to_booking(json=attachment)

        helpers.save_request_and_response(
            base_path=self.test_path,
            response=response,
            filename_prefix="CT-4510_user_can_upload_northbound_bol_export_bill_release"
        )

        self.add_report(
            test_data="CT-4510 | User can upload a TXT document",
            status_code=400,
            response=response,
            errors=""
        )

        confirmation = json.loads(response.text)
        assert (confirmation["OrderDataResponse"]["Result"] == "Fail", "Document result should be Fail")
        assert (confirmation["OrderDataResponse"]["ErrorMessage"] == "'Document cannot be uploaded at this time, please reach out to ‘PF_BLRevisionSB@crowley.com’ for assistance.", "Document should not be uploaded on northbound bol export release")

        # For north-bound related bookings error message should be sent as "Document cannot be uploaded at this time, please reach out to PF_BLRevisionSB@crowley.com" for assistance.
