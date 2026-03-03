import time
from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger
from core.data.sources.JSON_reader import JSONReader
from core.utils.helpers import print_json

logger = setup_logger('BookingsEndpoint')


class BookingsEndpoint(BaseApi):

    def __init__(self):
        super().__init__()
        # Name
        self._name = self.__class__.__name__
        self._endpoint = "v1/bookingRequests"
        self._endpoint_status = "v1/bookingRequests/status/"
        self._endpoint_confirm = "v1/bookingRequests/confirm/"
        self._endpoint_reserved = "v1/reserveBookingNumber"
        self._endpoint_upload = "v1/documents"
        self._endpoint_cancel = "v1/bookingRequests?"
        self._endpoint_update = "v1/bookingRequests?"

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    #
    def create_booking(self, json=None):
        logger.info(f"[{self._name}]: Create a Posts")

        request = self.post_request() \
            .set_endpoint(self._endpoint) \
            .add_header("client_id", self.get_client_id()) \
            .add_header("client_secret", self.get_client_secret()) \
            .add_header("Content-Type", "application/json") \
            .set_verify(False) \
            .set_json(json) \
            .set_timeout(10) \
            .send()

        return request

    def upload_document_to_booking(self, json=None):
        logger.info(f"[{self._name}]: Create a Posts")
        request = self.post_request() \
            .set_endpoint(self._endpoint_upload) \
            .add_header("Authorization", "Basic OGFmNWI1YTYxMDJjNDRhNmJmYzRlN2I5NDVjYWYzNjk6ODRhQTEyMjNmN0E0NEFGNjhENmQ3Y0U0NTdFNzg4MGU=") \
            .add_header("Content-Type", "application/json") \
            .set_verify(False) \
            .set_json(json) \
            .set_timeout(15) \
            .send()

        return request

    def cancel_booking_with_cat_number(self, crowleyBookingNumber: str, carrierBookingRequestReference: str, shipperCvif: str):
        logger.info(f"[{self._name}]: Delete Booking with CAT NUMBER:{crowleyBookingNumber}")
        request = self.delete_request() \
            .set_endpoint(f"{self._endpoint_cancel}crowleyBookingNumber={crowleyBookingNumber}&carrierBookingRequestReference={carrierBookingRequestReference}&shipperCvif={shipperCvif}") \
            .add_header("client_id", self.get_client_id()) \
            .add_header("client_secret", self.get_client_secret()) \
            .add_header("Content-Type", "application/json") \
            .set_verify(False) \
            .set_timeout(15) \
            .send()

        return request

    def update_booking_with_cat_number(self, crowleyBookingNumber: str, carrierBookingRequestReference: str, shipperCvif: str, json=None):
        logger.info(f"[{self._name}]: Update Booking with CAT NUMBER:{crowleyBookingNumber}")
        request = self.put_request() \
            .set_endpoint(f"{self._endpoint_update}crowleyBookingNumber={crowleyBookingNumber}&carrierBookingRequestReference={carrierBookingRequestReference}&shipperCvif={shipperCvif}") \
            .add_header("client_id", self.get_client_id()) \
            .add_header("client_secret", self.get_client_secret()) \
            .add_header("Content-Type", "application/json") \
            .set_verify(False) \
            .set_json(json) \
            .set_timeout(10) \
            .send()

        return request

    def get_booking_status_with_carrier_request_reference(self, carrier_booking_request_reference: str):
        logger.info(f"[{self._name}]: Get Status Booking with CARRIER REFERENCE NUMBER:{carrier_booking_request_reference}")
        request = self.get_request() \
            .set_endpoint(f"{self._endpoint_status}{carrier_booking_request_reference}") \
            .add_header("client_id", self.get_client_id()) \
            .add_header("client_secret", self.get_client_secret()) \
            .add_header("Content-Type", "application/json") \
            .set_verify(False) \
            .set_timeout(30) \
            .set_allow_redirects(False) \
            .send()
        return request

    def get_booking_status_confirm_with_cat_number(self, cat_number: str):
        logger.info(
            f"[{self._name}]: Get Status Booking with Cat Number:{cat_number}")
        request = self.get_request() \
            .set_endpoint(f"{self._endpoint_confirm}{cat_number}") \
            .add_header("client_id", self.get_client_id()) \
            .add_header("client_secret", self.get_client_secret()) \
            .add_header("Content-Type", "application/json") \
            .set_verify(False) \
            .set_allow_redirects(False) \
            .set_timeout(10) \
            .send()
        return request

    def wait_for_status_change_with_carrier_booking_request(self,
                                                            carrier_booking_request_reference: str,
                                                            expected_status="Active",
                                                            timeout=180,
                                                            interval=10,
                                                            expected_pending_reason_codes: list[str] = None):
        """
        Wait until the booking status changes to the expected one or the maximum time is reached.
        Optionally, validate the presence of specific codes in pendingDetails if status is 'Pending'.

        :param carrier_booking_request_reference: Reference number of the booking.
        :param expected_status: Expected status (default 'Active').
        :param timeout: Maximum wait time in seconds.
        :param interval: Interval between retries in seconds.
        :param expected_pending_reason_codes: Optional. List of expected codes in 'pendingDetails' if status is 'Pending'.
        :return: The last response obtained and the time it took to reach the expected status.
        """
        self.pause(15)
        start_time = time.time()

        while time.time() - start_time < timeout:
            response = self.get_booking_status_with_carrier_request_reference(
                carrier_booking_request_reference=carrier_booking_request_reference
            )

            response_text = JSONReader.text_to_dict(response.text)
            print_json("Request Response", response_text)

            current_status = response_text.get("status")
            elapsed = time.time() - start_time
            logger.info(f"⏳ Current State: {current_status} | Elapsed: {elapsed:.2f}s / {timeout}s")
            logger.info(f"Endpoint Status: {response.url}")

            if current_status == "Pending":
                pending_details = response_text.get("pendingDetails", [])

                # Validar que haya al menos una razón pendiente
                if not pending_details:
                    logger.info("⚠️ Pending state detected but no pendingDetails found.")
                    time.sleep(interval)
                    continue

                # Validar códigos específicos si se proporcionan
                if expected_pending_reason_codes is not None:
                    found_codes = {item.get("Code") for item in pending_details if "Code" in item}
                    if not all(code in found_codes for code in expected_pending_reason_codes):
                        logger.info(
                            f"⚠️ Pending codes mismatch. Expected: {expected_pending_reason_codes}, Found: {found_codes}")
                        time.sleep(interval)
                        continue

                logger.info(f"✅ Pending state validated with at least one pendingDetail.")
                response.elapsed_status_change = elapsed
                return response

            if current_status == expected_status:
                logger.info(f"✅ State Reached: {expected_status} in {elapsed:.2f} seconds")
                response.elapsed_status_change = elapsed
                return response

            time.sleep(interval)

        raise TimeoutError(f"❌ The status '{expected_status}' was not reached within {timeout} seconds.")

    def wait_for_status_change_with_cat_number(self, cat_number: str, expected_status="Active", timeout=180, interval=10):
        """
        Wait until the booking status changes to the expected one or the maximum time is reached.
        :param cat_number: Reference number of the booking.
        :param expected_status: Expected status (default 'active').
        :param timeout: Maximum wait time in seconds.
        :param interval: Interval between retries in seconds.
        :return: The last response obtained and the time it took to reach the expected status.
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            response = self.get_booking_status_confirm_with_cat_number(cat_number=cat_number)
            response_text = JSONReader.text_to_dict(response.text)

            print_json("Request Response", response_text)
            current_status = response_text.get("status")

            elapsed = time.time() - start_time
            logger.info(f"⏳ Current State: {current_status} | Elapsed: {elapsed:.2f}s / {timeout}s")
            logger.info(f"Endpoint Status: {response.url}")
            if current_status == expected_status:
                logger.info(f"✅ State Reached: {expected_status} in {elapsed:.2f} seconds")
                response.elapsed_status_change = elapsed  # opcional: agregar atributo al response
                return response

            time.sleep(interval)

        raise TimeoutError(f"❌ The status '{expected_status}' was not reached within {timeout} seconds.")

    def get_reserved_booking_number(self, json=None):
        logger.info(f"[{self._name}]: Reserved a Booking Number")

        request = self.post_request() \
            .set_endpoint(self._endpoint_reserved) \
            .add_header("client_id", self.get_client_id()) \
            .add_header("client_secret", self.get_client_secret()) \
            .add_header("Content-Type", "application/json") \
            .set_verify(False) \
            .set_json(json) \
            .set_timeout(10) \
            .send()

        return request
