import librosa

import base64
import io
import os

"""Methods that are useful across multiple Hay Say coding projects and are not necessarily related to file integration
or specific to servers"""


def create_link(existing_path, desired_link_path):
    if not os.path.exists(desired_link_path):
        os.symlink(existing_path, desired_link_path)

def get_audio_from_src_attribute(src, encoding):
    _, raw = src.split(',')
    b64_output_bytes = raw.encode(encoding)
    output_bytes = base64.b64decode(b64_output_bytes)
    buffer = io.BytesIO(output_bytes)
    return librosa.load(buffer, sr=None)


def read_audio(path):
    return librosa.load(path, sr=None)


def get_singleton_file(folder):
    """Given a folder, return the full path of the single file within that folder. If there is no file in that folder,
    or if there is more than one file in that folder, raise an Exception."""
    potential_filenames = [file for file in os.listdir(folder)]
    if len(potential_filenames) > 1:
        raise Exception('more than one file was found in the indicated folder. Only one was expected.')
    elif len(potential_filenames) == 0:
        raise Exception('No file was found in the indicated folder.')
    return os.path.join(folder, potential_filenames[0])


def get_single_file_with_extension(directory, extension):
    """Finds the single file with the given extension in the specified directory. If there is no such file or if there
    is more than one file with the extension, throw an Exception. Otherwise, return the path to the file."""
    all_files = get_files_with_extension(directory, extension)
    if len(all_files) > 1:
        raise Exception('More than one file with the extension ' + extension + ' was found in ' + directory)
    elif len(all_files) == 0:
        raise Exception('file with extension ' + extension + ' not found in ' + directory)
    return all_files[0]


def get_files_with_extension(directory, extension):
    """Find all files with the given extension in the specified directory. Returns a list of paths."""
    extension = ('.' + extension) if extension[0] != '.' else extension
    return get_files_ending_with(directory, extension)


def get_files_ending_with(directory, endswith):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(endswith)]
