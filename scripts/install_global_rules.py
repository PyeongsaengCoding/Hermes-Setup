#!/usr/bin/env python3
"""Add Aside and document delivery rules without overwriting the profile's SOUL."""
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_REPORT_START = '<!-- hermes-setup:report-writing:begin -->'
LEGACY_REPORT_END = '<!-- hermes-setup:report-writing:end -->'
LEGACY_REPORT_HEADING = '## Reports and AI-slop review'
BROWSER_START = '<!-- hermes-setup:aside-browser:begin -->'
BROWSER_END = '<!-- hermes-setup:aside-browser:end -->'
BROWSER_HEADING = '## Browser work in Aside'
DELIVERY_START = '<!-- hermes-setup:document-delivery:begin -->'
DELIVERY_END = '<!-- hermes-setup:document-delivery:end -->'
DELIVERY_HEADING = '## Document delivery in Hermes Desktop'


def browser_policy():
    return (ROOT / 'templates/aside-browser.md').read_text(encoding='utf-8').strip()


def delivery_policy():
    return (ROOT / 'templates/document-delivery.md').read_text(encoding='utf-8').strip()


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
        (browser_policy(), BROWSER_START, BROWSER_END, BROWSER_HEADING),
        (delivery_policy(), DELIVERY_START, DELIVERY_END, DELIVERY_HEADING),
    )
    # Validate every policy before writing, so a conflict preserves the whole file.
    additions = []
    for body, start, end, heading in policies:
        policy_state, block = policy_status(existing, body, start, end, heading)
        if policy_state == 'add':
            additions.append(block)
    status = 'add' if additions else 'unchanged'
    legacy_report_present = any(token in existing for token in (
        LEGACY_REPORT_START, LEGACY_REPORT_END, LEGACY_REPORT_HEADING
    ))
    if apply and status == 'add':
        target.parent.mkdir(parents=True, exist_ok=True)
        separator = '' if not existing else ('\n' if existing.endswith('\n') else '\n\n')
        target.write_text(existing + separator + '\n\n'.join(additions) + '\n', encoding='utf-8')
        status = 'added'
    return {
        'status': status, 'path': str(target), 'apply': apply,
        'legacy_report_policy': 'present_preserved' if legacy_report_present else 'absent',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', help='Chosen Hermes profile home; otherwise HERMES_HOME or ~/.hermes')
    parser.add_argument('--apply', action='store_true', help='Apply; default is read-only preview')
    args = parser.parse_args()
    print(json.dumps(install(resolve_home(args.home), args.apply), ensure_ascii=False))


if __name__ == '__main__':
    main()
