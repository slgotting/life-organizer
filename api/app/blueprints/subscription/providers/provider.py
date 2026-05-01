from abc import ABC, abstractmethod

CustomerID = str

class Provider(ABC):

    def __init__(self, customer_id, subscription_id) -> None:
        self.customer_id = customer_id
        self.subscription_id = subscription_id

    @staticmethod
    @abstractmethod
    def create_customer():
        ...

    @staticmethod
    @abstractmethod
    def get_or_create_customer(customer_id, email):
        ...

    @abstractmethod
    def get_customer(self, customer_id):
        ...

    @classmethod
    def get_or_create_customer(cls, customer_id, email) -> object:
        try:
            customer = cls.get_customer(customer_id)
        except:
            pass

        if not customer:
            customer = cls.create_customer(email)
        return customer

    @abstractmethod
    def get_plan(self):
        ...

    @abstractmethod
    def downgrade_plan(self):
        ...

    @abstractmethod
    def upgrade_plan(self):
        ...

    def update_subscription(self):
        ...

    @abstractmethod
    def get_update_subscription_url(self):
        ...