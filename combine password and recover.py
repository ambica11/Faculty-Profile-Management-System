import tkinter as tk
import smtplib
from email.message import EmailMessage
import subprocess

# Create a window
root = tk.Tk()
root.title("Login Page")

# Dictionary to store username and email
credentials = {
    "user123": {"email": "abc.com", "password": "password123"},
    "john_doe": {"email": "john.com", "password": "qwerty"},
    "alice_smith": {"email": "alice.smith@example.com", "password": "abc123"}
}

# Function to handle password recovery button click
def recover_password():
    username = username_entry.get()

    # Check if the username exists in the credentials dictionary
    if username in credentials:
        email = credentials[username]["email"]

        # Email configuration
        sender_email = 'abc@gmail.com'  # Your email address
        sender_password = 'xxxxx'  # Your app password (for Gmail with two-factor authentication)
        subject = 'Password Recovery'
        body = f'Hello {username},\n\nYour password recovery link: https://example.com/reset-password\n\nBest regards,\nThe Support Team'

        # Create an EmailMessage object
        message = EmailMessage()
        message.set_content(body)
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = email

        server = None  # Initialize the server variable to None
        try:
            # Establish a secure session with Gmail's outgoing SMTP server using your Gmail account
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, sender_password)

            # Send email
            server.send_message(message)
            result_label.config(text=f'Recovery email sent to {email} for username {username}.')
            print('Email sent successfully!')

        except Exception as e:
            result_label.config(text='Error sending recovery email. Please try again later.')
            print(f'Error: {e}')

        finally:
            # Close the server connection if it is not None
            if server is not None:
                server.quit()
    else:
        result_label.config(text="Invalid username. Please try again.")

# Function to handle login button click
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username exists and the entered password matches the stored password
    if username in credentials and credentials[username]["password"] == password:
        result_label.config(text="Login successful! Welcome, " + username + "!")
        
        # Execute the external script 1.py after successful login
        subprocess.Popen(["python", "1.py"])
    else:
        result_label.config(text="Invalid username or password. Please try again.")
# Function to handle forgot password button click
def forgot_password():
    # Create a new window for password recovery
    recovery_window = tk.Toplevel(root)
    recovery_window.title("Password Recovery")

    # Username Label and Entry in the recovery window
    username_label = tk.Label(recovery_window, text="Username:")
    username_label.pack()
    username_entry_recovery = tk.Entry(recovery_window)
    username_entry_recovery.pack()

    # Recovery Button in the recovery window
    recovery_button = tk.Button(recovery_window, text="Recover Password", command=recover_password)
    recovery_button.pack()

# Username Label and Entry in the main window
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Password Label and Entry in the main window
password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Login Button in the main window
login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

# Forgot Password Button in the main window
forgot_password_button = tk.Button(root, text="Forgot Password", command=forgot_password)
forgot_password_button.pack()

# Result Label (to display login status or recovery status) in the main window
result_label = tk.Label(root, text="")
result_label.pack()

# Start the Tkinter main loop
root.mainloop()
