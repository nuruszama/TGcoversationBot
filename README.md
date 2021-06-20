# TGcoversationBot
Trying to create a bot which can handle any conversation without bot's reply keyboard.
I'm a mechanical engineer and have no knowledge in programing. If you can help, I would be so much happy 😊

# Installation
Do I need to install pip?
pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from python.org 
If not installed, Download the latest Python 3 package from the official website. (https://www.python.org/downloads/)

Run the installation with the default configuration. Take note of where python is being installed, we will need this later. 

After the installation has completed, we will need to add the python package manager to the system path, in order to install the python-telegram-bot package. First, find the 'advanced system settings' through the control panel.

Then, click on 'environment variables'.

Click on new. Here, we enter the path to pip3, the Python 3 package manager. The path should look something like this,
    C:\Users\<your_username>\AppData\Local\Programs\Python\Python<version-number>\Scripts
  
Remember the second step that where python is being installed? This is just the "Scripts" folder within that location. So, from the first step, simply add in "\Scripts".
  
Be careful though, as adding in the wrong path will not produce an error in this step. Rather, the later steps will fail. If you want to make sure, you can navigate to the AppData folders by typing in %appdata% in the windows search menu.
  
After adding new path, Press 'OK' on everything, and proceed on to the next step.
  
  open script folder and do shift + right click, choose open command promt here.
  
Enter the following command to execute the installation.
  
    pip3 install python-telegram-bot
  
Now start running your bot anywhere from your system....
  
  For detailed guide visit (https://usp-python.github.io/)
