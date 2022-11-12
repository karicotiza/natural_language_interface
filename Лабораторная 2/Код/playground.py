import main
import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Система")

        self._ = tk.Label(text="Введите путь к папке с файлами")
        self._.grid(column=0, row=0)

        self.path = tk.Entry(width=40)
        self.path.grid(column=0, row=1)

        self.help_button = tk.Button(text="Помощь", width=20, command=self.get_help)
        self.help_button.grid(column=0, row=2)

        self.languages_button = tk.Button(text="Определить языки", width=20, command=self.get_languages)
        self.languages_button.grid(column=0, row=3)

        self.text = scrolledtext.ScrolledText(width=120)
        self.text.grid(column=0, row=4)

        self.root.mainloop()

    def get_help(self):
        self.text.insert(
            tk.INSERT,
            "Введите путь к папке в которой находятся файлы с расширением '.pdf'\n" +
            "После этого нажмите кнопку 'Определить языки'\n" +
            "Результаты работы программы появятся в поле ниже\n" +
            "Для метода коротких слов верный ответ меньшая метрика\n" +
            "Для других методов верный ответ - большая метрика\n\n"
        )

    def get_languages(self):
        path = Path(self.path.get())
        for file in path.iterdir():
            if file.suffix == ".pdf":
                pdf = main.SearchImageOfDocument(file)
                self.text.insert(
                    tk.INSERT,
                    f"Название: {file.name}\n" +
                    f"Язык (Метод коротких слов): {pdf.detect_language(mode='short_words')}\n" +
                    f"Язык (Алфавитный метод): {pdf.detect_language(mode='alphabet')}\n" +
                    f"Язык (Нейросетевой метод): {pdf.detect_language(mode='neural')}\n" +
                    f"Ссылка: {file.absolute()}\n\n",
                )
                with open("info.txt", mode="a", encoding="utf-8") as info:
                    info.write(
                        f"Название: {file.name}\n" +
                        f"Язык (Метод коротких слов): {pdf.detect_language(mode='short_words')}\n" +
                        f"Язык (Алфавитный метод): {pdf.detect_language(mode='alphabet')}\n" +
                        f"Язык (Нейросетевой метод): {pdf.detect_language(mode='neural')}\n" +
                        f"Ссылка: {file.absolute()}\n\n"
                    )


window = Window()
