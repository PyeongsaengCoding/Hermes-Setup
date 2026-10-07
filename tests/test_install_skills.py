import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install_skills.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.local').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / '.local')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / 'source'
        self.home = self.base / 'home'
        (self.source / 'skills/demo/scripts').mkdir(parents=True)
        (self.source / 'skills/demo/SKILL.md').write_text('---\nname: demo\ndescription: Test.\n---\nBody.\n')
        (self.source / 'skills/demo/scripts/helper.py').write_text('print("demo")\n')
        (self.source / 'LICENSE').write_text('fixture license')
        self.manifest = {'skills': [{'name': 'demo', 'source_kind': 'upstream', 'source_path': 'skills/demo', 'install_path': 'skills/test/demo'}]}

    def apply(self, apply=True):
        return installer.install(self.manifest, self.home, self.source, apply)

    def test_preview_does_not_write(self):
        self.assertEqual(self.apply(False)[0]['status'], 'add')
        self.assertFalse(self.home.exists())

    def test_install_supporting_files_and_license(self):
        self.apply()
        self.assertEqual((self.home / 'skills/test/demo/scripts/helper.py').read_text(), 'print("demo")\n')
        self.assertEqual((self.home / 'skills/test/demo/_UPSTREAM_LICENSE').read_text(), 'fixture license')

    def test_repeat_is_unchanged(self):
        self.apply()
        self.assertEqual(self.apply()[0]['status'], 'unchanged')

    def test_conflict_preserves_existing(self):
        self.apply()
        target = self.home / 'skills/test/demo/SKILL.md'
        target.write_text('---\nname: demo\n---\nPersonal edit.\n')
        with self.assertRaises(ValueError):
            self.apply()
        self.assertIn('Personal edit.', target.read_text())

    def test_existing_name_other_category(self):
        destination = self.home / 'skills/other/demo'
        destination.mkdir(parents=True)
        (destination / 'SKILL.md').write_text('---\nname: demo\n---\nPersonal edit.\n')
        with self.assertRaises(ValueError):
            self.apply()
        self.assertFalse((self.home / 'skills/test/demo').exists())

    def test_manifest_traversal(self):
        self.manifest['skills'][0]['install_path'] = '../escape'
        with self.assertRaises(ValueError):
            self.apply()
        self.assertFalse(self.home.exists())

    def test_source_symlink_refused(self):
        (self.source / 'skills/demo/unsafe').symlink_to(self.source / 'LICENSE')
        with self.assertRaises(ValueError):
            self.apply()
        self.assertFalse(self.home.exists())

    def test_target_symlink_refused(self):
        self.home.mkdir()
        (self.home / 'skills').symlink_to(self.source)
        with self.assertRaises(ValueError):
            self.apply()

    def test_duplicate_manifest(self):
        self.manifest['skills'].append(dict(self.manifest['skills'][0]))
        with self.assertRaises(ValueError):
            self.apply()


if __name__ == '__main__':
    unittest.main()
