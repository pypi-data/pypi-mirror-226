from .utility import read_audio

import soundfile

import os
import json
from datetime import datetime

"""Constants and methods related to file integration between the UI container and the various AI Architecture 
containers"""

ROOT_DIR = os.path.join(os.path.expanduser('~'), 'hay_say')
AUDIO_FOLDER = os.path.join(ROOT_DIR, 'audio_cache')
RAW_DIR = os.path.join(AUDIO_FOLDER, 'raw')
PREPROCESSED_DIR = os.path.join(AUDIO_FOLDER, 'preprocessed')
OUTPUT_DIR = os.path.join(AUDIO_FOLDER, 'output')
POSTPROCESSED_DIR = os.path.join(AUDIO_FOLDER, 'postprocessed')
CUSTOM_MODELS_DIR = os.path.join(ROOT_DIR, 'custom_models')
MODELS_DIR = os.path.join(ROOT_DIR, 'models')
METADATA_FILENAME = 'metadata.json'
TIMESTAMP_FORMAT = '%Y/%m/%d %H:%M:%S.%f'
MAX_FILES_PER_CACHE_FOLDER = 25

if not os.path.exists(AUDIO_FOLDER):
    # All Docker containers must have a shared volume mounted at AUDIO_FOLDER. This shared volume is one mechanism by
    # which the containers communicate with each other. If it does not exist, that means something is configured
    # incorrectly (probably in the docker-compose file), so raise an Exception to catch the issue early on, during
    # development and testing. Do not simply create an unmounted AUDIO_FOLDER directory, as that would result in errors
    # where the root cause is not immediately obvious.
    raise Exception('audio_cache directory does not exist! Did you forget to mount the audio_cache volume?')
