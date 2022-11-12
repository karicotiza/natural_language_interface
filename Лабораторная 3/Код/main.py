import sentence_extractor
import neural_api
import tkinter

from tqdm import tqdm
from pathlib import Path
from tkinter.scrolledtext import ScrolledText


class Window:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Реферирование")

        self._ = tkinter.Label(text="Путь к папке")
        self._.grid(
            row=0,
            column=0,
        )

        self.path = tkinter.Entry(
            width=80,
        )
        self.path.grid(
            row=0,
            column=1,
        )

        self.help = tkinter.Button(
            text="Помощь",
            command=self.__help,
            width=40,
        )
        self.help.grid(
            row=1,
            column=0,
            columnspan=2,
        )

        self.classic = tkinter.Button(
            text="Метод извлечения предложений",
            command=self.__sentence_extractor,
            width=40,
        )
        self.classic.grid(
            row=2,
            column=0,
            columnspan=2,
        )

        self.neural = tkinter.Button(
            text="Нейросетевой метод",
            command=self.__neural,
            width=40,
        )
        self.neural.grid(
            row=3,
            column=0,
            columnspan=2,
        )

        self.tags = tkinter.Button(
            text="Ключевые слова",
            command=self.__tags,
            width=40,
        )
        self.tags.grid(
            row=4,
            column=0,
            columnspan=2,
        )

        self.output = ScrolledText(
            width=120
        )

        self.output.grid(
            row=5,
            column=0,
            columnspan=2,
        )

        self.window.mainloop()

    def __print(self, text):
        self.output.insert(
            tkinter.INSERT,
            text + "\n"
        )

    @staticmethod
    def __save(path: str, mode: str, text: str):
        path_ = Path("saved", (path + mode + ".txt"))
        with open(path_, mode="w", encoding="utf-8") as file_:
            file_.write(text)

    def __get_path(self):
        return Path(self.path.get())

    def __help(self):
        self.__print(
            "Введите путь к папке в которой находятся файлы с расширением '.txt'\n" +
            "После этого нажмите кнопку в интересующим вас методом\n" +
            "Результаты работы программы появятся в поле ниже\n" +
            "Текст выведенный ниже - активный, его можно копировать и редактировать\n" +
            "Нейросетевой метод обращается к серверу для его работы нужен интернет\n" +
            "Также нейросетевой метод может выдать 'model is loading'\n" +
            "В таком случае подождите минуту и попробуйте снова\n"
        )

    def __sentence_extractor(self):
        folder_ = sentence_extractor.Folder(self.__get_path())
        crawler_ = sentence_extractor.Crawler(folder_)
        for summary in crawler_.get_summaries():
            self.__print(summary)
            self.__save(
                summary.split("\n")[0].split(": ")[1],
                "_extraction",
                summary
            )

    def __neural(self):
        folder_ = sentence_extractor.Folder(self.__get_path())

        for file_name in tqdm(folder_, desc="making request"):
            with open(file_name, mode="r", encoding="utf-8") as file_:
                memory = (
                    f"Файл: {file_name.stem}\n" +
                    f"Реферат: " + neural_api.NeuralAPI.summarize(
                        file_.read()
                    ) +
                    f"\nСсылка: {file_name}\n"
                )

            self.__print(memory)
            Window.__save(
                file_name.stem,
                "_Neural",
                memory
            )

    def __tags(self):
        folder_ = sentence_extractor.Folder(self.__get_path())
        for file_name in folder_:
            with open(file_name, mode="r", encoding="utf-8") as file_:
                dict_ = sentence_extractor.Document(file_.read()).get_counter()
                memory = (
                    f"Название: {file_name.stem}\n"
                    f"Ключевые слова: {str(sorted(dict_, key=dict_.get, reverse=True)[:10])}\n"
                    f"Ссылка: {file_name}\n"
                )

                self.__print(memory)
                Window.__save(
                    file_name.stem,
                    "_tags",
                    memory
                )


if __name__ == "__main__":
    window = Window()
