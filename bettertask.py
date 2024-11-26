import pyautogui
import keyboard
import time
from PIL import Image, ImageGrab
import json
import os
from datetime import datetime
import customtkinter as ctk
import threading
from tkinter import messagebox
from pynput import mouse, keyboard as kb
from pynput.keyboard import Key, KeyCode
import sys
import emoji

class BetterTask:
    def __init__(self):
        self.recording = []
        self.is_recording = False
        self.is_playing = False
        self.infinite_loop = False
        self.watch_point = None
        self.last_pixel = None
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        
    def start_recording(self):
        if self.is_recording:
            return
        self.recording = []
        self.is_recording = True
        self.start_time = time.time()
        
        def on_click(x, y, button, pressed):
            if not pressed or not self.is_recording:
                return
            current_time = time.time() - self.start_time
            self.recording.append({
                'time': current_time,
                'x': x,
                'y': y,
                'action': 'click',
                'button': str(button)
            })
            
        def on_press(key):
            if not self.is_recording:
                return
            if hasattr(key, 'char'):
                current_time = time.time() - self.start_time
                self.recording.append({
                    'time': current_time,
                    'key': key.char,
                    'action': 'key'
                })
        
        self.mouse_listener = mouse.Listener(on_click=on_click)
        self.keyboard_listener = kb.Listener(on_press=on_press)
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
    def stop_recording(self):
        self.is_recording = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
    def set_watch_point(self):
        pos = pyautogui.position()
        self.watch_point = (pos.x, pos.y)
        screenshot = ImageGrab.grab()
        self.last_pixel = screenshot.getpixel(self.watch_point)
        return f"Watch point set at {self.watch_point}"

    def check_pixel_changed(self):
        if not self.watch_point:
            return False
        screenshot = ImageGrab.grab()
        current_pixel = screenshot.getpixel(self.watch_point)
        return current_pixel != self.last_pixel

    def play_recording(self):
        if not self.recording:
            return "No recording to play!"

        self.is_playing = True
        
        def play():
            while self.is_playing:
                start_time = time.time()
                
                for action in self.recording:
                    if not self.is_playing:
                        break
                    
                    while (time.time() - start_time) < action['time']:
                        time.sleep(0.001)
                    
                    if action['action'] == 'click':
                        pyautogui.click(action['x'], action['y'])
                    elif action['action'] == 'key':
                        pyautogui.press(action['key'])
                    
                    if self.watch_point and self.check_pixel_changed():
                        self.is_playing = False
                        break
                
                if self.infinite_loop and self.is_playing:
                    continue
                else:
                    break
            
            self.is_playing = False
        
        threading.Thread(target=play, daemon=True).start()

    def stop_playback(self):
        self.is_playing = False

    def save_recording(self, filename):
        if not self.recording:
            return "No recording to save!"
            
        with open(filename, 'w') as f:
            json.dump(self.recording, f)
        return f"Recording saved to {filename}"

    def load_recording(self, filename):
        if not os.path.exists(filename):
            return "Recording file not found!"
            
        with open(filename, 'r') as f:
            self.recording = json.load(f)
        return f"Recording loaded from {filename}"

