from __future__ import annotations
from formatting import colour_block, rgb_to_hex
from capture import grab_screen_data
from analysis import sample_rgb_fixed_grid, sample_rgb_grid_random, sample_rgb_random
#from comms import open_serial_com
from colours import get_colour_name
from config import TICK_RATE

import time
import tkinter as tk
import threading

SIGNAL_ON = str("ON\n")
SIGNAL_OFF = str("OFF\n")

BG = "#efefef"
TEXT = "#111111"
GREEN = "#58a93f"
RED = "#c0392b"
SWATCH = "#000000"

class ControllerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Controller")
        self.root.geometry("430x480")
        self.root.resizable(False, False)
        self.root.configure(bg = BG)

        self.status_on = False
        self.sampling_mode = "Fixed Grid"

        self.current_name = "Black"
        self.current_rgb = (0, 0, 0)
        self.current_hex = "#000000"

        self.running = False
        self.output_enabled = False
        self.worker_thread = None

        self.build_ui()
        self.refresh_display()

    def build_ui(self):
        main = tk.Frame(self.root, bg = BG)
        main.pack(fill = "both", expand = True, padx = 28, pady = 28)

        top = tk.Frame(main, bg = BG)
        top.pack(fill = "x", pady = (10, 20))

        self.swatch = tk.Label(
            top,
            bg = SWATCH,
            width = 8,
            height = 8,
            relief = "flat",
            bd = 0
        )
        self.swatch.pack(side = "left", padx = (0, 14))

        info = tk.Frame(top, bg = BG)
        info.pack(side = "left", anchor = "n")

        self.name_label = tk.Label(
            info, text = "Black", bg = BG, fg = TEXT,
            font = ("Arial", 20)
        )
        self.name_label.pack(anchor = "w")

        self.rgb_label = tk.Label(
            info, text = "RGB: (0, 0, 0)", bg = BG, fg = TEXT,
            font = ("Arial", 16)
        )
        self.rgb_label.pack(anchor = "w")

        self.hex_label = tk.Label(
            info, text = "HEX: #000000", bg = BG, fg = TEXT,
            font = ("Arial", 16)
        )
        self.hex_label.pack(anchor = "w")

        self.mode_label = tk.Label(
            main,
            text = "Detection Mode: Fixed Grid",
            bg = BG, fg = TEXT,
            font = ("Arial", 16)
        )
        self.mode_label.pack(anchor = "w")

        status_row = tk.Frame(main, bg = BG)
        status_row.pack(anchor = "w", pady = (0, 28))

        status_prefix = tk.Label(
            status_row,
            text = "Status:",
            bg = BG, fg = TEXT,
            font = ("Arial", 16)
        )
        status_prefix.pack(side = "left")

        self.status_value = tk.Label(
            status_row,
            text = "ON",
            bg = BG, fg = TEXT,
            font = ("Arial", 16)
        )
        self.status_value.pack(side = "left", padx = (6, 0))

        buttons = tk.Frame(main, bg = BG)
        buttons.pack(fill = "x", pady = (8, 0))

        left_col = tk.Frame(buttons, bg = BG)
        left_col.pack(side = "left", padx = (32, 34), anchor = "n")

        right_col = tk.Frame(buttons, bg = BG)
        right_col.pack(side = "left", anchor = "n")

        self.on_button = tk.Button(
            left_col,
            text = "ON",
            font = ("Arial", 16),
            width = 8,
            relief = "raised",
            bd = 3,
            command = self.turn_on
        )
        self.on_button.pack(pady = (0, 8))

        self.off_button = tk.Button(
            left_col,
            text = "OFF",
            font = ("Arial", 16),
            width = 8,
            relief = "raised",
            bd = 3,
            command = self.turn_off
        )
        self.off_button.pack()

        self.random_button = tk.Button(
            right_col,
            text = "Random",
            font = ("Arial", 16),
            width = 12,
            relief = "raised",
            bd = 3,
            command = lambda: self.set_mode("Random")
        )
        self.random_button.pack(pady = (0, 8))

        self.fixed_grid_button = tk.Button(
            right_col,
            text = "Fixed Grid",
            font = ("Arial", 16),
            width = 12,
            relief = "raised",
            bd = 3,
            command = lambda: self.set_mode("Fixed Grid")
        )
        self.fixed_grid_button.pack(pady = (0, 8))

        self.random_grid_button = tk.Button(
            right_col,
            text = "Grid Random",
            font = ("Arial", 16),
            width = 12,
            relief = "raised",
            bd = 3,
            command = lambda: self.set_mode("Grid Random")
        )
        self.random_grid_button.pack()

    def refresh_display(self):
        r, g, b = self.current_rgb

        self.name_label.config(text = self.current_name)
        self.rgb_label.config(text = f"RGB: ({r:03d}, {g:03d}, {b:03d})")
        self.hex_label.config(text = f"HEX: {self.current_hex}")
        self.mode_label.config(text = f"Detection Mode: {self.sampling_mode}")
        self.status_value.config(
            text = "ON" if self.status_on else "OFF",
            fg = GREEN if self.status_on else RED
        )
        self.swatch.config(bg = self.current_hex)

    def turn_on(self):
        if not self.running:
            self.output_enabled = True
            self.running = True
            self.worker_thread = threading.Thread(target = self.sampling_loop,
                                                  daemon = True)
            self.worker_thread.start()
            #self.serial_send_on_signal()
            self.status_on = True
            self.refresh_display()

    def turn_off(self):
        self.output_enabled = False
        self.running = False
        self.status_on = False
        #self.serial_send_off_signal()
        self.refresh_display()

    def set_mode(self, mode: str) -> None:
        self.sampling_mode = mode
        self.refresh_display()

    def sampling_loop(self):
        tick = time.monotonic()

        while self.running:
            if not self.output_enabled:
                break

            img = grab_screen_data()
            width, height = img.size

            if self.sampling_mode == "Random":
                self.current_rgb = sample_rgb_random(img, width, height)
            elif self.sampling_mode == "Grid Random":
                self.current_rgb = sample_rgb_grid_random(img, width, height)
            elif self.sampling_mode == "Fixed Grid":
                self.current_rgb = sample_rgb_fixed_grid(img, width, height)
            else:
                raise ValueError(f"Unknown sampling mode: {self.sampling_mode!r}")
            
            self.current_hex = rgb_to_hex(self.current_rgb)
            self.current_name = get_colour_name(self.current_rgb)

            if not self.output_enabled:
                break

            #self.serial_send_rgb(self.current_rgb)

            print(self.current_rgb, self.current_hex, colour_block(self.current_rgb))
            self.root.after(0, self.refresh_display)

            tick += TICK_RATE
            sleep_time = tick - time.monotonic()
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                tick = time.monotonic()

    """
    def serial_send_rgb(self, rgb):
        if not self.output_enabled:
            return

        r, g, b = rgb
        line = f"{r},{g},{b}\n"
        #ser.write(line.encode("utf-8"))

    def serial_send_on_signal(self):
        ser.write(SIGNAL_ON.encode("utf-8"))

    def serial_send_off_signal(self):
        ser.write(SIGNAL_OFF.encode("utf-8"))
    """

if __name__ == "__main__":
    root = tk.Tk()
    app = ControllerUI(root)
    root.mainloop()
