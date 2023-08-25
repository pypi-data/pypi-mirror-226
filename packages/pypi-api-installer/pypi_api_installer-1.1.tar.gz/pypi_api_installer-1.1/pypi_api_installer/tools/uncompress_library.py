import tarfile


def uncompress_library (tar_gz_file:str, dst_path:str):
    file_path = tar_gz_file
    with tarfile.open(file_path, 'r:gz') as tar:
        tar.extractall(path=dst_path)