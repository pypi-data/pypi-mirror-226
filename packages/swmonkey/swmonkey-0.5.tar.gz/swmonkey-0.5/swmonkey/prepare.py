import os
from .util import get_out_dir


def clean():
    output_dir = get_out_dir()
    # clear all files under output_dir
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
