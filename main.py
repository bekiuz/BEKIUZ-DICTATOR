import tkinter as tk
from tkinter import ttk
import threading, subprocess, webbrowser

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None
try:
    import speech_recognition as sr
except ImportError:
    sr = None

class DictatorApp:
    def __init__(self, root):
        self.root = root
        root.title("BEKIUZ DICTATOR")
        root.geometry("720x520")
        root.configure(bg="#10111b")
        ttk.Style().theme_use("clam")
        tk.Label(root, text="BEKIUZ DICTATOR", fg="#a99bff", bg="#10111b",
                 font=("Segoe UI", 20, "bold")).pack(pady=(18, 4))
        tk.Label(root, text="Voice-controlled Windows assistant • Prototype",
                 fg="#aab0c5", bg="#10111b").pack()
        self.status = tk.StringVar(value="Ready")
        tk.Label(root, textvariable=self.status, fg="#8ee6bb", bg="#10111b").pack(pady=8)
        self.log = tk.Text(root, height=14, bg="#191b29", fg="#e8e9f2",
                          insertbackground="white", relief="flat", wrap="word")
        self.log.pack(fill="both", expand=True, padx=20, pady=8)
        self.log.insert("end", "Bekiuz Dictator tayyor. Buyruq yozing yoki Listen bosing.\n")
        bottom = tk.Frame(root, bg="#10111b")
        bottom.pack(fill="x", padx=20, pady=14)
        self.entry = ttk.Entry(bottom)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _e: self.submit())
        ttk.Button(bottom, text="Send", command=self.submit).pack(side="left", padx=6)
        ttk.Button(bottom, text="Listen", command=self.listen_thread).pack(side="left")
        try:
            self.engine = pyttsx3.init() if pyttsx3 else None
        except Exception:
            self.engine = None

    def say(self, text):
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass

    def add(self, text):
        self.log.insert("end", text + "\n")
        self.log.see("end")

    def submit(self):
        cmd = self.entry.get().strip()
        self.entry.delete(0, "end")
        if cmd:
            self.handle(cmd)

    def listen_thread(self):
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        if not sr:
            self.root.after(0, lambda: self.add("SpeechRecognition o'rnatilmagan."))
            return
        try:
            recog = sr.Recognizer()
            with sr.Microphone() as source:
                self.root.after(0, lambda: self.status.set("Listening..."))
                recog.adjust_for_ambient_noise(source, duration=0.5)
                audio = recog.listen(source, timeout=5, phrase_time_limit=12)
            text = recog.recognize_google(audio, language="uz-UZ")
            self.root.after(0, lambda: self.handle(text))
        except Exception as err:
            self.root.after(0, lambda: self.add("Mikrofon/ovoz xatosi: " + str(err)))
        finally:
            self.root.after(0, lambda: self.status.set("Ready"))

    def handle(self, command):
        self.add("Siz: " + command)
        cmd = command.lower()
        reply = "Bu buyruq hali qo'shilmagan."
        if any(k in cmd for k in ("notepad", "bloknot", "запис")):
            subprocess.Popen(["notepad.exe"]); reply = "Notepad ochildi."
        elif any(k in cmd for k in ("calculator", "kalkulyator", "калькулятор")):
            subprocess.Popen(["calc.exe"]); reply = "Kalkulyator ochildi."
        elif any(k in cmd for k in ("browser", "brauzer", "internet")):
            webbrowser.open("https://www.google.com"); reply = "Brauzer ochildi."
        elif cmd in ("salom", "hello", "привет"):
            reply = "Salom! Bekiuz Dictator ishga tayyor."
        self.add("Dictator: " + reply)
        self.say(reply)

if __name__ == "__main__":
    root = tk.Tk()
    DictatorApp(root)
    root.mainloop()
