from datetime import datetime
import mongoengine as me


class Section(me.EmbeddedDocument):
    id = me.StringField(required=True)
    name = me.StringField(required=True)
    day_configs = me.DictField(default=dict)


class Task(me.Document):
    meta = {'collection': 'organizer_tasks', 'strict': False}

    user_id = me.StringField(required=True)
    title = me.StringField(required=True)
    description = me.StringField(default='')
    section_id = me.StringField(default='')
    task_type = me.StringField(default='deep', choices=['deep', 'filler'])
    min_duration_min = me.IntField(default=60)
    max_duration_min = me.IntField(default=120)
    recurrence_min_days = me.IntField(default=1)
    recurrence_max_days = me.IntField(default=7)
    last_done = me.DateTimeField(default=None)
    snoozed_until = me.DateTimeField(default=None)
    is_active = me.BooleanField(default=True)
    is_one_off = me.BooleanField(default=False)
    pinned_dates = me.ListField(me.StringField(), default=list)
    priority = me.StringField(default='medium', choices=['high', 'medium', 'low'])
    overtime_eligible = me.BooleanField(default=False)
    created_at = me.DateTimeField(default=datetime.utcnow)
    schedule_type = me.StringField(default='recurring', choices=['recurring', 'deep_work', 'pulse'])
    scheduled_days = me.ListField(me.IntField(), default=list)
    daily_target_min = me.IntField(default=None)
    daily_target_manual = me.BooleanField(default=False)
    pulse_min_interval = me.IntField(default=None)
    pulse_max_interval = me.IntField(default=None)
    pulse_duration_min = me.IntField(default=5)
    pulse_deterministic = me.BooleanField(default=False)

    def urgency_at(self, reference_dt=None):
        ref = reference_dt or datetime.utcnow()
        if not self.last_done:
            return 'overdue'
        days_since = (ref - self.last_done).total_seconds() / 86400
        min_d = self.recurrence_min_days
        max_d = self.recurrence_max_days
        window = max(max_d - min_d, 1)
        if days_since >= max_d:
            return 'overdue'
        if days_since >= min_d + window * 2 / 3:
            return 'time_to_do'
        if days_since >= min_d + window * 1 / 3:
            return 'needs_doing'
        return 'upcoming'

    def urgency_deep_work(self, actual_min, days_elapsed_on_schedule):
        target = self.daily_target_min or 0
        expected = days_elapsed_on_schedule * target
        if expected <= 0:
            return 'upcoming'
        ratio = actual_min / expected
        if ratio < 0.5:
            return 'overdue'
        if ratio < 0.75:
            return 'time_to_do'
        if ratio < 1.0:
            return 'needs_doing'
        return 'upcoming'

    def to_dict(self):
        now = datetime.utcnow()
        days_since = None
        if self.last_done:
            days_since = round((now - self.last_done).total_seconds() / 86400, 1)
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'section_id': self.section_id,
            'task_type': self.task_type,
            'min_duration_min': self.min_duration_min,
            'max_duration_min': self.max_duration_min,
            'recurrence_min_days': self.recurrence_min_days,
            'recurrence_max_days': self.recurrence_max_days,
            'last_done': self.last_done.isoformat() if self.last_done else None,
            'snoozed_until': self.snoozed_until.strftime('%Y-%m-%d') if self.snoozed_until else None,
            'days_since': days_since,
            'urgency': self.urgency_at(now),
            'priority': self.priority,
            'is_active': self.is_active,
            'is_one_off': self.is_one_off,
            'pinned_dates': list(self.pinned_dates or []),
            'overtime_eligible': self.overtime_eligible,
            'created_at': self.created_at.isoformat(),
            'schedule_type': self.schedule_type or 'recurring',
            'scheduled_days': list(self.scheduled_days or []),
            'daily_target_min': self.daily_target_min,
            'daily_target_manual': bool(self.daily_target_manual),
            'pulse_min_interval': self.pulse_min_interval or 90,
            'pulse_max_interval': self.pulse_max_interval or (self.pulse_min_interval or 90),
            'pulse_duration_min': self.pulse_duration_min or 5,
            'pulse_deterministic': bool(self.pulse_deterministic),
        }


class WorkSession(me.Document):
    meta = {'collection': 'organizer_sessions'}

    user_id = me.StringField(required=True)
    task_id = me.StringField(required=True)
    start_time = me.DateTimeField(required=True)
    end_time = me.DateTimeField(default=None)
    duration_min = me.FloatField(default=None)

    def to_dict(self):
        return {
            'id': str(self.id),
            'task_id': self.task_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_min': self.duration_min,
        }


class UserConfig(me.Document):
    meta = {'collection': 'organizer_config', 'strict': False}

    user_id = me.StringField(required=True, unique=True)
    sections = me.EmbeddedDocumentListField(Section, default=list)
    pulse_min_gap_min = me.IntField(default=30)
    pulse_gap_mode = me.StringField(default='minimum', choices=['minimum', 'deterministic'])

    def to_dict(self):
        return {
            'sections': [
                {'id': s.id, 'name': s.name, 'day_configs': s.day_configs or {}}
                for s in self.sections
            ],
            'pulse_min_gap_min': self.pulse_min_gap_min if self.pulse_min_gap_min is not None else 30,
            'pulse_gap_mode': self.pulse_gap_mode or 'minimum',
        }
