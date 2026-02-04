from utils.constants import MAX_FILE_SIZE


def check_file_size(file) -> bool:
    file.stream.seek(0, 2)
    size = file.stream.tell()

    file.stream.seek(0)

    if size > MAX_FILE_SIZE:
        return True

    return False
