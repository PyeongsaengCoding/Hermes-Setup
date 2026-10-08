from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from scripts.configure_gpt_fallback import adapt, install

SOURCE = '''def _resolve_child_fallback_chain(parent_agent, routing_cfg, pinned):
    return scoped_fallback_chain(
        getattr(parent_agent, "_fallback_chain", None),
        routing_cfg.get("fallback_providers") if isinstance(routing_cfg, dict) else None,
        pinned=pinned, owner="delegation")
'''
CHAIN = [{'provider': provider, 'model': model} for provider, model in (
    ('anthropic', 'claude-fable-5-1'), ('openai-codex', 'gpt-6-astra'),
    ('anthropic', 'claude-opus-5-5'), ('anthropic', 'claude-sonnet-5-5'))]


class GPTFallbackTests(unittest.TestCase):
    def resolve(self, provider, model, pinned=True, chain=CHAIN):
        namespace = {'scoped_fallback_chain': lambda parent, declared, **kwargs: declared}
        exec(compile(adapt(SOURCE), '<fixture>', 'exec'), namespace)
        return namespace['_resolve_child_fallback_chain'](SimpleNamespace(_fallback_chain=[]),
            {'provider': provider, 'model': model, 'fallback_providers': chain}, pinned)

    def test_gpt_route_prioritizes_claude_without_mutating_config(self):
        before = [dict(entry) for entry in CHAIN]
        for model in ('gpt-6-astra', 'gpt-6.1-sol', 'gpt-6-luna'):
            result = self.resolve('openai-codex', model)
            self.assertEqual([entry['model'] for entry in result][:2],
                             ['claude-fable-5-1', 'claude-opus-5-5'])
            self.assertEqual(CHAIN, before)

    def test_claude_and_unpinned_routes_unchanged(self):
        self.assertEqual(self.resolve('anthropic', 'claude-fable-5-1'), CHAIN)
        self.assertEqual(self.resolve('openai-codex', 'gpt-6-astra', pinned=False), CHAIN)
        self.assertEqual(self.resolve('custom', 'gpt-6-astra'), CHAIN)
        self.assertEqual(self.resolve('openai-codex', 'gpt-6-astra', chain=[]), [])
        self.assertIsNone(self.resolve('openai-codex', 'gpt-6-astra', chain=None))

    def test_preview_apply_repeat_and_conflict(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            target = root / 'tools/delegate_tool_config.py'
            target.parent.mkdir()
            target.write_text(SOURCE)
            self.assertEqual(install(root)['status'], 'preview')
            self.assertEqual(target.read_text(), SOURCE)
            self.assertEqual(install(root, apply=True)['status'], 'applied')
            self.assertEqual(install(root, apply=True)['status'], 'unchanged')
            target.write_text(target.read_text().replace('ranks.get', 'changed.get'))
            with self.assertRaises(ValueError):
                install(root, apply=True)


if __name__ == '__main__':
    unittest.main()
