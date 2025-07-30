import tkinter as tk
import smtplib
from email.message import EmailMessage

# Create a window
root = tk.Tk()
root.title("Login Page")

# Dictionary to store username and email
credentials = {
    "user123": "john@gmail.com"
}

# Function to handle password recovery button click
def recover_password():
    username = username_entry.get()

    # Check if the username exists in the credentials dictionary
    if username in credentials:
        email = credentials[username]

        # Email configuration (same as in your previous code)
        sender_email = 'abc@gmail.com'
        sender_password = 'xxxxx'
        subject = 'Password Recovery'
        body = 'Hello, your password is password123. if you want to change your password click the given link below. \nyour password recovery link: https://example.com/reset-password \n thank you'

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
    if username in credentials and credentials[username] == password:
        result_label.config(text="Login successful! Welcome, " + username + "!")
    else:
        result_label.config(text="Invalid username or password. Please try again.")

# Username Label and Entry
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Password Label and Entry
password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Login Button
login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

# Forgot Password Button
forgot_password_button = tk.Button(root, text="Forgot Password", command=recover_password)
forgot_password_button.pack()

# Result Label (to display login status or recovery status)
result_label = tk.Label(root, text="")
result_label.pack()

# Start the Tkinter main loop
root.mainloop()
