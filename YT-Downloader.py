import tkinter as tk
import platform
from tkinter import ttk, filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification # Toast notification
from ttkbootstrap.tooltip import ToolTip    # Tooltip for button
import sys
import os
import yt_dlp
import threading
import time

system = platform.system().lower() # Variable for the identification of the current OS 

import ttkbootstrap.localization
ttkbootstrap.localization.initialize_localities = bool


def YoutubeDownload(url, outputFormat, outputQuality):
    global isDownloading

    
    try:

        if (folder_entry.get() == ""):
            path = os.path.join(os.getcwd(), 'downloads')
            os.makedirs(path, exist_ok=True)
        else:
            path = folder_entry.get()

        # Options used for the download
        if(system == 'linux'):
            yt_options = {
            "progress_hooks": [callable_hook],
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'ffmpeg_location': resource_path("ffmpeg"),
            'format': 'bestvideo[vcodec^=avc1][height<=1080]+bestaudio[acodec^=mp4a]/best[ext=mp4]',
            'merge_output_format': 'mp4',
        }
        elif(system == 'windows'):

            yt_options = {
                "progress_hooks": [callable_hook],
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                'ffmpeg_location': resource_path("ffmpeg.exe"),
                'format': 'bestvideo[vcodec^=avc1][height<=1080]+bestaudio[acodec^=mp4a]/best[ext=mp4]',
                'merge_output_format': 'mp4',
            }
        else:
            print("ffmpeg not available for your system. Aborting....")


        # DEBUG PURPOSES ONLY
        print(f'OUTPUT FORMAT: {outputFormat}')
        print(f'OUTPUT QUALITY: {outputQuality}')
        
        # Selecting output format and quality
        if outputFormat in ('mp3', 'm4a', 'ogg', 'aac', 'opus'):
            yt_options.update({
                'format': 'bestaudio',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': f'{outputFormat}',
                    'preferredquality': '192',
                }],
                'merge_output_format': f'{outputFormat}',
            })


            if(outputQuality == 'Worst Quality'):
                yt_options.update({
                    'format': 'worstaudio',
                })
        else:
            
            if outputQuality == 'Best Quality':
                yt_options.update({'format': 'bestvideo+bestaudio/best',  
                    'merge_output_format': f'{outputFormat}',          
                })
            elif outputQuality == 'Worst Quality':
                yt_options.update({
                    'format': 'worstvideo+worstaudio/worst',  
                    'merge_output_format': f'{outputFormat}',             
                })
            else:

                outputQuality = outputQuality[:-1] # Removing the final character 'p' (ex: 1080p becomes only 1080)

                yt_options.update({
                    'format': f'bestvideo[height<={outputQuality}]+bestaudio/best[height<={outputQuality}]',
                    'merge_output_format': f'{outputFormat}',                                           
                })

        with yt_dlp.YoutubeDL(yt_options) as youtubeDownloader:

            youtubeDownloader.download(url)

    except Exception as e:
        # In case an error occurs ----
        isDownloading = False
        window.focus_force()
        failedNotification.show_toast()
        downloadingLabel.config(text="Download failed. Retry with another link or verify that the entered link is correct.")
        download_button.config(text="Download video!")
        time.sleep(2)
        downloadingLabel.config(text="")
        titleLabel.config(text="Enter the link of the videos or playlists you want to download")
        return

    isDownloading = False
    window.focus_force()
    successNotification.show_toast()
    downloadingLabel.config(text="Download completed!")
    download_button.config(text="Download video!")
    time.sleep(2)
    downloadingLabel.config(text="")
    titleLabel.config(text="Enter the link of the videos or playlists you want to download")


# Hook used to show download percentage in the GUI
def callable_hook(response):
    global isDownloading

    if (isDownloading == False):
        sys.exit()

    if response["status"] == "downloading":

        downloaded_percent = (float(response["downloaded_bytes"]) * 100) / float(response["total_bytes"])
        downloadProgress.config(value=int(downloaded_percent))

        video_title = response['info_dict'].get('title', None)
        titleLabel.config(text = f"Video Title: {video_title}")

        


