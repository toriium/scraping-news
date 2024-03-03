import os

import requests

from src.utils.path_utils import create_path


def download_file(url: str, output_path: str, filename: str) -> None:
    create_path(path=output_path)

    full_path = os.path.join(output_path, filename)
    img_data = requests.get(url).content
    with open(full_path, 'wb') as handler:
        handler.write(img_data)
