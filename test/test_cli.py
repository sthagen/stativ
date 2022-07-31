import hashlib
import pathlib

import stativ.stativ as tripod

BRM_HASH_POLICY_DEFAULT = 'sha256'
BRM_HASH_POLICY_LEGACY = 'sha1'
BRM_HASH_POLICIES_KNOWN = (BRM_HASH_POLICY_DEFAULT, BRM_HASH_POLICY_LEGACY)

ALGORITHMS = {
    BRM_HASH_POLICY_DEFAULT: hashlib.sha256,
    BRM_HASH_POLICY_LEGACY: hashlib.sha1,
}

PREFIX_STORE_DATA_ROOT = pathlib.Path('test', 'fixtures', 'prefix_store')
PREFIX_DATA_SHA1 = pathlib.Path(PREFIX_STORE_DATA_ROOT, 'sha1')
SHA1 = '950e189624aa6d753077940f657b7ea8a67159d1'
SHA256 = 'a157d0670337432cb74ebb139f8f4febb314bce7218bf65df83770de73d0a78b'
PREFIX_STORE_DATA_FILE_1_CONTENT_SAMPLE = pathlib.Path(PREFIX_DATA_SHA1, SHA1[:2], SHA1)

FPS_DATA = f'{BRM_HASH_POLICY_DEFAULT}:{SHA256},{BRM_HASH_POLICY_LEGACY}:{SHA1}'

BACKUP_STORE_DATA_ROOT = pathlib.Path('test', 'fixtures', 'backup_store', 'daily')
BACKUP_DATA_REPO_SAMPLE = pathlib.Path(BACKUP_STORE_DATA_ROOT, 'repositories', 'foo-bar-baz-local')
BACKUP_DATA_REPO_FOLDER_LEVEL_1_SAMPLE = pathlib.Path(BACKUP_DATA_REPO_SAMPLE, 'ABC')
BACKUP_DATA_REPO_FOLDER_LEVEL_2_SAMPLE = pathlib.Path(BACKUP_DATA_REPO_FOLDER_LEVEL_1_SAMPLE, '2021')
BACKUP_DATA_REPO_FOLDER_LEVEL_3_SAMPLE = pathlib.Path(BACKUP_DATA_REPO_FOLDER_LEVEL_2_SAMPLE, 'Public')
BACKUP_DATA_REPO_FOLDER_LEVEL_3_FILE_1_CONTENT_SAMPLE = pathlib.Path(BACKUP_DATA_REPO_FOLDER_LEVEL_3_SAMPLE, 'DEF.txt')
BACKUP_DATA_REPO_FOLDER_LEVEL_3_FILE_1_META_SAMPLE = pathlib.Path(
    BACKUP_DATA_REPO_FOLDER_LEVEL_3_SAMPLE, 'DEF.txt.brm-metadata'
)

GIGA = 2 << (30 - 1)
BUFFER_BYTES = 2 << 15


def _hashes(path_string, algorithms=None):
    """Yield hashes per algorithms of path."""
    if algorithms is None:
        algorithms = {BRM_HASH_POLICY_DEFAULT: hashlib.sha256}
    for key in algorithms:
        if key not in BRM_HASH_POLICIES_KNOWN:
            raise ValueError('hashes received unexpected algorithm key.')

    path = pathlib.Path(path_string)
    if not path.is_file():
        raise IOError('path is no file.')

    accumulator = {k: f() for k, f in algorithms.items()}
    with open(path, 'rb') as in_file:
        for byte_block in iter(lambda in_f=in_file: in_f.read(BUFFER_BYTES), b''):
            for k in algorithms:
                accumulator[k].update(byte_block)

    return {k: f.hexdigest() for k, f in accumulator.items()}


def _derive_fingerprints(algorithms, file_path):
    fingerprints = _hashes(file_path, algorithms)
    fps = f'{",".join([f"{k}:{v}" for k, v in fingerprints.items()])}'
    return fps


def test_zero_minimal():
    assert '__name__' in dir(tripod)
    assert tripod.__name__ == 'stativ.stativ'


def test_prefix_store_fixture_ok():
    assert PREFIX_DATA_SHA1.is_dir()
    assert pathlib.Path(PREFIX_DATA_SHA1, SHA1[:2]).is_dir()
    assert PREFIX_STORE_DATA_FILE_1_CONTENT_SAMPLE.is_file()


def test_backup_store_fixture_ok():
    assert BACKUP_DATA_REPO_SAMPLE.is_dir()
    assert BACKUP_DATA_REPO_FOLDER_LEVEL_3_SAMPLE.is_dir()
    assert BACKUP_DATA_REPO_FOLDER_LEVEL_3_FILE_1_CONTENT_SAMPLE.is_file()
    assert BACKUP_DATA_REPO_FOLDER_LEVEL_3_FILE_1_META_SAMPLE.is_file()
    a_path = BACKUP_DATA_REPO_FOLDER_LEVEL_3_FILE_1_META_SAMPLE
    with open(a_path, 'rt', encoding=tripod.ENCODING) as handle:
        meta = handle.read()
    assert SHA1 in meta
    assert SHA256 in meta


def test_prefix_store_integrity():
    fps = _derive_fingerprints(ALGORITHMS, PREFIX_STORE_DATA_FILE_1_CONTENT_SAMPLE)
    assert fps == FPS_DATA


def test_prefix_backup_integrity():
    fps_prefix = _derive_fingerprints(ALGORITHMS, PREFIX_STORE_DATA_FILE_1_CONTENT_SAMPLE)
    fps_backup = _derive_fingerprints(ALGORITHMS, BACKUP_DATA_REPO_FOLDER_LEVEL_3_FILE_1_CONTENT_SAMPLE)
    assert fps_prefix == fps_backup
    assert fps_backup == FPS_DATA
