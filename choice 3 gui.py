import mysql.connector
from prettytable import PrettyTable
import tkinter as tk
from tkinter import messagebox

class ExamDutyManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Duty Management System")
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
        self.label = tk.Label(self.root, text="Exam Duty Management System", font=("Arial", 16))
        self.label.pack(pady=20)

        self.button_view_duty = tk.Button(self.root, text="View Duty Allocation", command=self.display_table)
        self.button_view_duty.pack()

        self.button_add_schedule = tk.Button(self.root, text="Add Exam Duty Schedule", command=self.open_add_schedule)
        self.button_add_schedule.pack()

        self.button_exit = tk.Button(self.root, text="Exit", command=self.root.destroy)
        self.button_exit.pack()

    def display_table(self):
        self.mycursor.execute("SELECT * FROM EXAM_DUTY")
        result = self.mycursor.fetchall()

        table = PrettyTable(["Exam Date", "Room Number"])

        for row in result:
            table.add_row(row)

        messagebox.showinfo("Exam Duties", str(table))

    def open_add_schedule(self):
        response = messagebox.askquestion("Add Exam Duty", "Do you want to add an extra exam duty?")
        if response == "yes":
            self.add_schedule()

    def add_schedule(self):
        add_window = tk.Toplevel(self.root)
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
        sql = "INSERT INTO EXAM_DUTY (exam_date, room_no) VALUES (%s, %s)"
        val = (exam_date, room_no)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        messagebox.showinfo("Success", "Exam duty schedule added successfully!")
        add_window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExamDutyManager(root)
    root.mainloop()
