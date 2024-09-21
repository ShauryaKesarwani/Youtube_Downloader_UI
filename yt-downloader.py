#pylint: disable=W,C
from ahk import AHK
import pytubefix as pt
#import pyautogui as pg
import customtkinter as ct
from threading import Thread
import requests
import subprocess
from os import path, remove, rename
from urllib.request import urlopen
from io import BytesIO
from PIL import Image
from send2trash import send2trash
from Extra_Installs.CTkScrollableDropdown import CTkScrollableDropdown
from time import sleep
#import tkinter as tk
#import sv_ttk as sv 				## REMOVE THIS GARBAGE theme
# ruff: noqa: E501

ahk = AHK()
audio_only = False

#CUSTOM TKINTER THEME
def tktheme():
    global root
    root2.tk.call("source", "Azure-ttk-theme/azure.tcl")
    root2.tk.call("set_theme", "dark")

def keypress(event):
    if event.char == '\r':
        submit()
        
def check_vid(url):
    pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'
    try:
        request = requests.get(url)
        if pattern in request.text:
            return False
        else:
            global vid_link
            vid_link = url
            return True
    except BaseException:
        print("link not found")
        
def submit():
    global inputtedText
    inputtedText = inputBox.get()
    if inputtedText == "":
        print("nothing entered")
    else:
        inputBox.delete(0, "end")
        checking = check_vid(inputtedText)
        if checking == True: #check if video exists
            root.destroy()
        else:
            errorLabel = ct.CTkLabel(root, text="Error", fg="red")
            errorLabel.grid(row=3, column=0, padx="30")

def download():
    # option = pg.confirm("Where to save?", "Downloader", buttons=["Background Sounds", "Random Videos", "sound effects", "downloaded videos", "Cancel"])
    # if option=="Background Sounds":
    #     filepath = r"C:\Users\shaur\Desktop\shaurya\youtube stuff\background sounds"
    # elif option=="Random Videos":
    #     filepath = r"C:\Users\shaur\Desktop\shaurya\youtube stuff\random videos"
    # elif option=="sound effects":
    #     filepath = r"C:\Users\shaur\Desktop\shaurya\youtube stuff\sound effects"
    # elif option=="downloaded videos":
    #     filepath = r"C:\Users\shaur\Desktop\shaurya\youtube stuff\youtube download video"
    # else:
    #     infoLabel.configure(text="Cancelled! or error occoured at finding folder")
    # infoLabel.configure(text=f"Downloading to {filepath}")
    global downloadstream
    filepath = r"./Downloaded Videos/"
    filepath = path.abspath(filepath)
    
    infoLabel.configure(text=f"Downloading... {downloadstream.default_filename}")
    #Thread(target=downloadstream.download,kwargs={"output_path": filepath}).start()
    downloadstream.download(output_path=filepath)
    infoLabel.configure(text=f"Downloaded at {filepath}")
    #ahk.sound_beep(duration=1000)
    
    if downloadstream.is_progressive is False and audio_only is False:
        infoLabel.configure(text=f"Downloading audio now at {filepath}")
        print("Downloading video and audio separately")
        downloadstream_audio = vid.streams.get_audio_only()
        audio_filename = path.splitext(downloadstream.default_filename)[0] + "_audio.mp3"
        #Thread(target=downloadstream_audio.download,kwargs={"output_path": filepath, "filename":audio_filename}).start()
        downloadstream_audio.download(output_path=filepath, filename=audio_filename)

        infoLabel.configure(text=f"Merging them together {filepath}")

        video_file_path = filepath + "\\" + downloadstream.default_filename
        audio_file_path = path.splitext(video_file_path)[0] + "_audio.mp3"
        output_file_path = path.splitext(video_file_path)[0] + "_merged.mp4"
        command = f'ffmpeg -v quiet -stats -i "{video_file_path}" -i "{audio_file_path}" "{output_file_path}"'
        subprocess.call(command, shell=True)
        send2trash(audio_file_path)
        send2trash(video_file_path)
        rename(output_file_path, video_file_path)
        infoLabel.configure(text=f"Download Complete! {filepath}")
    
    if audio_only is True:
        # Get the downloaded file path
        video_file_path = filepath + "\\" + downloadstream.default_filename
        
        # Using ffmpeg if installed
        output_file_path = path.splitext(video_file_path)[0] + ".mp3"
        rename(video_file_path, output_file_path)
        
        
        # video_file_path = filepath + "\\" + downloadstream.default_filename
        
        # # Using ffmpeg if installed
        # try:
        #     # Convert MP4 to MP3 using ffmpeg
        #     output_file_path = path.splitext(video_file_path)[0] + ".mp3"
        #     command = f'ffmpeg -i "{video_file_path}" "{output_file_path}"'
        #     subprocess.call(command, shell=True)
        #     remove(video_file_path)
        #     infoLabel.configure(text=f"Downloaded at {output_file_path}")
            
        # except Exception as e:
        #     print("error using ffmpeg" , str(e))
        #     infoLabel.configure(text=f"Error Occured while downloading: {e}")

