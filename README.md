# msi-afterburner-arduino
Displays: gpu and cpu temperature and usage, ram usage and fps from afterburner, to an arduino display

# How to use:
Upload the arduino code onto your arduino, you will only have to do this once, since it automatically saves the code on it's flash memory
connect your lcd display to the arduino like this:
![image](https://github.com/user-attachments/assets/f5619862-e0b2-4ab2-9a82-bc0ae0404f4d)
(if your display has more than 4 pins, meaning its uart, you will have to search up how to connect it and replace some code)

For the python code, place the .py and .png file inside a folder.
__make sure to change the ram variable__ to your computers amount of ram, which you can find in task manager (if you have for example 16 gb, instead type 16000, turning it into megabytes)
Also install all the dependencies, if you haven't already, by running in cmd:
```pip install pyserial```
```pip install pillow```
```pip install pystray```
```pip install tk```
If you'd like a different image, just replace the .png file with your own, which must have the same name.

Then, in order to turn the .py file into a .exe file, do the following:
copy your folder path, and type in cmd:
``` cd your_folder_path ```
``` pyinstalled --onefile --noconsole your_file_name.py ``` (if you havent changed it, file name should be display.py)

then, open the folder, you should see multiple files created. Head into dist, and you will find your .exe file!
you can copy it anywhere, without having to copy any other file.
__you can also put it in C:\Users\your_user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup if you want it to automatically run in startup__

__if you ever want to close the app, go to system tray, find the app, right click and click exit__
