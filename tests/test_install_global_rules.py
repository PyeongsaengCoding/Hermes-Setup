import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('global_rules', ROOT / 'scripts/install_global_rules.py')
assert spec is not None and spec.loader is not None
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class GlobalRulesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'profile'
        self.target = self.home / 'SOUL.md'

    def seed(self, content):
        self.home.mkdir(parents=True, exist_ok=True)
        self.target.write_text(content, encoding='utf-8')

    def test_preview_does_not_write(self):
        self.assertEqual(installer.install(self.home)['status'], 'add')
        self.assertFalse(self.home.exists())

    def test_first_install_and_repeat(self):
        self.assertEqual(installer.install(self.home, apply=True)['status'], 'added')
        content = self.target.read_bytes()
        self.assertEqual(installer.install(self.home, apply=True)['status'], 'unchanged')
        self.assertEqual(self.target.read_bytes(), content)
        self.assertEqual(content.decode().count(installer.START), 1)

    def test_preserves_existing_text(self):
        existing = '# My tone\nPersonal rules.\n'
        self.seed(existing)
        installer.install(self.home, apply=True)
        self.assertTrue(self.target.read_text().startswith(existing))

    def test_existing_unmarked_policy_not_duplicated(self):
        existing = '# My tone\n\n' + installer.policy() + '\n\n## Other rules\nKeep me.\n'
        self.seed(existing)
        self.assertEqual(installer.install(self.home, apply=True)['status'], 'unchanged')
        self.assertEqual(self.target.read_text(), existing)

    def test_preserves_existing_crlf_bytes(self):
        self.home.mkdir()
        existing = b'# My tone\r\nPersonal rules.\r\n'
        self.target.write_bytes(existing)
        installer.install(self.home, apply=True)
        self.assertTrue(self.target.read_bytes().startswith(existing))

    def test_different_report_policy_is_conflict(self):
        existing = '## Reports and AI-slop review\n\nMy existing policy.\n'
        self.seed(existing)
        with self.assertRaises(ValueError):
            installer.install(self.home, apply=True)
        self.assertEqual(self.target.read_text(), existing)

    def test_changed_managed_block_is_conflict(self):
        self.seed(installer.START + '\nPersonal edit.\n' + installer.END + '\n')
        before = self.target.read_bytes()
        with self.assertRaises(ValueError):
            installer.install(self.home, apply=True)
        self.assertEqual(self.target.read_bytes(), before)

    def test_malformed_markers_are_conflict(self):
        self.seed(installer.START + '\nIncomplete.\n')
        with self.assertRaises(ValueError):
            installer.install(self.home, apply=True)

    def test_symlink_refused(self):
        self.home.mkdir()
        other = self.home / 'other.md'
        other.write_text('Keep me.')
        self.target.symlink_to(other)
        with self.assertRaises(ValueError):
            installer.install(self.home, apply=True)
        self.assertEqual(other.read_text(), 'Keep me.')

    def test_environment_home_and_explicit_home(self):
        with patch.dict(os.environ, {'HERMES_HOME': str(self.home)}):
            self.assertEqual(installer.resolve_home(), self.home)
            self.assertEqual(installer.resolve_home(str(self.home / 'other')), self.home / 'other')


if __name__ == '__main__':
    unittest.main()
