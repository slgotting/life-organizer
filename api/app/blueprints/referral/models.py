import mongoengine as me

class ReferringUser(me.Document):
    phone_number: me.StringField()
    referred_numbers: me.ListField()
    referred_completed: me.ListField()
    jobs_completed: me.DictField()
    credits: me.IntField()