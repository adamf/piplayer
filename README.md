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

Example `/etc/asound.conf`

```
pcm.!default {
    type hw
    card "Device"
    device 0
}

ctl.!default {
    type hw
    card "Device"
}
```

This works for the USB device:
```
# aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: vc4hdmi0 [vc4-hdmi-0], device 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: Device [USB Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 2: vc4hdmi1 [vc4-hdmi-1], device 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```
