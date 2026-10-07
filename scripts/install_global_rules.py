#!/usr/bin/env python3
"""Add report-writing rules to a chosen Hermes profile without overwriting its SOUL."""
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- hermes-setup:report-writing:begin -->'
END = '<!-- hermes-setup:report-writing:end -->'
HEADING = '## Reports and AI-slop review'


def policy():
    return (ROOT / 'templates/report-writing.md').read_text(encoding='utf-8').strip()


def resolve_home(explicit=None):
    value = explicit or os.environ.get('HERMES_HOME') or str(Path.home() / '.hermes')
    return Path(value).expanduser().absolute()


def install(home, apply=False):
    target = Path(home) / 'SOUL.md'
    if target.is_symlink():
        raise ValueError('Refusing SOUL.md symlink')
    existing = target.read_bytes().decode('utf-8') if target.exists() else ''
    body = policy()
    block = START + '\n' + body + '\n' + END
    if START in existing or END in existing:
        if existing.count(START) != 1 or existing.count(END) != 1:
            raise ValueError('Malformed or duplicated report-writing markers; existing file preserved')
        start = existing.index(START)
        end = existing.index(END) + len(END)
        if end <= start or existing[start:end] != block:
            raise ValueError('Existing managed policy differs; review it before changing; file preserved')
        status = 'unchanged'
    elif body in existing:
        status = 'unchanged'
    elif HEADING in existing:
        raise ValueError('Existing report-writing policy differs; review it before changing; file preserved')
    else:
        status = 'add'
        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            separator = '' if not existing else ('\n' if existing.endswith('\n') else '\n\n')
            target.write_text(existing + separator + block + '\n', encoding='utf-8')
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
