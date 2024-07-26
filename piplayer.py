#!/usr/bin/env python
import json
from time import sleep
from glob import glob
from just_playback import Playback
import threading
import time
import keyboard
import os

MUSIC_DIR = "/home/music/music/"

class PlayerTimer(threading.Timer):
    started_at = None
    def start(self):
        self.started_at = time.time()
        threading.Timer.start(self)
    def elapsed(self):
        return time.time() - self.started_at
    def remaining(self):
        return self.interval - self.elapsed()

class Player():
    playlist = []
    player = None
    music_dir = None
    timer = None
    track_time_remaining = 0

    def __init__(self, music_dir):
        self.player = Playback()
        self.music_dir = music_dir
        self.load_playlist()
        self.track_time_remaining = 0

    def load_playlist(self):
        for mp3_file in sorted(glob(self.music_dir + "*.mp3")):
            if mp3_file not in self.playlist:
                self.playlist.append(mp3_file)

        to_remove = []
        for mp3_file in self.playlist:
            if not os.path.exists(mp3_file):
                to_remove.append(mp3_file)

        for mp3_file in to_remove:
            self.playlist.remove(mp3_file)

    def pause(self):
        print("pause", self.timer.remaining(), self.timer.elapsed())
        self.track_time_remaining = self.timer.remaining()
        self.timer.cancel()
        self.player.pause()


    def play(self):
        print("play")
        if self.player.paused:
            print("play, but we are paused")
            self.player.resume()
            self.timer = PlayerTimer(self.track_time_remaining, self.next_track)
            self.timer.start()
        else:
            self.next_track()

    def next_track(self):
        print("next_track")
        mp3_file = self.playlist.pop(0)
        print(mp3_file)
        self.playlist.append(mp3_file)
        self.player.load_file(mp3_file)
        self.player.play()
        if self.timer:
            self.timer.cancel()
        self.timer = PlayerTimer(self.player.duration, self.next_track)
        self.timer.start()
        self.load_playlist()
    
def on_release(key, player):
    if key == 'play':
        if player.player.playing:
            player.pause()
            print("paused")
        else:
            print("playing")
            player.play()
    if key == 'next' or not player.player.active:
        player.next_track()


player = Player(MUSIC_DIR)

keyboard.add_hotkey('a', on_release, args=['play', player])
keyboard.add_hotkey('b', on_release, args=['next', player])

keyboard.wait('esc')







