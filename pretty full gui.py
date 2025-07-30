import tkinter as tk
import mysql.connector
from prettytable import PrettyTable
from datetime import datetime

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        entered_username = input("Enter your username: ")
        entered_password = input("Enter your password: ")

        if entered_username == self.username and entered_password == self.password:
            print("Login successful! Welcome, " + self.username + "!")
            return True
        else:
            print("Invalid username or password. Please try again.")
            return False

class AdminUser(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def add_exam_duty(self):
        # Code for adding exam duty
        pass

class RegularUser(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def view_exam_duty(self):
        # Code for viewing exam duty
        pass

class AcademicCalendarGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Academic Calendar")
        self.master.geometry("400x300")

        self.month_label = tk.Label(master, text="Enter Month (1-5):")
        self.month_label.pack()

        self.month_entry = tk.Entry(master)
        self.month_entry.pack()

        self.show_button = tk.Button(master, text="Show Calendar",fg="black", bg="red", command=self.show_calendar)
        self.show_button.pack()

        self.calendar_text = tk.Text(master, height=35, width=80)
        self.calendar_text.pack()

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootcode",
            database="project"
        )

    def show_calendar(self):
        month = self.month_entry.get()
        try:
            mycursor = self.db_connection.cursor()
            query = f"SELECT * FROM {self.get_month_table(month)}"
            mycursor.execute(query)
            myresult = mycursor.fetchall()

            columns = [desc[0] for desc in mycursor.description]
            table = PrettyTable(columns)

            for row in myresult:
                table.add_row(row)

            self.calendar_text.delete(1.0, tk.END)
            self.calendar_text.insert(tk.END, str(table))
        except ValueError:
            print("Invalid input. Please enter a valid month.")

    def get_month_table(self, month):
        month_dict = {
            '1': 'july',
            '2': 'august',
            '3': 'september',
            '4': 'october',
            '5': 'november'
        }
        return month_dict.get(month, 'invalid_month')

def main():
    # Create instances of AdminUser or RegularUser based on user type
    user_type = input("Enter user type (admin or regular): ")
    if user_type.lower() == 'admin':
        user = AdminUser("admin", "admin123")
    elif user_type.lower() == 'regular':
        user = RegularUser("user123", "password123")
    else:
        print("Invalid user type.")
        return

    # GUI initialization
    gui = tk.Tk()
    academic_calendar_gui = AcademicCalendarGUI(gui)

    # Login functionality
    while not user.login():
        pass  # Continue prompting for login until successful

    # Run the GUI application
    gui.mainloop()

if __name__ == "__main__":
    main()
