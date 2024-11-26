# BetterTask

A lightweight screen automation tool inspired by TinyTask, with additional features for screen change detection.

## Features

- Record and replay mouse clicks
- Set watch points to detect screen changes
- Infinite loop option
- Save and load recordings
- Minimal resource usage

## Controls

- F5: Start Recording
- F6: Set Watch Point
- F7: Stop Playback
- F8: Stop Recording
- F9: Toggle Infinite Loop
- F10: Play Recording
- ESC: Exit

## Requirements

- Python 3.6+
- PyAutoGUI
- Keyboard
- Pillow

## Installation

1. Clone the repository:
```
git clone https://github.com/r3dc0dez/bettertask.git
cd bettertask
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Run the application:
```
python bettertask.py
```

## Usage

1. Press F5 to start recording your actions
2. Use mouse clicks to record actions
3. Press F8 to stop recording
4. (Optional) Press F6 to set a watch point for change detection
5. Press F10 to play the recording
6. Use F9 to toggle infinite loop mode

## Notes

- The tool monitors left click, right click, and enter key events
- When a watch point is set, the playback will stop if a pixel change is detected at that point
- Recordings can be saved and loaded for later use