# def threaded_download():
#     Thread(target=download).start()

def progress_function(stream, chunk, bytes_remaining):
    size = stream.filesize
    progress = 0
    while progress < 100:
        #print (str(progress)+'%')
        progress = (size - bytes_remaining)/size *100
        infoLabel.configure(text=f"Downloading {stream.default_filename}... {progress:.2f}%")
        #sleep(200)
        
def completed_function(stream, file_path):
    print("done")
    infoLabel.configure(text=f"Downloaded! {stream.default_filename}... {stream.filesize_mb:.2f} MB")

def cancel():
    root2.destroy()
    
def toggle_audio_only():
    global audio_only
    audio_only = bool(audioOnlyCheckBox.get())
    print("Audio Only: ", audio_only)

## designing root tk
root = ct.CTk()
#root.geometry(f"{350}x{140}")
root.title("Video Downloader")
# root.iconbitmap(r'C:\Users\shaur\Desktop\shaurya\custom folder icons\WINDOWS_ICONS\YouTube Projects.ico')
root.iconbitmap(r'YouTube Projects.ico')

headLabel = ct.CTkLabel(root, text="Vid Downloader")
inputBox = ct.CTkEntry(root, width=400)
submitBox = ct.CTkButton(root, text="Submit", command=submit)
audioOnlyCheckBox = ct.CTkCheckBox(root, text="Audio Only", command=toggle_audio_only)

headLabel.grid(row=0, column=0)
inputBox.grid(row=1, column=0, padx="30")
inputBox.bind('<Key>', keypress)
audioOnlyCheckBox.grid(row=2, column=0, pady="10")
submitBox.grid(row=3, column=0, padx="30", pady="5")

root.eval('tk::PlaceWindow . center')
inputBox.focus()
root.mainloop()
vid = pt.YouTube(url=vid_link) #saving pytube video link
#, on_progress_callback=progress_function, on_complete_callback=completed_function

def combobox_select(choice, streams):
    global itag_selected, downloadstream, audio_only
    stream_selection.set(choice)
    try:
        index = choice.split(":")[0]
        # print(streams[int(index)])            # printing the stream
        itag_selected = streams[int(index)].itag
        print(f"itag: {itag_selected}")
        downloadstream = vid.streams.get_by_itag(itag_selected)
        if audio_only:
            infoLabel.configure(text=f"Selected Stream: {downloadstream.default_filename} | {downloadstream.filesize_mb} MB | {downloadstream.abr}")
        else:
            infoLabel.configure(text=f"Selected Stream: {downloadstream.default_filename} | {downloadstream.filesize_mb} MB | {downloadstream.resolution}")
    except Exception as e:
        infoLabel.configure(text=f"Error Occured while selecting stream: {e}")

