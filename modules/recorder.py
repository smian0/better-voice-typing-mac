import sounddevice as sd
import soundfile as sf
import threading

# NOTE: Optimized settings for speech recording
# - 16kHz sample rate is optimal for STT, using 22.05kHz for safety margin
# - 16-bit depth is standard for speech
# - Mono channel as stereo provides no benefit
# - WAV format ensures compatibility and quality
# NOTE: Ends up being ~2.6 megabytes for every 60 seconds with these settings.

class AudioRecorder:
    def __init__(self, filename='temp_audio.wav'):
        self.filename = filename
        self.recording = False
        self.thread = None

    def _record(self):
        with sf.SoundFile(self.filename, mode='w', samplerate=22050,
                          channels=1, subtype='PCM_16', format='WAV') as file:
            with sd.InputStream(samplerate=22050, channels=1, callback=lambda indata, frames, time, status: file.write(indata.copy())):
                while self.recording:
                    # Sleep to prevent CPU spinning while allowing audio callback to process
                    sd.sleep(100)

    def start(self):
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop(self):
        self.recording = False
        self.thread.join()