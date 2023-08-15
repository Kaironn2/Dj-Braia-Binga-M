import tkinter as tk
from tkinter import filedialog
import pygame
import os

class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")

        self.playlist = []
        self.current_index = 0

        self.play_button = tk.Button(root, text="Play", command=self.play)
        self.play_button.pack()

        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack()
        
        self.load_button = tk.Button(root, text="Load MP3", command=self.load_mp3)
        self.load_button.pack()

        self.volume_scale = tk.Scale(root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, label="Volume", command=self.set_volume)
        self.volume_scale.set(0.5)
        self.volume_scale.pack()

    def load_mp3(self):
        mp3_file = tk.filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if mp3_file:
            self.playlist.append(mp3_file)

    def play(self):
        if self.playlist:
            pygame.mixer.init()
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

if __name__ == "__main__":
    root = tk.Tk()
    mp3_player = MP3Player(root)
    root.mainloop()