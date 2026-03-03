from core.config.logger_config import setup_logger
import json
from tabulate import tabulate

logger = setup_logger('CustomerAppliersAddressDto')


class ApiAccountSelectDto:

    mapping = {
        "agency": "agency",
        "company": "company",
        "depot_id": "depotId",
        "return_url": "returnUrl"
    }

    def __init__(self, agency, company, depotId, returnUrl):
        self.agency = agency
        self.company = company
        self.depot_id = depotId
        self.return_url = returnUrl

    def __repr__(self):
        return (f"ApiAccountSelectDto("
                f"agency={self.agency}"
                f"company={self.company}"
                f"depot_id={self.depot_id}"
                f"return_url={self.return_url}"
                f")")

    def to_dict(self):
        return {
            "agency": self.agency,
            "company": self.company,
            "depot_id": self.depot_id,
            "return_url": self.return_url
        }

    def to_json(self):
        return json.dumps({
            "agency": self.agency,
            "company": self.company,
            "depot_id": self.depot_id,
            "return_url": self.return_url
        })
