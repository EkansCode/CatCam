
# CatCam V0.1.0
# By EkansCode
def colored_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"


light_purple_text = colored_text("██▓▒░⡷⠂𝙲𝚊𝚝𝙲𝚊𝚖 V0.1.0⠐⢾░▒▓██", "95")
print(light_purple_text)

# Import Python header files
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from gpiozero import MotionSensor
from gpiozero import LED
import subprocess
import os
import pickle
import time


# dailycounterdef
def reset_daily_variable():
    current_date = datetime.datetime.now().date()
    return current_date, 0


def get_variable_value(variable):
    current_date, value = variable
    new_date = datetime.datetime.now().date()

    if new_date > current_date:
        return reset_daily_variable()

    return current_date, value


# daily counter variables set
number = 1
variable = (datetime.datetime.now().date(), number)
variable = get_variable_value(variable)
current_date, value = variable
catcam = "./catcamoutput/"
currentdatefolder = datetime.datetime.now().strftime("%Y-%m-%d")
catflapedtoday = f"Date: {current_date}, Times used flap today: {value}"

# Path to the base folder
base_folder = os.path.join(catcam, currentdatefolder)

# Check if a folder with today's date exists
if os.path.exists(base_folder):
    print("Today's folder exists.")

else:
    print("New folder created.")

# Find the next available numbered folder
numbered_folders = [name for name in os.listdir(catcam) if name.startswith(currentdatefolder + "_")]
if numbered_folders:
    last_number = max([int(name.split("_")[1]) for name in numbered_folders])
    next_number = last_number + 1
else:
    next_number = 1

# Create a new numbered folder
numbered_folder_name = f"{currentdatefolder}_{next_number:03d}"
numbered_folder_path = os.path.join(catcam, numbered_folder_name)
os.makedirs(numbered_folder_path)



# Check if login.pkl exists
if os.path.exists('login.pkl'):
    # Load variables from the file
    with open('login.pkl', 'rb') as file:
        login_variables = pickle.load(file)
        sender_email = login_variables['sender_email']
        sender_password = login_variables['sender_password']
        to_email = login_variables['to_email']
        email_enabled = login_variables['email_enabled']
else:
    # If login.pkl doesn't exist, ask for input and save variables
    light_purple_text = colored_text("██▓▒░⡷⠂ Email Setup ⠐⢾░▒▓██", "95")
    print(light_purple_text)
    print("If wrong details entered delete or edit login.pkl")
    email_enabled = input("Enable Emails Y/N: ")
    sender_email = input("Input Sender Email: ")
    sender_password = input("Input Sender Email Password: ")
    to_email = input("Input Recipient Email: ")

    login_variables = {
        'sender_email': sender_email,
        'sender_password': sender_password,
        'to_email': to_email,
        'email_enabled': email_enabled
    }

    with open('login.pkl', 'wb') as file:
        pickle.dump(login_variables, file)


# Email subject
subject = "Cat activity detected"

# Set a variable to hold the GPIO Pin identity
pir = MotionSensor(17)
red_led = LED(24)

# set variables
camera = Picamera2()
number_string = str(number)
time.sleep(2)
catcam_output_folder = numbered_folder_path

##output option
light_purple_text = colored_text("██▓▒░⡷⠂Picture/Video⠐⢾░▒▓██", "95")
print(light_purple_text)
print("If input is incorrect picture will be used")
output_option = input("Input P/V: ")

##set ending variable
if output_option == "V":
    ending = ".mp4"
    ending2 = ".mp4"
    video_config = camera.create_video_configuration()
    camera.configure(video_config)
    encoder = H264Encoder(bitrate=10000000)

else:
    ending = ".jpg"



# startup
print("Waiting for PIR to settle")
pir.wait_for_no_motion()
print("(CTRL-C to exit)")

# Variables to hold the current and last states
currentstate = False
previousstate = False

