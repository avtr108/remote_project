#!/usr/bin/env python3
"""Repo checks for the Hermes deploy: overlay, merge script, skills, railway.toml.

Run locally with `python3 scripts/check.py` (needs PyYAML). CI runs the same file.
"""
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OVERLAY = ROOT / "hermes-overlay.yaml"
MAX_DESCRIPTION = 1024  # Hermes' skill description limit (tools/skills_tool.py)
SECRET_KEY = re.compile(r"(api_key|token|secret|password)", re.I)

errors = []


def fail(msg):
    errors.append(msg)


def walk(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, node


def check_overlay():
    try:
        overlay = yaml.safe_load(OVERLAY.read_text())
    except yaml.YAMLError as exc:
        fail(f"{OVERLAY.name}: invalid YAML: {exc}")
        return
    if not isinstance(overlay, dict) or not overlay:
        fail(f"{OVERLAY.name}: must be a non-empty mapping")
        return
    for path, value in walk(overlay):
        if SECRET_KEY.search(path.rsplit(".", 1)[-1]) and value not in (None, ""):
            fail(f"{OVERLAY.name}: {path} looks like a secret; set it in Railway variables instead")


def run_merge(home):
    env = dict(os.environ, HERMES_HOME=str(home), HERMES_OVERLAY=str(OVERLAY))
    return subprocess.run(
        [sys.executable, str(ROOT / "merge-config.py")],
        env=env, capture_output=True, text=True,
    )


def check_merge():
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        # First boot: no config yet, must skip without failing.
        res = run_merge(home)
        if res.returncode != 0 or "first boot" not in res.stdout:
            fail(f"merge-config.py on first boot: rc={res.returncode} out={res.stdout!r} err={res.stderr!r}")

        config = home / "config.yaml"
        config.write_text(yaml.safe_dump({
            "model": {"provider": "openrouter", "default": "x", "base_url": "https://old.example"},
            "memory": {"memory_enabled": True, "user_char_limit": 1375},
            "keep_me": {"untouched": True},
        }))
        res = run_merge(home)
        if res.returncode != 0 or "merged" not in res.stdout:
            fail(f"merge-config.py merge: rc={res.returncode} out={res.stdout!r} err={res.stderr!r}")
            return
        merged = yaml.safe_load(config.read_text())
        overlay = yaml.safe_load(OVERLAY.read_text())
        for path, value in walk(overlay):
            node = merged
            for part in re.split(r"\.(?![^\[]*\])", path):
                m = re.fullmatch(r"(.+?)((?:\[\d+\])*)", part)
                node = node.get(m.group(1)) if isinstance(node, dict) else None
                for idx in re.findall(r"\[(\d+)\]", m.group(2)):
                    node = node[int(idx)] if isinstance(node, list) else None
            if node != value:
                fail(f"merge-config.py: {path} is {node!r} after merge, overlay says {value!r}")
        if merged.get("keep_me") != {"untouched": True}:
            fail("merge-config.py: dropped a key that is not in the overlay")
        if merged.get("memory", {}).get("user_char_limit") != 1375:
            fail("merge-config.py: dropped a nested key that is not in the overlay")
        if "base_url" in merged.get("model", {}) and overlay.get("model", {}).get("provider") != "openrouter":
            fail("merge-config.py: kept a stale base_url after a provider switch")
        if not (home / "config.yaml.bak").exists():
            fail("merge-config.py: no config.yaml.bak written before changing the config")

        res = run_merge(home)
        if "already up to date" not in res.stdout:
            fail(f"merge-config.py is not idempotent: second run said {res.stdout!r}")


def check_skills():
    skills = sorted((ROOT / "skills").rglob("SKILL.md"))
    if not skills:
        fail("skills/: no SKILL.md found")
    for path in skills:
        rel = path.relative_to(ROOT)
        text = path.read_text()
        parts = text.split("---", 2)
        if not text.startswith("---") or len(parts) < 3:
            fail(f"{rel}: missing YAML frontmatter")
            continue
        try:
            meta = yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError as exc:
            fail(f"{rel}: invalid frontmatter: {exc}")
            continue
        name, desc = meta.get("name"), meta.get("description")
        if name != path.parent.name:
            fail(f"{rel}: name {name!r} must match its folder {path.parent.name!r}")
        if not desc or not isinstance(desc, str):
            fail(f"{rel}: description is missing")
        elif len(desc) > MAX_DESCRIPTION:
            fail(f"{rel}: description is {len(desc)} chars, Hermes allows {MAX_DESCRIPTION}")
        if not parts[2].strip():
            fail(f"{rel}: body is empty")


def check_railway():
    try:
        cfg = tomllib.loads((ROOT / "railway.toml").read_text())
    except tomllib.TOMLDecodeError as exc:
        fail(f"railway.toml: invalid TOML: {exc}")
        return
    dockerfile = cfg.get("build", {}).get("dockerfilePath")
    if dockerfile and not (ROOT / dockerfile).exists():
        fail(f"railway.toml: dockerfilePath {dockerfile!r} does not exist")


def check_dockerfile():
    text = (ROOT / "Dockerfile").read_text()
    for src in re.findall(r"^COPY(?:\s+--\S+)*\s+(\S+)\s+\S+\s*$", text, re.M):
        if not (ROOT / src).exists():
            fail(f"Dockerfile: COPY source {src!r} does not exist")
    base = re.search(r"^FROM\s+(\S+)", text, re.M)
    if not base or "@sha256:" not in base.group(1):
        fail("Dockerfile: base image must be pinned by digest (@sha256:...)")


for check in (check_overlay, check_merge, check_skills, check_railway, check_dockerfile):
    check()

if errors:
    print("FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("All checks passed.")
