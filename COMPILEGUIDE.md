###### GUIDE of HOW TO COMPILE the script into a single .exe file #####
<br>
<br>
To compile the script into a single file, you need to use the <a href="https://pypi.org/project/pyinstaller">Pyinstaller Library</a>.<br>
Then, execute the following command from CMD: <i></i><br>

```
pyinstaller YT-Downloader.py --onefile --noconsole --add-data="AppImage.png;." --add-data="icon.ico;." --add-binary="ffmpeg.exe;." --icon=icon.ico
```
Obviously, all the files used to compile the program into a single .exe need to be in the same location of the YT-Downloader script (remember to install ffmpeg.exe from <a href="https://github.com/yt-dlp/FFmpeg-Builds/wiki/Latest">here</a>

<br><br> WARNING: If during pyinstaller compiling the process fails, try to add the folder to antivirus exceptions, because due to temp folders created when using pyinstaller the antivirus might block the process
