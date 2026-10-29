"""Metadata-only edits, original backups and fail-closed temporary fixtures."""
import copy
import hashlib
import json
from pathlib import Path
import runpy
import stat
import tempfile
import unittest

REPOSITORY = Path(__file__).resolve().parents[1]
TOOL = runpy.run_path(str(REPOSITORY / 'scripts' / 'apply_library_proof_fixes.py'))


def sha(value):
    return hashlib.sha256(value).hexdigest()


class LibraryProofFixTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.original = b'''(|sample|
 (|first| 0
  (|first-1| NIL 123
   ("" (LEMMA "shostak") NIL NIL)
   NIL
   "shostak"))
 (|second| 0
  (|second-1| NIL 124
   ("" (GRIND) NIL NIL)
   NIL
   "shostak" (|second| SUBTYPE "x" "nat" (1 1 1 2)))))
'''
        self.expected = self.original.replace(b'\n   "shostak"', b'\n   SHOSTAK')
        self.statement_bytes = b'sample: THEORY BEGIN value: nat = 1 END sample\n'
        scripts = [b'("" (LEMMA "shostak") NIL NIL)', b'("" (GRIND) NIL NIL)']
        offsets = []
        start = 0
        for _ in range(2):
            start = self.original.index(b'\n   "shostak"', start) + 4
            offsets.append(start)
            start += len(b'"shostak"')
        self.change = {
            'path': 'analysis/sample.prf',
            'before_sha256': sha(self.original), 'after_sha256': sha(self.expected),
            'pvs_sha256': sha(self.statement_bytes),
            'proof_programs_sha256': sha(json.dumps([
                ['sample', 'first', 0, sha(scripts[0])],
                ['sample', 'second', 0, sha(scripts[1])],
            ], separators=(',', ':')).encode()),
            'replacements': [
                {'offset': offset, 'old_text': '"shostak"', 'new_text': 'SHOSTAK',
                 'theory': 'sample', 'formula': formula, 'proof_id': formula+'-1',
                 'proof_index': 0, 'default_index': 0, 'script_sha256': sha(script)}
                for offset, formula, script in zip(offsets, ['first', 'second'], scripts)
            ],
        }
        self.document = {'schema': 2, 'library': 'NASAlib', 'changes': [self.change]}
        self.manifest = self.root/'manifest.json'
        self.save_manifest()
        self.target = self.root/self.change['path']
        self.target.parent.mkdir(parents=True)
        self.target.write_bytes(self.original)
        self.target.chmod(0o640)
        self.statement = self.target.with_suffix('.pvs')
        self.statement.write_bytes(self.statement_bytes)

    def save_manifest(self):
        self.manifest.write_text(json.dumps(self.document))

    def run_tool(self, apply=False):
        return TOOL['run_fixes'](self.root, apply_changes=apply, manifest_path=self.manifest)

    def test_multi_slot_check_and_apply_preserve_programs_source_and_backup(self):
        self.assertEqual(self.run_tool()[0]['status'], 'needs-fix')
        self.assertEqual(self.target.read_bytes(), self.original)
        self.assertEqual(list(self.target.parent.glob('*.bak')), [])
        result = self.run_tool(apply=True)[0]
        self.assertEqual(result['status'], 'applied')
        self.assertEqual(self.target.read_bytes(), self.expected)
        self.assertIn(b'(LEMMA "shostak")', self.target.read_bytes())
        self.assertEqual(Path(result['backup']).read_bytes(), self.original)
        self.assertEqual(stat.S_IMODE(self.target.stat().st_mode), 0o640)
        self.assertEqual(self.statement.read_bytes(), self.statement_bytes)
        self.assertEqual(list(self.target.parent.glob('.*.ppg-*')), [])

    def test_already_fixed_is_idempotent(self):
        self.run_tool(apply=True)
        timestamp = self.target.stat().st_mtime_ns
        backups = list(self.target.parent.glob('*.bak'))
        self.assertEqual(self.run_tool(apply=True)[0]['status'], 'already-fixed')
        self.assertEqual(self.target.stat().st_mtime_ns, timestamp)
        self.assertEqual(list(self.target.parent.glob('*.bak')), backups)
        self.assertEqual(self.run_tool()[0]['status'], 'already-fixed')

    def test_unknown_proof_or_backup_is_rejected_without_overwrite(self):
        self.target.write_bytes(self.original+b'changed')
        with self.assertRaises(TOOL['FixError']):
            self.run_tool(apply=True)
        self.assertEqual(self.target.read_bytes(), self.original+b'changed')
        self.assertEqual(list(self.target.parent.glob('*.bak')), [])
        self.target.write_bytes(self.original)
        backup = self.target.with_name(self.target.name+'.ppg-original-'+self.change['before_sha256']+'.bak')
        backup.write_bytes(b'preexisting user data')
        with self.assertRaises(TOOL['FixError']):
            self.run_tool(apply=True)
        self.assertEqual(backup.read_bytes(), b'preexisting user data')
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_tactic_string_is_rejected_even_with_matching_proposed_hash(self):
        attack = copy.deepcopy(self.change['replacements'][0])
        attack['offset'] = self.original.index(b'"shostak"')
        self.change['replacements'] = [attack]
        altered = self.original[:attack['offset']]+b'SHOSTAK'+self.original[attack['offset']+9:]
        self.change['after_sha256'] = sha(altered)
        self.save_manifest()
        with self.assertRaises(TOOL['FixError']):
            self.run_tool(apply=True)
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_record_identity_and_program_hash_are_checked(self):
        for key, wrong in [('formula', 'different'), ('script_sha256', '0'*64)]:
            original = self.change['replacements'][0][key]
            self.change['replacements'][0][key] = wrong
            self.save_manifest()
            with self.assertRaises(TOOL['FixError']):
                self.run_tool(apply=True)
            self.change['replacements'][0][key] = original
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_pvs_source_changes_are_rejected(self):
        self.statement.write_bytes(self.statement_bytes+b'% changed\n')
        with self.assertRaises(TOOL['FixError']):
            self.run_tool(apply=True)
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_manifest_path_escape_and_duplicate_offsets_are_rejected(self):
        original_path = self.change['path']
        for bad in ['../escape.prf', '/tmp/escape.prf', 'analysis/sample.pvs']:
            self.change['path'] = bad
            self.save_manifest()
            with self.assertRaises(TOOL['FixError']):
                self.run_tool(apply=True)
        self.change['path'] = original_path
        self.change['replacements'].append(copy.deepcopy(self.change['replacements'][0]))
        self.save_manifest()
        with self.assertRaises(TOOL['FixError']):
            self.run_tool(apply=True)
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_all_files_are_prevalidated_before_any_write(self):
        second = copy.deepcopy(self.change)
        second['path'] = 'analysis/second.prf'
        self.document['changes'].append(second)
        (self.root/second['path']).write_bytes(b'unknown proof bytes')
        (self.root/second['path']).with_suffix('.pvs').write_bytes(self.statement_bytes)
        self.save_manifest()
        with self.assertRaises(TOOL['FixError']):
            self.run_tool(apply=True)
        self.assertEqual(self.target.read_bytes(), self.original)
        self.assertEqual(list(self.target.parent.glob('*.bak')), [])

    def test_legacy_one_context_manifest_is_supported_with_metadata_guard(self):
        original = b'(|legacy| (|f| 0 (|p| NIL 123 ("" (GRIND) NIL NIL) NIL\n   "shostak")))\n'
        old = '\n   "shostak"'
        expected = original.replace(old.encode(), old.replace('"shostak"', 'SHOSTAK').encode())
        self.target.write_bytes(original)
        self.document = {'schema': 1, 'library': 'NASAlib', 'changes': [{
            'path': self.change['path'], 'before_sha256': sha(original),
            'after_sha256': sha(expected), 'old_text': old,
            'new_text': old.replace('"shostak"', 'SHOSTAK')}]}
        self.save_manifest()
        self.assertEqual(self.run_tool(apply=True)[0]['status'], 'applied')
        self.assertEqual(self.target.read_bytes(), expected)

    def test_escaped_symbols_and_old_metadata_layout(self):
        records = TOOL['checked_records'](b'(T (foo\\|bar 0 (p NIL 123 124 ("" (GRIND)) PROVED NIL 1 1 NIL "shostak")))')
        self.assertEqual(records[0]['formula'], 'foo\\|bar')
        self.assertEqual(records[0]['format'], 'legacy-11')
        self.assertEqual(records[0]['dp_kind'], 'string')


if __name__ == '__main__':
    unittest.main()
