import sounddevice as sd
import soundfile as sf
import threading

class AudioRecorder:
    def __init__(self, filename='temp_audio.wav'):
        self.filename = filename
        self.recording = False
        self.thread = None

    def _record(self):
        with sf.SoundFile(self.filename, mode='w', samplerate=44100,
                          channels=1, format='WAV') as file:
            with sd.InputStream(samplerate=44100, channels=1, callback=lambda indata, frames, time, status: file.write(indata.copy())):
                while self.recording:
                    sd.sleep(100)

    def start(self):
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop(self):
        self.recording = False
        self.thread.join()