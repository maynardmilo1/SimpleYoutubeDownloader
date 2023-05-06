import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
import re
import os
from moviepy.editor import AudioFileClip

def choose_directory():
    global download_directory
    download_path = filedialog.askdirectory()

    download_directory.set(download_path)
    # update the download directory indicator label
    download_directory_label.configure(text="Download Directory: {}".format(download_path))


def start_download():
    link = link_entry.get()
    download_path = download_directory.get()
    format_choice = format_var.get()
    # check if a link is entered
    if not link:
        message_label.configure(text="Error: Please enter a valid YouTube link.")
        return

    # check if a download directory is set
    if not download_path:
        message_label.configure(text="Error: Please choose a download directory.")
        return
    
    try:
        yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
     
        # get the video with the highest resolution and download as video
        if format_choice == "video":
            stream = yt.streams.get_highest_resolution()
            stream.download(download_path)
        if format_choice == "audio":
            stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            # downloads the file as webm temporarily
            stream.download(download_path)
            # convert the downloaded audio file to mp3 format
            webm_file_path = os.path.join(download_path, stream.default_filename)
            mp3_file_path = os.path.splitext(webm_file_path)[0] + '.mp3'
            audio = AudioFileClip(webm_file_path)
            audio.write_audiofile(mp3_file_path)
            audio.close()
            # removes the webm file
            os.remove(webm_file_path)
            
        
        # display the success message
        message_label.configure(text="Successfully downloaded the youtube video in {} format".format(format_choice))

    except Exception as e:
        # display the error message
        message_label.configure(text="Error: {}".format(str(e)))


def validate_url(url):
    # check if the URL is valid
    if not url:
        return False
    pattern = re.compile(r"(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+(&\S*)?$")
    return pattern.match(url)

# create the main window
window = tk.Tk()
window.title("YouTube Downloader")
window.resizable(width=False, height=False)

# get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# calculate x and y coordinates to center the window
x = (screen_width / 2) - (600 / 2)
y = (screen_height / 2) - (250 / 2)
window.geometry('600x250+{}+{}'.format(int(x), int(y)))

# create the label for the link entry
link_label = ttk.Label(window, text="Enter the Youtube Link: ")
link_label.grid(row=0, column=0, padx=10, pady=10)

# create the entry for the link
link_entry = ttk.Entry(window, validate="focusout", validatecommand=(window.register(validate_url), '%P'), width = 70)
link_entry.grid(row=0, column=1, padx=10, pady=10)

# create the label for the download format option
format_label = ttk.Label(window, text="Choose Format: ")
format_label.grid(row=1, column=0, padx=10, pady=10)

# create the radio button options for the download format
format_var = tk.StringVar(value="audio")
mp3_radio = ttk.Radiobutton(window, text="Audio(MP3)", variable=format_var, value="audio")
mp3_radio.grid(row=1, column=1, padx=10, pady=10)
mp4_radio = ttk.Radiobutton(window, text="Video(MP4)", variable=format_var, value="video")
mp4_radio.grid(row=2, column=1, padx=10, pady=10)

# create the button for choosing the download directory
directory_button = ttk.Button(window, text="Choose Directory", command=choose_directory)
directory_button.grid(row=3, column=0, padx=10, pady=10)

# create the label for the download directory indicator
download_directory = tk.StringVar()
download_directory_label = ttk.Label(window, text="Download Directory: Not Set")
download_directory_label.grid(row=3, column=1, padx=10, pady=10)

# create the button for starting the download
download_button = ttk.Button(window, text="Download", command=start_download)
download_button.grid(row=5, column=0, padx=10, pady=10)

# create the label for the download status
message_label = ttk.Label(window, text="")
message_label.grid(row=5, column=1, padx=10, pady=10)
window.minsize(600, 250)
window.mainloop()