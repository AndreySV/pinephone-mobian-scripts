# powerkey-reboot

If GUI is not working, then only hard reset is possible to restore phone functions.
Hard reset can be triggered by holding power button for a long time.
This could potentially cause filesystem corruption or
problems with internal flash in modem. To avoid all these problems correct shutdown is recommended.

This simple service allows reboot pinephone in case GUI is not working (phosh/phoc crash or driver issue)
by just pressing power button for 5 seconds. After 5 seconds device will vibrate to indicate that
normal reboot process is started and user should not hold power button anymore to avoid hard reset.

# install
copy powerkey-reboot.service into /etc/systemd/system
copy powerkey_reboot.py into /home/mobian/bin/
systemctl daemon-reload
systemctl enable powerkey-reboot.service
systemctl start  powerkey-reboot.service
