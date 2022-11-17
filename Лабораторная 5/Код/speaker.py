from document import Folder, Document
from voice import Voice
import os


class Speaker:
    def __init__(self):
        self.__voice = Voice()
        self.__path = "data"

    def get_name(self):
        print("🔊: Which one ?")
        self.__voice.speak("Which one ?")

    def list(self):
        folder = Folder(self.__path)
        names = [file for file in folder]
        text = f"I know {str(', ').join(names[:-1])} and {names[-1]}"
        print(f"🔊: {text}")
        self.__voice.speak(text)

    def read(self, name: str):
        if name in [file for file in Folder(self.__path)]:
            document = Document(self.__path + "/" + name + ".txt")
            for line in document:
                print(f"🔊: {line}")
                self.__voice.speak(line)
        else:
            print(f"🔊: I don't know it")
            self.__voice.speak(f"I don't know it")

    def open(self, name: str):
        if name in [file for file in Folder(self.__path)]:
            print(f"🔊: Here's the {name}")
            self.__voice.speak(f"Here's the {name}")
            os.system(f"notepad.exe data/{name}.txt")
        else:
            print(f"🔊: I don't know it")
            self.__voice.speak(f"I don't know it")

    # def unknown(self):
    #     print(f"🔊: I can't understand")
    #     self.__voice.speak(f"I can't understand")
