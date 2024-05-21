import os
import shutil
import pygame
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess

# Initialize Pygame
pygame.init()

# Colors
WHITE = "#FFFFFF"  # White color in hexadecimal format
BLACK = "black"    # Black color as a string
GREEN = "#00FF00"  # Green color in hexadecimal format

class PlaylistCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Playlist Creator")
        self.root.configure(bg=BLACK)

        # Connect to the MySQL database
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",      # Enter your MySQL username
            password="",      # Enter your MySQL password
            database="playlist_db"  # Enter the name of your database
        )

        # Create a cursor object to execute SQL queries
        self.cursor = self.db_connection.cursor()

        # Variables
        self.playlist_name = tk.StringVar()
        self.search_text = tk.StringVar()
        self.selected_songs = []

        # Frames
        self.playlist_frame = tk.Frame(self.root, bg=BLACK)
        self.playlist_frame.pack(pady=20)

        # Playlist Name Entry
        tk.Label(self.playlist_frame, text="Playlist Name:", fg=WHITE, bg=BLACK).grid(row=0, column=0, padx=10, pady=5)
        self.playlist_entry = tk.Entry(self.playlist_frame, textvariable=self.playlist_name, bg=BLACK, fg=WHITE)
        self.playlist_entry.grid(row=0, column=1, padx=10, pady=5)

        # Search Textbox
        self.search_entry = tk.Entry(self.playlist_frame, textvariable=self.search_text, bg=BLACK, fg=WHITE)
        self.search_entry.grid(row=1, column=0, padx=10, pady=5)
        
        # Search Button
        self.search_button = tk.Button(self.playlist_frame, text="Search", command=self.search, bg=BLACK, fg=WHITE)
        self.search_button.grid(row=1, column=1, padx=3, pady=5)

        # Song List Frame
        self.song_list_frame = tk.Frame(self.root, bg=BLACK)
        self.song_list_frame.pack(pady=10)

        # Create Playlist Button
        self.create_playlist_btn = tk.Button(self.root, text="Create Playlist", command=self.create_playlist, bg=BLACK, fg=WHITE)
        self.create_playlist_btn.pack(pady=10)

        # Load Songs
        self.load_songs()

    def load_songs(self):
        # Load songs from the directory
        self.songs = []
        current_directory = r'C:\xampp\htdocs\MusicPlayer\Music'
        if os.path.exists(current_directory):
            for file in os.listdir(current_directory):
                if file.endswith(".mp3"):
                    self.songs.append(file)

    def search(self):
        search_text = self.search_text.get().lower()
        self.clear_song_list_frame()

        for song in self.songs:
            if search_text.lower() in song.lower():
                song_frame = tk.Frame(self.song_list_frame, bg=BLACK)
                song_frame.pack(side="top", padx=10, pady=5, fill="x")
                tk.Label(song_frame, text=song, fg=WHITE, bg=BLACK).pack(side="left")
                tk.Button(song_frame, text="Add", command=lambda s=song: self.add_song_to_playlist(s), fg=BLACK, bg=GREEN).pack(side="right")

    def add_song_to_playlist(self, song):
        playlist_name = self.playlist_name.get()
        if not playlist_name:
            messagebox.showerror("Error", "Please enter a playlist name.")
            return

        if song in self.selected_songs:
            messagebox.showinfo("Info", "This song is already added to the playlist.")
            return

        self.selected_songs.append(song)

    def create_playlist(self):
        playlist_name = self.playlist_name.get()
        if not playlist_name:
            messagebox.showerror("Error", "Please enter a playlist name.")
            return

        if not self.selected_songs:
            messagebox.showerror("Error", "Please select at least one song for the playlist.")
            return

        # Create a table for playlist metadata (name and number of songs)
        create_playlist_table_query = f"CREATE TABLE IF NOT EXISTS playlists (id INT AUTO_INCREMENT PRIMARY KEY, playlist_name VARCHAR(255) UNIQUE NOT NULL, num_songs INT)"
        self.cursor.execute(create_playlist_table_query)
        self.db_connection.commit()

        # Insert playlist metadata into the table
        insert_playlist_query = f"INSERT INTO playlists (playlist_name, num_songs) VALUES (%s, %s)"
        self.cursor.execute(insert_playlist_query, (playlist_name, len(self.selected_songs)))
        self.db_connection.commit()

        # Create a new table for the playlist songs
        create_table_query = f"CREATE TABLE IF NOT EXISTS {playlist_name} (id INT AUTO_INCREMENT PRIMARY KEY, song_name VARCHAR(255) NOT NULL)"
        self.cursor.execute(create_table_query)
        self.db_connection.commit()

        # Insert songs into the playlist table
        for song in self.selected_songs:
            insert_song_query = f"INSERT INTO {playlist_name} (song_name) VALUES (%s)"
            self.cursor.execute(insert_song_query, (song,))
        self.db_connection.commit()

        # Create a folder for the playlist
        playlist_folder = os.path.join(os.getcwd(), playlist_name)
        if not os.path.exists(playlist_folder):
            os.makedirs(playlist_folder)

            # Copy selected songs into the playlist folder
            for song in self.selected_songs:
                song_path = os.path.join(os.getcwd(), r'C:\xampp\htdocs\MusicPlayer\Music', song)
                shutil.copy(song_path, playlist_folder)

            # Copy Music_Player.py into the playlist folder
            shutil.copy(os.path.join(r'C:\xampp\htdocs\MusicPlayer\Music', 'Music_Player.py'), playlist_folder)
            shutil.copy(os.path.join(r'C:\xampp\htdocs\MusicPlayer\Music', 'Music_Player_P.py'), playlist_folder)

        messagebox.showinfo("Success", "Playlist created successfully!")
        subprocess.Popen(["python", "Name.py"])
        exit()

    def clear_song_list_frame(self):
        for widget in self.song_list_frame.winfo_children():
            widget.destroy()

    def __del__(self):
        # Close the cursor and database connection
        self.cursor.close()
        self.db_connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistCreator(root)
    root.mainloop()
