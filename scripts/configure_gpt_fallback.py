#!/usr/bin/env python3
"""Keep Fable first and Opus last for pinned GPT children; preview by default."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import tempfile

ANCHOR = '''    return scoped_fallback_chain(
        getattr(parent_agent, "_fallback_chain", None),
        routing_cfg.get("fallback_providers") if isinstance(routing_cfg, dict) else None,
        pinned=pinned, owner="delegation")'''
REPLACEMENT = ANCHOR.replace('    return ', '    chain = ', 1) + '''
    # hermes-setup:gpt-child-claude-fallback
    cfg = routing_cfg if isinstance(routing_cfg, dict) else {}
    if (pinned and cfg.get("provider") in {"openai-codex", "openai"}
            and cfg.get("model") in {"gpt-6-astra", "gpt-6.1-sol", "gpt-6-luna"}
            and chain):
        ranks = {("anthropic", "claude-fable-5-1"): 0,
                 ("anthropic", "claude-opus-5-5"): 3}
        chain = sorted(chain, key=lambda entry: ranks.get(
            (entry.get("provider"), entry.get("model")), 2))
    return chain'''

LEGACY_REPLACEMENT = REPLACEMENT.replace(
    '("anthropic", "claude-opus-5-5"): 3}',
    '("anthropic", "claude-opus-5-5"): 1}')


def adapt(source):
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == '_resolve_child_fallback_chain']
    if len(functions) != 1:
        raise ValueError('Unsupported child fallback function; source preserved')
    node = functions[0]
    lines = source.splitlines(keepends=True)
    section = ''.join(lines[node.lineno - 1:node.end_lineno])
    if 'hermes-setup:gpt-child-claude-fallback' in source:
        if section.count(LEGACY_REPLACEMENT) == 1:
            result = ''.join(lines[:node.lineno - 1]) + section.replace(
                LEGACY_REPLACEMENT, REPLACEMENT, 1) + ''.join(lines[node.end_lineno:])
            ast.parse(result)
            return result
        if section.count(REPLACEMENT) != 1:
            raise ValueError('Changed GPT fallback adapter; source preserved')
        return source
    if section.count(ANCHOR) != 1:
        raise ValueError('Customized child fallback function; source preserved')
    result = ''.join(lines[:node.lineno - 1]) + section.replace(ANCHOR, REPLACEMENT, 1) + ''.join(lines[node.end_lineno:])
    ast.parse(result)
    return result


def install(source_root, apply=False):
    target = Path(source_root).expanduser().absolute() / 'tools/delegate_tool_config.py'
    if any(path.is_symlink() for path in (target, *target.parents)) or not target.is_file():
        raise ValueError('Refusing symlink or non-file source path')
    original = target.read_bytes()
    updated = adapt(original.decode()).encode()
    status = 'unchanged' if updated == original else 'preview'
    if apply and updated != original:
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.fallback-', delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(updated)
                stream.flush()
                os.fchmod(stream.fileno(), target.stat().st_mode & 0o777)
            if target.read_bytes() != original:
                raise ValueError('Hermes source changed during preview; preserved')
            os.replace(temporary, target)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        if target.read_bytes() != updated:
            raise OSError('GPT fallback adapter read-back failed')
        status = 'applied'
    return {'status': status, 'target': 'tools/delegate_tool_config.py',
            'sha256': hashlib.sha256(updated).hexdigest(), 'restart_required': status == 'applied'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    print(json.dumps(install(args.source_root, apply=args.apply), indent=2))


if __name__ == '__main__':
    main()
