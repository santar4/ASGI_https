import gzip


def compress_response(data: str) -> bytes:
    return gzip.compress(data.encode('utf-8'))