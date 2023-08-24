import base64
import gzip
from io import BytesIO

default_encoding = 'UTF-8'


def decode_gzip_base64_to_plain_base64(gz_content, encoding=default_encoding):
    """
    Convert a base64 encoded gzip-compressed string to a base64 encoded uncompressed string.

    Args:
    - gz_content (str): Base64 encoded gzip-compressed content.
    - encoding (str, optional): Encoding format of the uncompressed content. Defaults to 'UTF-8'.

    Returns:
    - str: Base64 encoded representation of the uncompressed content.
    """
    binary_data = base64.b64decode(gz_content)
    decompressed_content = gzip.decompress(binary_data)
    return base64.b64encode(decompressed_content).decode(encoding)


def write_to_original_file(gz_content, file_name, encoding='UTF-8'):
    """Uncompress a gzip-compressed file content or encoded content to original file.

        Args:
        - gz_content (str): The base64-encoded gzip compressed content.
        - file_name (str): The name of the file where the decompressed content will be written.
        - encoding (str, optional): The encoding of the decompressed content. Defaults to 'UTF-8'.

        """
    # Decode the base64 string and decompress using gzip
    binary_data = base64.b64decode(gz_content)
    decompressed_content = gzip.decompress(binary_data)

    # Decode the decompressed content with the desired encoding
    text_content = decompressed_content.decode(encoding)

    # Write the decoded content to the specified file in text mode
    with open(file_name, 'w', encoding=encoding) as f_out:
        f_out.write(text_content)


def compress_file_to_base64(file_name, encoding='UTF-8'):
    """Compress a file to gzip format and return its base64 representation.

    Args:
    - file_name (str): The name of the file to compress.
    - encoding (str, optional): The encoding of the file. Defaults to 'UTF-8'.

    Returns:
    - str: The base64-encoded representation of the compressed file.
    """
    with open(file_name, 'r', encoding=encoding) as f_in:
        file_content = f_in.read()

        # Compress the content using gzip
        buffer = BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode='wb') as f_out:
            f_out.write(file_content.encode(encoding))
        compressed_content = buffer.getvalue()

        # Convert the compressed content to base64
        b64_string = base64.b64encode(compressed_content)
        return b64_string.decode()
