from app.V1.dao import File

class PaymentContract(object):
    def get_name(self,data):
        pass

    def get_card_type(self,data):
        pass

    def get_card_number(self,data):
        pass

    def get_card_cvc(self,data):
        pass

    def get_expiration_date(self,data):
        pass

    def get_billing_address(self,data):
        pass

    def process_payment(self,data):
        pass

class DaoPayment(PaymentContract):
    def __init__(self,DaoObj):
        self.Dao = DaoObj

    def process_payment(self):
        return self.Dao.process_payment()
        
