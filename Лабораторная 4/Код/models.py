import transformers

from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def predict(self, context: str) -> str:
        raise NotImplementedError


class WMT19RuEn(Model):
    def __init__(self):
        self.__model = transformers.AutoModelForSeq2SeqLM.from_pretrained("C://Storage//Net//wmt19-ru-en")
        self.__tokenizer = transformers.AutoTokenizer.from_pretrained("C://Storage//Net//wmt19-ru-en")

    def predict(self, context: str):
        translator = transformers.pipeline("translation", model=self.__model, tokenizer=self.__tokenizer)
        translate = translator(context)

        return translate[0].get("translation_text")


class OpusMTEnRu(Model):
    def __init__(self):
        self.__model = transformers.AutoModelForSeq2SeqLM.from_pretrained("C://Storage//Net//opus-mt-en-ru")
        self.__tokenizer = transformers.AutoTokenizer.from_pretrained("C://Storage//Net//opus-mt-en-ru")

    def predict(self, context: str):
        translator = transformers.pipeline("translation", model=self.__model, tokenizer=self.__tokenizer)
        translate = translator(context)

        return translate[0].get("translation_text")
