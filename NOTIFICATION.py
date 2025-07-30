import mysql.connector
from prettytable import PrettyTable
import time
from datetime import datetime
from plyer import notification

class ReminderManager:
    def __init__(self, reminders):
        self.reminders = reminders

    def calculate_seconds_until_target_datetime(self, target_datetime):
        current_datetime = datetime.now()
        seconds_until_target_datetime = (target_datetime - current_datetime).total_seconds()

        # If the target datetime is in the past, set the reminder for the next occurrence
        if seconds_until_target_datetime < 0:
            seconds_until_target_datetime = 0

        return seconds_until_target_datetime

    def set_notifications(self):
        for reminder in self.reminders:
            reminder_message, target_datetime_str = reminder
            target_datetime = datetime.strptime(target_datetime_str, "%Y-%m-%d %H:%M:%S")
            seconds_until_target_datetime = self.calculate_seconds_until_target_datetime(target_datetime)
            time.sleep(seconds_until_target_datetime)
            notification.notify(
                title='Reminder',
                message=reminder_message,
                app_name='Reminder App',  # Optional: You can set the app name for some platforms
            )

if __name__ == "__main__":
    reminders = [
        ("kindly check the exam duty time table, it's time for your invigilation", "2023-11-04 23:40:00"),
        ("kindly check the exam duty time table, it's time for your invigilation", "2023-11-04 23:40:10"),
        ("kindly check the exam duty time table, it's time for your invigilation", "2023-11-04 23:40:30")
    ]

    reminder_manager = ReminderManager(reminders)
    reminder_manager.set_notifications()
