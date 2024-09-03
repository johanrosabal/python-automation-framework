from core.api.common.BaseApi import BaseApi
from core.config.logger_config import setup_logger

logger = setup_logger('AuthorizationOauth2')


class Bookings(BaseApi):

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = Bookings()
            cls.name = __class__.__name__
            cls.endpoint = "services/data/v46.0/query/"
        return cls._instance

    def get_confirmation(self, token, booking_id):
        logger.info(f"[{self.name}]:Get Booking Confirmation")

        response = self.post_request() \
            .set_endpoint(f"{self.endpoint}?q=Select+Id+FROM+Booking__c+WHERE+Booking_Number__c+=+'{booking_id}'+AND+Available_for_Booking__c+=+False") \
            .add_header("Authorization", f"Bearer {token}") \
            .set_timeout(10) \
            .send()

        return response
