import tkinter as tk
import mysql.connector
from prettytable import PrettyTable

class DatabaseHandler:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootcode",
            database="project"
        )
        self.mycursor = self.mydb.cursor()

    def get_month_data(self, month):
        queries = {
            "1": "SELECT * FROM july",
            "2": "SELECT * FROM august",
            "3": "SELECT * FROM september",
            "4": "SELECT * FROM october",
            "5": "SELECT * FROM november",
        }

        if month.lower() in queries:
            self.mycursor.execute(queries[month.lower()])
            myresult = self.mycursor.fetchall()
            columns = [desc[0] for desc in self.mycursor.description]
            table = PrettyTable(columns)

            for row in myresult:
                table.add_row(row)

            return str(table)
        else:
            return "Invalid month input."

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

        self.calendar_text = tk.Text(master, height=40, width=80)
        self.calendar_text.pack()

    def show_calendar(self):
        month = self.month_entry.get()
        database_handler = DatabaseHandler()
        result = database_handler.get_month_data(month)
        self.calendar_text.delete(1.0, tk.END)
        self.calendar_text.insert(tk.END, result)

def main():
    gui = tk.Tk()
    academic_calendar_gui = AcademicCalendarGUI(gui)
    gui.mainloop()

if __name__ == "__main__":
    main()
