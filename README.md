# Batak

WIP

Raspberry Pi 4 buttons Batak.

Implemented in Python.

## systemd install

```bash
cd /etc/systemd/system
sudo ln -s /home/pi/dev/batak/configs/batak.service .
sudo systemctl enable batak.service
sudo systemctl start batak.service
```
## Go version

A Go version is in the pipeline, but not sure when.
First idea was to use Gobot but it's is too generic for RPi and it's easier to use direct package.

