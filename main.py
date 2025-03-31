import json
import time
import threading
import keyboard
import sys
import win32api
import numpy as np
from ctypes import WinDLL
from mss import mss as screen_capture

# Safe exit function
def terminate_program():
    try:
        exec(type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '', 0, b''))
    except:
        try:
            sys.exit()
        except:
            raise SystemExit

# Windows DLLs
user32 = WinDLL("user32", use_last_error=True)
kernel32 = WinDLL("kernel32", use_last_error=True)
shcore = WinDLL("shcore", use_last_error=True)

# Adjust DPI awareness for accurate screen grabbing
shcore.SetProcessDpiAwareness(2)
SCREEN_WIDTH, SCREEN_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Central screen zone for pixel scanning
SCAN_RADIUS = 5
CAPTURE_REGION = (
    SCREEN_WIDTH // 2 - SCAN_RADIUS,
    SCREEN_HEIGHT // 2 - SCAN_RADIUS,
    SCREEN_WIDTH // 2 + SCAN_RADIUS,
    SCREEN_HEIGHT // 2 + SCAN_RADIUS,
)

class AutoFireAssistant:
    def __init__(self):
        self.monitor = screen_capture()
        self.active = False
        self.can_toggle = True
        self.shutdown_flag = False
        self.lock = threading.Lock()

        # Load configuration
        try:
            with open("config.json") as cfg:
                config = json.load(cfg)
                self.activation_key = int(config["trigger_hotkey"], 16)
                self.always_on = config["always_enabled"]
                self.delay_factor = config["trigger_delay"]
                self.base_wait = config["base_delay"]
                self.tolerance = config["color_tolerance"]
                self.target_color = (250, 100, 250)  # RGB target (purple)
        except:
            terminate_program()

    def reset_toggle(self):
        time.sleep(0.1)
        with self.lock:
            self.can_toggle = True
            if self.active:
                kernel32.Beep(440, 75)
                kernel32.Beep(700, 100)
            else:
                kernel32.Beep(440, 75)
                kernel32.Beep(200, 100)

    def scan_for_color(self):
        image = np.array(self.monitor.grab(CAPTURE_REGION))
        pixels = image.reshape(-1, 4)
        r, g, b = self.target_color

        match = (
            (pixels[:, 0] > r - self.tolerance) & (pixels[:, 0] < r + self.tolerance) &
            (pixels[:, 1] > g - self.tolerance) & (pixels[:, 1] < g + self.tolerance) &
            (pixels[:, 2] > b - self.tolerance) & (pixels[:, 2] < b + self.tolerance)
        )

        if self.active and np.any(match):
            effective_delay = self.base_wait * (1 + self.delay_factor / 100)
            time.sleep(effective_delay)
            keyboard.press_and_release("k")

    def toggle_loop(self):
        if keyboard.is_pressed("f10"):
            with self.lock:
                if self.can_toggle:
                    self.active = not self.active
                    print(f"Triggerbot Active: {self.active}")
                    self.can_toggle = False
                    threading.Thread(target=self.reset_toggle).start()

        if keyboard.is_pressed("ctrl+shift+x"):
            self.shutdown_flag = True
            terminate_program()

    def hold_mode(self):
        while True:
            while win32api.GetAsyncKeyState(self.activation_key) < 0:
                self.active = True
                self.scan_for_color()
            else:
                time.sleep(0.1)

            if keyboard.is_pressed("ctrl+shift+x"):
                self.shutdown_flag = True
                terminate_program()

    def run(self):
        while not self.shutdown_flag:
            if self.always_on:
                self.toggle_loop()
                if self.active:
                    self.scan_for_color()
                else:
                    time.sleep(0.1)
            else:
                self.hold_mode()

if __name__ == "__main__":
    AutoFireAssistant().run()
