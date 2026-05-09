import uuid
from datetime import datetime, timedelta
from flask import request, jsonify
from app.blueprints.mongo.api_token_auth.helpers import get_user_from_request_headers
from app.blueprints.mongo.api_token_auth.token_verification import verify_token
from app.blueprints.organizer import bp
from app.blueprints.organizer.models import Task, WorkSession, UserConfig, Section
from app.blueprints.organizer.services import build_schedule, get_or_create_config, check_capacity_warning


def _user_id(headers):
    user = get_user_from_request_headers(headers)
    return str(user.id) if user else None


@bp.route('/tasks', methods=['GET'])
@verify_token
def get_tasks():
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    tasks = Task.objects(user_id=uid, is_active=True)
    return jsonify({'success': True, 'tasks': [t.to_dict() for t in tasks]})


@bp.route('/tasks', methods=['POST'])
@verify_token
def create_task():
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    data = request.get_json() or {}
    task = Task(
        user_id=uid,
        title=data.get('title', 'Untitled'),
        description=data.get('description', ''),
        section_id=data.get('section_id', ''),
        task_type=data.get('task_type', 'deep'),
        min_duration_min=int(data.get('min_duration_min', 60)),
        max_duration_min=int(data.get('max_duration_min', 120)),
        recurrence_min_days=int(data.get('recurrence_min_days', 1)),
        recurrence_max_days=int(data.get('recurrence_max_days', 7)),
        priority=data.get('priority', 'medium'),
        overtime_eligible=bool(data.get('overtime_eligible', False)),
        is_one_off=bool(data.get('is_one_off', False)),
        pinned_dates=data.get('pinned_dates', []),
    )
    task.save()
    return jsonify({'success': True, 'task': task.to_dict()}), 201


@bp.route('/tasks/<task_id>', methods=['GET'])
@verify_token
def get_task(task_id):
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    task = Task.objects(id=task_id, user_id=uid).first()
    if not task:
        return jsonify({'success': False}), 404
    return jsonify({'success': True, 'task': task.to_dict()})


@bp.route('/tasks/<task_id>', methods=['PUT'])
@verify_token
def update_task(task_id):
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    task = Task.objects(id=task_id, user_id=uid).first()
    if not task:
        return jsonify({'success': False}), 404
    data = request.get_json() or {}
    fields = [
        'title', 'description', 'section_id', 'task_type',
        'min_duration_min', 'max_duration_min', 'recurrence_min_days',
        'recurrence_max_days', 'priority', 'overtime_eligible', 'is_one_off',
    ]
    for f in fields:
        if f in data:
            setattr(task, f, data[f])
    if 'pinned_dates' in data:
        task.pinned_dates = data['pinned_dates'] or []
    task.save()
    return jsonify({'success': True, 'task': task.to_dict()})


@bp.route('/tasks/<task_id>', methods=['DELETE'])
@verify_token
def delete_task(task_id):
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    task = Task.objects(id=task_id, user_id=uid).first()
    if not task:
        return jsonify({'success': False}), 404
    task.delete()
    return jsonify({'success': True})


@bp.route('/tasks/<task_id>/start', methods=['POST'])
@verify_token
def start_task(task_id):
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    task = Task.objects(id=task_id, user_id=uid).first()
    if not task:
        return jsonify({'success': False}), 404
    existing = WorkSession.objects(user_id=uid, end_time=None).first()
    if existing:
        return jsonify({'success': False, 'message': 'Already have an active session'}), 400
    session = WorkSession(user_id=uid, task_id=str(task.id), start_time=datetime.utcnow())
    session.save()
    return jsonify({'success': True, 'session': session.to_dict()})


@bp.route('/tasks/<task_id>/stop', methods=['POST'])
@verify_token
def stop_task(task_id):
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    session = WorkSession.objects(user_id=uid, task_id=task_id, end_time=None).first()
    if not session:
        return jsonify({'success': False, 'message': 'No active session'}), 404
    now = datetime.utcnow()
    session.end_time = now
    session.duration_min = (now - session.start_time).total_seconds() / 60
    session.save()
    task = Task.objects(id=task_id, user_id=uid).first()
    return jsonify({'success': True, 'session': session.to_dict(), 'task': task.to_dict() if task else None})


