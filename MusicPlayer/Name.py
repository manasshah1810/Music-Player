import tkinter as tk
import subprocess
from mutagen.mp3 import MP3
import os

def get_folder_names():
    current_directory = os.getcwd()
    folder_names = [folder for folder in os.listdir(current_directory) if os.path.isdir(folder) and folder != 'Music']
    return folder_names

def play_music_player(folder):
    playlist_folder_path = os.path.join(os.getcwd(), folder)
    music_player_path = os.path.join(playlist_folder_path, "Music_Player.py")
    subprocess.Popen(["python", music_player_path])

def create_playlist():
    subprocess.Popen(["python", "Playlists.py"])
    exit()

def on_folder_click(event):
    selected_indices = folder_listbox.curselection()
    if selected_indices:
        selected_index = selected_indices[0]
        selected_folder = folder_listbox.get(selected_index)
        song_list.delete(0, tk.END)
        for song, duration in get_song_info(selected_folder):
            song_list.insert(tk.END, f"{song} - {duration} minutes")
            song_list.song_paths.append(song)

def on_song_click(event):
    selected_indices = song_list.curselection()
    if selected_indices:
        selected_index = selected_indices[0]
        song_path = song_list.song_paths[selected_index]
        subprocess.Popen(["python", song_path])
        exit()

def get_song_info(folder):
    song_info = []
    folder_path = os.path.join(os.getcwd(), folder)
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                song_path = os.path.join(folder_path, file)
                audio = MP3(song_path)
                duration_minutes = int(audio.info.length // 60)
                song_info.append((file, duration_minutes))
    return song_info

def open_download_window():
    subprocess.Popen(["python", "download.py"])

root = tk.Tk()
root.title("Music Folders and Songs")
root.configure(bg="black")

# Folder List
folder_frame = tk.Frame(root, bg="black")
folder_frame.pack(side=tk.LEFT, padx=10, pady=10)
folder_label = tk.Label(folder_frame, text="Folders", font=("Arial", 12, "bold"), fg="white", bg="black")
folder_label.pack()
folder_listbox = tk.Listbox(folder_frame, width=30, height=20, bg="black", fg="white")
folder_listbox.pack()
for folder in get_folder_names():
    folder_listbox.insert(tk.END, folder)
folder_listbox.bind("<<ListboxSelect>>", on_folder_click)

# Song List
song_frame = tk.Frame(root, bg="black")
song_frame.pack(side=tk.RIGHT, padx=10, pady=10)
song_label = tk.Label(song_frame, text="Songs", font=("Arial", 12, "bold"), fg="white", bg="black")
song_label.pack()
song_list = tk.Listbox(song_frame, width=50, height=20, bg="black", fg="white")
song_list.pack()
song_list.bind("<<ListboxSelect>>", on_song_click)

# Store song paths
song_list.song_paths = []

# Create Playlist Button
create_playlist_button = tk.Button(root, text="Create Playlist", command=create_playlist, bg="black", fg="white")
create_playlist_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Play Button
play_button = tk.Button(root, text="Play", command=lambda: play_music_player(folder_listbox.get(tk.ACTIVE)), bg="black", fg="white")
play_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Download Music Button
download_button = tk.Button(root, text="Download Music", command=open_download_window, bg="black", fg="white")
download_button.pack(side=tk.BOTTOM, padx=10, pady=10)

root.mainloop()
