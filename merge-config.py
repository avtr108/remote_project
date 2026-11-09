#!/usr/bin/env python3
"""Merge hermes-overlay.yaml into Hermes' config.yaml. Idempotent and fail-soft."""
import os
import shutil
import sys
import tempfile

import yaml

OVERLAY = os.environ.get("HERMES_OVERLAY", "/usr/local/share/hermes-overlay/hermes-overlay.yaml")
CONFIG = os.path.join(os.environ.get("HERMES_HOME", "/data/.hermes"), "config.yaml")


def merge(dst, src):
    for key, value in src.items():
        if isinstance(value, dict) and isinstance(dst.get(key), dict):
            merge(dst[key], value)
        else:
            dst[key] = value


def main():
    if not os.path.exists(OVERLAY):
        print(f"[overlay] {OVERLAY} missing, skipping")
        return
    if not os.path.exists(CONFIG):
        print(f"[overlay] {CONFIG} not created yet (first boot), skipping; it applies on the next restart")
        return
    with open(OVERLAY) as f:
        overlay = yaml.safe_load(f) or {}
    with open(CONFIG) as f:
        config = yaml.safe_load(f) or {}
    before = yaml.safe_dump(config, sort_keys=False)

    # A provider switch invalidates a stale endpoint/wire mode from the previous provider.
    new_provider = (overlay.get("model") or {}).get("provider")
    old_model = config.get("model")
    if new_provider and isinstance(old_model, dict) and old_model.get("provider") not in (None, new_provider):
        old_model.pop("base_url", None)
        old_model.pop("api_mode", None)
    if isinstance(old_model, str):  # legacy string form
        config["model"] = {"default": old_model}

    merge(config, overlay)
    after = yaml.safe_dump(config, sort_keys=False)
    if after == before:
        print("[overlay] config already up to date")
        return

    shutil.copy2(CONFIG, CONFIG + ".bak")
    st = os.stat(CONFIG)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(CONFIG), prefix=".config-", suffix=".yaml")
    with os.fdopen(fd, "w") as f:
        f.write(after)
    os.chmod(tmp, st.st_mode & 0o7777)
    try:
        os.chown(tmp, st.st_uid, st.st_gid)
    except OSError:
        pass
    os.replace(tmp, CONFIG)
    print(f"[overlay] merged {sorted(overlay)} into {CONFIG} (backup: config.yaml.bak)")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never block startup
        print(f"[overlay] failed, continuing without it: {exc}", file=sys.stderr)
