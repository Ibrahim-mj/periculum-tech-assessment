from datetime import datetime


class OwnerInfo:
    def __init__(self, owner_name, owner_address, owner_telephone):
        self.owner_name = owner_name
        self.owner_address = owner_address
        self.owner_telephone = owner_telephone

    def to_dict(self):
        return {
            "owner_name": self.owner_name,
            "owner_address": self.owner_address,
            "owner_telephone": self.owner_telephone,
        }


class Inventory:
    def __init__(
        self, purchase_date, serial_number, description, source_style_area, value
    ):
        self.purchase_date = purchase_date
        self.serial_number = serial_number
        self.description = description
        self.source_style_area = source_style_area
        self.value = value

    def format_date(self):
        try:
            date_obj = datetime.strptime(self.purchase_date, "%d/%m/%Y")
            return date_obj.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return self.purchase_date

    def to_dict(self):
        return {
            "purchase_date": self.format_date(),
            "serial_number": self.serial_number,
            "description": self.description,
            "source_style_area": self.source_style_area,
            "value": self.value,
        }
