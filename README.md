# Cpu Temperature Monitor

Simple Python app (microservice) to read `/sys/class/thermal/thermal_zone0/temp` and write output to stdio or Redis server on a Raspberry Pi running Ubuntu Server 20.04 LTS. It is intended to be run from systemd as a service.

requires a running Redis server, Python 3.7+, Redis-py, e.g., pip install redis.

## installation as a systemd service

Assuming you are running this as `ubuntu` user, with a virtual environment setup under `~/.venvs/default/`, and your script is installed under `~/Projects/cpu_temp_monitor`,
add the following to your `/etc/systemd/system` folder, name it something sensible like `temperature-monitor.service`:

```
[Unit]
Description=Temperature Monitor Service
After=redis-server.service

[Service]
Type=simple
User=ubuntu
ExecStart=/home/ubuntu/.venvs/default/bin/python /home/ubuntu/Projects/cpu_temp_monitor/cpu_temp_monitor.py -r -f 10
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

After installation, run `sudo systemctl daemon-reload` to pick up the changes, then `sudo systemctl start temperature-monitor.service` (assuming that's the name you gave it).

You can be sure it's running by checking `sudo systemctl status temperature-monitor` and `sudo journalctl -u temperature-monitor` for details.

When satisfied that everything is working as intended, you can permanently install the temperature monitor by entering `sudo systemctl enable temperature-monitor-service`.

## License

Do what you want with this.
