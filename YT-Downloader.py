import os
import yt_dlp
from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox 
import time
import threading
from threading import Event
import sys

# YT-Downloader script

def YoutubeDownload(url, outputFormat):

        global isDownloading
        
        try:

            if(folder_entry.get() == ""):
                path = os.path.join(os.getcwd(), 'downloads')
                os.makedirs(path, exist_ok=True)
            else:
                path = folder_entry.get() 
            
            # Options used for the download
            yt_options = {
                "progress_hooks": [callable_hook],
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                'ffmpeg_location': resource_path("ffmpeg.exe"),
                'format': 'bestvideo[vcodec^=avc1][height<=1080]+bestaudio[acodec^=mp4a]/best[ext=mp4]',    # Default 1080p for max quality
                'merge_output_format': 'mp4',
            }
        
            # Controlling for the selected output format
            if outputFormat == 'mp4 [Best Quality]':
                yt_options.update({
                    'format': 'bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[ext=mp4]',
                })
            elif outputFormat == 'mp4 [1080p MAX]':
                yt_options.update({
                    'format': 'bestvideo[vcodec^=avc1][height<=1080p]+bestaudio[acodec^=mp4a]/best[ext=mp4]'
                })
            elif outputFormat == 'mp4 [720p MAX]': 
                yt_options.update({
                    'format': 'bestvideo[vcodec^=avc1][height<=720p]+bestaudio[acodec^=mp4a]/best[ext=mp4]',
                })
            elif outputFormat == 'mp3 [BEST]':
                yt_options.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'merge_output_format': 'mp3',
            }   )
            elif outputFormat == 'mp3 [WORST]':
                yt_options.update({
                    'format': 'worstaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'merge_output_format': 'mp3',
            }   )
                

            with yt_dlp.YoutubeDL(yt_options) as youtubeDownloader:
                youtubeDownloader.download(url)
            
        except Exception as e:
            isDownloading = False
            downloadingLabel.config(text = "Download failed. Retry with another link or verify that the entered link is correct.")
            download_button.config(text="Download video!")
            time.sleep(2) 
            downloadingLabel.config(text = "")
            return

        isDownloading = False    
        downloadingLabel.config(text = "Download completed!")
        download_button.config(text="Download video!")
        time.sleep(2) 
        downloadingLabel.config(text = "")


# Hook used to show download percentage in the GUI
def callable_hook(response):

    global isDownloading

    if(isDownloading == False):
        sys.exit()

    if response["status"] == "downloading":
        downloaded_percent = (float(response["downloaded_bytes"])*100)/float(response["total_bytes"])
        downloadingLabel.config(text=f"Downloading.... ({int(downloaded_percent)}%)")


# Function used to start the thread with the function download_youtube_video 
def startDownloadThread():
    global isDownloading

    if(isDownloading == True):
        
        if(messagebox.askyesno("Warning", "Do you want to stop the download of the video/playlist?") == True):
            isDownloading = False
            downloadingLabel.config(text = "")
            download_button.config(text="Scarica video!")

        return

    isDownloading = True
    downloadingLabel.config(text = "Downloading....")
    download_button.config(text="Stop Download")
    t = threading.Thread(target=YoutubeDownload, args=(url_entry.get(), comboBox.get())).start()


# Function for selecting folder
def selectFolder():
    selectedPath = filedialog.askdirectory()

    if(selectedPath != ""):
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

    window = Tk()   
    window.geometry("700x400")
    window.iconbitmap(resource_path("icon.ico"))
    window.grid_columnconfigure(0, weight=1)
    window.resizable(width=False, height=False)
    window.title("YT Downloader - Public Build []")

    window.configure(background="gray58")

    # Title and image section
    titleLabel = Label(window,text="Welcome! enter the link of the video or videos you want to download:", font=("Comic Sans MS", 15), background="gray58", foreground="black")
    titleLabel.grid(row="1", column="0")

    mainImage = PhotoImage(file=resource_path("AppImage.png"))
    mainImageLabel = Label(window, image=mainImage, background="gray58")
    mainImageLabel.grid(row="0", column="0", pady=25)

    # Input video URL da scaricare
    url_entry = Entry(font=("Comic Sans MS", 12), background="lightcyan4")
    url_entry.grid(row="2", column="0", pady=8, padx=8, sticky="WE", ipady=8)


    # Combo box for choosing output format of the downloaded vid
    choices = ["mp4 [Best Quality]", "mp4 [1080p MAX]", "mp4 [720p MAX]", "mp3 [BEST]", "mp3 [WORST]"]
    comboBox = ttk.Combobox(window, values = choices, state="readonly")
    comboBox.set("mp4 [Best Quality]") # Default value
    comboBox.grid(row="3", column="0", sticky=E, padx=20, ipadx=20)

    # Select path
    folder_entry = Entry()
    folder_entry.grid(row="3", column="0", sticky=W, padx=20, ipady=4, ipadx=40)
    
    folder_button = Button(text="Select destination path", command=selectFolder)
    folder_button.grid(row="4", column="0", sticky=W, padx=20)

    # Downloading label
    downloadingLabel = Label(window, text="", font=("Impact", 15), background="gray58", foreground="black")
    downloadingLabel.grid(row="5", column="0", pady=20)

    download_button = Button(window, text="Download video!", font=("Papyrus"), command=startDownloadThread)
    download_button.grid(row="3", column="0")

    window.mainloop()        
