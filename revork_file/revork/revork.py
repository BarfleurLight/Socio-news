import os
import shutil

from aiogram import types, Bot
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageOps

from revork_file.counter.counter import Counter

START_DIR = Path("revork_file/start/")
RESULT_DIR = Path("revork_file/result/")


class RevorkFile:
    def __init__(self, file_name, start_dir=START_DIR, result_dir=RESULT_DIR):
        self.file_name = file_name[0]
        self.old_name = file_name[1].split('.')[0]
        self.error = '_(Повреждён)'
        self.START_DIR = start_dir
        self.RESULT_DIR = result_dir

    def treatment(self):
        """Определение метода обработки и запуск обработки"""
        ras = self.file_name.split('.')[1]
        ls = {
            "pdf": self._pdf,
            "jpg": self._image,
            "png": self._image,
            "zip": self._zip_7z,
        }
        return ls.get(ras, self._dont_supported)()

    @staticmethod
    def _move(func):
        def wrapper(self):
            try:
                func(self)
            except Exception as ex:
                new_name = self.old_name + self.error + '.' +\
                           self.file_name.split('.')[1]
                os.rename(self.START_DIR/self.file_name,
                          self.START_DIR/new_name)
                self.file_name = new_name
                Counter().decrease_count(self.file_name)
            shutil.move(self.START_DIR/self.file_name,
                        self.RESULT_DIR/self.file_name)
            return self.file_name
        return wrapper

    @_move
    def _dont_supported(self):
        self.error = '_(Не поддерживается)'
        raise Exception

    @_move
    def _pdf(self):
        reader = PdfReader(self.START_DIR/self.file_name)
        writer = PdfWriter()

        with open(self.START_DIR/self.file_name, "wb",) as f:
            writer.append_pages_from_reader(reader)
            writer.add_metadata(
                {
                    "/Author": "Socio",
                    "/Producer": "None",
                    "/Title": f"socio_doc"
                }
            )
            writer.write(f)

    @_move
    def _image(self):
        with Image.open(self.START_DIR/self.file_name) as img:
            # Переводим фтографию в RGB
            img = img.convert("RGB")
            # Контраст
            cmyk_img = ImageOps.autocontrast(img, preserve_tone=True)
            # Размер
            cmyk_img = ImageOps.contain(cmyk_img, (1600, 1600), method=Image.LANCZOS)
            # Сохранение
            cmyk_img.save(self.START_DIR/self.file_name, quality="web_high")

    @_move
    def _zip_7z(self):
        # Подготовить имя папки
        direct = self.file_name.split('.')
        # Распаковать содержимое архива в новую директорию
        shutil.unpack_archive(self.START_DIR/self.file_name,
                              self.START_DIR/direct[0])
        # Для каждого файла в директории выполнить обработку
        # walk итератор всех вложеных файлов
        for adress, dirs, files in os.walk(self.START_DIR/direct[0]):
            for name in files:
                new_name = Counter().get_name(name)
                os.rename(Path(adress)/name, Path(adress)/new_name)
                RevorkFile([new_name, name], Path(adress), Path(adress)).treatment()

        os.remove(self.START_DIR/self.file_name)
        shutil.make_archive(self.START_DIR/direct[0], 'zip', self.START_DIR/direct[0])
        shutil.rmtree(self.START_DIR/direct[0])


if __name__ == '__main__':
    pass