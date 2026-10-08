"""Verify the two quota-oriented routing presets and their copyable commands."""
import json
from pathlib import Path
import re
import shlex
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHANGED = {'visual-engineering', 'artistry', 'capable', 'deep-work', 'writing'}


class RoutingPresetTests(unittest.TestCase):
    def setUp(self):
        self.presets = {name: json.loads((ROOT / 'routing-presets' / (name + '.json')).read_text())
                        for name in ['claude-generous', 'gpt-generous']}
        self.chains = {name: {item['category']: item['chain'] for item in preset['categories']}
                       for name, preset in self.presets.items()}

    def test_only_five_category_orders_differ(self):
        a, b = self.chains['claude-generous'], self.chains['gpt-generous']
        self.assertEqual(len(a), 12)
        self.assertEqual(set(a), set(b))
        self.assertEqual({key for key in a if a[key] != b[key]}, CHANGED)
        for key in a:
            self.assertEqual(sorted((x['model'], x['reasoning_effort']) for x in a[key]),
                             sorted((x['model'], x['reasoning_effort']) for x in b[key]))

    def test_gpt_restores_previous_astra_positions(self):
        chains = self.chains['gpt-generous']
        for key in ['visual-engineering', 'artistry', 'capable']:
            self.assertEqual([x['model'] for x in chains[key]][:3],
                             ['claude-fable-5-1', 'gpt-6-astra', 'claude-opus-5-5'])
        self.assertEqual([x['model'] for x in chains['deep-work']],
                         ['gpt-6-astra', 'claude-fable-5-1', 'claude-opus-5-5'])

    def test_shared_fallbacks_are_identical_and_opus_last(self):
        a, b = self.presets.values()
        for key in ['fallback_providers', 'delegation_fallback_providers', 'gpt_child_fallback_adapter']:
            self.assertEqual(a[key], b[key])
        self.assertEqual([x['model'] for x in a['delegation_fallback_providers']],
                         ['claude-fable-5-1', 'gpt-6-astra', 'claude-sonnet-5-5', 'claude-opus-5-5'])
        self.assertEqual(a['fallback_providers'],
                         [{'provider': 'anthropic', 'model': 'claude-opus-5-5'}])

    def test_removed_families_are_absent_and_writing_uses_sol_opus(self):
        for name, chains in self.chains.items():
            for chain in chains.values():
                self.assertTrue(all(item['model'].startswith(('gpt-', 'claude-'))
                                    for item in chain))
            expected = ['claude-opus-5-5', 'gpt-6.1-sol']
            if name == 'gpt-generous':
                expected.reverse()
            self.assertEqual([item['model'] for item in chains['writing']], expected)
            self.assertTrue(all(item['reasoning_effort'] == 'medium'
                                for item in chains['writing']))

    def test_legacy_snapshot_stays_claude_compatible(self):
        legacy = json.loads((ROOT / 'routing-snapshot.json').read_text())
        for key in ['categories', 'fallback_providers', 'delegation_fallback_providers']:
            self.assertEqual(legacy[key], self.presets['claude-generous'][key])

    def test_documented_commands_match_selected_presets(self):
        doc = (ROOT / 'docs/model-routing.md').read_text()
        for name, chains in self.chains.items():
            section = doc.split('### ' + name + ' CLI', 1)[1].split('\n### ', 1)[0]
            lines = re.findall(r'^omh model-chains set .+$', section, re.M)
            self.assertEqual(len(lines), 12)
            for line in lines:
                command = shlex.split(line)
                key = command[3]
                expected = ', '.join(x['model'] + ':' + x['reasoning_effort'] for x in chains[key])
                self.assertEqual(command[4], expected)


if __name__ == '__main__':
    unittest.main()
