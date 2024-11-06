import os
import zipfile
from pathlib import Path

def create_zip_archive(archive_name, list_files, list_dirs):
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_STORED) as zipf:
        for file in list_files:
            file_path = Path(file)
            if file_path.is_file():
                zipf.write(file_path, arcname=file_path.relative_to(file_path.parent))
                print(f"Добавлен файл: {file_path}")
            else:
                print(f"Файл не найден и не будет добавлен: {file_path}")

        for directory in list_dirs:
            dir_path = Path(directory)
            if dir_path.is_dir():
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_full_path = Path(root) / file
                        if '__pycache__' in file_full_path.parts: continue
                        arcname = file_full_path.relative_to(dir_path.parent)
                        zipf.write(file_full_path, arcname=arcname)
                        print(f"Добавлен файл: {file_full_path}")
            else:
                print(f"Директория не найдена и не будет добавлена: {dir_path}")

def main():
    list_files = [
        'compile_zip_archive.py',
        'main.py',
        'requirements.txt',
        'start.bat',
        'start_install.bat',
    ]

    list_dirs = [
        'assets',
        'class_utility',
        'data_utility',
        'flet_utility',
        'logger_utility',
        'sql_utility'
    ]

    archive_name = 'containers_farm.zip'

    create_zip_archive(archive_name, list_files, list_dirs)
    print(f"ZIP архив создан: {archive_name}")

if __name__ == "__main__":
    main()
