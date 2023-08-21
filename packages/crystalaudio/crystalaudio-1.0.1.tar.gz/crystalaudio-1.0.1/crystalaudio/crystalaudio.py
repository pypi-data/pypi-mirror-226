import platform

#3verlaster

class CrystalPlay:
    def __init__(self, file_path):
        self.file_path = file_path
        self.play()

    def play(self):
        system = platform.system()
        print(f"[DEBUG] System:{system}")

        if system == "Windows":
            self.play_windows()
        elif system == "Linux":
            self.play_linux()
        elif system == "Darwin":
            self.play_macos()
        else:
            print("Unsupported operating system")

    def play_windows(self):
        try:
            import ctypes
            winmm = ctypes.windll.winmm
            alias = "audio_alias"
            winmm.mciSendStringW(f"open \"{self.file_path}\" alias {alias}", None, 0, 0)
            winmm.mciSendStringW(f"play {alias} wait", None, 0, 0)
            winmm.mciSendStringW(f"close {alias}", None, 0, 0)
        except ImportError:
            print("ctypes module not available")

    def play_linux(self):
        try:
            import subprocess
        except ImportError:
            print("subprocess module not available")
        try:
            subprocess.run(["aplay", self.file_path], check=True)
        except subprocess.CalledProcessError:
            print("CalledProcessError")

    def play_macos(self):
        try:
            subprocess.run(["afplay", self.file_path], check=True)
        except subprocess.CalledProcessError:
            print("CalledProcessError")
