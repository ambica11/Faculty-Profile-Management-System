import tkinter as tk
import mysql.connector
from prettytable import PrettyTable

class DatabaseManager:
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

    def get_timetable_data(self):
        self.mycursor.execute("SELECT * FROM timetable")
        myresult = self.mycursor.fetchall()
        columns = [desc[0] for desc in self.mycursor.description]
        table = PrettyTable(columns)

        for row in myresult:
            table.add_row(row)

        return str(table)

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Database Viewer")
        self.geometry("600x400")

        self.database_manager = DatabaseManager()

        self.choice_label = tk.Label(self, text="Enter your choice (1-4):")
        self.choice_label.pack()

        self.choice_entry = tk.Entry(self)
        self.choice_entry.pack()

        self.result_text = tk.Text(self, height=15, width=60)
        self.result_text.pack()

        self.submit_button = tk.Button(self, text="Submit", command=self.handle_choice)
        self.submit_button.pack()

    def handle_choice(self):
        choice = self.choice_entry.get()

        if choice == '1':
            month = input("Enter the month (1-5): ")
            calendar_data = self.database_manager.get_month_data(month)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, calendar_data)
        elif choice == '2':
            pass
        elif choice == '3':
            # Display existing data
            display_table()

            # Ask user if they want to input additional data
            while True:
                add_data = input("Do you want to input additional data? (yes/no): ").lower()
                if add_data == 'no':
                    break
                elif add_data == 'yes':
                    # Take user input for exam date and room number
                    exam_date = input("Enter exam date (YYYY-MM-DD): ")
                    room_no = input("Enter room number: ")

                    # SQL query to insert data into the database
                    sql = "INSERT INTO EXAM_DUTY (exam_date, room_no) VALUES (%s, %s)"
                    val = (exam_date, room_no)

                    # Execute the SQL query to insert data
                    mycursor.execute(sql, val)

                    # Commit the changes to the database
                    mydb.commit()

                    print(mycursor.rowcount, "record inserted.")
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

            # Display updated data after adding extra data
            display_table()
        elif choice == '4':
            print("Exiting program. Goodbye!")
            self.destroy()
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Invalid choice. Please enter a valid option (1-4).")

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