@bp.route('/tasks/<task_id>/snooze', methods=['POST'])
@verify_token
def snooze_task(task_id):
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    task = Task.objects(id=task_id, user_id=uid).first()
    if not task:
        return jsonify({'success': False}), 404
    task.snoozed_until = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    task.save()
    return jsonify({'success': True, 'task': task.to_dict()})


@bp.route('/tasks/<task_id>/complete', methods=['POST'])
@verify_token
def complete_task(task_id):
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    task = Task.objects(id=task_id, user_id=uid).first()
    if not task:
        return jsonify({'success': False}), 404
    now = datetime.utcnow()
    session = WorkSession.objects(user_id=uid, task_id=task_id, end_time=None).first()
    if session:
        session.end_time = now
        session.duration_min = (now - session.start_time).total_seconds() / 60
        session.save()
    task.last_done = now
    today_str = now.strftime('%Y-%m-%d')
    task.pinned_dates = [d for d in (task.pinned_dates or []) if d != today_str]
    if task.is_one_off:
        task.is_active = False
    task.save()
    return jsonify({'success': True, 'task': task.to_dict()})


@bp.route('/history', methods=['GET'])
@verify_token
def get_history():
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    week_start_str = request.args.get('week_start')
    if week_start_str:
        week_start = datetime.strptime(week_start_str, '%Y-%m-%d')
    else:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=7)
    sessions = WorkSession.objects(user_id=uid, start_time__gte=week_start, start_time__lt=week_end, end_time__ne=None)
    task_ids = list({s.task_id for s in sessions})
    tasks_map = {str(t.id): t for t in Task.objects(id__in=task_ids)} if task_ids else {}
    cfg = get_or_create_config(uid)
    sections_map = {s.id: s for s in cfg.sections}
    time_blocks = {}
    for i in range(7):
        day = week_start + timedelta(days=i)
        date_str = day.strftime('%Y-%m-%d')
        dow = str(day.weekday())
        blocks = []
        for section in cfg.sections:
            day_cfg = (section.day_configs or {}).get(dow, {})
            if day_cfg.get('mode') == 'time_block':
                sh, eh = day_cfg.get('start_hour', 0), day_cfg.get('end_hour', 0)
                if eh > sh:
                    blocks.append({'section_id': section.id, 'section_name': section.name, 'start_hour': sh, 'end_hour': eh})
        time_blocks[date_str] = blocks
    session_list = []
    for s in sessions:
        task = tasks_map.get(s.task_id)
        section = sections_map.get(task.section_id) if task else None
        session_list.append({
            'id': str(s.id),
            'task_id': s.task_id,
            'task_title': task.title if task else 'Unknown',
            'section_id': task.section_id if task else '',
            'section_name': section.name if section else '',
            'start_time': s.start_time.isoformat(),
            'end_time': s.end_time.isoformat(),
            'duration_min': round(s.duration_min or 0),
        })
    return jsonify({
        'success': True,
        'week_start': week_start.strftime('%Y-%m-%d'),
        'sessions': session_list,
        'time_blocks': time_blocks,
        'sections': [{'id': s.id, 'name': s.name} for s in cfg.sections],
    })


@bp.route('/sessions/<session_id>', methods=['PUT'])
@verify_token
def update_session(session_id):
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    session = WorkSession.objects(id=session_id, user_id=uid).first()
    if not session:
        return jsonify({'success': False}), 404
    data = request.get_json() or {}
    def parse_iso(s):
        return datetime.strptime(s.rstrip('Z').split('.')[0], '%Y-%m-%dT%H:%M:%S')
    if 'start_time' in data:
        session.start_time = parse_iso(data['start_time'])
    if 'end_time' in data:
        session.end_time = parse_iso(data['end_time'])
    if session.start_time and session.end_time:
        session.duration_min = (session.end_time - session.start_time).total_seconds() / 60
    session.save()
    return jsonify({'success': True, 'session': session.to_dict()})


@bp.route('/sessions/active', methods=['GET'])
@verify_token
def get_active_session():
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    session = WorkSession.objects(user_id=uid, end_time=None).first()
    if not session:
        return jsonify({'success': True, 'session': None})
    task = Task.objects(id=session.task_id).first()
    return jsonify({
        'success': True,
        'session': session.to_dict(),
        'task': task.to_dict() if task else None,
    })


