import unittest
from scheduler import Scheduler


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler(url='https://ofc-test-01.tspb.su/test-task/')

    def test_get_busy_slots(self):
        self.assertEqual(self.scheduler.get_busy_slots('2025-02-15'), [('09:00', '12:00'), ('17:30', '20:00')])
        self.assertEqual(self.scheduler.get_busy_slots('2025-02-19'), [])
        self.assertEqual(self.scheduler.get_busy_slots('2025-2-20'), None)

    def test_get_free_slots(self):
        self.assertEqual(self.scheduler.get_free_slots('2025-02-16'), [('08:00', '09:30'), ('11:00', '14:30'), ('18:00', '22:00')])
        self.assertEqual(self.scheduler.get_free_slots('2025-02-19'), 'Весь рабочий день свободен.')
        self.assertEqual(self.scheduler.get_free_slots('2025-2-20'), 'Указанной даты не существует.')

    def test_is_available(self):
        self.assertEqual(self.scheduler.is_available('2025-02-18', '12:00', '17:30'), False)
        self.assertEqual(self.scheduler.is_available('2025-02-18', '11:00', '11:15'), True)
        self.assertEqual(self.scheduler.is_available('2025-02-20', '11:00', '11:15'), None)

    def test_find_slot_for_duration(self):
        self.assertEqual(self.scheduler.find_slot_for_duration(duration_minutes=60), ('2025-02-15', '12:00', '13:00'))
        self.assertEqual(self.scheduler.find_slot_for_duration(duration_minutes=520), ('2025-02-19', '09:00', '17:40'))
        self.assertEqual(self.scheduler.find_slot_for_duration(duration_minutes=600), None)


if __name__ == '__main__':
    unittest.main()
