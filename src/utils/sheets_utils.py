import pandas
import os
from src.utils.path_utils import create_path


def create_sheet(data, output_path: str, filename: str) -> str:
    create_path(output_path)
    full_path = os.path.join(output_path, filename)

    pandas.DataFrame(data).to_excel(full_path, index=False)

    return full_path
