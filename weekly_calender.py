import tkinter as tk
import calendar



def showCal(year_entry):
    global cal_year
    try:
        fetch_year = int(year_entry.get())
        cal_content = calendar.calendar(fetch_year)
        cal_year.config(text=cal_content)
    except ValueError:
        cal_year.config(text="Invalid input. Please enter a valid year.")

def exitProgram():
    gui.destroy()

def show_calendar_page():
    global year_field
    global cal_year
    global gui

    # Create a GUI window
    gui = tk.Tk()
    gui.title("ACADEMIC CALENDAR")
    gui.geometry("550x600")
    gui.config(background="white")

    cal = tk.Label(gui, text="ACADEMIC CALENDAR", bg="dark gray", font=("times", 28, 'bold'))
    year_label = tk.Label(gui, text="Enter Year", bg="light green")
    year_field = tk.Entry(gui)
    show_button = tk.Button(gui, text="Show Calendar", fg="Black", bg="Red", command=lambda: showCal(year_field))
    exit_button = tk.Button(gui, text="Exit", fg="Black", bg="Red", command=exitProgram)
    cal_year = tk.Label(gui, text="", font="Consolas 10 bold")

    cal.grid(row=1, column=1)
    year_label.grid(row=2, column=1)
    year_field.grid(row=3, column=1)
    show_button.grid(row=4, column=1)
    cal_year.grid(row=5, column=1, padx=20)
    exit_button.grid(row=6, column=1)

    # Start the GUI
    gui.mainloop()

# Call the function to show the calendar page
show_calendar_page()
