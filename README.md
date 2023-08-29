# CatCam

CatCam is a Python script that detects motion using a PIR motion sensor and captures images using a camera. It sends email notifications with the captured images when motion is detected.

## Prerequisites

- Raspberry Pi or compatible device
- PIR motion sensor
- Camera module
- Gmail account with 2-Step Verification enabled
- Python 3.x

#enable 2-Step Verification - Get app password/email password

Please note that the specific steps to generate an app password may change over time, so it's a good idea to refer to Gmail's official documentation for the most up-to-date instructions.

Once you have 2FA enabled, you can generate an app password:

a. While still on the "Security" page, find the "Signing in to Google" section.
b. Look for the "App passwords" option. If you don't see it, you might need to scroll down.
c. Click on "App passwords." You might be prompted to enter your Google account password again.
d. Select the app you want to generate an app password for. Choose "Mail" if the specific app is not listed.
e. Choose the device type that corresponds to your situation (e.g., "Other (Custom name)").
f. Click "Generate."
g. Google will generate a unique 16-character app password for you. This is what is used when asked to input email password by ui, or when set in CatCam.py to fast login (check ##Configuration).

## Installation

1. Clone this repository to your Raspberry Pi or download the script, make sure you keep CatCam.py and catcamoutput folder in the CatCam folder.
2. Install the required Python packages using the following command:
   
pip install picamera2 
pip install gpiozero

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

## Configuration

#Fast Login - Set email adresses without ui
- Locate line 55
- Modify the `sender_email`, `sender_password`, and `to_email` variables in the script to set up email notifications.


## Usage

Run CatCam.py using terminal or prefered method, input emails and passwords.
CatCam will now be active and will email you when motion is detected 🥳
Ctrl c to exit

Make sure you keep CatCam.py and catcamoutput folder in the CatCam folder.

## Contributions

Contributions and improvements are welcome! If you find a bug or want to add a feature, feel free to open an issue or submit a pull request.

## License

This project is licensed under the GNU General Public License v3.0 

---

Created by [EkansCode](https://github.com/EkansCode)
