import hashlib
import requests
import os
import shutil
import zipfile

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

TEMP_PATH = 'TEMP_CT_GTFS.zip'
GTFS_PATH = 'CT_GTFS.zip'
GTFS_URL = 'https://data.calgary.ca/download/npk7-z3bj/application/zip'
GTFS_OUTPUT_DIR = 'CT_GTFS'

def download_file(url: str, path: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f'downloaded {url} -> {path}')
    else:
        print(f'failed to download file from {url}')

def hash_file(path: str) -> str:
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def write_hash_to_file(hash: str, path: str):
    with open(path, 'w') as f:
        f.write(hash)
    return path

def read_hash_from_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()
    
def update_gtfs():
    download_file(GTFS_URL, TEMP_PATH)
    gtfs_hash = hash_file(GTFS_PATH)
    temp_gtfs_hash = hash_file(TEMP_PATH)

    # ct_gtfs.zip does not need to be updated
    if gtfs_hash == temp_gtfs_hash:
        print(f'{TEMP_PATH} hash == {GTFS_PATH} hash !')
        os.remove(TEMP_PATH)
        return

    # remove existing ct_gtfs.zip and extracted directory
    os.remove(GTFS_PATH)
    print(f'removing {GTFS_PATH}')
    try:
        shutil.rmtree(GTFS_OUTPUT_DIR)
        print(f'removed directory {GTFS_OUTPUT_DIR}')
    except OSError as e:
        print(f'Error: {e.filename} - {e.strerror}.')

    os.rename(TEMP_PATH, GTFS_PATH)
    print(f'renamed {TEMP_PATH} to {GTFS_PATH}')

    unzip_file(GTFS_PATH, GTFS_OUTPUT_DIR)

def unzip_file(file_path: str, target_dir: str):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
    print(f'unzipped file {file_path} to directory {target_dir}')