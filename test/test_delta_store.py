# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import json
import pathlib

import stativ.delta_store as delta
import stativ.stativ as tripod

DELTA_STORE_DATA_ROOT = pathlib.Path('test', 'fixtures', 'delta_store')
DELTA_PROXY_ROOT = pathlib.Path(DELTA_STORE_DATA_ROOT, 'store')
DELTA_PROXY_DB_SAMPLE = pathlib.Path(DELTA_PROXY_ROOT, 'proxy.json')


def test_delta_store_fixture_present():
    assert DELTA_STORE_DATA_ROOT.is_dir()
    assert DELTA_PROXY_ROOT.is_dir()
    assert DELTA_PROXY_DB_SAMPLE.is_file()


def test_delta_store_fixture_proxy_present():
    with open(DELTA_PROXY_DB_SAMPLE, 'rt', encoding=tripod.ENCODING) as handle:
        proxy = json.load(handle)
    assert '_meta' in proxy


def test_delta_store_fixture_proxy_intact():
    with open(DELTA_PROXY_DB_SAMPLE, 'rt', encoding=tripod.ENCODING) as handle:
        proxy = json.load(handle)
    meta = proxy['_meta']
    assert 'key' in meta
    assert 'timestamp' in meta
    proxy_entry_count_including_meta = 2
    assert len(proxy) == proxy_entry_count_including_meta
    entry = {key: value for key, value in proxy.items() if key != '_meta'}
    entry_key, entry_data = next(iter(entry.items()))
    assert entry_key
    assert 'repo_key' in entry_data
    assert 'path' in entry_data
    recombined_key = f'{entry_data["repo_key"]}/{entry_data["path"]}'
    assert recombined_key == entry_key


def test_delta_is_delta_store():
    assert delta.is_delta_store(DELTA_PROXY_DB_SAMPLE) is False
    assert delta.is_delta_store(DELTA_PROXY_ROOT) is False
    assert delta.is_delta_store(DELTA_STORE_DATA_ROOT) is True
