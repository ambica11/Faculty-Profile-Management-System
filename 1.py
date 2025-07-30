import tkinter as tk
import mysql.connector
from prettytable import PrettyTable
from tkinter import messagebox
from datetime import datetime
from plyer import notification
import time

class DatabaseManager:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootcode",
            database="project"
        )
        self.mycursor = self.db_connection.cursor()

    def get_month_data(self, month):
        # Similar to the previous implementation
        queries = {
            "1": "SELECT * FROM july",
            "2": "SELECT * FROM august",
            "3": "SELECT * FROM september",
            "4": "SELECT * FROM october",
            "5": "SELECT * FROM november",
        }

        if month in queries:
            self.mycursor.execute(queries[month])
            myresult = self.mycursor.fetchall()
            columns = [desc[0] for desc in self.mycursor.description]
            table = PrettyTable(columns)

            for row in myresult:
                table.add_row(row)

            return str(table)
        else:
            return "Invalid month input."

    def get_timetable_data(self):
        self.mycursor.execute("SELECT * FROM timetable")
        myresult = self.mycursor.fetchall()
        columns = [desc[0] for desc in self.mycursor.description]
        table = PrettyTable(columns)

        for row in myresult:
            table.add_row(row)

        return str(table)


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

        
class MainPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Page")
        self.geometry("400x300")
        self.database_manager = DatabaseManager()

        self.choice_label = tk.Label(self, text="Enter your choice (1-4):\n\n1.Academic Calendar\n2.Time Table\n3.Exam Duty\n4.Exit")
        self.choice_label.pack()

        self.choice_entry = tk.Entry(self)
        self.choice_entry.pack()

        self.submit_button = tk.Button(self, text="Submit", fg="black", bg="red", command=self.navigate)
        self.submit_button.pack()

    def navigate(self):
        choice = self.choice_entry.get()
        if choice == '1':
            self.academic_calendar_gui = AcademicCalendarPage(self)
        elif choice == '2':
            timetable_data = self.database_manager.get_timetable_data()
            self.timetable_gui = TimetablePage(self, timetable_data)
        elif choice == '3':
            self.duty_allocation_page = DutyAllocationPage(self)
        elif choice == '4':
            reminders = [
                ("kindly check the exam duty time table, it's time for your invigilation", "2023-11-04 23:49:00"),
                ("kindly check the exam duty time table, it's time for your invigilation", "2023-11-04 23:49:10"),
                ("kindly check the exam duty time table, it's time for your invigilation", "2023-11-04 23:49:30")
            ]
            reminder_manager = ReminderManager(reminders)
            reminder_manager.set_notifications()
            self.destroy()
        else:
            ErrorPage(self, "Invalid choice. Please enter a valid option (1-4).")
            self.destroy()
       
class TimetablePage(tk.Toplevel):
    def __init__(self, master, timetable_data):
        super().__init__(master)
        self.title("Timetable")
        self.geometry("700x300")

        self.timetable_text = tk.Text(self, height=45, width=180)
        self.timetable_text.pack()

        self.timetable_text.insert(tk.END, timetable_data)
        

        self.exit_button = tk.Button(self, text="Exit",fg="black", bg="red", command=self.close_window)
        self.exit_button.pack()

    def close_window(self):
        self.destroy()


class AcademicCalendarPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Academic Calendar")
        self.geometry("400x300")

        self.db_manager = DatabaseManager()

        self.month_label = tk.Label(self, text="Enter Month:\n\n1.july\n2.August\n3.September\n4.October\n5.November\n")
        self.month_label.pack()

        self.month_entry = tk.Entry(self)
        self.month_entry.pack()

        self.show_button = tk.Button(self, text="Show Calendar",fg="black", bg="red", command=self.show_calendar)
        self.show_button.pack()

        self.calendar_text = tk.Text(self, height=35, width=80)
        self.calendar_text.pack()
        

    def show_calendar(self):
        month = self.month_entry.get()
        database_manager = DatabaseManager()
        calendar_data = self.db_manager.get_month_data(month)
        self.calendar_text.delete(1.0, tk.END)
        self.calendar_text.insert(tk.END, calendar_data)



class DutyAllocationPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Exam Duty")
        self.initialize_database()
        self.create_gui()

    def initialize_database(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootcode",
            database="project"
        )
        self.mycursor = self.mydb.cursor()

    def create_gui(self):
        self.label = tk.Label(self, text="Exam Duty Management System", font=("Arial", 16))
        self.label.pack(pady=20)

        self.button_view_duty = tk.Button(self, text="View Duty Allocation", command=self.display_table)
        self.button_view_duty.pack()

        self.button_add_schedule = tk.Button(self, text="Add Exam Duty Schedule", command=self.open_add_schedule)
        self.button_add_schedule.pack()

        self.button_exit = tk.Button(self, text="Exit", command=self.destroy)
        self.button_exit.pack()

    def display_table(self):
        self.mycursor.execute("SELECT * FROM EXAM_DUTY")
        result = self.mycursor.fetchall()

        table = PrettyTable(["S_No","Exam Date", "Room Number"])

        for row in result:
            table.add_row(row)

        messagebox.showinfo("Exam Duties", str(table))

    def open_add_schedule(self):
        response = messagebox.askquestion("Add Exam Duty", "Do you want to add an extra exam duty?")
        if response == "yes":
            self.add_schedule()

    def add_schedule(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Exam Duty Schedule")

        label_date = tk.Label(add_window, text="Exam Date:")
        label_date.pack()
        entry_date = tk.Entry(add_window)
        entry_date.pack()

        label_room = tk.Label(add_window, text="Room Number:")
        label_room.pack()
        entry_room = tk.Entry(add_window)
        entry_room.pack()

        button_add = tk.Button(add_window, text="Add", command=lambda: self.save_schedule(entry_date.get(), entry_room.get(), add_window))
        button_add.pack()

    def save_schedule(self, exam_date, room_no, add_window):
        sql = "INSERT INTO EXAM_DUTY (exam_date, room_number) VALUES (%s, %s)"
        val = (exam_date, room_no)
        try:
          self.mycursor.execute(sql, val)
          self.mydb.commit()
          messagebox.showinfo("Success", "Exam duty schedule added successfully!")
          add_window.destroy()
        except mysql.connector.Error as err:
          messagebox.showerror("Error", f"Failed to add exam duty schedule: {err}")

class ErrorPage(tk.Toplevel):
    def __init__(self, master, message):
        super().__init__(master)
        self.title("Error")
        self.geometry("300x100")

        self.error_label = tk.Label(self, text=message)
        self.error_label.pack()



if __name__ == "__main__":
    app = MainPage()
    app.mainloop()
    
    
