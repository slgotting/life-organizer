import mongoengine as me

class Event(me.Document):
    event_id = me.StringField(required=True, unique=True)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    @classmethod
    def event_processed(cls, event_id):
        return True if cls.objects(event_id=event_id).first() else False

    @classmethod
    def delete_all(cls):
        cls.objects.delete()
        return True