else:
    if not os.path.exists(RAW_DIR):
        os.mkdir(RAW_DIR)
    if not os.path.exists(PREPROCESSED_DIR):
        os.mkdir(PREPROCESSED_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    if not os.path.exists(POSTPROCESSED_DIR):
        os.mkdir(POSTPROCESSED_DIR)


if not os.path.exists(MODELS_DIR):
    # All Docker containers must have a shared volume mounted at MODELS_DIR. This is where character models are stored.
    raise Exception('"models" directory does not exist! Did you forget to mount the models volume?')


if not os.path.exists(CUSTOM_MODELS_DIR):
    # All Docker containers must have a shared volume mounted at CUSTOM_MODELS_DIR. This is where custom character
    # models were originally stored. This volume is no longer used, but it must still exist for backwards compatibility.
    raise Exception('custom_models directory does not exist! Did you forget to mount the custom_models volume?')

CACHE_FORMAT, CACHE_EXTENSION, CACHE_MIMETYPE = 'FLAC', '.flac', 'audio/flac;base64'  # FLAC compression is lossless


def model_dirs(architecture_name):
    """Deprecated. Use characters_dir or character_dir instead.
    Returns a list of all directories which may contain character subdirectories with model files for the given
    architecture."""
    return model_pack_dirs(architecture_name) \
        + [custom_model_dir(architecture_name)] \
        + [characters_dir(architecture_name)]


def model_pack_dirs(architecture_name):
    """Deprecated. Use characters_dir or character_dir instead.
    Returns a list of absolute paths to all the model pack directories for the given architecture."""
    return [directory for directory in possible_model_pack_dirs(architecture_name) if os.path.isdir(directory)]


def possible_model_pack_dirs(architecture_name):
    """A helper method for model_pack_dirs"""
    return [os.path.join(ROOT_DIR, architecture_name + '_model_pack_' + str(index)) for index in range(100)]


def custom_model_dir(architecture_name):
    """Deprecated. Use characters_dir or character_dir instead.
    Returns the directory containing custom models for the given architecture."""
    return get_guaranteed_directory(os.path.join(CUSTOM_MODELS_DIR, architecture_name))


def characters_dir(architecture_name):
    """Returns the directory containing all the character model subdirectories for the given architecture."""
    return get_guaranteed_directory(os.path.join(MODELS_DIR, architecture_name, 'characters'))


def get_guaranteed_directory(directory):
    """Creates the directory if it does not exist and returns the path to the directory that now definitely exists"""
    if not os.path.isdir(directory):
        os.makedirs(directory)
    return directory


def character_dir(architecture_name, character_name):
    """Returns the directory where the files for a given character model in a given architecture are stored."""
    return os.path.join(MODELS_DIR, architecture_name, 'characters', character_name)


def multispeaker_model_dir(architecture_name, model_name):
    """Returns the directory where multi-speaker models are stored for the given architecture."""
    return os.path.join(MODELS_DIR, architecture_name, 'multispeaker_models', model_name)


def read_metadata(folder):
    """Return the metadata dictionary of a given audio_cache subfolder.
    'folder' should be one of: RAW_DIR, PREPROCESSED_DIR, OUTPUT_DIR, or POSTPROCESSED_DIR."""
    path_to_file = os.path.join(folder, METADATA_FILENAME)
    metadata = dict()
    if os.path.isfile(path_to_file):
        with open(path_to_file, 'r') as file:
            metadata = json.load(file)
    return metadata


def write_metadata(folder, dict_contents):
    """Writes the supplied dictionary to the metadata file in the specified audio_cache folder, overwriting existing
    contents."""
    path = os.path.join(folder, METADATA_FILENAME)
    with open(path, 'w') as file:
        file.write(json.dumps(dict_contents, sort_keys=True, indent=4))


def read_audio_from_cache(folder, filename_sans_extension):
    """Read the specified file from the audio_cache folder.
    'folder' should be one of: RAW_DIR, PREPROCESSED_DIR, OUTPUT_DIR, or POSTPROCESSED_DIR."""
    path = os.path.join(folder, filename_sans_extension + CACHE_EXTENSION)
    return read_audio(path)


def save_audio_to_cache(folder, filename_sans_extension, array, samplerate):
    """saves the supplied audio data to the specified audio_cache folder with the specified filename. The oldest file in
    the audio_cache folder is deleted if saving this file would cause the total number of files cached in the folder to
    exceed MAX_FILES_PER_CACHE_FOLDER.
    'folder' should be one of: RAW_DIR, PREPROCESSED_DIR, OUTPUT_DIR, or POSTPROCESSED_DIR."""
    if count_audio_cache_files(folder) >= MAX_FILES_PER_CACHE_FOLDER:
        delete_oldest_cache_file(folder)
    write_audio_file(folder, filename_sans_extension, array, samplerate)


def write_audio_file(folder, filename_sans_extension, array, samplerate):
    """writes audio data to the specified audio_cache folder with the specified filename. The file is written in the
    format specified by CACHE_FORMAT.
    'folder' should be one of: RAW_DIR, PREPROCESSED_DIR, OUTPUT_DIR, or POSTPROCESSED_DIR."""
    path = os.path.join(folder, filename_sans_extension + CACHE_EXTENSION)
    soundfile.write(path, array, samplerate, format=CACHE_FORMAT)


def count_audio_cache_files(folder):
    """Return the number of audio files stored in the specified audio_cache folder.
    'folder' should be one of: RAW_DIR, PREPROCESSED_DIR, OUTPUT_DIR, or POSTPROCESSED_DIR."""
    metadata = read_metadata(folder)
    return len(metadata.keys())


def delete_oldest_cache_file(folder):
    """Deletes the oldest file in the specified audio_cache folder.
    'folder' should be one of: RAW_DIR, PREPROCESSED_DIR, OUTPUT_DIR, or POSTPROCESSED_DIR."""
    # delete the file itself
    oldest_filename_sans_extension = get_hashes_sorted_by_timestamp(folder)[-1]
    oldest_path = os.path.join(folder, oldest_filename_sans_extension + CACHE_EXTENSION)
    os.remove(oldest_path)

    # remove entry from metadata file
    metadata = read_metadata(folder)
    del metadata[oldest_filename_sans_extension]
    write_metadata(folder, metadata)


def get_hashes_sorted_by_timestamp(folder):
    """Returns the hashes/filenames (without extension) of the audio files in the specified audio_cache folder, sorted
    by their timestamp. 'folder' should be one of: RAW_DIR, PREPROCESSED_DIR, OUTPUT_DIR, or POSTPROCESSED_DIR."""
    metadata = read_metadata(folder)
    return sorted(metadata.keys(),
                  key=lambda key: datetime.strptime(metadata[key]['Time of Creation'], TIMESTAMP_FORMAT),
                  reverse=True)


def get_full_file_path(folder, filename_sans_extension):
    """Given a folder and a filename without an extension, find the full path of that file with the extension.
    Assumption: there should only be one file in the folder whose name without the extension is
    filename_sans_extension."""
    potential_filenames = [file for file in os.listdir(folder) if file.split('.')[0] == filename_sans_extension]
    if len(potential_filenames) > 1:
        raise Exception('more than one file with the same hash found')
    elif len(potential_filenames) == 0:
        raise Exception('file with name ' + filename_sans_extension + ' not found')
    return os.path.join(folder, potential_filenames[0])


def file_is_already_cached(folder, filename_sans_extension):
    """Return True if the specified file is already present in the specified audio_cache folder, otherwise False"""
    metadata = read_metadata(folder)
    return True if filename_sans_extension in metadata.keys() else False
