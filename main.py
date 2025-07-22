from scheduler import Scheduler

scheduler = Scheduler(url='https://ofc-test-01.tspb.su/test-task/')

scheduler.get_busy_slots('2025-02-18')
scheduler.get_free_slots('2025-02-18')
scheduler.is_available('2025-02-18', '12:00', '17:30')
scheduler.is_available('2025-02-18', '11:00', '11:15')
scheduler.find_slot_for_duration(duration_minutes=70)
