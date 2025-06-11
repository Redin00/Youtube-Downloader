## GUIDE of HOW TO COMPILE the script into a single executable file #####
<br>
<br>


To compile the script into a single file, you need to use the <a href="https://pypi.org/project/pyinstaller">Pyinstaller Library</a>.<br>
Then, execute the following command from terminal: <i></i><br>

### Both Windows & Linux
```
pyinstaller YT-Downloader.py --onefile --noconsole --add-data="AppImage.png":"." --add-data="icon.png":"." --add-binary="ffmpeg":"." --icon=icon.png --hidden-import='PIL._tkinter_finder'
```
Obviously, all the files used to compile the program into a single file need to be in the same location of the YT-Downloader script (remember to install ffmpeg binary from <a href="https://github.com/yt-dlp/FFmpeg-Builds/wiki/Latest">here</a>

<br><br> WARNING: If during pyinstaller compiling the process fails, try to add the folder to antivirus exceptions, because due to temp folders created when using pyinstaller the antivirus might block the process
