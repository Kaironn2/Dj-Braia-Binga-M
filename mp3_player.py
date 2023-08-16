import tkinter as tk
from tkinter import filedialog
import pygame
import os

class DJBraiaBingaM:
    def __init__(self, root):
        self.root = root
        self.root.title("DJ Braia Binga M")

        self.playlist = []
        self.current_index = 0
        self.playing = False

        self.load_button = tk.Button(root, text="Load MP3", command=self.load_mp3)
        self.load_button.pack(pady=10)

        self.playlist_display = tk.Listbox(root, selectmode=tk.SINGLE, height=10, width=30)
        self.playlist_display.pack()
        self.playlist_display.bind("<<ListboxSelect>>", self.update_current_index)

        self.current_song_label = tk.Label(root, text="Current Song:")
        self.current_song_label.pack()

        self.current_song_display = tk.Label(root, text="")
        self.current_song_display.pack()

        self.volume_scale = tk.Scale(root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, label="Volume", command=self.set_volume)
        self.volume_scale.set(0.5)
        self.volume_scale.pack()

        self.play_stop_frame = tk.Frame(root)
        self.prev_button = tk.Button(self.play_stop_frame, text="Previous", command=self.play_previous)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.play_button = tk.Button(self.play_stop_frame, text="Play", command=self.toggle_play_pause)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.next_button = tk.Button(self.play_stop_frame, text="Next", command=self.play_next)
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
                pygame.mixer.init()
            
            if pygame.mixer.music.get_busy() and self.playing:
                pygame.mixer.music.pause()
                self.play_button.config(text="Play")
            elif pygame.mixer.music.get_busy() and not self.playing:
                pygame.mixer.music.unpause()
                self.play_button.config(text="Pause")
            else:
                self.play_music()
    
    def play_music(self):
        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play()
        self.play_button.config(text="Pause")
        self.playing = True
    
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
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self.update_current_song_display()

            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            self.check_music_end()

    def check_music_playing(self):
        if pygame.mixer.music.get_busy() and not self.playing:
            self.play_button.config(text="Pause")
            self.playing = True
        elif not pygame.mixer.music.get_busy() and self.playing:
            self.play_button.config(text="Play")
            self.playing = False
        self.root.after(100, self.check_music_playing)
        
    def check_music_end(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.play_next_auto()
        self.root.after(100, self.check_music_end)

    def play_next_auto(self):
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.play()
        else:
            pygame.mixer.music.stop()

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
    root.geometry("400x500")
    dj_player = DJBraiaBingaM(root)
    root.mainloop()
