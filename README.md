CatCam is a Python script that utilizes a Raspberry Pi along with a pir to create a motion-activated camera system. This version, v0.1.0, introduces the initial set of features for capturing images and videos when motion is detected and sending notifications via email.

Features:

    Image and Video Capture:
    Users can choose to capture either images or videos when motion is detected. The captured content is saved to a designated output folder.

    Email Notifications:
    CatCam can send email notifications when motion is detected, along with the captured media as attachments. Users can enable or disable email notifications during setup. Gmail's SMTP server is used for sending emails.

    Folder Organization:
    Captured media is stored in folders organized by date and numbered subfolders for each session. This helps in keeping track of different instances of motion detection. That can be merged or purged with respective .py files (check bottom of description).

    Saved email credentials:
    Using pickle to store and retrieve login-related data in a serialized format. This helps to maintain email-related settings across different runs of the script without the need for manual input each time, streamlining the process.  

    .Mpeg-4 to .mp4:
    Using ffmpeg to enhance video compatibility and accessibility by converting the video files to a format that is widely supported across various platforms and players. This enables users to easily view and share the captured videos without encountering compatibility issues.



## Prerequisites

- Raspberry Pi or compatible device
- PIR motion sensor
- Camera module
- Gmail account with 2-Step Verification enabled
- Python 3.x
- ffmpeg 

#enable 2-Step Verification - Get app password/email password

Please note that the specific steps to generate an app password may change over time, so it's a good idea to refer to Gmail's official documentation for the most up-to-date instructions.

Once you have 2FA enabled, you can generate an app password:

While still on the "Security" page, find the "Signing in to Google" section.
Look for the "App passwords" option. If you don't see it, you might need to scroll down.
Click on "App passwords." You might be prompted to enter your Google account password again.
Select the app you want to generate an app password for. Choose "Mail" if the specific app is not listed.
Choose the device type that corresponds to your situation (e.g., "Other (Custom name)").
Click "Generate."
Google will generate a unique 16-character app password for you. This is what is used when asked to input email password by ui, or when set in CatCam.py to fast login (check ##Configuration).

## Installation

1. Clone this repository to your Raspberry Pi or download the script, make sure you keep CatCam.py, merger.py, purger.py and catcamoutput folder in the CatCam folder.
2. Install the required Python packages using the following command:
   
pip install picamera2 
pip install gpiozero

3. Install ffmpeg and put it in your CatCam folder. Depending on your pi's processor you will need the 32 (armhf) or 64 (arm64) bit ffmpeg both can be downloaded from https://johnvansickle.com/ffmpeg/ if you are confused which bit your processor is use cat /proc/cpuinfo in terminal. If link is invaild search for FFmpeg Static Builds for linux.
   

#Hardware

Hardware needed:
Any raspberry pi model (except pico)
PIR sensor
Picamera
7x m to f jumper wire


Connect pi camera to 
Make Circuit as shown in photo

![image](https://github.com/EkansCode/CatCam/assets/143468031/b94dcf57-28e7-402c-802b-e4d3bb808f7d)



(PIR inputs are unclear in photo, black to -, yellow to output, red to +) 


## Usage

    Ensure you have the required Python libraries and dependencies installed.
    Ensure ffmpeg is downloaded for the right cpu architecture and that it is in CatCam folder.
    Set up the PIR motion sensor and LED on the appropriate GPIO pins.
    Run the script using python catcam.py in the terminal.
    Follow the prompts to configure email settings and output preferences.
    The script will continuously monitor for motion and capture media as configured.

Merger.py:
Merger.py" consolidates files from numbered subfolders in catcamoutput into a merged folder for organized management.

Purger.py: 
removes .h264 files from merged folder and clears all files in catcamoutput for decluttering.

Please note that this release focuses on basic motion detection, photo and video capture, video conversion, email login, and email notification functionality. Future versions may introduce enhancements, optimizations, and additional features.

## Contributions

Contributions and improvements are welcome! If you find a bug or want to add a feature, feel free to open an issue or submit a pull request.

## License

This project is licensed under the GNU General Public License v3.0 

---

Created by [EkansCode](https://github.com/EkansCode)
