# CatCam V0.1
# By EkansCode

# Import Python header files
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from picamera2 import Picamera2, Preview
from gpiozero import MotionSensor
from gpiozero import LED
import time

#dailycounterdef
def reset_daily_variable():
    current_date = datetime.datetime.now().date()
    return current_date, 0

def get_variable_value(variable):
    current_date, value = variable
    new_date = datetime.datetime.now().date()

    if new_date > current_date:
        return reset_daily_variable()
    
    return current_date, value
#daily counter set
number = 1
variable = (datetime.datetime.now().date(), number)
variable = get_variable_value(variable)
current_date, value = variable

# Sender's email credentials
sender_email = "ChangeMe@gmail.com"
sender_password = "**ChangeMe**"

# Recipient's email address
to_email = "ChangeMe@gmail"
# Email subject
subject = "Cat activity detected"

# Email content
message = """
Hello,
A cat has been detected using the catflap.
""" + f"Date: {current_date}, Times used flap today: {value}"
# Set a variable to hold the GPIO Pin identity
pir = MotionSensor(17)
red_led = LED(24)
ending = ".jpg"
camera = Picamera2()
number_string = str(number)
time.sleep(2)
catcam = "/home/f01/Desktop/catcam/"

print("Waiting for PIR to settle")
pir.wait_for_no_motion()

print("PIR Module Test (CTRL-C to exit)")

# Variables to hold the current and last states
currentstate = False
previousstate = False

try:
    # Loop until users quits with CTRL-C
    while True:
        # Read PIR state
        currentstate = pir.motion_detected

        # If the PIR is triggered
        if currentstate == True and previousstate == False:
            print("    Motion detected!")
            red_led.on()
            camera.start()
            time.sleep(1)
            camera.capture_file(catcam + number_string + ending)
            print(number)
            camera.stop()
            ###daily counter 
            
            variable = (datetime.datetime.now().date(), number)
            variable = get_variable_value(variable)
            current_date, value = variable
            print(f"Date: {current_date}, Times used flap today: {value}")

            
            ###email
            # Create the MIMEText object
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Attach the image file EDITTTTT
            image_path = "/home/f01/Desktop/catcam/" + number_string + ".jpg"
            with open(image_path, 'rb') as attachment:
                image_part = MIMEImage(attachment.read())
                image_part.add_header('Content-Disposition', f'attachment; filename= {image_path}')
                msg.attach(image_part)

            # Connect to Gmail's SMTP server
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

            # Log in to the Gmail account
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, to_email, msg.as_string())

            # Quit the SMTP server
            server.quit()

            print("Email with attachment sent successfully!")
            
            number = number + 1
            number_string = str(number)
            
            # Record previous state
            previousstate = True
        # If the PIR has returned to ready state
        elif currentstate == False and previousstate == True:
            print("    No Motion")
            previousstate = False
            time.sleep(1)
            red_led.off()
           

        # Wait for 10 milliseconds
        time.sleep(0.01)

except KeyboardInterrupt:
    print("    Quit")
