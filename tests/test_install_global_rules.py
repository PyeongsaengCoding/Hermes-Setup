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

    def test_browser_policy_requires_direct_repl_without_aside_agent(self):
        body = installer.browser_policy()
        for requirement in (
            'Hermes model',
            '`repl`',
            'Do not use Aside\'s own AI agent',
            '`aside exec`',
            'natural-language prompts',
            'Do not switch to `exec`',
        ):
            self.assertIn(requirement, body)
        installer.install(self.home, apply=True)
        self.assertIn(body, self.target.read_text())

    def test_preview_does_not_write(self):
        self.assertEqual(installer.install(self.home)['status'], 'add')
        self.assertFalse(self.home.exists())

    def test_first_install_and_repeat(self):
        self.assertEqual(installer.install(self.home, apply=True)['status'], 'added')
        content = self.target.read_bytes()
        self.assertEqual(installer.install(self.home, apply=True)['status'], 'unchanged')
        self.assertEqual(self.target.read_bytes(), content)
        self.assertNotIn(installer.LEGACY_REPORT_START, content.decode())
        self.assertNotIn(installer.LEGACY_REPORT_HEADING, content.decode())
        self.assertEqual(installer.install(self.home)['legacy_report_policy'], 'absent')
        self.assertEqual(content.decode().count(installer.BROWSER_START), 1)
        self.assertNotIn('hermes-setup:user-intent:begin', content.decode())
        self.assertNotIn('## User intent and course correction', content.decode())
        self.assertIn(installer.delivery_policy(), content.decode())
        self.assertEqual(content.decode().count(installer.DELIVERY_START), 1)

    def test_preserves_existing_text(self):
        existing = '# My tone\nPersonal rules.\n'
        self.seed(existing)
        installer.install(self.home, apply=True)
        self.assertTrue(self.target.read_text().startswith(existing))

    def test_existing_unmarked_browser_policy_not_duplicated(self):
        existing = '# My tone\n\n' + installer.browser_policy() + '\n\n## Other rules\nKeep me.\n'
        self.seed(existing)
        self.assertEqual(installer.install(self.home, apply=True)['status'], 'added')
        updated = self.target.read_text()
        self.assertTrue(updated.startswith(existing))
        self.assertEqual(updated.count(installer.browser_policy()), 1)
        self.assertNotIn(installer.BROWSER_START, updated)

    def test_retired_unmarked_rule_is_preserved(self):
        retired = '## User intent and course correction\nPersonal existing rule.\n'
        existing = installer.browser_policy() + '\n\n' + retired + '\n' + installer.delivery_policy() + '\n'
        self.seed(existing)
        self.assertEqual(installer.install(self.home, apply=True)['status'], 'unchanged')
        self.assertEqual(self.target.read_text(), existing)

    def test_retired_managed_rule_is_not_validated_or_changed(self):
        existing = '<!-- hermes-setup:user-intent:begin -->\nPersonal edit.\n<!-- hermes-setup:user-intent:end -->\n'
        self.seed(existing)
        self.assertEqual(installer.install(self.home, apply=True)['status'], 'added')
        self.assertTrue(self.target.read_text().startswith(existing))
        self.assertEqual(self.target.read_text().count('hermes-setup:user-intent:begin'), 1)

    def test_delivery_policy_requires_folder_card_without_auto_open(self):
        body = installer.delivery_policy()
        self.assertIn('::preview{file=', body)
        self.assertIn('Do not automatically open Finder', body)
        self.assertIn('explicitly asks', body)

    def test_existing_unmarked_delivery_not_duplicated(self):
        existing = installer.delivery_policy() + '\n'
        self.seed(existing)
        installer.install(self.home, apply=True)
        updated = self.target.read_text()
        self.assertTrue(updated.startswith(existing))
        self.assertEqual(updated.count(installer.delivery_policy()), 1)
        self.assertNotIn(installer.DELIVERY_START, updated)

    def test_changed_delivery_rule_preserves_whole_file(self):
        existing = installer.DELIVERY_START + '\nPersonal edit.\n' + installer.DELIVERY_END + '\n'
        self.seed(existing)
        with self.assertRaises(ValueError):
            installer.install(self.home, apply=True)
        self.assertEqual(self.target.read_text(), existing)

    def test_retired_incomplete_rule_does_not_block_installation(self):
        self.seed('<!-- hermes-setup:user-intent:begin -->\nIncomplete.\n')
        before = self.target.read_bytes()
        self.assertEqual(installer.install(self.home, apply=True)['status'], 'added')
        self.assertTrue(self.target.read_bytes().startswith(before))

    def test_retired_template_is_not_an_installation_dependency(self):
        self.assertFalse((ROOT / 'templates/user-intent.md').exists())
        installer.install(self.home, apply=True)
        content = self.target.read_text()
        self.assertIn(installer.browser_policy(), content)
        self.assertIn(installer.delivery_policy(), content)
        self.assertNotIn('hermes-setup:user-intent:', content)

    def test_adds_browser_rule_to_existing_managed_report(self):
        report = installer.LEGACY_REPORT_START + '\nPersonal report policy.\n' + installer.LEGACY_REPORT_END + '\n'
        self.seed(report)
        self.assertEqual(installer.install(self.home, apply=True)['status'], 'added')
        updated = self.target.read_text()
        self.assertTrue(updated.startswith(report))
        self.assertEqual(updated.count(installer.BROWSER_START), 1)
        self.assertEqual(installer.install(self.home, apply=True)['status'], 'unchanged')
        self.assertEqual(installer.install(self.home)['legacy_report_policy'], 'present_preserved')

    def test_changed_browser_rule_is_conflict(self):
        existing = installer.BROWSER_START + '\nPersonal edit.\n' + installer.BROWSER_END + '\n'
        self.seed(existing)
        with self.assertRaises(ValueError):
            installer.install(self.home, apply=True)
        self.assertEqual(self.target.read_text(), existing)

    def test_preserves_existing_crlf_bytes(self):
        self.home.mkdir()
        existing = b'# My tone\r\nPersonal rules.\r\n'
        self.target.write_bytes(existing)
        installer.install(self.home, apply=True)
        self.assertTrue(self.target.read_bytes().startswith(existing))

    def test_personal_unmarked_report_policy_is_preserved(self):
        existing = '## Reports and AI-slop review\n\nMy existing policy.\n'
        self.seed(existing)
        result = installer.install(self.home, apply=True)
        self.assertEqual(result['status'], 'added')
        self.assertEqual(result['legacy_report_policy'], 'present_preserved')
        self.assertTrue(self.target.read_text().startswith(existing))

    def test_malformed_legacy_report_is_preserved(self):
        existing = installer.LEGACY_REPORT_START + '\nPersonal edit.\n'
        self.seed(existing)
        installer.install(self.home, apply=True)
        self.assertTrue(self.target.read_text().startswith(existing))

    def test_changed_managed_browser_block_is_conflict(self):
        self.seed(installer.BROWSER_START + '\nPersonal edit.\n' + installer.BROWSER_END + '\n')
        before = self.target.read_bytes()
        with self.assertRaises(ValueError):
            installer.install(self.home, apply=True)
        self.assertEqual(self.target.read_bytes(), before)

    def test_malformed_markers_are_conflict(self):
        self.seed(installer.BROWSER_START + '\nIncomplete.\n')
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
