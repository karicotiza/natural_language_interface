import IPython.display as ipd
import playsound
import datetime
# import time

from fairseq.checkpoint_utils import load_model_ensemble_and_task
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface


class Voice:
    def __init__(self, test: bool = False):
        self.__path = "models/fastspeech2-en-ljspeech/"
        if test:
            self.__path = "models/fastspeech2-en-200_speaker-cv4/"
        self.__models, self.__cfg, self.__task = self.__load_model()

        self.__model = self.__models[0]
        TTSHubInterface.update_cfg_with_data_cfg(self.__cfg, self.__task.data_cfg)
        self.__generator = self.__task.build_generator(self.__models, self.__cfg)

    def __load_model(self):
        return load_model_ensemble_and_task(
            [self.__path + "pytorch_model.pt"],
            arg_overrides={
                "data": self.__path,
                "vocoder": "hifigan",
                "fp16": False,
            }
        )

    def speak(self, text: str):
        sample = TTSHubInterface.get_model_input(self.__task, text + ".")
        wav, rate = TTSHubInterface.get_prediction(self.__task, self.__model, self.__generator, sample)

        time_ = datetime.datetime.now()
        time_ = str().join([digit for digit in str(time_) if digit.isdigit()])

        with open(f'{time_}.wav', 'wb') as file:
            file.write(ipd.Audio(wav, rate=rate).data)

        playsound.playsound(f'{time_}.wav')

        # time.sleep(len(text) * 0.005)
