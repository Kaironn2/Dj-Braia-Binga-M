import tkinter as tk
from tkinter import filedialog
import pygame
import os

class DJBraiaBingaM:
    def __init__(self, root):
        self.root = root
        self.root.title("DJ Braia Binga M")         # window title

        self.playlist = []
        self.current_index = 0
        self.playing = False

        self.load_button = tk.Button(root, text="Load MP3", command=self.load_mp3)              # load mp3 button
        self.load_button.pack(pady=10)

        self.playlist_display = tk.Listbox(root, selectmode=tk.SINGLE, height=10, width=30)     # playlist
        self.playlist_display.pack()
        self.playlist_display.bind("<<ListboxSelect>>", self.update_current_index)
        
        self.current_song_label = tk.Label(root, text="Current Song:")                          # current song text
        self.current_song_label.pack()

        self.current_song_display = tk.Label(root, text="")                                     # current song
        self.current_song_display.pack()
        
        self.volume_scale = tk.Scale(root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, label="Volume", command=self.set_volume)    # volume
        self.volume_scale.set(0.5)
        self.volume_scale.pack()
        
        self.play_stop_frame = tk.Frame(root)
        self.prev_button = tk.Button(self.play_stop_frame, text="Previous", command=self.play_previous)     # previous button
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.play_button = tk.Button(self.play_stop_frame, text="Play", command=self.toggle_play_pause)     # play/pause button    
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.next_button = tk.Button(self.play_stop_frame, text="Next", command=self.play_next)             # next button
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.play_stop_frame.pack()


    def load_mp3(self):
        mp3_files = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        for mp3_file in mp3_files:
            self.playlist.append(mp3_file)
        self.update_playlist_display()

    def toggle_play_pause(self):
        if self.playlist:
            if not pygame.mixer.get_init():
                pygame.mixer.init()  # Inicialize o mixer se ainda não estiver inicializado
            if self.playing:
                pygame.mixer.music.pause()
                self.play_button.config(text="Play")
            else:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.load(self.playlist[self.current_index])
                    pygame.mixer.music.play()
                self.play_button.config(text="Pause")
            self.playing = not self.playing

    def play_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.play()

    def play_next(self):
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.play()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def play(self):
        if self.playlist:
            pygame.mixer.init()
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self.update_current_song_display()

    def update_playlist_display(self):
        self.playlist_display.delete(0, tk.END)
        for song in self.playlist:
            self.playlist_display.insert(tk.END, os.path.basename(song))

    def update_current_index(self, event):
        selected_index = self.playlist_display.curselection()
        if selected_index:
            self.current_index = selected_index[0]

    def update_current_song_display(self):
        if self.playlist:
            current_song = os.path.basename(self.playlist[self.current_index])
            self.current_song_display.config(text=current_song)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x500")            # window lenght
    dj_player = DJBraiaBingaM(root)
    root.mainloop()
