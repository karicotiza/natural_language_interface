import sounddevice as sd
import datetime

from transformers import pipeline
from scipy.io.wavfile import write


class Listener:
    def __init__(self):
        self.__pipe = pipeline("automatic-speech-recognition", "models/wav2vec2-base-960h")

    def listen(self):
        frequency = 44400
        duration = 5

        print("🖊️: Recording started")

        recording = sd.rec(
            int(duration * frequency),
            samplerate=frequency,
            channels=2
        )

        time_ = datetime.datetime.now()
        time_ = str().join([digit for digit in str(time_) if digit.isdigit()])
        file = f"{time_}.wav"

        sd.wait()

        write(file, frequency, recording)

        recognized_text = self.__recognize(file).lower()
        print(f"🎙: {recognized_text}")
        return recognized_text

    def __recognize(self, file: str):
        return self.__pipe(file)["text"].lower()
