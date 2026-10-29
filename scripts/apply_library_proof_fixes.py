#!/usr/bin/env python3
"""Check or apply exact metadata-only NASAlib proof compatibility fixes."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile


MANIFEST = Path(__file__).resolve().parents[1] / 'library-proof-fixes' / 'manifest.json'


class FixError(Exception):
    pass


def sha256(content):
    return hashlib.sha256(content).hexdigest()


# Byte offsets refer to the original file. The parser retains only the top
# three list levels; tactic and dependency subtrees are skipped structurally.
TOKEN = re.compile(r';[^\n]*|"(?:\\.|[^"\\])*"|\|(?:\\.|[^|\\])*\||[()]|(?:\\.|[^\\\s()";|])+', re.S)


def symbol(node):
    return node['value'].strip('|') if node['kind'] == 'atom' else None


def integer(node):
    return node['kind'] == 'atom' and re.fullmatch(r'[+-]?[0-9]+', node['value'])


def proof_metadata(raw):
    text=raw.decode('latin1');stack=[];records=[];unknown=[];forms=0
    def examine(fields,parent,proof_index,shape):
        if len(fields) in [6,7]:script_slot=3;dp_slot=5;kind='modern-'+str(len(fields))
        elif len(fields)==11:script_slot=4;dp_slot=10;kind='legacy-11'
        else:
            unknown.append({'theory':symbol(parent[0]),'formula':symbol(parent[1]),'proof_index':proof_index,'fields':len(fields),'shape':shape})
            return
        if fields[0]['kind']!='atom' or not integer(fields[2]):
            unknown.append({'theory':symbol(parent[0]),'formula':symbol(parent[1]),'proof_index':proof_index,'fields':len(fields),'shape':'invalid-proof-id/date'})
            return
        s=fields[script_slot];d=fields[dp_slot]
        records.append({'theory':symbol(parent[0]),'formula':symbol(parent[1]),'proof_id':symbol(fields[0]),'proof_index':proof_index,'format':kind,'script_start':s['start'],'script_end':s['end'],'script_sha256':sha256(raw[s['start']:s['end']]),'dp_kind':d['kind'],'dp_value':d['value'],'dp_start':d['start'],'dp_end':d['end'],'dp_line':text.count('\n',0,d['start'])+1,'default_index':parent[2]})
    for match in TOKEN.finditer(text):
        token=match.group();start,end=match.span()
        if token.startswith(';'):continue
        if token=='(':
            stack.append({'start':start,'fields':[]})
        elif token==')':
            if not stack:raise ValueError('unmatched close at '+str(start))
            frame=stack.pop();node={'kind':'list','value':None,'start':frame['start'],'end':end,'fields':frame['fields']}
            if len(stack)==2:
                # Normal theory -> declaration -> proofinfo, with a numeric default index.
                parent=stack[-1]['fields'];theory=stack[-2]['fields']
                if len(parent)>=2 and theory and integer(parent[1]):
                    examine(node['fields'],[theory[0],parent[0],int(parent[1]['value'])],len(parent)-2,'nested')
            if len(stack)==1:
                # Pre-multiple-proof inline legacy record, when present.
                f=node['fields'];theory=stack[-1]['fields']
                if f and len(f)>1 and not integer(f[1]) and f[1]['kind']=='atom' and theory:
                    examine(f[1:],[theory[0],f[0],0],0,'inline')
            if stack and len(stack)<=3:stack[-1]['fields'].append(node)
            elif not stack:forms+=1
        else:
            node={'kind':'string' if token.startswith('"') else 'atom','value':token[1:-1] if token.startswith('"') else token,'start':start,'end':end}
            if stack and len(stack)<=3:stack[-1]['fields'].append(node)
    if stack:raise ValueError('unclosed list')
    return {'records':records,'unknown':unknown,'top_level_forms':forms}



def load_manifest(path=MANIFEST):
    document = json.loads(Path(path).read_text())
    if document.get('schema') not in (1, 2) or document.get('library') != 'NASAlib':
        raise FixError('Unsupported library-fix manifest')
    changes = document.get('changes')
    if not isinstance(changes, list) or not changes:
        raise FixError('The manifest must contain explicit fixes')
    seen = set()
    for change in changes:
        relative = PurePosixPath(change['path'])
        if (relative.is_absolute() or '..' in relative.parts
                or relative.suffix != '.prf' or str(relative) in seen):
            raise FixError('Only distinct relative .prf paths are allowed')
        seen.add(str(relative))
        for key in ['before_sha256', 'after_sha256']:
            if not re.fullmatch(r'[0-9a-f]{64}', change[key]):
                raise FixError('Invalid expected SHA-256 for ' + str(relative))
        if 'replacements' in change:
            replacements = change['replacements']
            if not isinstance(replacements, list) or not replacements:
                raise FixError('Explicit metadata offset hunks are required')
            offsets = set()
            for item in replacements:
                offset = item['offset']
                if type(offset) is not int or offset < 0 or offset in offsets:
                    raise FixError('Offsets must be distinct nonnegative integers')
                offsets.add(offset)
                if item.get('old_text') != '"shostak"' or item.get('new_text') != 'SHOSTAK':
                    raise FixError('Only quoted metadata shostak to symbol SHOSTAK is allowed')
                for key in ['theory', 'formula', 'proof_id']:
                    if not isinstance(item.get(key), str) or not item[key]:
                        raise FixError('An exact proof-record identity is required')
                if type(item.get('proof_index')) is not int or item['proof_index'] < 0:
                    raise FixError('An exact proof variant index is required')
                if not re.fullmatch(r'[0-9a-f]{64}', item.get('script_sha256', '')):
                    raise FixError('An exact proof-program hash is required')
            for key in ['proof_programs_sha256', 'pvs_sha256']:
                if not re.fullmatch(r'[0-9a-f]{64}', change.get(key, '')):
                    raise FixError('Expected source and complete proof-program hashes are required')
        else:
            # Retain schema-1 context hunks, with the same metadata-only guard.
            old, new = change['old_text'], change['new_text']
            if (not isinstance(old, str) or not isinstance(new, str)
                    or old.count('"shostak"') != 1
                    or new != old.replace('"shostak"', 'SHOSTAK', 1)):
                raise FixError('Only the documented metadata replacement is allowed')
    return changes


def checked_records(content):
    try:
        result = proof_metadata(content)
    except (ValueError, IndexError, TypeError) as error:
        raise FixError('Unsupported saved-proof syntax: ' + str(error))
    if result['unknown']:
        raise FixError('Unsupported proof-record metadata shape')
    return result['records']


def programs_fingerprint(records):
    programs = [(r['theory'], r['formula'], r['proof_index'], r['script_sha256']) for r in records]
    return sha256(json.dumps(programs, separators=(',', ':')).encode())


def checked_replacement(content, change):
    records = checked_records(content)
    if 'proof_programs_sha256' in change and programs_fingerprint(records) != change['proof_programs_sha256']:
        raise FixError('Complete proof-program fingerprint differs')
    metadata = {r['dp_start']: r for r in records}
    if 'replacements' in change:
        replacements = change['replacements']
    else:
        context = change['old_text'].encode()
        if content.count(context) != 1:
            raise FixError('Expected exactly one legacy metadata context')
        replacements = [{'offset': content.index(context) + context.index(b'"shostak"'),
                         'old_text': '"shostak"', 'new_text': 'SHOSTAK'}]
    updated = content
    for item in sorted(replacements, key=lambda x: x['offset'], reverse=True):
        offset = item['offset']; record = metadata.get(offset)
        old, new = item['old_text'].encode(), item['new_text'].encode()
        if (record is None or record['dp_kind'] != 'string'
                or record['dp_value'] != 'shostak'
                or record['dp_end'] != offset + len(old)
                or content[offset:offset+len(old)] != old):
            raise FixError('Offset is not the exact decision-procedure metadata slot')
        for key in ['theory', 'formula', 'proof_id', 'proof_index', 'default_index', 'script_sha256']:
            if key in item and item[key] != record[key]:
                raise FixError('Proof-record identity or program hash differs: ' + key)
        updated = updated[:offset] + new + updated[offset+len(old):]
    if sha256(updated) != change['after_sha256']:
        raise FixError('Metadata hunks do not produce the expected proof hash')
    if programs_fingerprint(checked_records(updated)) != programs_fingerprint(records):
        raise FixError('A proof program changed; refusing replacement')
    return updated


def plan_fixes(nasalib_root, manifest_path=MANIFEST):
    root = Path(nasalib_root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise FixError('NASAlib root is not a directory')
    plan = []
    for change in load_manifest(manifest_path):
        target = root / change['path']
        if target.is_symlink() or not target.is_file():
            raise FixError('Expected a regular proof file: ' + str(target))
        try:
            target.resolve(strict=True).relative_to(root)
        except ValueError:
            raise FixError('Proof path escapes the selected NASAlib root')
        if 'pvs_sha256' in change:
            source = target.with_suffix('.pvs')
            if source.is_symlink() or not source.is_file() or sha256(source.read_bytes()) != change['pvs_sha256']:
                raise FixError('Adjacent pinned source declarations differ: ' + change['path'])
        content = target.read_bytes(); digest = sha256(content)
        if digest == change['after_sha256']:
            if 'proof_programs_sha256' in change and programs_fingerprint(checked_records(content)) != change['proof_programs_sha256']:
                raise FixError('Fixed proof-program fingerprint differs')
            plan.append(dict(path=change['path'], target=target, status='already-fixed'))
            continue
        if digest != change['before_sha256']:
            raise FixError('Unknown proof bytes for ' + change['path'] + ': SHA-256 ' + digest)
        updated = checked_replacement(content, change)
        backup = target.with_name(target.name + '.ppg-original-' + digest + '.bak')
        if backup.is_symlink() or (backup.exists() and backup.read_bytes() != content):
            raise FixError('Refusing to overwrite an unexpected original-file backup: ' + str(backup))
        plan.append(dict(path=change['path'], target=target, status='needs-fix',
                         before=content, after=updated, backup=backup,
                         expected_after=change['after_sha256']))
    return plan


def apply_plan(item):
    target, backup = item['target'], item['backup']
    if target.is_symlink() or target.read_bytes() != item['before']:
        raise FixError('Proof file changed after validation: ' + str(target))
    original_stat = target.stat()
    mode = stat.S_IMODE(original_stat.st_mode)
    try:
        descriptor = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    except FileExistsError:
        if backup.is_symlink() or backup.read_bytes() != item['before']:
            raise FixError('Existing backup differs from the original proof bytes')
    else:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(item['before'])
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(backup, mode)
        os.utime(backup, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))
    if backup.read_bytes() != item['before']:
        raise FixError('Original-file backup verification failed')

    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.' + target.name + '.ppg-',
                                         dir=target.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(item['after'])
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        if target.is_symlink() or target.read_bytes() != item['before']:
            raise FixError('Proof file changed before atomic replacement')
        os.replace(temporary, target)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    if sha256(target.read_bytes()) != item['expected_after']:
        raise FixError('Final proof hash verification failed; the original backup was retained')


def run_fixes(nasalib_root, apply_changes=False, manifest_path=MANIFEST):
    """Validate every target before writing any; return explicit per-file status."""
    plan = plan_fixes(nasalib_root, manifest_path)
    results = []
    for item in plan:
        status = item['status']
        if status == 'needs-fix' and apply_changes:
            apply_plan(item)
            status = 'applied'
        result = {'path': item['path'], 'status': status}
        if status == 'applied':
            result['backup'] = str(item['backup'])
        results.append(result)
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--nasalib-root', type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='Read-only check (default)')
    mode.add_argument('--apply', action='store_true', help='Back up and atomically apply known fixes')
    args = parser.parse_args(argv)
    try:
        results = run_fixes(args.nasalib_root, args.apply)
    except (FixError, OSError, ValueError, KeyError, TypeError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        return 2
    for result in results:
        print(result['status'].upper() + ' ' + result['path'])
        if 'backup' in result:
            print('Original backup: ' + result['backup'])
    return 1 if any(result['status'] == 'needs-fix' for result in results) else 0


if __name__ == '__main__':
    sys.exit(main())
