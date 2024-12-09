import os
import time
from tqdm import tqdm
import shutil
import filetype

input_dir = "./contents" # 이곳을 contents 폴더 위치로 수정하거나 현재 위치에 contents 폴더를 넣어주세요.
output_dir = "./result"

def process_files(directory):
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    with tqdm(total=total_files, desc="Processing files", unit="file") as progress_bar:
        for root, _, files in os.walk(directory):
            for file_name in files:
                full_file_path = os.path.join(root, file_name)
                date_path = time.strftime("/%Y.%m.%d", time.localtime(os.path.getmtime(full_file_path)))
                file_type = filetype.guess(full_file_path)
                if file_type is not None:
                    extension = file_type.extension
                else:
                    extension = 'unknown'
                destination_dir = os.path.join(output_dir, date_path.strip('/'))
                os.makedirs(destination_dir, exist_ok=True)
                shutil.copy(full_file_path, os.path.join(destination_dir, f"{file_name}.{extension}"))
                progress_bar.update(1)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

process_files(input_dir)