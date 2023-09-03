import os, shutil

from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageOps, ImageGrab


class RevorkFile:
    def __init__(self, file_name):
        self.file_name = file_name

    def treatment(self):
        """Определение метода обработки и запуск обработки"""
        ras = self.file_name.split('.')[1]
        ls = {
            "pdf": self._pdf,
            "jpg": self._image,
            "png": self._image,
            "zip": self._zip_7z,
            "7z": self._zip_7z,
            "txt": self._pdf,
        }
        ls[ras]()

    def _pdf(self):
        reader = PdfReader(f"revork_file/start/{self.file_name}")
        writer = PdfWriter()

        with open(f"revork_file/start/{self.file_name}", "wb",) as f:
            writer.append_pages_from_reader(reader)
            writer.add_metadata(
                {
                    "/Author": "None",
                    "/Producer": "None",
                    "/Title": f"{self.file_name.split('.')[0]}"
                }
            )
            writer.write(f)
        shutil.move(f'revork_file/start/{self.file_name}',
                    f'revork_file/result/{self.file_name}')

    def _image(self):
        with Image.open(f'../start/{self.file_name}') as img:
            img = img.convert("RGB")
            # img.load()
            # cmyk_img = ImageOps.autocontrast(img, preserve_tone=True)
            cmyk_img = ImageOps.contain(img, (1600, 1600), method=Image.LANCZOS)
            # cmyk_img = ImageOps.fit(cmyk_img, (1600, 1600), method=Image.LANCZOS, centering=(0.5, 0.5))
            # сохраним для сравнения
            cmyk_img.save('../start/test-autocontrast.jpeg', quality="web_high")
            # cmyk_img.show()




    def _zip_7z(self):
        pass


if __name__ == '__main__':
    RevorkFile('2023090307.jpg').treatment()