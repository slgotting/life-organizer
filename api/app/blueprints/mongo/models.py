import mongoengine as me

class IPAddress(me.Document):
    meta = {'collection': 'ip_address'}
    ip_route = me.ListField()
    ip_address = me.StringField()
    quote_request_count = me.IntField()
    addresses_requested = me.ListField()
