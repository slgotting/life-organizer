from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from app import sql_db as db

class IPAddress(db.Model):
    __tablename__ = 'ip_address'

    id = Column(Integer, primary_key=True)
    ip_address = Column(String)
    quote_request_count = Column(Integer)
    addresses_requested = Column(String)
    ip_route = Column(String)

    def append_address_requested(self, address):
        if self.addresses_requested:
            self.addresses_requested += f',{address}'
        else:
            self.addresses_requested = [address]

    def get_addresses_requested(self):
        if self.addresses_requested:
            return self.addresses_requested.split(',')
        return []

    def set_ip_route(self, ip_route):
        self.ip_route = ','.join(ip_route)  # Serialize the list to a string

    def get_ip_route(self):
        if self.ip_route:
            return self.ip_route.split(',')  # Deserialize the string to a list
        return []
