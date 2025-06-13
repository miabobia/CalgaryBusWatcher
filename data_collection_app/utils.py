import hashlib
import requests
import zipfile

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

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

def unzip_file(file_path: str, target_dir: str):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
    print(f'unzipped file {file_path} to directory {target_dir}')