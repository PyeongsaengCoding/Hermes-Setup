#!/usr/bin/env python3
"""Preserve delegated task effort during native fallback; preview by default."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import tempfile

ANCHOR = '        agent.reasoning_config = resolve_reasoning_config(load_config() or {}, agent.model)'
GUARD = '''        # hermes-setup:preserve-delegation-effort
        if (isinstance(getattr(agent, "_delegate_depth", None), int)
                and agent._delegate_depth > 0
                and getattr(agent, "reasoning_config", None) is not None):
            return
'''


def adapt(source):
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == '_reresolve_fallback_reasoning_config']
    if len(functions) != 1:
        raise ValueError('Unsupported Hermes fallback function; source preserved')
    node = functions[0]
    lines = source.splitlines(keepends=True)
    section = ''.join(lines[node.lineno - 1:node.end_lineno])
    if section.count(ANCHOR) != 1:
        raise ValueError('Customized fallback resolver; source preserved')
    if 'hermes-setup:preserve-delegation-effort' in source:
        if section.count(GUARD + ANCHOR) != 1:
            raise ValueError('Changed effort guard; source preserved')
        return source
    patched = section.replace(ANCHOR, GUARD + ANCHOR, 1)
    result = ''.join(lines[:node.lineno - 1]) + patched + ''.join(lines[node.end_lineno:])
    ast.parse(result)
    return result


def install(source_root, apply=False):
    root = Path(source_root).expanduser().absolute()
    target = root / 'agent/chat_completion_helpers.py'
    if any(path.is_symlink() for path in (target, *target.parents)):
        raise ValueError('Refusing symlink source path')
    original = target.read_bytes()
    updated = adapt(original.decode()).encode()
    status = 'unchanged' if updated == original else 'preview'
    if apply and updated != original:
        mode = target.stat().st_mode & 0o777
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.reasoning-', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(updated)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
        try:
            if target.read_bytes() != original:
                raise ValueError('Hermes source changed during preview; preserved')
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
        if target.read_bytes() != updated:
            raise OSError('Effort guard read-back failed')
        status = 'applied'
    return {'status': status, 'target': 'agent/chat_completion_helpers.py',
            'sha256': hashlib.sha256(updated).hexdigest(),
            'scope': 'delegated children only; main-session reasoning unchanged',
            'restart_required': status == 'applied'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', required=True, help='Verified active Hermes source root')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    print(json.dumps(install(args.source_root, apply=args.apply), indent=2))


if __name__ == '__main__':
    main()
