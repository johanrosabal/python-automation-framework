from datetime import datetime, timedelta

class DateUtils:

    @staticmethod
    def validate_date_time_format(date_time):
        try:
            datetime.strptime(date_time, "%m/%d/%Y %H:%M")
            return True
        except (ValueError, OverflowError):
            return False

    @staticmethod
    def generate_date(date_format: str, days_to_add: float) -> str:
        current_date = datetime.now()
        new_date = current_date + timedelta(days=days_to_add)
        return new_date.strftime(date_format)