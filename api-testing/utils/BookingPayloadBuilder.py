from datetime import datetime


class BookingPayloadBuilder:
    def __init__(self):
        current_date = datetime.now().date()
        formatted_date = current_date.strftime("%Y-%m-%d")
        self.payload = {
            "date": formatted_date,
            "destination": "MAD",
            "origin": "DUB",
            "userId": 999,
        }

    def with_wrong_format_date(self):
        self.payload["date"] = "2023-18-01"
        return self

    def with_date(self, date):
        self.payload["date"] = date
        return self

    def with_user_id(self, user_id):
        self.payload["userId"] = user_id
        return self

    def with_destination(self, destination):
        self.payload["destination"] = destination
        return self

    def with_origin(self, origin):
        self.payload["origin"] = origin
        return self

    def build(self):
        return self.payload
