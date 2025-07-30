import smtplib
from email.message import EmailMessage

# Email configuration
sender_email = 'abc@gmail.com'
sender_password = 'xxxx'
recipient_email = 'john@gmail.com'
subject = 'Test Email'
body = 'This is a test email sent from Python.'

# Create an EmailMessage object
message = EmailMessage()
message.set_content(body)
message['Subject'] = subject
message['From'] = sender_email
message['To'] = recipient_email

try:
    # Establish a secure session with Gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, sender_password)

    # Send email
    server.send_message(message)
    print('Email sent successfully!')

except Exception as e:
    print(f'Error: {e}')

finally:
    # Close the server connection
    server.quit()
