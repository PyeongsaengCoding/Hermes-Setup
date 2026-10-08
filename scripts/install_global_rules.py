#!/usr/bin/env python3
"""Add managed global rules to a chosen Hermes profile without overwriting its SOUL."""
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- hermes-setup:report-writing:begin -->'
END = '<!-- hermes-setup:report-writing:end -->'
HEADING = '## Reports and AI-slop review'
BROWSER_START = '<!-- hermes-setup:aside-browser:begin -->'
BROWSER_END = '<!-- hermes-setup:aside-browser:end -->'
BROWSER_HEADING = '## Browser work in Aside'


def policy():
    return (ROOT / 'templates/report-writing.md').read_text(encoding='utf-8').strip()


def browser_policy():
    return (ROOT / 'templates/aside-browser.md').read_text(encoding='utf-8').strip()


def policy_status(existing, body, start_marker, end_marker, heading):
    block = start_marker + '\n' + body + '\n' + end_marker
    if start_marker in existing or end_marker in existing:
        if existing.count(start_marker) != 1 or existing.count(end_marker) != 1:
            raise ValueError(f'Malformed or duplicated {heading} markers; existing file preserved')
        start = existing.index(start_marker)
        end = existing.index(end_marker) + len(end_marker)
        if end <= start or existing[start:end] != block:
            raise ValueError(f'Existing managed {heading} policy differs; review it before changing; file preserved')
        return 'unchanged', block
    if body in existing:
        return 'unchanged', block
    if heading in existing:
        raise ValueError(f'Existing {heading} policy differs; review it before changing; file preserved')
    return 'add', block


def resolve_home(explicit=None):
    value = explicit or os.environ.get('HERMES_HOME') or str(Path.home() / '.hermes')
    return Path(value).expanduser().absolute()


def install(home, apply=False):
    target = Path(home) / 'SOUL.md'
    if target.is_symlink():
        raise ValueError('Refusing SOUL.md symlink')
    existing = target.read_bytes().decode('utf-8') if target.exists() else ''
    policies = (
        (policy(), START, END, HEADING),
        (browser_policy(), BROWSER_START, BROWSER_END, BROWSER_HEADING),
    )
    additions = []
    for body, start_marker, end_marker, heading in policies:
        state, block = policy_status(existing, body, start_marker, end_marker, heading)
        if state == 'add':
            additions.append(block)
    status = 'add' if additions else 'unchanged'
    if apply and additions:
        target.parent.mkdir(parents=True, exist_ok=True)
        separator = '' if not existing else ('\n' if existing.endswith('\n') else '\n\n')
        target.write_text(existing + separator + '\n\n'.join(additions) + '\n', encoding='utf-8')
        status = 'added'
    return {'status': status, 'path': str(target), 'apply': apply}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', help='Chosen Hermes profile home; otherwise HERMES_HOME or ~/.hermes')
    parser.add_argument('--apply', action='store_true', help='Apply; default is read-only preview')
    args = parser.parse_args()
    print(json.dumps(install(resolve_home(args.home), args.apply), ensure_ascii=False))


if __name__ == '__main__':
    main()
