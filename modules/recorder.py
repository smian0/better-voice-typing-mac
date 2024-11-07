import sounddevice as sd
import soundfile as sf
import threading
import numpy as np

# NOTE: Optimized settings for speech recording
# - 16kHz sample rate is optimal for STT, using 22.05kHz for safety margin
# - 16-bit depth is standard for speech
# - Mono channel as stereo provides no benefit
# - WAV format ensures compatibility and quality
# NOTE: Ends up being ~2.6 megabytes for every 60 seconds with these settings.

class AudioRecorder:
    # Controls how smooth/reactive the audio level indicator bar appears in the UI
    # (0.0 to 1.0) Higher = more responsive but jerky, Lower = more smooth, but slower
    # 0.2 provides a good balance between smoothness and responsiveness
    SMOOTHING_FACTOR = 0.2

    def __init__(self, filename='temp_audio.wav', level_callback=None):
        self.filename = filename
        self.recording = False
        self.thread = None
        self.level_callback = level_callback
        self.smoothed_level = 0.0

    def _calculate_level(self, indata):
        """Calculate audio level from input data"""
        # Get the RMS value from the audio data
        rms = np.sqrt(np.mean(np.square(indata)))
        # Convert to a log scale and normalize
        # -60 dB to 0 dB range mapped to 0.0 to 1.0
        db = 20 * np.log10(max(1e-10, rms))  # Avoid log(0)
        normalized = (db + 60) / 60  # Map -60..0 to 0..1
        current_level = max(0.0, min(1.0, normalized))  # Clamp to 0..1

        # Apply smoothing
        self.smoothed_level = (self.SMOOTHING_FACTOR * current_level) + ((1 - self.SMOOTHING_FACTOR) * self.smoothed_level)
        return self.smoothed_level

    def _record(self):
        def audio_callback(indata, frames, time, status):
            if self.level_callback:
                level = self._calculate_level(indata)
                self.level_callback(level)
            file.write(indata.copy())

        with sf.SoundFile(self.filename, mode='w', samplerate=22050,
                         channels=1, subtype='PCM_16', format='WAV') as file:
            with sd.InputStream(samplerate=22050, channels=1,
                              callback=audio_callback):
                while self.recording:
                    sd.sleep(100)

    def start(self):
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop(self):
        self.recording = False
        if self.thread:
            self.thread.join()