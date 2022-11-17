from listener import Listener
from speaker import Speaker


class Controller:
    def __init__(self):
        self.__listener = Listener()
        self.__speaker = Speaker()

        self.__command = {
            "list": self.__speaker.list,
            "read": self.__speaker.read,
            "open": self.__speaker.open,
        }

    def work(self):
        recognized_text = self.__listener.listen()
        recognized_text = "Can you read a poem ?"
        for key, function in self.__command.items():
            if key in recognized_text:
                if key in ["read", "open"]:
                    self.__speaker.get_name()
                    name = self.__listener.listen()
                    name = "dirge"
                    function(name)
                else:
                    function()
