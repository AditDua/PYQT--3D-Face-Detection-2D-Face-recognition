import tempfile
import os
import hashlib
from tqdm import tqdm
from zipfile import ZipFile
from urllib.request import urlopen


def get_file(origin, file_hash, is_zip=False):
    tmp_file = os.path.join(tempfile.gettempdir(), "FaceIDLight", origin.split("/")[-1])
    os.makedirs(os.path.dirname(tmp_file), exist_ok=True)
    if not os.path.exists(tmp_file):
        download = True
    else:
        hasher = hashlib.sha256()
        with open(tmp_file, "rb") as file:
            for chunk in iter(lambda: file.read(65535), b""):
                hasher.update(chunk)
        if not hasher.hexdigest() == file_hash:
            print(
                "A local file was found, but it seems to be incomplete or outdated because the file hash does not "
                "match the original value of " + file_hash + " so data will be downloaded."
            )
            download = True
        else:
            download = False

    if download:
        response = urlopen(origin)
        with tqdm.wrapattr(
            open(tmp_file, "wb"),
            "write",
            miniters=1,
            desc="Downloading " + origin.split("/")[-1] + " to: " + tmp_file,
            total=getattr(response, "length", None),
        ) as file:
            for chunk in response:
                file.write(chunk)
            file.close()
    if is_zip:
        with ZipFile(tmp_file, "r") as zipObj:
            zipObj.extractall(tmp_file.split(".")[0])
        tmp_file = os.path.join(tmp_file.split(".")[0])
    return tmp_file


def get_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(65535), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
