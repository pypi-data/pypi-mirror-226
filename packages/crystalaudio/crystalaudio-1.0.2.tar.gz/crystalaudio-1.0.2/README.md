# CrystalAudio

CrystalAudio is a Python package that provides a simple way to play audio files on different operating systems without displaying any player windows. It utilizes system-specific methods to achieve smooth audio playback.

## Installation

You can install CrystalAudio using pip:
pip install crystalaudio

## Usage
CrystalAudio supports Windows, Linux, and MacOS. It automatically detects the operating system and plays the audio file using the appropriate method.

## Note
On Windows, CrystalAudio uses the ctypes library to control audio playback.
On Linux, CrystalAudio relies on the aplay utility for audio playback.
On MacOS, CrystalAudio utilizes the afplay utility for audio playback.