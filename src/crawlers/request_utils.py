import os

import requests


def download_file(url: str, output_path: str, filename: str) -> None:
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    full_path = os.path.join(output_path, filename)
    img_data = requests.get(url).content
    with open(full_path, 'wb') as handler:
        handler.write(img_data)