class BetterTaskGUI:
    def __init__(self):
        self.app = BetterTask()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.window = ctk.CTk()
        self.window.title("BetterTask")
        self.window.geometry("500x750")
        self.window.resizable(False, False)
        self.window.grid_columnconfigure(0, weight=1)
        
        self.record_emoji = emoji.emojize("🔴")  
        self.play_emoji = emoji.emojize("▶️")    
        self.stop_emoji = emoji.emojize("⏹️")   
        self.target_emoji = emoji.emojize("🎯")  
        
        self.title_label = ctk.CTkLabel(
            self.window,
            text="BetterTask",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=20)
        
        self.status_frame = ctk.CTkFrame(self.window)
        self.status_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Status: Ready",
            font=("Helvetica", 12)
        )
        self.status_label.pack(pady=10)
        
        self.controls_frame = ctk.CTkFrame(self.window)
        self.controls_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.record_button = ctk.CTkButton(
            self.controls_frame,
            text=f"{self.record_emoji} Start Recording",
            command=self.toggle_recording,
            height=40,
            font=("Helvetica", 12)
        )
        self.record_button.pack(pady=10, padx=20, fill="x")
        
        self.play_button = ctk.CTkButton(
            self.controls_frame,
            text=f"{self.play_emoji} Play Recording",
            command=self.play_recording,
            height=40,
            font=("Helvetica", 12)
        )
        self.play_button.pack(pady=10, padx=20, fill="x")
        
        self.stop_button = ctk.CTkButton(
            self.controls_frame,
            text=f"{self.stop_emoji} Stop Playback",
            command=self.stop_playback,
            height=40,
            font=("Helvetica", 12)
        )
        self.stop_button.pack(pady=10, padx=20, fill="x")
        
        self.watch_frame = ctk.CTkFrame(self.window)
        self.watch_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.watch_label = ctk.CTkLabel(
            self.watch_frame,
            text="Watch Point: Not Set",
            font=("Helvetica", 12)
        )
        self.watch_label.pack(pady=10)
        
        self.set_watch_button = ctk.CTkButton(
            self.watch_frame,
            text=f"{self.target_emoji} Set Watch Point (3s)",
            command=self.set_watch_point,
            height=40,
            font=("Helvetica", 12)
        )
        self.set_watch_button.pack(pady=10, padx=20, fill="x")
        
        # Infinite loop toggle
        self.infinite_loop_var = ctk.StringVar(value="off")
        self.infinite_loop_switch = ctk.CTkSwitch(
            self.window,
            text="🔄 Infinite Loop",
            variable=self.infinite_loop_var,
            onvalue="on",
            offvalue="off",
            command=self.toggle_infinite_loop,
            font=("Helvetica", 12)
        )
        self.infinite_loop_switch.grid(row=4, column=0, padx=20, pady=(0, 20))
        
        # Hotkeys frame
        self.hotkeys_frame = ctk.CTkFrame(self.window)
        self.hotkeys_frame.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        hotkeys_label = ctk.CTkLabel(
            self.hotkeys_frame,
            text="⌨️ Hotkeys",
            font=("Helvetica", 16, "bold")
        )
        hotkeys_label.pack(pady=10)
        
        hotkeys = [
            ("F5", "Start/Stop Recording"),
            ("F6", "Set Watch Point"),
            ("F7", "Stop Playback"),
            ("F8", "Toggle Infinite Loop"),
            ("F9", "Play Recording")
        ]
        
        for key, action in hotkeys:
            hotkey_label = ctk.CTkLabel(
                self.hotkeys_frame,
                text=f"{key}: {action}",
                font=("Helvetica", 12)
            )
            hotkey_label.pack(pady=5)
        
        keyboard.on_press_key('F5', lambda _: self.toggle_recording())
        keyboard.on_press_key('F6', lambda _: self.set_watch_point())
        keyboard.on_press_key('F7', lambda _: self.stop_playback())
        keyboard.on_press_key('F8', lambda _: self.infinite_loop_switch.toggle())
        keyboard.on_press_key('F9', lambda _: self.play_recording())
        
    def update_status(self, text):
        self.status_label.configure(text=f"Status: {text}")
        
    def toggle_recording(self):
        if not self.app.is_recording:
            self.app.start_recording()
            self.record_button.configure(text=f"{self.record_emoji} Stop Recording")
            self.update_status("Recording...")
        else:
            self.app.stop_recording()
            self.record_button.configure(text=f"{self.record_emoji} Start Recording")
            self.update_status("Recording stopped")
            
    def play_recording(self):
        result = self.app.play_recording()
        if result:
            self.update_status(result)
        else:
            self.update_status("Playing recording...")
            
    def stop_playback(self):
        self.app.stop_playback()
        self.update_status("Playback stopped")
        
    def set_watch_point(self):
        self.update_status("Move cursor to desired position (3s)...")
        self.window.after(3000, self._set_watch_point)
        
    def _set_watch_point(self):
        result = self.app.set_watch_point()
        self.watch_label.configure(text=result)
        self.update_status("Ready")
        
    def toggle_infinite_loop(self):
        self.app.infinite_loop = self.infinite_loop_var.get() == "on"
        self.update_status(f"Infinite loop: {self.infinite_loop_var.get()}")
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = BetterTaskGUI()
    gui.run()
