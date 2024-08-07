# HRV_Project_Metro

This is project from the subject Hardware 2 in the first year of the ICT program in Metropolia.

## About
-   The project is to create a part of a IoT Sytem, which include the Edge Devices, The API Gateway and the End User. The Cloud storage is not included in this project. However, the past measurement is stored inside the flash memory of the edge device.
-   The device is standalone, or it is a plug-and-play device. Using any 3-5V power source to turn on the device and it is ready to use.


## Components
###  Hardware
-   Crowtail Pulse Sensor
-   Raspberry Pi Pico
-   Raspberry Pi Pico W
-   Asus Router AX1800
-   LED SSD1306
### Software    
- Language: MicroPython
- IDE: Thorny
- Mpremote Library
- Raspberry Firstware v1.22.2


## How it work  
- The user will put the sensor over the middle of his forehead
- The sensor will detect the pulse and send it to the Raspberry Pi Pico as a analog signal.
- There are 4 options to choose:
    1. Measure HR: this program will display user's heart rate value in real-time on the led screen.
    2. HRV Analysis: This program will display user's heart rate in real-time on the led screen. Then after 30s, it will send the result to the end user via the MQTT service. The result also be shown on the led screen.
    3. Kubios: This program will display the user's heart rate in real-time on the led screen. The measurement is then sent to the KUBIOS Cloud Service to do the Advanced HRV analysis. When the HRV Cloud Service sent back the response, the result is shown on the LED screen.
    4. History: This program will this display the 5 most-recent measurements. The user can see the detail of each measurements.
- The usage of the deviced is based on the interaction with the rotator and the switch on the device. Turn the rotator to go move between optino, press the switch to choose the option or to go to the next stage of the program.

### How to use
- Connect the raspberry with the laptop
- git clone this project with the following command:

`git clone --recurse-submodules https://gitlab.metropolia.fi/viettrud/g4-hr_monitor.git
`
- cd to this project
- open the terminal of this directory
- Flash and install a new firmware to the raspberry
- If you use Windows PowerShell or Command Prompt run:
`.\install.cmd`
- If you use Linux, OSX or GitBash run:
`./install.sh`
- Press Reset Button on the Raspberry or connect the raspberry to the power source.
- Have fun
