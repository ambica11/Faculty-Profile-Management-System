import tkinter as tk
import smtplib
from email.message import EmailMessage

# Create a window
root = tk.Tk()
root.title("Login Page")

# Function to handle password recovery button click
def recover_password():
    username = username_entry.get()

    # Check if the username exists in the credentials dictionary
    if username in credentials:
        email = credentials[username]

        # Email configuration
        sender_email = 'abc@gmail.com'  # Your email address
        sender_password = 'xxxxx'  # Your app password (for Gmail with two-factor authentication)
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



# Dictionary to store username and email
credentials = {
    "user123": "saikeerthansk1@gmail.com"
}

# Username Label and Entry
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Recovery Button
recovery_button = tk.Button(root, text="Recover Password", command=recover_password)
recovery_button.pack()

# Result Label (to display recovery status)
result_label = tk.Label(root, text="")
result_label.pack()

# Start the Tkinter main loop
root.mainloop()