@bp.route('/schedule', methods=['GET'])
@verify_token
def get_schedule():
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    days = int(request.args.get('days', 7))
    tz_offset = int(request.args.get('tz_offset', 0))
    schedule, overload = build_schedule(uid, days=days, tz_offset_minutes=tz_offset)
    return jsonify({'success': True, 'schedule': schedule, 'overload_warning': overload})


@bp.route('/capacity', methods=['GET'])
@verify_token
def get_capacity():
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    at_capacity, demand, capacity = check_capacity_warning(uid)
    return jsonify({'success': True, 'at_capacity': at_capacity, 'weekly_demand_min': demand, 'weekly_capacity_min': capacity})


@bp.route('/stats', methods=['GET'])
@verify_token
def get_stats():
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    week_ago = datetime.utcnow() - timedelta(days=7)
    sessions = WorkSession.objects(user_id=uid, end_time__ne=None)
    task_total, task_week = {}, {}
    for s in sessions:
        task_total[s.task_id] = task_total.get(s.task_id, 0) + (s.duration_min or 0)
        if s.start_time >= week_ago:
            task_week[s.task_id] = task_week.get(s.task_id, 0) + (s.duration_min or 0)
    task_ids = list(task_total.keys())
    tasks = Task.objects(id__in=task_ids) if task_ids else []
    cfg = get_or_create_config(uid)
    sections_map = {s.id: s.name for s in cfg.sections}
    section_total = {}
    task_stats = []
    for task in tasks:
        tid = str(task.id)
        sid = task.section_id or ''
        total = round(task_total.get(tid, 0))
        task_stats.append({
            'id': tid,
            'title': task.title,
            'section_id': sid,
            'section_name': sections_map.get(sid, ''),
            'week_min': round(task_week.get(tid, 0)),
            'total_min': total,
        })
        section_total[sid] = section_total.get(sid, 0) + total
    section_stats = [
        {'id': s.id, 'name': s.name, 'total_min': round(section_total.get(s.id, 0))}
        for s in cfg.sections
    ]
    if '' in section_total:
        section_stats.append({'id': '', 'name': 'Unsectioned', 'total_min': round(section_total[''])})
    return jsonify({'success': True, 'sections': section_stats, 'tasks': task_stats})



@bp.route('/sections', methods=['GET'])
@verify_token
def get_sections():
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    cfg = get_or_create_config(uid)
    return jsonify({'success': True, 'sections': cfg.to_dict()['sections']})


@bp.route('/sections', methods=['POST'])
@verify_token
def create_section():
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    cfg = get_or_create_config(uid)
    data = request.get_json() or {}
    section = Section(
        id=str(uuid.uuid4()),
        name=data.get('name', 'New Section'),
        day_configs=data.get('day_configs', {}),
    )
    cfg.sections.append(section)
    cfg.save()
    return jsonify({'success': True, 'sections': cfg.to_dict()['sections']}), 201


@bp.route('/sections/<section_id>', methods=['PUT'])
@verify_token
def update_section(section_id):
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    cfg = get_or_create_config(uid)
    data = request.get_json() or {}
    for s in cfg.sections:
        if s.id == section_id:
            if 'name' in data:
                s.name = data['name']
            if 'day_configs' in data:
                s.day_configs = data['day_configs']
            cfg.save()
            return jsonify({'success': True, 'sections': cfg.to_dict()['sections']})
    return jsonify({'success': False}), 404


@bp.route('/sections/reorder', methods=['PUT'])
@verify_token
def reorder_sections():
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    cfg = get_or_create_config(uid)
    ids = (request.get_json() or {}).get('section_ids', [])
    section_map = {s.id: s for s in cfg.sections}
    cfg.sections = [section_map[i] for i in ids if i in section_map]
    cfg.save()
    return jsonify({'success': True, 'sections': cfg.to_dict()['sections']})


@bp.route('/sections/<section_id>', methods=['DELETE'])
@verify_token
def delete_section(section_id):
    uid = _user_id(request.headers)
    if not uid:
        return jsonify({'success': False}), 401
    cfg = get_or_create_config(uid)
    cfg.sections = [s for s in cfg.sections if s.id != section_id]
    cfg.save()
    return jsonify({'success': True, 'sections': cfg.to_dict()['sections']})