try:
    # Loop until users quits with CTRL-C
    light_purple_text = colored_text("██▓▒░⡷⠂CatCam Active⠐⢾░▒▓██", "95")
    print(light_purple_text)

    while True:
        # Read PIR state
        currentstate = pir.motion_detected

        # If the PIR is triggered
        if currentstate == True and previousstate == False:
            print("    Motion detected!")
            red_led.on()

            ##picture
            if output_option == "P":
                camera.start()
                time.sleep(0.5)
                pic_filename = f"{number_string}{ending}"
                epic_filename = f"{number_string}.jpg"
                pic_path = os.path.join(catcam_output_folder, pic_filename)
                epic_path = os.path.join(catcam_output_folder, epic_filename)
                camera.capture_file(pic_path)
                camera.stop()

                ###daily counter
                variable = (datetime.datetime.now().date(), number)
                variable = get_variable_value(variable)
                current_date, value = variable
                catflapedtoday = f"Date: {current_date}, Times used flap today: {value}"
                print(f"Date: {current_date}, Times used flap today: {value}")

                if email_enabled == "Y":
                    ###emailcontent
                    message = "Hello, a cat has been detected using the catflap. " + catflapedtoday

                    ###email
                    # Create the MIMEText object
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = to_email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(message, 'plain'))

                    # Attach the image file EDITTTTT
                    image_path = epic_path
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

                previousstate = True

    ##video
            if output_option == "V":

                vid_filename = f"{number_string}cnvrt{ending}"
                vid_convfilename = f"{number_string}.mp4"
                vid_convfilepath = os.path.join(catcam_output_folder, vid_convfilename)
                vid_path = os.path.join(catcam_output_folder, vid_filename)

                output = vid_path
                camera.start_recording(encoder, output)
                time.sleep(5)
                camera.stop_recording()

                ##mpeg-4 to mp4
                import subprocess

                # Get the current directory (where the script is located)
                script_directory = os.path.dirname(os.path.abspath(__file__))

                # Construct the path to the ffmpeg executable
                ffmpeg_path = os.path.join(script_directory, "ffmpeg")

                input_filename = output
                output_filename = vid_convfilepath
                ffmpeg_binary = ffmpeg_path  # Provide the path to the ffmpeg binary

                command = [
                    ffmpeg_binary,
                    "-i", input_filename,
                    "-c:v", "libx264",  # Specify the video codec
                    "-c:a", "aac",  # Specify the audio codec
                    "-strict", "experimental",  # Needed for using the aac codec
                    "-preset", "fast",
                    vid_convfilepath
                ]

                subprocess.run(command, shell=False)
                print("Conversion completed.")
                print("vid_convfilename:", vid_convfilename)
                print("vid_convfilepath:", vid_convfilepath)
                time.sleep(1)
                # Remove the original h264 file

                ###daily counter
                variable = (datetime.datetime.now().date(), number)
                variable = get_variable_value(variable)
                current_date, value = variable
                catflapedtoday = f"Date: {current_date}, Times used flap today: {value}"
                print(f"Date: {current_date}, Times used flap today: {value}")

                if os.path.exists(vid_convfilepath):
                    if email_enabled == "Y":
                        print("test!!!!")
                        ###emailcontent
                        message = "Hello, a cat has been detected using the catflap. " + catflapedtoday

                        ###email
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = to_email
                        msg['Subject'] = subject
                        msg.attach(MIMEText(message, 'plain'))

                        # Attach the video file
                        with open(vid_convfilepath, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', f'attachment; filename= {vid_filename}')
                            msg.attach(part)

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
                        time.sleep(4)
                        previousstate = True

                    if email_enabled == "N":
                        time.sleep(4)
                        previousstate = True

                    vid_filename = f"{number_string}cnvrt{ending}"
                    vid_path = os.path.join(catcam_output_folder, vid_filename)

                    try:
                        os.remove(vid_path)
                        print(f"File {vid_path} deleted successfully.")
                    except OSError as e:
                        print(f"Error deleting {vid_path}: {e}")

                # Record previous state




        # If the PIR has returned to ready state
        elif currentstate == False and previousstate == True:
            print("    No Motion")
            previousstate = False
            time.sleep(1)
            red_led.off()
            number = number + 1
            number_string = str(number)

        # Wait for 10 milliseconds
        time.sleep(0.01)

except KeyboardInterrupt:
    print("    Quit")

