# BEKIUZ DICTATOR

Windows desktop voice assistant prototype.

## Features
- Tkinter desktop UI
- Speech input via SpeechRecognition/Google (internet required)
- Windows text-to-speech via pyttsx3
- Safe starter commands: Notepad, Calculator, browser
- Typed commands

## Setup
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py main.py
```
Microphone recognition needs internet and a working mic. This prototype does not provide unrestricted computer control.