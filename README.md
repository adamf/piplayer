# piplayer

Linux only.

This allows a keyboard to control some mp3s in a directory. Why? So I can have a three-button keyboard
connected to a raspi, and raspi connected to a speaker, and my 2 year old can push a button and play/pause/skip
as she sees fit.

Do all this as root on a Pi 5 with headless raspberry pi debian:

* Use python 3.12
* `pip install just_playback keyboard`
* edit `/etc/asound.conf` to set your default device (look with `aplay -l`)
* Copy the service file into /etc/systemd/<correct dir>
* Enable & start the service


