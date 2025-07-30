import smtplib
from email.message import EmailMessage

try:
# Ask for sender's email and password
    sender_email = 'abc@gmail.com'
    sender_password = 'xxxxx'

# Ask for recipient's email
    recipient_email = input("Enter recipient's email address: ")

    subject = 'Test Email'
    body = 'This is a test email sent from Python.'

    # Create an EmailMessage object
    message = EmailMessage()
    message.set_content(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email

    # Establish a secure session with Gmail's outgoing SMTP server using the provided email account
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, sender_password)

    # Send email
    server.send_message(message)
    print('Email sent successfully!')

except Exception as e:
    print(f'Error: {e}')

finally:
    try:
        # Close the server connection
        server.quit()
    except NameError:
        # Handle the case where the server variable is not defined
        pass