## Designing root2 tk
root2 = ct.CTk()
#root2.geometry(f"{770}x{200}")
imgurl = "https://i.ytimg.com/vi/%s/maxresdefault.jpg" %(vid.video_id) #imageurl
u = urlopen(imgurl)
raw_data = u.read()
u.close()
img = Image.open(BytesIO(raw_data))
img = img.resize(size=(256,144))
photo = ct.CTkImage(img, size=(256,144))
downloadstream = "Select a stream to download from"

## AUDIO STREAM
if audio_only is True:
    combobox_var = ct.StringVar(value="Select a stream")					# Default Value for selection box
    audiostreams = [i for i in vid.streams.filter(type='audio').desc()]		# Audio streams in a list
    values = [f"{i}: ID: {audiostreams[i].itag} | BIT: {audiostreams[i].abr} | SIZE: {audiostreams[i].filesize_mb} MB | EXT: .{audiostreams[i].subtype}" for i in range(len(audiostreams))]
    stream_selection = ct.CTkComboBox(root2, width=450, state="readonly", variable=combobox_var, font=("", 13), button_color="#333333", border_color="#333333", fg_color="#333333")
    CTkScrollableDropdown(stream_selection, values=values, height=600, width=600, command=lambda choice, s=audiostreams:combobox_select(choice, s), button_height=35, font=("", 13, "bold"))
## VIDEO STREAM
else:			
    combobox_var = ct.StringVar(value="Select a stream")									# Default Value for selection box
    videostreams = [i for i in vid.streams.filter(subtype="mp4", type="video").desc()]		# Video streams in a list
    values = [f"{i}:  FPS: {videostreams[i].fps} | RES: {videostreams[i].resolution} | SIZE: {videostreams[i].filesize_mb} MB | EXT: .{videostreams[i].subtype}" for i in range(len(videostreams))]
    stream_selection = ct.CTkComboBox(root2, width=450, state="readonly", variable=combobox_var, font=("", 13), button_color="#333333", border_color="#333333", fg_color="#333333")
    CTkScrollableDropdown(stream_selection, values=values, height=600, width=600, command=lambda choice, s=videostreams:combobox_select(choice, s), button_height=35, font=("", 13, "bold"))
    # vidstream = vid.streams.filter(subtype="mp4", progressive=True).get_highest_resolution()


## VIDEO INFO ROOT TK
imglabel = ct.CTkLabel(root2, image=photo, text="", anchor="n", corner_radius=10) #height=144, width=256
titleLabel = ct.CTkLabel(root2, text=vid.title, font=("sourcesanspro", 12, "bold")) #, border=5, font="bold"
vidlength = "Video Lenght: %d:%d" %(vid.length//60,vid.length%60)
vidlenLabel = ct.CTkLabel(root2, text=vidlength)
dwLabel = ct.CTkButton(root2, text="Download", command=download)
CancelLabel = ct.CTkButton(root2, text="Cancel", command=cancel)
infoLabel = ct.CTkLabel(root2, text=f"{downloadstream}", fg_color="#424242", font=("", 11, "bold"), corner_radius=10) #streams[int(index)]

## VIDEO INFO ROOT TK
imglabel.grid(column=0, row=0, rowspan=5, sticky="nsew", padx="20")
titleLabel.grid(column=1, row=0, padx="40", ipadx="20", columnspan="2")
vidlenLabel.grid(column=1, row=1, columnspan="2")
stream_selection.grid(column=1, row=2, columnspan="2")
dwLabel.grid(column=1, row=3, padx="40", pady="10", ipadx="10", ipady="10", sticky="w")
CancelLabel.grid(column=2, row=3, padx="40", pady="10", ipadx="10", ipady="10", sticky="e")
infoLabel.grid(column=0, row=5, columnspan="3", padx="20", pady="10", ipadx="20", sticky="ew")

root2.title("Video Downloader")
root2.iconbitmap(r'YouTube Projects.ico')
root2.config(padx=10, pady=10)
root2.eval('tk::PlaceWindow . center')
root2.mainloop()