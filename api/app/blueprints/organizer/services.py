from datetime import datetime, timedelta
from app.blueprints.organizer.models import Task, UserConfig

URGENCY_RANK  = {'overdue': 0, 'time_to_do': 1, 'needs_doing': 2, 'upcoming': 3}
PRIORITY_RANK = {'high': 0, 'medium': 1, 'low': 2}


def _urgency(task, ref_dt, last_done=None):
    last = last_done if last_done is not None else task.last_done
    if not last:
        return 'overdue'
    days_since = (ref_dt - last).total_seconds() / 86400
    min_d = task.recurrence_min_days
    max_d = task.recurrence_max_days
    window = max(max_d - min_d, 1)
    if days_since >= max_d:
        return 'overdue'
    if days_since >= min_d + window * 2 / 3:
        return 'time_to_do'
    if days_since >= min_d + window * 1 / 3:
        return 'needs_doing'
    return 'upcoming'


def task_score(task, reference_dt):
    urgency = task.urgency_at(reference_dt)
    return URGENCY_RANK.get(urgency, 4) * 2 + PRIORITY_RANK.get(task.priority, 1)


def get_or_create_config(user_id):
    cfg = UserConfig.objects(user_id=user_id).first()
    if not cfg:
        cfg = UserConfig(user_id=user_id)
        cfg.save()
    return cfg


def _build_pools(cfg, date, now=None):
    dow = str(date.weekday())
    pools = {}
    for s in cfg.sections:
        day_cfg = (s.day_configs or {}).get(dow, {})
        mode = day_cfg.get('mode', 'off')
        if mode == 'time_block':
            sh, eh = day_cfg.get('start_hour', 0), day_cfg.get('end_hour', 0)
            if eh > sh:
                if now is not None:
                    current_min = now.hour * 60 + now.minute
                    remaining = max(0, eh * 60 - current_min)
                else:
                    remaining = (eh - sh) * 60
                if remaining > 0:
                    pools[s.id] = remaining
        elif mode == 'duration':
            m = day_cfg.get('duration_min', 0)
            if m > 0:
                pools[s.id] = m
    return pools


