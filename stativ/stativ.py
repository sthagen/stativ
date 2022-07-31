# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring
"""Harvest the release mappings to bucket store from the backup tree."""
import copy
import datetime as dti
import json
import os
import pathlib

import stativ.delta_store as delta

BRM_NAME = os.getenv('BRM_NAME', 'brm')
BRM_ANCHOR = os.getenv('BRM_ANCHOR', '/')
BRM_STORE_ROOT = pathlib.Path(BRM_ANCHOR, BRM_NAME, 'data', 'filestore')
ENCODING = 'utf-8'

BRM_BACKUP_ROOT = pathlib.Path(BRM_ANCHOR, BRM_NAME, 'backup/')


def main(argv=None):
    """Harvest information."""
    if argv:
        print('Unexpected arguments ...')
        return 2

    print(f'Starting execution in folder ({pathlib.Path(".")})')
    print(f'- Assuming BRM storage root at ({BRM_STORE_ROOT}) i.e. the bucket store')
    print(f'- Assuming BRM backup root at ({BRM_BACKUP_ROOT}) i.e. the archival class artifacts')

    if not delta.is_delta_store(pathlib.Path('')):
        print('There is no delta store in the current directory ...')
        return 2

    with open(pathlib.Path('store', 'proxy.json'), 'rt', encoding=ENCODING) as handle:
        proxy = json.load(handle)

    enter, change, gone, keep = {}, {}, {}, {}
    remain = {}
    entered, changed, removed, kept = 0, 0, 0, 0
    print('---')
    exclude = str(pathlib.Path(BRM_BACKUP_ROOT, 'backup-daily', 'current', 'etc'))  # HACK A DID ACK
    for path in BRM_BACKUP_ROOT.glob('**/*'):
        if str(path).startswith(exclude):
            continue
        if path.name == f'{BRM_NAME}.properties':
            with open(path, 'rt', encoding=ENCODING) as handle:
                text_data = handle.readlines()
            meta = {}
            for line in text_data:
                if line.strip():
                    key, value = line.strip().split('=', 1)
                    if key.startswith(f'{BRM_NAME}.'):
                        _, key = key.split('.', 1)
                    if key == 'timestamp':
                        meta[key] = dti.datetime.utcfromtimestamp(float(value) / 1.0e3).astimezone().isoformat()

                    else:
                        meta['key'] = value
            if proxy['_meta'] != meta:
                print(f'WARNING {BRM_NAME} version info changed')
            del proxy['_meta']
            remain['_meta'] = copy.deepcopy(meta)
        elif path.name == f'{BRM_NAME}-file.xml':
            with open(path, 'rt', encoding=ENCODING) as handle:
                text_data = handle.readlines()
            meta = {}
            next_sha1_hash = False
            next_md5_hash = False
            next_sha256_hash = False
            for line in text_data:
                if line.strip():
                    rec = line.strip()
                    if rec.startswith('<size>'):
                        size_bytes = rec.split('<size>', 1)[1].split('</size>')[0]
                        meta['size_bytes'] = int(size_bytes)
                        continue
                    if rec.startswith('<repoKey>'):
                        repo_key = rec.split('<repoKey>', 1)[1].split('</repoKey>')[0]
                        meta['repo_key'] = repo_key
                        continue
                    if rec.startswith('<path>'):
                        a_path = rec.split('<path>', 1)[1].split('</path>')[0]
                        meta['path'] = a_path
                        continue
                    if rec.startswith('<lastUpdated>'):
                        last_update = rec.split('<lastUpdated>', 1)[1].split('</lastUpdated>')[0]
                        meta['last_update'] = (
                            dti.datetime.utcfromtimestamp(float(last_update) / 1.0e3).astimezone().isoformat()
                        )
                        continue
                    if rec.startswith('<type>sha1<'):
                        next_sha1_hash = True
                        continue
                    if next_sha1_hash and rec.startswith('<actual>'):
                        sha1_lc_hex = rec.split('<actual>', 1)[1].split('</actual>')[0]
                        meta['sha1_lc_hex'] = sha1_lc_hex
                        next_sha1_hash = False
                        continue
                    if rec.startswith('<type>md5<'):
                        next_md5_hash = True
                        continue
                    if next_md5_hash and rec.startswith('<actual>'):
                        md5_lc_hex = rec.split('<actual>', 1)[1].split('</actual>')[0]
                        meta['md5_lc_hex'] = md5_lc_hex
                        next_md5_hash = False
                        continue
                    if rec.startswith('<type>sha256<'):
                        next_sha256_hash = True
                        continue
                    if next_sha256_hash and rec.startswith('<actual>'):
                        sha256_lc_hex = rec.split('<actual>', 1)[1].split('</actual>')[0]
                        meta['sha256_lc_hex'] = sha256_lc_hex
                        next_sha256_hash = False
                        continue

            bucket = meta['sha1_lc_hex']
            prefix = bucket[:2]
            bucket_path = pathlib.Path(BRM_STORE_ROOT, prefix, bucket)
            meta['bucket_path'] = str(bucket_path)
            bucket_present = bucket_path.is_file()
            meta['bucket_present'] = bucket_present
            if bucket_present:
                b_stat = bucket_path.stat()
                meta['bucket_size_bytes'] = b_stat.st_size
                meta['bucket_modify'] = dti.datetime.utcfromtimestamp(b_stat.st_mtime).astimezone().isoformat()

            p_key = str(pathlib.Path(meta['repo_key'], meta['path']))
            if p_key not in proxy:
                print('INFO ENTER found new', p_key)
                enter[p_key] = copy.deepcopy(meta)
                entered += 1
                remain[p_key] = copy.deepcopy(meta)
            elif proxy[p_key] != meta:
                print('INFO CHANGE found changed', p_key)
                change[p_key] = copy.deepcopy(meta)
                del proxy[p_key]
                changed += 1
                remain[p_key] = copy.deepcopy(meta)
            else:
                keep[p_key] = copy.deepcopy(meta)
                del proxy[p_key]
                kept += 1
                remain[p_key] = copy.deepcopy(meta)

    removed = len(proxy)
    print('INFO GONE processing', removed, 'gone entries')
    for key, val in proxy.items():
        gone[key] = val

    delta.dump_gone(gone, indent=True)
    delta.dump_change(change, indent=True)
    delta.dump_enter(enter, indent=True)
    delta.dump_keep(keep, indent=True)
    delta.dump_remain(remain, indent=True)

    if len(remain) != 1 + entered + changed + kept:
        print('WARNING:  len(remain) != 1 + entered + changed + kept')

    print(
        f'SUMMARY: ENTER({entered}), CHANGE({changed}), KEPT({kept}), GONE({removed})'
        f' --> REMAIN({entered + changed + kept})'
    )
    return 0
