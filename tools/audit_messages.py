from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ACCEL = re.compile(r"&.")


def read_po(path: Path):
    entries = []
    msgid = None
    msgstr = None
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("msgid "):
                if msgid is not None:
                    entries.append((msgid, msgstr or ""))
                msgid = line[7:-1]  # naive, assumes single-line
                msgid = msgid.encode("utf-8").decode("unicode_escape").replace('\\"', '"')
                msgstr = None
            elif line.startswith("msgstr "):
                msgstr = line[8:-1]
                msgstr = msgstr.encode("utf-8").decode("unicode_escape").replace('\\"', '"')
        if msgid is not None:
            entries.append((msgid, msgstr or ""))
    # drop header empty key
    return [(k, v) for (k, v) in entries if k]


def main():
    # Prefer in-package assets; fall back to repo-level locales for dev
    candidates = [
        Path("src/ttkbootstrap/assets/locales"),
        Path("locales"),
    ]
    root = next((p for p in candidates if p.exists()), candidates[-1])
    per_locale = defaultdict(list)
    for loc_dir in root.iterdir():
        po = loc_dir / "LC_MESSAGES" / "ttkbootstrap.po"
        if po.exists():
            per_locale[loc_dir.name].extend(read_po(po))

    # 1) case variants of the same msgid
    canonical = defaultdict(set)
    for entries in per_locale.values():
        for k, _ in entries:
            canonical[k.lower()].add(k)
    weird = {base: forms for base, forms in canonical.items() if len(forms) > 1}
    if weird:
        print("\n[Case variants detected] unify these msgids:")
        for base, forms in sorted(weird.items()):
            print(" ", sorted(forms))

    # 2) keys that embed accelerators (&X)
    accel_keys = sorted({k for entries in per_locale.values() for k, _ in entries if ACCEL.search(k)})
    if accel_keys:
        print("\n[Msgids with accelerators '&']: move mnemonics to separate keys")
        for k in accel_keys:
            print(" ", k)

    print("\nAudit complete.")


if __name__ == "__main__":
    main()
