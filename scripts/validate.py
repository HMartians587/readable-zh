"""Validate the distributed skill, manifests, licenses and local document links."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/readable-zh'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    files = [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts and '__pycache__' not in p.relative_to(ROOT).parts]
    for path in files:
        rel = path.relative_to(ROOT)
        require(not set(rel.parts).intersection({'evals', 'private', 'candidates', 'upstream', 'dist'}), f'Unexpected distribution directory: {rel}')
        require(not path.name.startswith('.env') and path.suffix not in {'.zip', '.jsonl', '.log'}, f'Unexpected distribution file: {rel}')
        text = path.read_text(encoding='utf-8')
        require(not re.search(r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----)', text), f'Possible credential: {rel}')
        require(not re.search(r'[A-Za-z]:[\\/](?:Users[\\/]|日志[\\/]|codex_home[\\/])', text), f'Personal absolute path: {rel}')
    entry = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    require(entry.startswith('---\n'), 'Missing skill frontmatter')
    frontmatter = entry.split('---', 2)[1]
    require(re.search(r'^name: readable-zh$', frontmatter, re.M), 'Skill name must match its directory')
    require(re.search(r'^description: .+', frontmatter, re.M), 'Missing skill description')
    version = re.search(r'^\s+version: "([0-9]+\.[0-9]+\.[0-9]+)"$', frontmatter, re.M)
    require(version is not None, 'Missing semantic version')
    plugin = json.loads((ROOT / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
    marketplace = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
    require(plugin['name'] == 'readable-zh' and plugin['version'] == version.group(1), 'Plugin and skill metadata must agree')
    require(marketplace['plugins'][0]['name'] == plugin['name'] and marketplace['plugins'][0]['source'] == './', 'Marketplace entry must refer to this plugin')
    require(not any(k in plugin for k in ['hooks', 'mcpServers', 'lspServers']), 'Unexpected executable plugin component')
    for relative in ['LICENSE', 'THIRD_PARTY_NOTICES.md']:
        require((SKILL / relative).is_file(), f'Standalone skill missing {relative}')
        require((ROOT / relative).read_bytes() == (SKILL / relative).read_bytes(), f'Root and skill copies differ: {relative}')
    notices = (SKILL / 'THIRD_PARTY_NOTICES.md').read_text(encoding='utf-8')
    for name in ['歸藏', 'Nanako Tsai', 'Siqi Chen', 'Hardik Pandya']:
        require(name in notices, f'Missing source attribution: {name}')
    require(notices.count('Permission is hereby granted, free of charge,') == 4, 'Expected four full MIT notices')
    link_count = 0
    for path in files:
        if path.suffix != '.md':
            continue
        text = path.read_text(encoding='utf-8')
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', text):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                continue
            local = (path.parent / unquote(target.split('#')[0])).resolve()
            require(local.is_relative_to(ROOT), f'Link leaves distribution: {path.name}: {target}')
            require(local.exists(), f'Broken link: {path.name}: {target}')
            link_count += 1
    print(f'Validated Readable ZH {version.group(1)}: {len(files)} files, {link_count} local links, skill/plugin metadata and bundled licenses.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f'Validation failed: {exc}', file=sys.stderr)
        raise SystemExit(1)
