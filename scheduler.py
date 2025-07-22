import requests


def to_mins(time):
    hours, mins = time.split(':')
    return int(hours) * 60 + int(mins)


def to_hours(time):
    hours = time // 60
    mins = time % 60
    return str(hours).zfill(2) + ':' + str(mins).zfill(2)


def slot_availability(date, slot, duration_minutes):
    slot_start = to_mins(slot[0])
    slot_end = to_mins(slot[1])
    slot_duration = slot_end - slot_start
    if duration_minutes <= slot_duration:
        result = (date, slot[0], to_hours(slot_start + duration_minutes))
        print(result)
        return result
    return False


class Scheduler:
    def __init__(self, url):
        self.data = requests.get(url).json()

    def retrieve_busy_slots(self, date_value):
        day_id = None
        day_starts = None
        day_ends = None
        for day in self.data['days']:
            if day['date'] == date_value:
                day_id = day['id']
                day_starts = day['start']
                day_ends = day['end']
                break

        if day_id is None:
            return None

        busy_slots = []
        for timeslot in self.data['timeslots']:
            if timeslot['day_id'] == day_id:
                busy_slots.append((timeslot['start'], timeslot['end']))
        busy_slots = sorted(busy_slots, key=lambda slot: slot[0])
        return day_starts, day_ends, busy_slots

    def get_busy_slots(self, date_value):
        busy_slots = self.retrieve_busy_slots(date_value)
        if busy_slots is None:
            print('Указанной даты не существует.')
            return None
        elif len(busy_slots[2]) == 0:
            print('Заявок на указанную дату не найдено.')
        else:
            print(busy_slots[2])
        return busy_slots[2]

    def retrieve_free_slots(self, date_value):
        busy_slots_data = self.retrieve_busy_slots(date_value)

        if busy_slots_data is None:
            return 'Указанной даты не существует.'

        day_starts, day_ends, busy_slots = busy_slots_data[0], busy_slots_data[1], busy_slots_data[2]

        if len(busy_slots) == 0:
            return 'Весь рабочий день свободен.'

        free_slots = []
        for slot in busy_slots:
            if day_starts == slot[0]:
                day_starts = slot[1]
                continue
            free_slots.append((day_starts, slot[0]))
            day_starts = slot[1]
        end_busy_timeslot = busy_slots[-1][1]
        if end_busy_timeslot != day_ends:
            free_slots.append((end_busy_timeslot, day_ends))
        return free_slots

    def get_free_slots(self, date_value):
        free_slots = self.retrieve_free_slots(date_value)
        print(free_slots)
        return free_slots

    def is_available(self, date_value, start_time, end_time):
        result = False
        free_slots = self.retrieve_free_slots(date_value)

        if free_slots == 'Указанной даты не существует.':
            print(free_slots)
            return None

        if free_slots == 'Весь рабочий день свободен.':
            result = True
            print(result)
            return result

        for slot in free_slots:
            if start_time >= slot[0] and end_time <= slot[1]:
                result = True
                break
        print(result)
        return result

    def find_slot_for_duration(self, duration_minutes):
        dates = {day['date']: [day['start'], day['end']] for day in self.data['days']}
        for date, work_time in dates.items():
            free_slots = self.retrieve_free_slots(date)
            for slot in free_slots:
                try:
                    result = slot_availability(date, slot, duration_minutes)
                    if result:
                        return result
                except ValueError:
                    result = slot_availability(date, work_time, duration_minutes)
                    if result:
                        return result
        else:
            print('Доступного промежутка не найдено.')
            return None
