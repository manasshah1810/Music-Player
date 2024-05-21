import tkinter as tk
from tkinter import messagebox
import youtube_dl
import os

def download_music(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'aac',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join('C:\\xampp\\htdocs\\MusicPlayer\\Music', '%(title)s.%(ext)s'),
        'verbose': True,  # Add the --verbose flag
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        messagebox.showinfo("Success", "Audio downloaded successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download audio: {str(e)}")

def download_button_clicked():
    video_url = entry.get()
    if video_url:
        download_music(video_url)
    else:
        messagebox.showwarning("Warning", "Please enter a YouTube video URL.")

# Create the main window
root = tk.Tk()
root.title("YouTube Audio Downloader")
root.configure(bg='black')  # Set background color to black

# Create a label
label = tk.Label(root, text="Enter YouTube Video URL:", fg='white', bg='black')  # Set text color to white and background color to black
label.pack()

# Create an entry widget
entry = tk.Entry(root, width=50)
entry.pack()

# Create a download button
download_button = tk.Button(root, text="Download", command=download_button_clicked, bg='white', fg='black')  # Set background color to white and text color to black
download_button.pack()

# Run the Tkinter event loop
root.mainloop()
