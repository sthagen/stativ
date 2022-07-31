# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
import json
import pathlib

ENCODING = 'utf-8'


def is_delta_store(delta_store_root: pathlib.Path, deep_inspection=False) -> bool:
    """Belts and braces."""
    if not delta_store_root.is_dir():
        return False

    store_path = pathlib.Path(delta_store_root, 'store')
    if not store_path.is_dir():
        return False

    proxy_path = pathlib.Path(store_path, 'proxy.json')
    if not proxy_path.is_file():
        return False

    if deep_inspection:
        try:
            with open(proxy_path, 'rt', encoding=ENCODING) as handle:
                _ = json.load(handle)
        except json.JSONDecodeError:
            return False

    return True


def _dump(aspect_store: dict, path: pathlib.Path, indent=False) -> bool:
    """DRY."""
    options = {'indent': 2} if indent else {}
    try:
        with open(path, 'wt', encoding=ENCODING) as handle:
            json.dump(aspect_store, handle, **options)
    except Exception:  # pylint: disable=broad-except
        return False
    return True


def dump_gone(aspect_store: dict, indent=False) -> bool:
    """Not too dry ..."""
    return _dump(aspect_store, pathlib.Path('gone.json'), indent)


def dump_change(aspect_store: dict, indent=False) -> bool:
    """Not too dry ..."""
    return _dump(aspect_store, pathlib.Path('change.json'), indent)


def dump_enter(aspect_store: dict, indent=False) -> bool:
    """Not too dry ..."""
    return _dump(aspect_store, pathlib.Path('enter.json'), indent)


def dump_keep(aspect_store: dict, indent=False) -> bool:
    """Not too dry ..."""
    return _dump(aspect_store, pathlib.Path('keep.json'), indent)


def dump_remain(aspect_store: dict, indent=False) -> bool:
    """Not too dry ..."""
    return _dump(aspect_store, pathlib.Path('remain.json'), indent)
