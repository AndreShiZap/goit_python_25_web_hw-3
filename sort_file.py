# сортування файлів

import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging

"""
--source  - папка з файлами для сортування
--output  - папка з відсортованими файлами
"""

# обробка аргументів командного рядка
parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument("--source", type=str, help="Source folder", required=True)
parser.add_argument("--output", type=str, help="Output folder", default="dist")

args = vars(parser.parse_args())

source = args.get("source")  # папка з файлами для сортування
output = args.get("output")  # папка з відсортованими файлами
print(f"вихідна та кінцева папки: source = {source}, output = {output}")

folders = []

# створення списку підпапок вихідної папки з файлами для сортування
def list_folder(path: Path) -> None:
    for current_name in path.iterdir():
        if current_name.is_dir():
            folders.append(current_name)
            list_folder(current_name)

# копіювання файлів з вихідних папок до папок розширення
def copy_file(path: Path) -> None:
    for file_current in path.iterdir():
        if file_current.is_file():
            ext = file_current.suffix  # виділяємо розширення файлу
            new_path = output_folder / ext  # створюємо назву папки для розширення
            try:
                new_path.mkdir(exist_ok=True, parents=True)  # створюємо папку
                copyfile(file_current, new_path / file_current.name)
            except OSError as err:
                logging.error(err)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    base_folder = Path(source)
    output_folder = Path(output)
    folders.append(base_folder)
    list_folder(base_folder)  
    print(f"список усіх папок для сортування:\n {folders}")

    threads = []
    
    # створення окремого потоку для кожної вихідної папки зі списку folder
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)
    
    # очікування закінчення всіх потоків
    [th.join() for th in threads]

    print(f"Усі файли з папки '{source}' відсортовані.\nПапку '{source}' можна видалити")