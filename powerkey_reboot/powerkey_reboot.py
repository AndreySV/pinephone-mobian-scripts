#!/usr/bin/env python3

import evdev
import threading
import os
import sys
import time
import asyncio


def vibrate():
    # to avoid  RuntimeError: There is no current event loop in thread
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # find haptic device
    for name in evdev.list_devices():
        dev = evdev.InputDevice(name)
        if evdev.ecodes.EV_FF in dev.capabilities():
            break
    else:
        sys.stderr.write("Failed to find the haptic motor.\n")
        return

    rumble = evdev.ff.Rumble(strong_magnitude=0xff, weak_magnitude=0xffff)
    effect_type = evdev.ff.EffectType(ff_rumble_effect=rumble)
    duration_ms = 400
    effect = evdev.ff.Effect(
        evdev.ecodes.FF_RUMBLE,
        -1,  # id (set by ioctl)
        0,   # direction
        evdev.ff.Trigger(0, 0),           # no triggers
        evdev.ff.Replay(duration_ms, 0),  # length and delay
        effect_type
    )
    repeat_count = 1
    effect_id = dev.upload_effect(effect)

    # vibrate
    dev.write(evdev.ecodes.EV_FF, effect_id, repeat_count)
    time.sleep(duration_ms / 1000.0)
    dev.erase_effect(effect_id)


def reboot_device():
    print("power key pressed for a long time: rebooting...")
    vibrate()
    os.system("systemctl reboot -i")


def main():
    timeout = 5  # seconds

    # find device for power button
    for name in evdev.list_devices():
        dev = evdev.InputDevice(name)
        caps = dev.capabilities()
        if evdev.ecodes.EV_KEY in caps:
            if evdev.ecodes.KEY_POWER in caps[evdev.ecodes.EV_KEY]:
                break
    else:
        sys.stderr.write("Failed to find power button")

    for event in dev.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            if event.code == evdev.ecodes.KEY_POWER:
                if event.value == 1:
                    reboot_timer = threading.Timer(timeout, reboot_device)
                    reboot_timer.start()
                else:
                    reboot_timer.cancel()


if __name__ == "__main__":
    main()
