#!/usr/bin/env python
import json
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
from pynput import keyboard
from glob import glob
from just_playback import Playback
from threading import Timer
import threading
import time


# On OS X, install portaudio and pyaudio, or playback is pretty slow.
# brew install ffmpeg portaudio && pip install pyaudio

MUSIC_DIR = "./music/"


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
        self.timer = PlayerTimer(100, self.next_track)
        self.timer.start()
        self.track_time_remaining = 0

    def load_playlist(self):
        for mp3_file in sorted(glob(self.music_dir + "*.mp3")):
            if mp3_file not in self.playlist:
                self.playlist.append(mp3_file)

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


def on_press(key, player):
    try:
        if key.char == 'p':
            if player.player.playing:
                player.pause()
                print("paused")
            else:
                print("playing")
                player.play()
        if key.char == 'n':
            player.next_track()

    except AttributeError as e:
        print(e)
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


player = Player(MUSIC_DIR)

with keyboard.Listener(
    on_press=lambda event: on_press(event, player),
    on_release=on_release) as listener:
    listener.join()