def build_schedule(user_id, days=7, tz_offset_minutes=0):
    cfg = get_or_create_config(user_id)
    tasks = list(Task.objects(user_id=user_id, is_active=True))
    now = datetime.utcnow() - timedelta(minutes=tz_offset_minutes)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    window_end = today + timedelta(days=days)

    day_structs = []
    for i in range(days):
        d = today + timedelta(days=i)
        pools = _build_pools(cfg, d, now=now if i == 0 else None)
        day_structs.append({
            'date': d,
            'pools': pools,
            'available_min': sum(pools.values()),
            'tasks': [],
        })

    # next_eligible: earliest date each task can next be scheduled
    # virtual_last_done: last planned completion (for urgency display on re-scheduled tasks)
    next_eligible = {}
    virtual_last_done = {}
    for task in tasks:
        tid = str(task.id)
        virtual_last_done[tid] = task.last_done
        if task.last_done:
            ld = task.last_done.replace(hour=0, minute=0, second=0, microsecond=0)
            next_eligible[tid] = ld + timedelta(days=task.recurrence_min_days)
        else:
            next_eligible[tid] = today
        if task.snoozed_until:
            snooze_day = task.snoozed_until.replace(hour=0, minute=0, second=0, microsecond=0)
            if snooze_day >= today:
                next_eligible[tid] = max(next_eligible[tid], snooze_day + timedelta(days=1))
            else:
                task.snoozed_until = None
                task.save()

    # Pre-pass: place pinned tasks on their designated days before greedy runs.
    for task in tasks:
        if not task.pinned_dates:
            continue
        tid = str(task.id)
        expired = []
        placed_any = False
        for date_str in sorted(task.pinned_dates):
            target = datetime.strptime(date_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
            if target < today:
                expired.append(date_str)
                continue
            for ds in day_structs:
                if ds['date'] != target:
                    continue
                if task.section_id in ds['pools'] and ds['pools'][task.section_id] >= task.min_duration_min:
                    urgency = _urgency(task, ds['date'], virtual_last_done[tid])
                    ds['tasks'].append({
                        'id': tid,
                        'title': task.title,
                        'task_type': task.task_type,
                        'section_id': task.section_id,
                        'urgency': urgency,
                        'min_duration_min': task.min_duration_min,
                        'max_duration_min': task.max_duration_min,
                        'overtime': False,
                        'pinned': True,
                    })
                    ds['pools'][task.section_id] = max(0, ds['pools'][task.section_id] - task.max_duration_min)
                    virtual_last_done[tid] = ds['date']
                    next_eligible[tid] = ds['date'] + timedelta(days=task.recurrence_min_days)
                    placed_any = True
                break
        if expired:
            task.pinned_dates = [d for d in task.pinned_dates if d not in expired]
            task.save()

    # Day-first greedy: for each day, repeatedly pick the highest-priority
    # eligible task until no more tasks fit. This ensures high-priority recurring
    # tasks claim their slot each day before lower-priority tasks fill the pool.
    for ds in day_structs:
        while True:
            best = None
            best_score = float('inf')
            for task in tasks:
                tid = str(task.id)
                if next_eligible[tid] > ds['date']:
                    continue
                if task.section_id not in ds['pools']:
                    continue
                if ds['pools'][task.section_id] < task.min_duration_min:
                    continue
                score = (
                    URGENCY_RANK.get(_urgency(task, ds['date'], virtual_last_done.get(tid)), 4) * 2
                    + PRIORITY_RANK.get(task.priority, 1)
                )
                if score < best_score:
                    best_score = score
                    best = task
            if best is None:
                break
            tid = str(best.id)
            ds['tasks'].append({
                'id': tid,
                'title': best.title,
                'task_type': best.task_type,
                'section_id': best.section_id,
                'urgency': _urgency(best, ds['date'], virtual_last_done[tid]),
                'min_duration_min': best.min_duration_min,
                'max_duration_min': best.max_duration_min,
                'overtime': False,
            })
            ds['pools'][best.section_id] = max(0, ds['pools'][best.section_id] - best.max_duration_min)
            virtual_last_done[tid] = ds['date']
            next_eligible[tid] = ds['date'] + timedelta(days=best.recurrence_min_days)

    # Overload: urgent tasks that could not be placed anywhere (no capacity)
    placed_ids = {t['id'] for ds in day_structs for t in ds['tasks']}
    overload_warning = any(
        task.urgency_at(today) in ('overdue', 'time_to_do')
        and task.section_id
        and str(task.id) not in placed_ids
        for task in tasks
    )

    schedule = []
    for ds in day_structs:
        total = sum(t['min_duration_min'] for t in ds['tasks'])
        schedule.append({
            'date': ds['date'].strftime('%Y-%m-%d'),
            'day_name': ds['date'].strftime('%A'),
            'is_work_day': ds['available_min'] > 0,
            'available_min': ds['available_min'],
            'tasks': ds['tasks'],
            'total_scheduled_min': total,
            'overloaded': False,
        })

    return schedule, overload_warning


def check_capacity_warning(user_id):
    cfg = get_or_create_config(user_id)
    tasks = list(Task.objects(user_id=user_id, is_active=True))

    weekly_capacity = 0
    for s in cfg.sections:
        for day_cfg in (s.day_configs or {}).values():
            mode = day_cfg.get('mode', 'off')
            if mode == 'time_block':
                sh, eh = day_cfg.get('start_hour', 0), day_cfg.get('end_hour', 0)
                weekly_capacity += max(0, (eh - sh) * 60)
            elif mode == 'duration':
                weekly_capacity += day_cfg.get('duration_min', 0)

    weekly_demand = 0
    for task in tasks:
        if task.recurrence_max_days > 0:
            times_per_week = 7.0 / task.recurrence_max_days
            weekly_demand += times_per_week * task.min_duration_min

    at_capacity = weekly_capacity > 0 and weekly_demand >= weekly_capacity * 0.85
    return at_capacity, round(weekly_demand), round(weekly_capacity)
