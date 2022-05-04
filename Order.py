import datetime
from email_validate import validate, validate_or_fail
import phonenumbers

class Order:
    def __init__(self, email:str = "", name:str = "", phone:int = 0, amount:int = 0, place:str = "", date_giving:int = 0, comment:str = ""):
       self.email = email
       self.name = name
       self.phone = phone
       self.amount = amount
       self.place = place
       self.date_giving = date_giving
       self.comment = comment

    def return_info(self, message_id):
        json_file = [message_id, self.email, self.name, self.phone, self.amount, self.place, self.date_giving, self.comment]
        return json_file
    
    def validate_email(self, email:str):
        return validate(
        email_address=email,
        check_format=True,
        check_blacklist=True,
        check_dns=True,
        dns_timeout=10,
        check_smtp=True,
        smtp_debug=False)

    def validate_phone(self, phone:str):
        try:
            phonenumbers.parse(phone, "RU")
            return True
        except phonenumbers.phonenumberutil.NumberParseException:
            return False