# Function used to start the thread with the function download_youtube_video
def startDownloadThread():
    global isDownloading

    if (isDownloading == True):

        if tk.messagebox.askyesno("Warning", "You want to stop the download of the video/playlist?"):
            isDownloading = False
            downloadingLabel.config(text="")
            download_button.config(text="Download video!")
            downloadProgress.config(value=0)

        return

    isDownloading = True
    downloadingLabel.config(text="Downloading....")
    download_button.config(text="Stop Download")

    # Changing title label to the title of the video


    t = threading.Thread(target=YoutubeDownload, args=(url_entry.get(), comboBoxFormats.get(), comboBoxQuality.get())).start()


# Function for selecting folder
def selectFolder():
    selectedPath = filedialog.askdirectory()

    if (selectedPath != ""):
        folder_entry.delete(0, END)
        folder_entry.insert(0, selectedPath)


# Used to get a resource path if the searched file is bundled inside the .exe main application
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":

    isDownloading = False

    window = tb.Window(title="Youtube-Downloader [1.2.5]", themename="darkly", resizable=(False, False))

    window.iconphoto(False, (ImageTk.PhotoImage(Image.open(resource_path("icon.png")))))
    window.geometry("700x400")

    titleLabel = tk.Label(window, text="Enter the link of the videos or playlists you want to download:", font=("Comic Sans MS", 10),
                       background="gray58", foreground="black")
    titleLabel.grid(row="1", column="0")

    mainImage = tk.PhotoImage(file=resource_path("AppImage.png"))
    mainImageLabel = tk.Label(window, image=mainImage, background="gray58")
    mainImageLabel.grid(row="0", column="0", pady=25)

    # Input video URL to download
    url_entry = tb.Entry(font=("Comic Sans MS", 12), background="lightcyan4")
    url_entry.grid(row="2", column="0", pady=8, padx=8, sticky="WE", ipady=8)

    # Combo box for choosing output format of the downloaded vid
    choices = ["mp4", "mp3", "mpeg", "webm", "m4a", "ogg", "aac"]
    comboBoxFormats = tb.ttk.Combobox(window, values=choices, state="readonly")
    comboBoxFormats.set("mp4")  # Default value
    comboBoxFormats.grid(row="3", column="0", sticky=E, padx=20, ipadx=20)

    ToolTip(comboBoxFormats, text="Select to change output format", bootstyle=TOOLBUTTON)

    # Radio buttons for choosing the download quality

    choices = ["Best Quality", "Worst Quality", "1080p", "720p", "480p"]
    comboBoxQuality = tb.ttk.Combobox(window, values=choices, state="readonly", width=15)
    comboBoxQuality.grid(row="4", column="0", sticky=E, padx=20, ipadx=20)

    comboBoxQuality.set("Best Quality")

    ToolTip(comboBoxQuality, text="Select to change output quality", bootstyle=TOOLBUTTON)

    # Select path
    folder_entry = tb.Entry()
    folder_entry.grid(row="3", column="0", sticky=W, padx=10, ipady=4, ipadx=20)

    folder_button = tb.Button(text="Select destination", command=selectFolder, style="outline", width=15)
    folder_button.grid(row="4", column="0", sticky=W, padx=10)

    ToolTip(folder_button, text="Select the output's path.", bootstyle=TOOLBUTTON)


    # Download progress bar
    downloadProgress = tb.Progressbar(window, bootstyle="success", maximum=100, value=0, length=200)
    downloadProgress.grid(row=4)

    # Downloading label
    downloadingLabel = tk.Label(window, text="", font=("", 12), background="gray58", foreground="black")
    downloadingLabel.grid(row="5", column="0", pady=20)

    download_button = tb.Button(window, text="Download video!", command=startDownloadThread, width=20)
    download_button.grid(row="3", column="0")

    ToolTip(download_button, text="Click to start the download", bootstyle=TOOLBUTTON)

    # Toast notification download
    failedNotification = ToastNotification(title="YT-Downloader",
                                     message="The download of the video(s) failed.",
                                     duration=5000, icon="\u26A0", bootstyle=DANGER, alert=True)

    successNotification = ToastNotification(title="YT-Downloader",
                                     message="The video(s) download was completed.",
                                     duration=5000, icon="\u26A0", bootstyle=SUCCESS, alert=True)

    window.mainloop()
